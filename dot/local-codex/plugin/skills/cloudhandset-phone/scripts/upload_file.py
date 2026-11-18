#!/usr/bin/env python3
"""Inspect a file or send it once using a file-bound CloudHandset upload ticket from stdin."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.request

ORIGIN = "https://device.cloudhandset.com"
MAX_BYTES = 30 * 1024 * 1024


class UploadError(Exception):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, url):
        raise UploadError("upload_redirect_blocked")


def file_bytes(path):
    source = Path(path)
    with source.open("rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    if not 1 <= len(data) <= MAX_BYTES:
        raise UploadError("file_size_out_of_range")
    name = source.name
    if len(name) > 160 or not name.strip() or re.search(r"[\\/\x00-\x1f]", name):
        raise UploadError("invalid_filename")
    return data, {"name": name, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def send_file(path, ticket):
    data, metadata = file_bytes(path)
    if not isinstance(ticket, dict):
        raise UploadError("invalid_upload_ticket")
    upload_id = ticket.get("upload_id", "")
    if not isinstance(upload_id, str) or not re.fullmatch(r"[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12}", upload_id):
        raise UploadError("invalid_upload_ticket")
    route = "/mcp/uploads/" + upload_id
    token = ticket.get("upload_token", "")
    if (ticket.get("upload_path") != route or ticket.get("method") != "PUT"
            or ticket.get("content_type") != "application/octet-stream"
            or not isinstance(token, str) or not re.fullmatch(r"[a-f0-9]{64}", token)):
        raise UploadError("invalid_upload_ticket")
    if ticket.get("size") != metadata["size"] or ticket.get("sha256") != metadata["sha256"]:
        raise UploadError("file_changed_since_prepare")
    request = urllib.request.Request(ORIGIN + route, data=data, method="PUT", headers={
        "Authorization": "Upload " + token, "Content-Type": "application/octet-stream",
        "Accept": "application/json", "Accept-Encoding": "identity",
        "User-Agent": "CloudHandset-File-Upload/0.1.0",
    })
    started = time.monotonic()
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=180) as response:
            raw = response.read(65537)
            if response.status != 200 or len(raw) > 65536 or response.headers.get_content_type() != "application/json":
                raise UploadError("invalid_upload_response")
            result = json.loads(raw)
    except urllib.error.HTTPError as error:
        raise UploadError("upload_http_" + str(error.code)) from None
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        raise UploadError("upload_outcome_unknown") from None
    if not isinstance(result, dict) or result.get("upload_id") != upload_id or result.get("session_id") != ticket.get("session_id"):
        raise UploadError("invalid_upload_response")
    receipt = result.get("receipt", {})
    status = receipt.get("result", {}).get("state", receipt.get("state"))
    if receipt.get("error_code") or status in ("failed", "canceled", "unknown", "rejected_before_dispatch", "canceled_before_dispatch"):
        result["isError"] = True
    result["client_transfer_ms"] = round((time.monotonic() - started) * 1000)
    result["retry_performed"] = False
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["inspect", "send"])
    parser.add_argument("file")
    args = parser.parse_args(argv)
    ticket = {}
    try:
        if args.command == "inspect":
            result = file_bytes(args.file)[1]
        else:
            raw = sys.stdin.read(16385)
            if len(raw) > 16384:
                raise UploadError("invalid_upload_ticket")
            ticket = json.loads(raw)
            result = send_file(args.file, ticket)
        print(json.dumps(result))
        return 2 if result.get("isError") else 0
    except Exception as error:
        context = {key: ticket[key] for key in ("session_id", "upload_id", "complete_operation_id") if isinstance(ticket, dict) and key in ticket}
        print(json.dumps({"error": str(error) if isinstance(error, UploadError) else "upload_failed", "retry_performed": False,
                          "outcome": "check_status_before_retry", **context}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
