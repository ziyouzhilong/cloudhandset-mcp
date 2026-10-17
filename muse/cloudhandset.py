#!/usr/bin/env python3
"""MCP requests using Muse's credential surrogate; no automatic retries or acquisition."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import base64
import binascii
import importlib.util
import inspect
import json
import math
import os
import re
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
import uuid

ENDPOINT = "https://device.cloudhandset.com/mcp"
ALLOWED_HOSTS = ["device.cloudhandset.com"]
PROTOCOL = "2026-07-28"
MAX_RESPONSE = 8 * 1024 * 1024
MAX_IMAGE = 2 * 1024 * 1024
MAX_CONCURRENT_DEVICES = 16
HELPER = "/opt/muse/skills/custom-connector-setup/bin/dynamic_credentials.py"
LEGACY_HELPER = "/opt/hatch/skills/skill-creator/bin/dynamic_credentials.py"


class AdapterError(Exception):
    def __init__(self, code, retry_after_seconds=None):
        super().__init__(code)
        self.retry_after_seconds = retry_after_seconds


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, url):
        raise AdapterError("redirect_blocked")


class LimitedResponse:
    def __init__(self, response, deadline=None):
        self.response, self.remaining, self.deadline = response, MAX_RESPONSE, deadline
        if deadline is not None and not callable(getattr(response, "read1", None)):
            raise AdapterError("response_deadline_read_unsupported")

    def check_deadline(self):
        if self.deadline is not None and time.monotonic() >= self.deadline:
            raise AdapterError("response_deadline_exceeded")

    def read(self, size=-1):
        self.check_deadline()
        limit = self.remaining + 1
        # read1 returns currently available bytes without waiting to fill the whole block.
        reader = self.response.read1 if self.deadline is not None else self.response.read
        data = reader(limit if size < 0 else min(size, limit))
        self.check_deadline()
        self.remaining -= len(data)
        if self.remaining < 0:
            raise AdapterError("response_too_large")
        return data


def muse_credentials():
    path = next((value for value in (HELPER, LEGACY_HELPER) if os.path.isfile(value)), None)
    if path is None:
        raise AdapterError("credential_helper_missing")
    try:
        spec = importlib.util.spec_from_file_location("dynamic_credentials", path)
        if spec is None or spec.loader is None:
            raise ImportError()
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception:
        raise AdapterError("credential_helper_load_failed") from None
    try:
        inspect.signature(module.add_surrogate_to_request).bind(None, "connector", allowed_hosts=ALLOWED_HOSTS)
        inspect.signature(module.read_response_body).bind(None)
    except (AttributeError, TypeError, ValueError):
        raise AdapterError("credential_helper_incompatible") from None
    return module


def parse_response(raw, content_type, request_id):
    if not isinstance(raw, bytes) or len(raw) > MAX_RESPONSE:
        raise AdapterError("response_too_large")
    try:
        text = raw.decode("utf-8")
        if content_type == "application/json":
            messages = [json.loads(text)]
        elif content_type == "text/event-stream":
            messages = []
            for event in text.replace("\r\n", "\n").replace("\r", "\n").split("\n\n"):
                data = [line[5:].removeprefix(" ") for line in event.split("\n") if line.startswith("data:")]
                if data:
                    messages.append(json.loads("\n".join(data)))
        else:
            raise AdapterError("unsupported_response_type")
    except (ValueError, UnicodeError):
        raise AdapterError("invalid_response") from None
    matches = [item for item in messages if isinstance(item, dict) and item.get("id") == request_id]
    if len(matches) != 1 or matches[0].get("jsonrpc") != "2.0":
        raise AdapterError("response_id_mismatch")
    message = matches[0]
    if "error" in message:
        code = message["error"].get("code") if isinstance(message["error"], dict) else None
        raise AdapterError(f"rpc_error_{code}" if type(code) is int else "rpc_error")
    if not isinstance(message.get("result"), dict):
        raise AdapterError("invalid_result")
    return message["result"]


def image_bytes(data, mime):
    """Check encoding and file signatures; Muse must still decode and inspect the image."""
    if mime not in ("image/png", "image/jpeg") or not isinstance(data, str) or len(data) > (MAX_IMAGE + 2) // 3 * 4:
        raise ValueError("invalid_image")
    raw = base64.b64decode(data, validate=True)
    if not raw or len(raw) > MAX_IMAGE or base64.b64encode(raw).decode() != data:
        raise ValueError("invalid_image")
    if mime == "image/png":
        valid = (len(raw) >= 45 and raw.startswith(b"\x89PNG\r\n\x1a\n\x00\x00\x00\x0dIHDR")
                 and raw.endswith(b"\x00\x00\x00\x00IEND\xaeB`\x82")
                 and all(0 < int.from_bytes(raw[i:i + 4], "big") <= 1280 for i in (16, 20)))
    else:
        valid = len(raw) >= 32 and raw.startswith(b"\xff\xd8\xff") and raw.endswith(b"\xff\xd9")
    if not valid:
        raise ValueError("invalid_image")
    return raw


def present_result(result):
    images, failures = [], []

    def clean(value):
        if isinstance(value, list):
            return [clean(item) for item in value]
        if isinstance(value, dict):
            if value.get("type") == "image":
                try:
                    raw = image_bytes(value.get("data"), value.get("mimeType"))
                    directory = tempfile.mkdtemp(prefix="cloudhandset-muse-")
                    os.chmod(directory, 0o700)
                    descriptor, path = tempfile.mkstemp(dir=directory, suffix=".png" if value["mimeType"] == "image/png" else ".jpg")
                    with os.fdopen(descriptor, "wb") as output:
                        output.write(raw)
                    image = {"path": path, "mimeType": value["mimeType"]}
                    images.append(image)
                    return {"type": "image", **image}
                except (ValueError, TypeError, binascii.Error, OSError):
                    failures.append("image_validation_or_write_failed")
                    return {"type": "image", "error": failures[-1]}
            return {key: "[redacted]" if key.lower() in ("authorization", "cookie", "set-cookie", "access_token", "refresh_token", "client_secret", "upload_token")
                    else "[binary omitted]" if key in ("data", "blob") and isinstance(item, str)
                    else clean(item) for key, item in value.items()}
        if isinstance(value, str):
            return re.sub(r"(?i)hsurr:[^\s\"'<>]+|Bearer\s+[^\s\"'<>]+|chmcp_[A-Za-z0-9_-]+|[A-Za-z0-9+/]{128,}={0,2}", "[redacted]", value)
        return value

    cleaned = clean(result)
    return {"result": cleaned, "images": images, "image_errors": failures,
            "image_acceptance": "not_verified", "retry_performed": False}


class ArgumentError(AdapterError):
    """A local rejection: no credential helper or remote request has run."""
    def __init__(self, code, hint, **details):
        super().__init__(code)
        self.details = {"hint": hint, **details}


def is_preflight_error(error):
    return isinstance(error, ArgumentError) or isinstance(error, AdapterError) and str(error) in {
        "parallel_worker_limit_exceeded", "parallel_device_limit_exceeded",
        "invalid_arguments", "invalid_credential_name", "invalid_credential_request", "request_too_large",
        "invalid_upload_wait_options", "invalid_upload_context",
        "invalid_parallel_arguments", "invalid_parallel_target", "duplicate_parallel_session", "duplicate_parallel_target",
        "mixed_parallel_target", "invalid_parallel_action", "observation_expiry_required",
        "credential_helper_missing", "credential_helper_load_failed", "credential_helper_incompatible", "credential_unavailable",
    }


def parse_argument_json(value):
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        raise ArgumentError("invalid_tool_arguments", "Supply valid JSON; never paste credentials into arguments.") from None


def observation_expiry(value):
    try:
        expiry = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if expiry.tzinfo is None:
            raise ValueError()
        return expiry.timestamp()
    except (ValueError, TypeError, AttributeError, OverflowError):
        raise ArgumentError("invalid_coordinate_context", "Copy expires_at from the current observe result, including its timezone.") from None


def prepare_arguments(tool, arguments, *, coordinate_space=None, observation=None):
    """Focused preflight; the live server schema remains authoritative for other actions."""
    if not isinstance(arguments, dict):
        raise ArgumentError("invalid_tool_arguments", "Tool arguments must be a JSON object.")

    def fields(value, required, optional=()):
        allowed = set(required) | set(optional)
        if set(value) - allowed or set(required) - set(value):
            # Report the contract, never caller-supplied values or arbitrary field names.
            raise ArgumentError("invalid_tool_arguments", "Use exactly the fields listed; do not add operation_id or observation_id to read/release calls unless their schema requires them.",
                                allowed_fields=sorted(allowed), missing_fields=sorted(set(required) - set(value)))

    def identifier(name, value):
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}", value):
            raise ArgumentError("invalid_tool_arguments", "Use the UUID returned by the service.", field=name)

    def number(name, value, low, high, integer=False):
        if (type(value) not in (int, float) or not low <= value <= high or not math.isfinite(value)
                or integer and int(value) != value):
            raise ArgumentError("invalid_coordinate_value", "Use a finite number within the stated range and unit; screenshot pixels must be integers.",
                                field=name, minimum=low, maximum=high, integer_required=integer)

    def finite_json(value):
        if isinstance(value, float) and not math.isfinite(value):
            raise ArgumentError("invalid_tool_arguments", "NaN and infinity are not valid tool arguments.")
        if isinstance(value, (list, dict)):
            for child in value.values() if isinstance(value, dict) else value:
                finite_json(child)

    if tool == "release_control":
        fields(arguments, {"session_id"})
    elif tool == "device_tool" and arguments.get("action") == "clipboard.read":
        fields(arguments, {"action", "session_id"})
    finite_json(arguments)
    if any(key in arguments for key in ("coordinate_space", "observation", "image_width", "image_height", "control_width", "control_height")):
        raise ArgumentError("invalid_tool_arguments", "Coordinate metadata belongs in call options or the outer parallel job, never in tool arguments.")
    for name in ("session_id", "observation_id"):
        if name in arguments:
            identifier(name, arguments[name])
    if "operation_id" in arguments and (not isinstance(arguments["operation_id"], str)
            or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", arguments["operation_id"])):
        raise ArgumentError("invalid_tool_arguments", "operation_id must contain 1-64 ASCII letters, digits, underscores, or hyphens.")
    positions = {"tap": ("x", "y"), "scroll": ("x", "y"),
                 "swipe": ("start_x", "start_y", "end_x", "end_y"), "gesture": ()}
    if coordinate_space not in (None, "screenshot_pixels", "normalized_1000"):
        raise ArgumentError("unsupported_coordinate_space", "Use screenshot_pixels or normalized_1000 for the entire action; never mix coordinate units.")
    if tool not in positions:
        if coordinate_space is not None or observation is not None:
            raise ArgumentError("invalid_coordinate_context", "Coordinate options apply only to tap, swipe, gesture, or scroll.")
        return dict(arguments)

    extra = {"tap": set(), "swipe": {"duration_ms"}, "gesture": {"points"}, "scroll": {"deltaX", "deltaY"}}[tool]
    fields(arguments, {"session_id", "operation_id", "observation_id"} | set(positions[tool]) | extra)
    normalized = coordinate_space == "normalized_1000"
    if normalized and observation is None:
        raise ArgumentError("invalid_coordinate_context", "normalized_1000 requires the current observe structuredContent: session_id, observation_id, image_width, image_height, and expires_at.")
    dimensions = None
    if observation is not None:
        if (not isinstance(observation, dict) or not {"session_id", "observation_id", "image_width", "image_height", "expires_at"} <= set(observation)
                or any(observation.get(key) != arguments[key] for key in ("session_id", "observation_id"))):
            raise ArgumentError("invalid_coordinate_context", "Copy the current observe structuredContent for this exact session_id and observation_id.")
        dimensions = (observation["image_width"], observation["image_height"])
        if any(type(value) is not int or not 1 <= value <= 16384 for value in dimensions):
            raise ArgumentError("invalid_coordinate_context", "Use actual integer image_width/image_height, never control_width/control_height or assumed dimensions.")
        if observation_expiry(observation["expires_at"]) <= time.time() + 1:
            raise ArgumentError("observation_expired_before_dispatch", "Observe and inspect a fresh image before preparing another visual action.")

    def point(value, names):
        result = dict(value)
        for index, name in enumerate(names):
            number(name, value[name], 0, 1000 if normalized else 16384, integer=not normalized)
            size = dimensions[index % 2] if dimensions else None
            if normalized:
                result[name] = min(size - 1, math.floor(value[name] * size / 1000))
            elif size is not None and value[name] >= size:
                raise ArgumentError("invalid_coordinate_value", "Screenshot coordinates must be smaller than the actual image width/height.", field=name)
        return result

    prepared = point(arguments, positions[tool])
    if tool == "swipe":
        number("duration_ms", arguments["duration_ms"], 50, 5000, integer=True)
    if tool == "scroll":
        for name in ("deltaX", "deltaY"):
            number(name, arguments[name], -10000, 10000)
    if tool == "gesture":
        if not isinstance(arguments["points"], list) or not 2 <= len(arguments["points"]) <= 512:
            raise ArgumentError("invalid_tool_arguments", "gesture requires 2-512 points.")
        prepared["points"] = []
        for item in arguments["points"]:
            if not isinstance(item, dict):
                raise ArgumentError("invalid_tool_arguments", "Each gesture point must be an object using one coordinate unit for the whole action.")
            fields(item, {"pointerId", "phase", "x", "y", "at_ms"})
            number("pointerId", item["pointerId"], 0, 9, integer=True)
            number("at_ms", item["at_ms"], 0, 5000, integer=True)
            if item["phase"] not in ("down", "move", "up"):
                raise ArgumentError("invalid_tool_arguments", "Gesture phase must be down, move, or up.")
            prepared["points"].append(point(item, ("x", "y")))
    return prepared


def invoke(credential_name, method, tool=None, arguments=None, *, raw_result=False,
           coordinate_space=None, observation=None, request_timeout=30, response_deadline=None):
    if not isinstance(credential_name, str) or not credential_name.strip() or len(credential_name) > 256 or any(ord(c) < 32 for c in credential_name):
        raise AdapterError("invalid_credential_name")
    if method not in ("tools/list", "tools/call") or (method == "tools/call" and (
            not isinstance(tool, str) or not re.fullmatch(r"[A-Za-z0-9_.-]{1,80}", tool) or not isinstance(arguments, dict))):
        raise AdapterError("invalid_arguments")
    if method == "tools/call":
        arguments = prepare_arguments(tool, arguments, coordinate_space=coordinate_space, observation=observation)
    elif coordinate_space is not None or observation is not None:
        raise ArgumentError("invalid_coordinate_context", "Coordinate options apply only to a visual tools/call request.")
    if type(request_timeout) not in (int, float) or not 0 < request_timeout <= 30 or not math.isfinite(request_timeout):
        raise ArgumentError("invalid_request_timeout", "Request timeout must be greater than zero and at most 30 seconds.")
    if response_deadline is not None:
        if type(response_deadline) not in (int, float) or not math.isfinite(response_deadline):
            raise ArgumentError("invalid_response_deadline", "Response deadline must be a finite monotonic timestamp.")
        if time.monotonic() >= response_deadline:
            raise AdapterError("response_deadline_exceeded")
    request_id = str(uuid.uuid4())
    payload = {"jsonrpc": "2.0", "id": request_id, "method": method, "params": {"_meta": {
        "io.modelcontextprotocol/protocolVersion": PROTOCOL,
        "io.modelcontextprotocol/clientCapabilities": {},
        "io.modelcontextprotocol/clientInfo": {"name": "cloudhandset-muse-adapter", "version": "0.1.2"}}}}
    if method == "tools/call":
        payload["params"].update({"name": tool, "arguments": arguments})
    data = json.dumps(payload, allow_nan=False).encode()
    if len(data) > 65536:
        raise AdapterError("request_too_large")
    headers = {"User-Agent": "CloudHandset-Muse/0.1.2",
               "Content-Type": "application/json", "Accept": "application/json, text/event-stream",
               "Accept-Encoding": "identity", "Mcp-Protocol-Version": PROTOCOL, "Mcp-Method": method}
    if tool:
        headers["Mcp-Name"] = tool
    request = urllib.request.Request(ENDPOINT, data=data, headers=headers, method="POST")
    helper = muse_credentials()
    try:
        helper.add_surrogate_to_request(request, credential_name, allowed_hosts=ALLOWED_HOSTS)
    except Exception:
        raise AdapterError("credential_unavailable") from None
    if request.full_url != ENDPOINT or request.get_method() != "POST":
        raise AdapterError("invalid_credential_request")
    try:
        if response_deadline is not None:
            remaining = response_deadline - time.monotonic()
            if remaining <= 0:
                raise AdapterError("response_deadline_exceeded")
            request_timeout = min(request_timeout, remaining)
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=request_timeout) as response:
            if response.status != 200:
                raise AdapterError(f"http_{response.status}")
            if response.headers.get("Content-Encoding", "identity").lower() != "identity":
                raise AdapterError("unsupported_content_encoding")
            raw = helper.read_response_body(LimitedResponse(response, response_deadline))
            content_type = response.headers.get_content_type()
    except urllib.error.HTTPError as error:
        delay = error.headers.get("Retry-After", "60")
        raise AdapterError(f"http_{error.code}", int(delay) if error.code == 429 and delay.isdigit() else 60 if error.code == 429 else None) from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise AdapterError("network_error_outcome_unknown") from None
    result = parse_response(raw, content_type, request_id)
    return result if raw_result else present_result(result)


def _upload_wait_options(wait_seconds, poll_interval_seconds):
    if (type(wait_seconds) not in (int, float) or not 0 <= wait_seconds <= 300
            or type(poll_interval_seconds) not in (int, float) or not 2 <= poll_interval_seconds <= 60):
        raise AdapterError("invalid_upload_wait_options")


def wait_upload_completion(credential_name, session_id, upload_id, complete_operation_id, expected_size,
                           *, wait_seconds=120, poll_interval_seconds=5, initial_receipt=None):
    """Read only the original completion; never replay begin, PUT, or complete."""
    _upload_wait_options(wait_seconds, poll_interval_seconds)
    try:
        if any(str(uuid.UUID(value)) != value for value in (session_id, upload_id)):
            raise ValueError()
    except (ValueError, TypeError, AttributeError):
        raise AdapterError("invalid_upload_context") from None
    if (not isinstance(complete_operation_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", complete_operation_id)
            or type(expected_size) is not int or not 1 <= expected_size <= 30 * 1024 * 1024):
        raise AdapterError("invalid_upload_context")
    context = {"session_id": session_id, "upload_id": upload_id,
               "complete_operation_id": complete_operation_id, "expected_size": expected_size}
    deadline = time.monotonic() + wait_seconds
    last_receipt = initial_receipt
    reads = 0

    def finish(state, code=None, **extra):
        return present_result({**context, "isError": state != "succeeded", "completion_state": state,
            "upload_complete": state == "succeeded", "can_start_next_upload": False,
            "session_checked_active": False, "retry_performed": False,
            "status_queries": reads, "last_receipt": last_receipt,
            **({"error_code": code} if code else {}), **extra})

    def status_error_details(error):
        return {"status_dispatch_state": "not_dispatched", "status_outcome": "validation_rejected", "automatic_retry": False,
                **(error.details if isinstance(error, ArgumentError) else {})} if is_preflight_error(error) else {}

    def confirm_active(file):
        nonlocal reads
        if time.monotonic() >= deadline:
            return finish("succeeded", "upload_session_check_pending", isError=True, file=file)
        try:
            reads += 1
            response = invoke(credential_name, "tools/call", "device_tool", {
                "action": "file.upload_status", "session_id": session_id, "upload_id": upload_id,
            }, raw_result=True, request_timeout=min(30, max(0.001, deadline - time.monotonic())), response_deadline=deadline)
            metadata = response.get("structuredContent", {})
            result = metadata.get("result", {}) if isinstance(metadata, dict) else {}
            code = metadata.get("error_code") if isinstance(metadata, dict) else None
            valid = (not response.get("isError") and not code and isinstance(result, dict)
                and not result.get("error_code") and metadata.get("session_id") == session_id
                and metadata.get("action") == "file.upload_status" and metadata.get("state") == "submitted_to_device"
                and result.get("state", result.get("status")) == "succeeded"
                and upload_id in (metadata.get("job_id"), result.get("job_id"), result.get("upload_id"))
                and all(value is None or value == upload_id for value in
                        (metadata.get("job_id"), result.get("job_id"), result.get("upload_id")))
                and type(result.get("bytes")) is int and result["bytes"] == expected_size and result.get("path") == file["path"])
            extra = {"file": file, "session_check_receipt": response}
            if valid:
                return finish("succeeded", session_checked_active=True, can_start_next_upload=True,
                    continuation_scope="as_of_check_only", **extra)
            if code == "rate_limited":
                values = [metadata.get("retry_after_seconds"),
                    metadata.get("retry_after_ms", 0) / 1000 if type(metadata.get("retry_after_ms")) in (int, float) else None]
                delays = [value for value in values if type(value) in (int, float) and 0 <= value < float("inf")]
                extra["retry_after_seconds"] = max(delays) if delays else 60
            return finish("succeeded", code or "upload_session_status_unverified", isError=True, **extra)
        except (Exception, KeyboardInterrupt) as error:
            extra = {"retry_after_seconds": error.retry_after_seconds} if isinstance(error, AdapterError) and error.retry_after_seconds is not None else {}
            return finish("succeeded", str(error) if isinstance(error, AdapterError) else "upload_session_check_unavailable",
                isError=True, file=file, **extra, **status_error_details(error))

    def terminal(receipt):
        if not isinstance(receipt, dict):
            return finish("pending", "invalid_completion_receipt")
        # A received/submitted RPC is not evidence that the Android phone finished the upload.
        if (receipt.get("session_id") != session_id or receipt.get("operation_id") != complete_operation_id
                or receipt.get("action") != "file.upload_complete"):
            return finish("pending", "completion_receipt_mismatch")
        result = receipt.get("result", {})
        if not isinstance(result, dict):
            return finish("pending", "invalid_completion_receipt")
        if any(value is not None and value != upload_id for value in (
                receipt.get("job_id"), result.get("job_id"), result.get("upload_id"))):
            return finish("pending", "completion_receipt_mismatch")
        state = result.get("state", result.get("status"))
        if receipt.get("state") == "unknown" or state == "unknown":
            return finish("unknown", receipt.get("error_code") or result.get("error_code") or "upload_outcome_unknown")
        if (receipt.get("state") in ("rejected_before_dispatch", "canceled_before_dispatch")
                or state in ("failed", "canceled", "cancelled")):
            return finish("failed", receipt.get("error_code") or result.get("error_code") or "upload_completion_failed")
        if receipt.get("error_code") or result.get("error_code"):
            return finish("unknown", receipt.get("error_code") or result.get("error_code"))
        if state == "succeeded":
            path = result.get("path")
            if (receipt.get("state") != "submitted_to_device"
                    or upload_id not in (receipt.get("job_id"), result.get("job_id"), result.get("upload_id"))
                    or type(result.get("bytes")) is not int or result["bytes"] != expected_size
                    or not isinstance(path, str) or not re.fullmatch(
                        r"/sdcard/Download/CloudHandset/" + re.escape(upload_id[:8]) + r"-[^/\\\x00-\x1f]{1,160}", path)):
                return finish("pending", "upload_completion_unverified")
            return confirm_active(result)
        if receipt.get("state") not in ("received", "dispatching", "submitted_to_device"):
            return finish("pending", "upload_completion_unverified")
        return None

    if last_receipt is not None:
        resolved = terminal(last_receipt)
        if resolved:
            return resolved
    while time.monotonic() < deadline:
        delay = poll_interval_seconds
        try:
            reads += 1
            response = invoke(credential_name, "tools/call", "device_tool", {
                "action": "operation.status", "session_id": session_id, "operation_id": complete_operation_id,
            }, raw_result=True, request_timeout=min(30, max(0.001, deadline - time.monotonic())), response_deadline=deadline)
            metadata = response.get("structuredContent", {})
            if not isinstance(metadata, dict):
                return finish("pending", "invalid_completion_receipt")
            code = metadata.get("error_code")
            if code == "rate_limited":
                delays = [metadata.get("retry_after_seconds"),
                          metadata.get("retry_after_ms", 0) / 1000 if type(metadata.get("retry_after_ms")) in (int, float) else None]
                valid = [value for value in delays if type(value) in (int, float) and 0 <= value < float("inf")]
                delay = max([poll_interval_seconds, *valid]) if valid else max(poll_interval_seconds, 60)
            elif code == "operation_not_found":
                # Read progress once, but never equate a missing completion record with success.
                progress = None
                if time.monotonic() < deadline:
                    try:
                        reads += 1
                        progress = invoke(credential_name, "tools/call", "device_tool", {
                            "action": "file.upload_status", "session_id": session_id, "upload_id": upload_id,
                        }, raw_result=True, request_timeout=min(30, max(0.001, deadline - time.monotonic())), response_deadline=deadline)
                    except Exception as error:
                        progress = {"isError": True, "error_code": str(error) if isinstance(error, AdapterError) else "upload_progress_unavailable",
                                    **status_error_details(error)}
                return finish("pending", "operation_not_found", upload_progress=progress)
            elif response.get("isError") and metadata.get("operation_id") != complete_operation_id:
                return finish("unknown", code or "upload_status_failed")
            else:
                last_receipt = metadata
                resolved = terminal(last_receipt)
                if resolved:
                    return resolved
        except KeyboardInterrupt:
            return finish("pending", "upload_wait_interrupted")
        except Exception as error:
            if time.monotonic() >= deadline or isinstance(error, AdapterError) and str(error) == "response_deadline_exceeded":
                return finish("pending", "upload_completion_pending")
            if isinstance(error, AdapterError) and error.retry_after_seconds is not None:
                delay = max(poll_interval_seconds, error.retry_after_seconds)
                code = "rate_limited"
            else:
                return finish("unknown", str(error) if isinstance(error, AdapterError) else "upload_status_unavailable",
                    **status_error_details(error))
        remaining = deadline - time.monotonic()
        if delay >= remaining:
            return finish("pending", "upload_completion_pending", **({"retry_after_seconds": delay} if code == "rate_limited" else {}))
        try:
            time.sleep(delay)
        except KeyboardInterrupt:
            return finish("pending", "upload_wait_interrupted")
    return finish("pending", "upload_completion_pending")


def upload_file(credential_name, path, session_id, operation_id, *, wait_seconds=120, poll_interval_seconds=5):
    _upload_wait_options(wait_seconds, poll_interval_seconds)
    spec = importlib.util.spec_from_file_location("cloudhandset_upload", os.path.join(os.path.dirname(__file__), "upload_file.py"))
    uploader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(uploader)
    metadata = uploader.file_bytes(path)[1]
    try:
        prepared = invoke(credential_name, "tools/call", "device_tool", {
            "action": "file.upload_begin", "session_id": session_id, "operation_id": operation_id, **metadata,
        }, raw_result=True)
    except (Exception, KeyboardInterrupt) as error:
        rejected = is_preflight_error(error)
        return present_result({"isError": True, "session_id": session_id, "operation_id": operation_id,
            "completion_state": "not_started_this_attempt" if rejected else "unknown", "upload_complete": False, "can_start_next_upload": False,
            "error_code": str(error) if isinstance(error, AdapterError) else "upload_begin_outcome_unknown",
            **({"dispatch_state": "not_dispatched", "outcome": "validation_rejected", "automatic_retry": False,
                **(error.details if isinstance(error, ArgumentError) else {})} if rejected else {})})
    if prepared.get("isError"):
        return present_result({**prepared, "session_id": session_id, "operation_id": operation_id,
            "upload_complete": False, "can_start_next_upload": False})
    details = prepared.get("structuredContent", {})
    ticket = details.get("upload") if isinstance(details, dict) else None
    if not isinstance(ticket, dict) or not ticket:
        legacy = details.get("result", {}) if isinstance(details, dict) else {}
        return present_result({"isError": True, "session_id": session_id, "operation_id": operation_id,
            "upload_id": legacy.get("upload_id") if isinstance(legacy, dict) else None,
            "upload_complete": False, "can_start_next_upload": False, "error_code": "fast_upload_not_supported"})
    context = {key: ticket.get(key) for key in ("session_id", "upload_id", "complete_operation_id")}
    context.update(operation_id=operation_id, expected_size=metadata["size"])
    try:
        # Validate recovery context before transferring; no credentials/ticket are returned.
        wait_upload_completion(credential_name, context["session_id"], context["upload_id"],
            context["complete_operation_id"], metadata["size"], wait_seconds=0)
        if context["session_id"] != session_id:
            raise AdapterError("invalid_upload_context")
        receipt, transfer_error = None, None
        try:
            receipt = uploader.send_file(path, ticket)
        except Exception as error:
            transfer_error = str(error) if isinstance(error, uploader.UploadError) else "upload_outcome_unknown"
        result = wait_upload_completion(credential_name, context["session_id"], context["upload_id"],
            context["complete_operation_id"], metadata["size"], wait_seconds=wait_seconds,
            poll_interval_seconds=poll_interval_seconds, initial_receipt=receipt.get("receipt") if isinstance(receipt, dict) else None)
        result["result"].update(operation_id=operation_id)
        if receipt is not None:
            result["result"]["transfer_receipt"] = present_result(receipt)["result"]
        if transfer_error:
            result["result"]["transfer_error"] = transfer_error
        return result
    except (Exception, KeyboardInterrupt) as error:
        return present_result({"isError": True, **context, "completion_state": "unknown", "upload_complete": False, "can_start_next_upload": False,
            "error_code": str(error) if isinstance(error, AdapterError) else "upload_outcome_unknown"})

def parallel(credential_name, batch, workers, calls_per_minute):
    """One step per Android phone, with pacing local to this finite batch."""
    session_tools = {"observe", "release_control", "tap", "swipe", "input_text",
                     "press_key", "gesture", "scroll", "key_event", "device_tool"}
    if (type(workers) is not int or workers < 1 or type(calls_per_minute) is not int
            or not 1 <= calls_per_minute <= 180 or not isinstance(batch, dict)
            or set(batch) != {"sessions", "requests"} or not isinstance(batch["sessions"], dict)
            or not isinstance(batch["requests"], list) or not batch["requests"]):
        raise AdapterError("invalid_parallel_arguments")
    if workers > MAX_CONCURRENT_DEVICES:
        raise AdapterError("parallel_worker_limit_exceeded")
    try:
        batch_size = len(json.dumps(batch, allow_nan=False).encode())
    except (ValueError, TypeError):
        raise ArgumentError("invalid_parallel_arguments", "Use finite JSON values; NaN and infinity are not valid arguments.") from None
    if batch_size > 65536:
        raise AdapterError("request_too_large")

    def identifier(value):
        try:
            return str(uuid.UUID(value))
        except (ValueError, TypeError, AttributeError):
            raise AdapterError("invalid_parallel_target") from None

    sessions = {identifier(device): identifier(session) for device, session in batch["sessions"].items()}
    if len(sessions) != len(batch["sessions"]) or len(set(sessions.values())) != len(sessions):
        raise AdapterError("duplicate_parallel_session")
    targets, jobs = set(), []
    for item in batch["requests"]:
        if (not isinstance(item, dict) or set(item) - {"device_id", "tool", "arguments", "observation_expires_at", "coordinate_space", "observation"}
                or not {"device_id", "tool", "arguments"} <= set(item)
                or not isinstance(item["tool"], str) or item["tool"] not in session_tools | {"acquire_control"}
                or not isinstance(item["arguments"], dict)):
            raise AdapterError("invalid_parallel_arguments")
        device, tool, arguments = identifier(item["device_id"]), item["tool"], item["arguments"]
        if device in targets:
            raise AdapterError("duplicate_parallel_target")
        targets.add(device)
        if tool == "acquire_control":
            if (identifier(arguments.get("device_id")) != device or "session_id" in arguments
                    or device in sessions):
                raise AdapterError("mixed_parallel_target")
        elif (device not in sessions or identifier(arguments.get("session_id")) != sessions[device]
              or "device_id" in arguments):
            raise AdapterError("mixed_parallel_target")
        if tool == "device_tool" and (not isinstance(arguments.get("action"), str)
                                      or arguments["action"].startswith("share.") or arguments["action"] == "apps.list"):
            raise AdapterError("invalid_parallel_action")
        try:
            arguments = prepare_arguments(tool, arguments, coordinate_space=item.get("coordinate_space"), observation=item.get("observation"))
        except ArgumentError as error:
            error.details.update(device_id=device, tool=tool)
            raise
        expires = None
        if "observation_id" in arguments:
            identifier(arguments["observation_id"])
            try:
                context_expiry = item.get("observation", {}).get("expires_at") if isinstance(item.get("observation"), dict) else None
                expiry = datetime.fromisoformat(item.get("observation_expires_at", context_expiry).replace("Z", "+00:00"))
                if expiry.tzinfo is None:
                    raise ValueError()
                expires = expiry.timestamp()
                if context_expiry is not None and observation_expiry(context_expiry) != expires:
                    raise ArgumentError("invalid_coordinate_context", "observation_expires_at must match the supplied observe result's expires_at.")
            except (KeyError, ValueError, TypeError, AttributeError, OverflowError):
                raise AdapterError("observation_expiry_required") from None
        safety = tool == "release_control" or tool == "device_tool" and arguments.get("action") == "operation.status"
        jobs.append((device, tool, arguments, expires, "control" if safety else "tool"))
    if len(targets | set(sessions)) > MAX_CONCURRENT_DEVICES:
        raise AdapterError("parallel_device_limit_exceeded")

    # One coordinator must own the connection; independent processes do not share this budget.
    lock = threading.Lock()
    canceled = threading.Event()
    next_start = {"tool": 0.0, "control": 0.0, "acquire": 0.0}
    blocked = {}
    intervals = {"tool": 60 / calls_per_minute, "control": 1.0}

    def run(job):
        device, tool, arguments, expires, bucket = job
        context = {"device_id": device, "tool": tool, **{key: arguments[key] for key in (
            "session_id", "operation_id", "observation_id", "after_operation_id") if key in arguments}}
        context = present_result(context)["result"]
        with lock:
            slot = max(time.monotonic(), next_start[bucket])
            if tool == "acquire_control":
                slot = max(slot, next_start["acquire"])
                next_start["acquire"] = slot + 1.0
            next_start[bucket] = slot + intervals[bucket]
        while True:
            if canceled.is_set():
                return {**context, "dispatch_state": "not_dispatched", "response": {
                    "error": "batch_canceled", "retry_performed": False}}
            with lock:
                pause = blocked.get(bucket)
                account_full = blocked.get("acquire_limit") if tool == "acquire_control" else None
            if account_full:
                return {**context, "dispatch_state": "not_dispatched", "response": {
                    "error": "account_device_limit_reached", "max_concurrent_devices": MAX_CONCURRENT_DEVICES,
                    "required_action": "release_another_device", "automatic_retry": False, "retry_performed": False}}
            if pause is not None:
                return {**context, "dispatch_state": "not_dispatched", "response": {
                    "error": "batch_rate_limited", "retry_after_seconds": pause, "retry_performed": False}}
            if expires is not None and expires <= time.time() + 1:
                return {**context, "dispatch_state": "not_dispatched", "response": {
                    "error": "observation_expired_before_dispatch", "retry_performed": False}}
            wait = slot - time.monotonic()
            if wait <= 0:
                break
            time.sleep(min(wait, 0.05))
        try:
            response = invoke(credential_name, "tools/call", tool, arguments)
            state = "response_received"
            metadata = response.get("result", {}).get("structuredContent", {})
            if metadata.get("dispatch_state") == "not_dispatched":
                state = "not_dispatched"
            delay = metadata.get("retry_after_seconds", 60) if metadata.get("error_code") == "rate_limited" else None
            if metadata.get("error_code") == "account_device_limit_reached":
                with lock:
                    blocked["acquire_limit"] = True
        except Exception as error:
            rejected = is_preflight_error(error)
            response = {"error": str(error) if isinstance(error, AdapterError) else "adapter_failed",
                        "outcome": "validation_rejected" if rejected else "unknown_no_retry", "retry_performed": False,
                        **(error.details if isinstance(error, ArgumentError) else {})}
            state = "not_dispatched" if rejected else "outcome_unknown"
            delay = error.retry_after_seconds if isinstance(error, AdapterError) else None
            if delay is not None:
                response["retry_after_seconds"] = delay
        if delay is not None:
            with lock:
                blocked[bucket] = delay
        return {**context, "dispatch_state": state, "response": response}

    completed = {}

    def collect(index):
        result = run(jobs[index])
        with lock:
            completed[index] = result
        return result

    with ThreadPoolExecutor(max_workers=min(workers, len(jobs))) as executor:
        # Dispatch cleanup first while returning results in the caller's original order.
        order = sorted(range(len(jobs)), key=lambda i: 0 if jobs[i][1] == "release_control" else 1 if jobs[i][4] == "control" else 2)
        futures = []
        try:
            for i in order:
                futures.append(executor.submit(collect, i))
            for future in futures:
                future.result()
        except KeyboardInterrupt:
            canceled.set()
    # A canceled submit may already be running even when its Future was not registered.
    results = [completed[i] if i in completed else run(jobs[i]) for i in range(len(jobs))]
    failed = any(item["response"].get("error") or item["response"].get("result", {}).get("isError")
                 or item["response"].get("image_errors") for item in results)
    return {"result": {"isError": failed, "results": results}, "images": [], "image_errors": [],
            "retry_performed": False, "pacing": {"scope": "this_batch_only", "calls_per_minute": calls_per_minute,
            "next_batch_delay_seconds": {bucket: max(0, when - time.monotonic()) for bucket, when in next_start.items()}}}


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentError("invalid_arguments", "Check the command's required arguments and options with --help.")


def main(argv=None):
    try:
        parser = Parser(description=__doc__)
        parser.add_argument("--credential-name", required=True)
        commands = parser.add_subparsers(dest="command", required=True)
        commands.add_parser("tools/list")
        call = commands.add_parser("call")
        call.add_argument("tool")
        call.add_argument("arguments", help="JSON object, with the exact live tool schema")
        call.add_argument("--coordinate-space", choices=("screenshot_pixels", "normalized_1000"),
                          help="Position coordinates for the whole action; default is unchanged screenshot pixels")
        call.add_argument("--observation", help="Current observe structuredContent JSON; required for normalized_1000")
        batch = commands.add_parser("parallel", help="One step per distinct Android phone; no automatic follow-up")
        batch.add_argument("arguments", help="JSON object with sessions and one request per phone; at most 16 distinct phones")
        batch.add_argument("--workers", type=int, required=True, help="Concurrent requests (1-16); the service enforces 16 controlled phones across the account")
        batch.add_argument("--calls-per-minute", type=int, required=True, help="Ordinary call budget for this batch (1-180)")
        upload = commands.add_parser("upload", help="Send one file once, then check its original completion within a deadline")
        upload.add_argument("file")
        upload.add_argument("--session-id", required=True)
        upload.add_argument("--operation-id", required=True)
        upload.add_argument("--wait-seconds", type=int, default=120, help="Completion-check budget after PUT (0-300 seconds)")
        upload.add_argument("--poll-interval-seconds", type=int, default=5, help="Read-only status interval (2-60 seconds); share the control budget")
        upload_status = commands.add_parser("upload-status", help="Check an existing upload; never send file data or repeat completion")
        upload_status.add_argument("--session-id", required=True)
        upload_status.add_argument("--upload-id", required=True)
        upload_status.add_argument("--complete-operation-id", required=True)
        upload_status.add_argument("--expected-size", type=int, required=True)
        upload_status.add_argument("--wait-seconds", type=int, default=120)
        upload_status.add_argument("--poll-interval-seconds", type=int, default=5)
        args = parser.parse_args(argv)
        if args.command == "parallel":
            result = parallel(args.credential_name, parse_argument_json(args.arguments), args.workers, args.calls_per_minute)
        elif args.command == "upload":
            result = upload_file(args.credential_name, args.file, args.session_id, args.operation_id,
                wait_seconds=args.wait_seconds, poll_interval_seconds=args.poll_interval_seconds)
        elif args.command == "upload-status":
            result = wait_upload_completion(args.credential_name, args.session_id, args.upload_id,
                args.complete_operation_id, args.expected_size, wait_seconds=args.wait_seconds,
                poll_interval_seconds=args.poll_interval_seconds)
        else:
            result = invoke(args.credential_name, "tools/list") if args.command == "tools/list" else invoke(
                args.credential_name, "tools/call", args.tool, parse_argument_json(args.arguments),
                coordinate_space=args.coordinate_space, observation=parse_argument_json(args.observation) if args.observation is not None else None)
        print(json.dumps(result, ensure_ascii=False))
        return 2 if result["result"].get("isError") or result["image_errors"] else 0
    except Exception as error:
        code = str(error) if isinstance(error, AdapterError) else "adapter_failed"
        rejected = is_preflight_error(error)
        print(json.dumps({"error": code, "outcome": "validation_rejected" if rejected else "unknown_no_retry", "retry_performed": False,
                          **({"dispatch_state": "not_dispatched", "automatic_retry": False} if rejected else {}),
                          **({"max_concurrent_devices": MAX_CONCURRENT_DEVICES} if code in {"parallel_worker_limit_exceeded", "parallel_device_limit_exceeded"} else {}),
                          **(error.details if isinstance(error, ArgumentError) else {})}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
