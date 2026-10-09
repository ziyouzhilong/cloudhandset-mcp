#!/usr/bin/env python3
"""One MCP request using Muse's credential surrogate; never retries or acquires control automatically."""
import argparse
import base64
import binascii
import importlib.util
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.request
import uuid

ENDPOINT = "https://device.cloudhandset.com/mcp"
ALLOWED_HOSTS = ["device.cloudhandset.com"]
PROTOCOL = "2026-07-28"
MAX_RESPONSE = 8 * 1024 * 1024
MAX_IMAGE = 2 * 1024 * 1024
HELPER = "/opt/hatch/skills/skill-creator/bin/dynamic_credentials.py"


class AdapterError(Exception):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, url):
        raise AdapterError("redirect_blocked")


class LimitedResponse:
    def __init__(self, response):
        self.response, self.remaining = response, MAX_RESPONSE

    def read(self, size=-1):
        limit = self.remaining + 1
        data = self.response.read(limit if size < 0 else min(size, limit))
        self.remaining -= len(data)
        if self.remaining < 0:
            raise AdapterError("response_too_large")
        return data


def muse_credentials():
    spec = importlib.util.spec_from_file_location("dynamic_credentials", HELPER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
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
            return {key: "[redacted]" if key.lower() in ("authorization", "cookie", "set-cookie", "access_token", "refresh_token", "client_secret")
                    else "[binary omitted]" if key in ("data", "blob") and isinstance(item, str)
                    else clean(item) for key, item in value.items()}
        if isinstance(value, str):
            return re.sub(r"(?i)hsurr:[^\s\"'<>]+|Bearer\s+[^\s\"'<>]+|chmcp_[A-Za-z0-9_-]+|[A-Za-z0-9+/]{128,}={0,2}", "[redacted]", value)
        return value

    cleaned = clean(result)
    return {"result": cleaned, "images": images, "image_errors": failures,
            "image_acceptance": "not_verified", "retry_performed": False}


def invoke(credential_name, method, tool=None, arguments=None):
    if not isinstance(credential_name, str) or not credential_name.strip() or len(credential_name) > 256 or any(ord(c) < 32 for c in credential_name):
        raise AdapterError("invalid_credential_name")
    if method not in ("tools/list", "tools/call") or (method == "tools/call" and (
            not isinstance(tool, str) or not re.fullmatch(r"[A-Za-z0-9_.-]{1,80}", tool) or not isinstance(arguments, dict))):
        raise AdapterError("invalid_arguments")
    request_id = str(uuid.uuid4())
    payload = {"jsonrpc": "2.0", "id": request_id, "method": method, "params": {"_meta": {
        "io.modelcontextprotocol/protocolVersion": PROTOCOL,
        "io.modelcontextprotocol/clientCapabilities": {},
        "io.modelcontextprotocol/clientInfo": {"name": "cloudhandset-muse-adapter", "version": "0.1.0"}}}}
    if method == "tools/call":
        payload["params"].update({"name": tool, "arguments": arguments})
    data = json.dumps(payload, allow_nan=False).encode()
    if len(data) > 65536:
        raise AdapterError("request_too_large")
    headers = {"User-Agent": "CloudHandset-Muse/0.1.0",
               "Content-Type": "application/json", "Accept": "application/json, text/event-stream",
               "Accept-Encoding": "identity", "Mcp-Protocol-Version": PROTOCOL, "Mcp-Method": method}
    if tool:
        headers["Mcp-Name"] = tool
    request = urllib.request.Request(ENDPOINT, data=data, headers=headers, method="POST")
    helper = muse_credentials()
    helper.add_surrogate_to_request(request, credential_name, allowed_hosts=ALLOWED_HOSTS)
    if request.full_url != ENDPOINT or request.get_method() != "POST":
        raise AdapterError("invalid_credential_request")
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=30) as response:
            if response.status != 200:
                raise AdapterError(f"http_{response.status}")
            if response.headers.get("Content-Encoding", "identity").lower() != "identity":
                raise AdapterError("unsupported_content_encoding")
            raw = helper.read_response_body(LimitedResponse(response))
            content_type = response.headers.get_content_type()
    except urllib.error.HTTPError as error:
        raise AdapterError(f"http_{error.code}") from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise AdapterError("network_error_outcome_unknown") from None
    return present_result(parse_response(raw, content_type, request_id))


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise AdapterError("invalid_arguments")


def main(argv=None):
    try:
        parser = Parser(description=__doc__)
        parser.add_argument("--credential-name", required=True)
        commands = parser.add_subparsers(dest="command", required=True)
        commands.add_parser("tools/list")
        call = commands.add_parser("call")
        call.add_argument("tool")
        call.add_argument("arguments", help="JSON object, with the exact live tool schema")
        args = parser.parse_args(argv)
        result = invoke(args.credential_name, "tools/list") if args.command == "tools/list" else invoke(
            args.credential_name, "tools/call", args.tool, json.loads(args.arguments))
        print(json.dumps(result, ensure_ascii=False))
        return 2 if result["result"].get("isError") or result["image_errors"] else 0
    except Exception as error:
        code = str(error) if isinstance(error, AdapterError) else "adapter_failed"
        print(json.dumps({"error": code, "outcome": "unknown_no_retry", "retry_performed": False}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
