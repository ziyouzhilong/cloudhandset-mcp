# CloudHandset file upload

Use the authenticated `device_tool`. Call `list_devices`, match the requested phone, and `acquire_control`; retain its `session_id`. Upload requires exclusive control but no `observation_id`.

## Exact arguments

All fields are top-level arguments, without an `input` or `parameters` wrapper. The tool name may have a connector prefix.

| `action` | Required fields in addition to `action` |
| --- | --- |
| `file.upload_begin` | `session_id`, `operation_id`, `name`, `size`, `sha256` |
| `file.upload_chunk` | `session_id`, `operation_id`, `upload_id`, `offset`, `data` |
| `file.upload_complete` | `session_id`, `operation_id`, `upload_id` |
| `file.upload_status` | `session_id`, `upload_id` |
| `file.upload_cancel` | `session_id`, `operation_id`, `upload_id` |

- IDs: actual returned UUIDs for `session_id` and `upload_id`. Each intended mutation gets a new `operation_id` of 1–64 letters, digits, `_`, or `-`; preserve the original ID when resolving a lost response.
- `name`: safe source basename, 1–160 characters, nonblank, no slash, backslash, or control characters.
- `size`: exact integer byte size, 1–31457280 (30 MiB).
- `sha256`: actual complete-file SHA-256, 64 lowercase hexadecimal characters.
- `offset`: integer decoded-byte offset starting at 0, advanced only by confirmed received bytes.
- `data`: standard base64 of at most 32768 source bytes, maximum 44000 encoded characters. Do not send a data URL or a filename in this field.

## Read and transfer the source file

Use the host's execution environment to read a real attached/local file. Python's `pathlib.Path(path).read_bytes()`, `hashlib.sha256(bytes).hexdigest()`, and `base64.b64encode(bytes[offset:offset + 32768]).decode('ascii')` produce the inputs. Python, requests, and curl do not automatically inherit MCP credentials. Send generated arguments through the authenticated discovered tool.

1. Begin with name, size, and digest. Read the returned `result` object and retain `result.upload_id`/`result.job_id`; `receiving` only means staging started.
2. Send ordered chunks one at a time with distinct operation IDs. Confirm `bytes_received` (or `received`) before advancing. The final chunk may be smaller. A roughly 4.5 MiB video needs about 144 chunks.
3. Device limits are 60 mutations/minute and 2/second per grant: pace at least 1.1 seconds between upload mutations by default, and honor any longer returned delay. Do not send chunks concurrently. Ordinary tool calls have a separate 180/minute allowance; release and operation-status reserve separate capacity.
4. When confirmed received bytes equal size, call complete. Completion may return `running`/`bridge_task_accepted` before the phone finishes. Query `action: operation.status` with the **original complete operation ID** until its `result.state` is `succeeded` or a terminal failure. Retain `result.bytes` and `result.path`. Digest verification precedes transfer; phone file size is checked afterward. A transport response alone is insufficient.
5. Files arrive under `/sdcard/Download/CloudHandset/` with an upload-ID prefix. Use the returned exact path/name. Supported videos and images request Android media indexing; `media_scan_requested` confirms the request, not that an app already refreshed. Reopen/refresh the intended picker and verify the file is visible. Use Files/Downloads only if that app actually offers it; some photo pickers do not. A scan error does not undo the verified transfer or justify re-uploading it. Transfer success does not establish publication.
6. Release control on completion/interruption and confirm closed/drained.

## Lost responses and cleanup

For a timed-out begin/chunk/complete, query `device_tool` with `action: operation.status`, the session, and the **original** operation ID. Never generate a fresh ID to replay an uncertain mutation. During staging, `file.upload_status` reports progress and is exempt from the device-action quota. Completion removes temporary staging, so afterward use the original complete operation's result/status rather than treating upload-status as a permanent file listing.

If the transfer cannot continue, cancel the known staged upload when permitted, then release. On lost control/authentication/lease, stop and report unresolved state. Do not install APKs, reboot, change accounts, or use a shell/URL fetch to bypass upload.

If the host exposes a stale/untyped `device_tool`, refresh/rediscover the existing connection's tools. Report the precise missing field or file-reading capability; documented parameters cannot authorize calls that the host cannot express.
