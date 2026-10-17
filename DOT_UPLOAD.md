# CloudHandset file upload — Codex, Dot and Muse

Included in Codex **0.1.3**, Dot **0.2.4**, and Muse **0.1.2**. Codex and Dot use `scripts/upload_file.py` in the installed skill. Muse uses its `cloudhandset.py upload` command; see the [Muse tool reference](muse/TOOLS.md#fast-upload-011).

Suggested request: “Upload my attached file to [PHONE NAME] using the packaged fast uploader. Verify completion and the returned Android path, check the intended media picker if needed, and release control. Do not publish anything.”

Use this workflow for a user-requested file transfer. It reuses CloudHandset's existing upload, integrity check and Android phone writer. Maximum file size is 30 MiB. Obtain the selected phone's exclusive `session_id` first.

1. In the host execution environment, run `python3 scripts/upload_file.py inspect /absolute/path/to/file`. Use the actual attachment/local file. The result contains `name`, `size`, and `sha256`; no file bytes enter the model context.
2. Through the existing authenticated MCP connection, call `device_tool` with `action: "file.upload_begin"`, that `session_id`, a fresh `operation_id`, and the three returned file fields. Save `result.upload_id` and the returned `upload` ticket (including `complete_operation_id`) in private process memory or a temporary file accessible only to the user. Never display or publish `upload_token`. It is a one-use capability for this exact file and control session, valid for at most ten minutes; it cannot list or operate phones. Do not extract OAuth credentials.
3. Run `python3 scripts/upload_file.py send /absolute/path/to/file`, supplying only the returned `upload` ticket object as JSON on **stdin**, not command-line arguments. The helper sends one binary PUT to the fixed CloudHandset host. It checks file size/digest, blocks redirects, never retries, and never uses browser cookies or another client's credentials. Remove any private temporary ticket file afterward.
4. A successful PUT means staging finished and final phone transfer was submitted. If `receipt.result.state` is `running`, call the authenticated `device_tool` with `action: "operation.status"`, `session_id`, and the returned **complete_operation_id** until a terminal state, using bounded polling. Success requires `result.state: "succeeded"` plus the expected `bytes` and returned `path`. Preserve both operation IDs on interruption. A lost PUT response is not permission to repeat PUT or prepare another upload: query the original completion operation; if absent, inspect `file.upload_status` for the same upload and report the unresolved transfer.
5. Supported videos/images request Android media scanning where the device Bridge supports it. Verify visibility in the intended app if the task requires it. A successful transfer does not establish publication. Release control and confirm closed/drained after the task.

To cancel, use authenticated `device_tool`, `action: "file.upload_cancel"`, the original `session_id`/`upload_id` and a new operation ID for the cancellation. Session release, lease expiry, revoked account access and manual pause stop the upload writer. Failed transfers are not automatically replayed.

The transfer uses an independent 4 MiB/s byte budget and continuously sends the original 32 KiB chunks from the server. It does not consume one phone-action quota entry per chunk. Normal phone controls retain their existing limits. Each chunk rechecks account/lease/session access; Bridge permits are checked before every original chunk and final device write.

If the current tools do not expose `file.upload_begin`, refresh the existing connection's tools and reload the updated skill. If the begin response does not include an `upload` ticket, the server or selected Android phone does not support this workflow. Report that specific gap. The older `file.upload_begin/chunk/complete` protocol remains compatible, but do not silently fall back to hundreds of slow tool calls.

The host must be able to read the selected file and run the packaged uploader. A local path is read by the host helper, never by the remote MCP server. If that execution/file capability is unavailable, report it; do not invent file bytes or substitute an arbitrary URL fetch.

## Muse 0.1.2 completion checks

The `upload` wrapper verifies the original completion operation instead of treating submission as success. Its default query budget is 120 seconds, checked between available response chunks; a final silent in-flight read can take up to 30 additional seconds to time out. Success requires matching session/upload/operation IDs, `succeeded`, the expected byte count, and the generated Android path. A final read checks whether that session is still active. A completed transfer stays complete if the later session check fails, but the agent must not assume it can start another upload.

For pending or uncertain results, keep `session_id`, `upload_id`, `complete_operation_id`, and `expected_size` and use the read-only `upload-status` command in [SETUP.md](muse/SETUP.md). Never repeat PUT or create another upload ID to resolve an unknown result. Polling and releases share the connection's control-call budget; see [PARALLEL_CONTROL.md](PARALLEL_CONTROL.md) before running multiple waiters. Completion does not itself prove gallery visibility or app publication.
