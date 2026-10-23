# CloudHandset native MCP tools

Reference checked against `server/mcpToolSchemas.ts` on 2026-10-23. Discover the live schemas through Grok Bot's authenticated CloudHandset connection before use. The dedicated Grok OAuth client and private single-phone image/basic-action/small-text-upload/release flow were verified on 2026-10-23. This reference does not grant access or establish acceptance of every tool; each connection requires its own login.

Only `list_devices` and `observe` have the server's top-level read-only hint. The sole OAuth scope is `device:control`; there is no read-only scope. All other tools, including mixed-purpose `device_tool`, retain potentially consequential host approval handling. No host-specific calling API is assumed here.

## Common fields

- `device_id`, `session_id`, `observation_id`, `upload_id`, `app_id`, and `access_id` are UUIDs from service results. Never invent them or move them between phones.
- `operation_id` is 1–64 ASCII letters, digits, underscores, or hyphens. Use a distinct ID per new intended mutation; retain the original request and ID for uncertainty. Changed arguments under the same ID cause `operation_conflict`.
- **S** below means `session_id`; **M** means S plus `operation_id`; **O** means M plus `observation_id`. These are documentation abbreviations, not JSON fields. Inputs are top-level fields and unlisted fields are rejected.
- Coordinates are integer pixels of the current screenshot, within its actual bounds, with a schema ceiling of 16384. The server maps them to the control surface. Observations expire after at most 30 seconds and are invalidated by mutations.
- `observe` returns actual PNG/JPEG pixels as a native MCP `content` image block. `structuredContent.image` contains metadata only. The model must inspect the image before visual actions; no audio is returned.

## The 12 tools

| Tool | Inputs | Effect / result |
| --- | --- | --- |
| `list_devices` | `{}` | Lists currently authorized phones and their availability without acquiring control. Refresh for each task and after adding a phone. |
| `acquire_control` | `device_id`, `operation_id` | Acquires one exclusive session. Check `acquired: true`, `state: "active"`; save `session_id`, epoch, expiry, capabilities. Does not evict a busy writer. |
| `observe` | S; optional `after_operation_id` | Captures a fresh image, observation ID, expiry, and geometry. The optional field associates an existing operation receipt; it does not prove its business outcome. |
| `tap` | O + `x`, `y` | One tap at the observed screenshot position. |
| `swipe` | O + `start_x`, `start_y`, `end_x`, `end_y`, integer `duration_ms` (50–5000) | One swipe. |
| `input_text` | O + nonempty `text`, at most 4096 UTF-8 bytes | Types into the focused field through the clipboard path; does not clear or submit the field. |
| `press_key` | M + `key`: `HOME`, `BACK`, `RECENTS`, `POWER`, `VOLUME_UP`, `VOLUME_DOWN` | Navigation/power/volume operation. Does not take `observation_id`. |
| `release_control` | S only | Stops and drains this writer. Require `closed: true`, `state: "closed"`, and drain evidence in `closed_evidence`; authorization remains valid. |
| `gesture` | O + `points` (2–512 objects) | Each point: integer `pointerId` 0–9, `phase` (`down`, `move`, `up`), integer `x`, `y`, integer `at_ms` 0–5000. Use valid ordered pointer lifecycles. |
| `scroll` | O + `x`, `y`, `deltaX`, `deltaY` | Deltas range from −10000 to 10000; x/y are screenshot pixels. |
| `key_event` | M + `code`, `phase` (`down`, `up`); optional boolean `shiftKey`, `altKey`, `ctrlKey`, `metaKey` | Codes: `KeyA`–`KeyZ`, `Digit0`–`Digit9`, `Enter`, `NumpadEnter`, `Backspace`, `Delete`, `Escape`, `Tab`, `Space`, `ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight`. Release held keys when done. |
| `device_tool` | `action` + exact fields below | Mixed read/write actions, validated separately by action. No arbitrary shell, URL fetch, or APK install. |

`release_control` accepts only `session_id`; `clipboard.read` accepts only `action` and `session_id`. Neither accepts `operation_id` or `observation_id`.

## `device_tool` actions

Every row includes the literal `action` shown, plus the listed fields. “Read” describes the device effect, not a different OAuth scope or top-level read-only hint.

| Action | Additional fields | Effect / result |
| --- | --- | --- |
| `clipboard.read` | S | Read clipboard; `available: false` or timeout is not proof of an empty clipboard. |
| `clipboard.write` | O + `text` (at most 16384 UTF-8 bytes); optional boolean `paste` | Write and optionally paste. Requires a fresh observation even with `paste: false`. |
| `display.rotate` | M | Rotate display. Observe again before visual actions. |
| `device.open_settings` | M | Open Android Settings; verify the screen afterward. |
| `media.status` | S | Read media/control readiness. |
| `media.recover` | M | Request recovery; observe to verify restoration. |
| `media.set_mode` | M + `mode`: `webrtc` or `jpeg` | Change supported media mode; observations remain on-demand images. |
| `file.upload_begin` | M + `name`, integer `size`, `sha256` | Name 1–160 characters, nonblank, no slash/backslash/control characters; size 1–31457280 bytes; SHA-256 64 lowercase hexadecimal characters. Preserve returned upload ID and ticket. |
| `file.upload_chunk` | M + `upload_id`, integer `offset` ≥ 0, base64 `data` | Legacy staging chunk, at most 32768 decoded bytes and 44000 encoded characters. Prefer [fast upload](file-upload.md). |
| `file.upload_complete` | M + `upload_id` | Complete staging and submit transfer. A running result is not completion. |
| `file.upload_status` | S + `upload_id` | Read staging progress; after completion use the original completion operation status. |
| `file.upload_cancel` | M + `upload_id` | Cancel the known staged upload; inspect its receipt. |
| `apps.list` | No other fields | Read the service's installable catalog, not all installed apps. |
| `apps.install` | M + catalog `app_id` | Install a catalog app. Arbitrary APK URLs are unsupported. |
| `operation.status` | S + original `operation_id` | Read a session operation receipt and job progress without replaying it. Cannot query grant-scoped sharing operations. |
| `airplane.get` | S | Read airplane-mode status. |
| `airplane.set` | M + boolean `enabled`, `confirmed: true` | Change connectivity only within the user's authorization; the confirmation field does not create permission. |
| `device.restart` | M + `confirmed: true` | Restart only when authorized; never use to clear an unknown operation. |
| `share.status` | `device_id` | Read sharing status without a control session. |
| `share.create`, `share.regenerate` | `device_id`, `operation_id`, `permission`: `view` or `control`, `duration`: `24h`, `7d`, or `lease` | Replace active shares and close matching share connections before issuing a link, limited by grant/lease expiry. Treat the URL as a credential. |
| `share.revoke`, `share.take_back` | `device_id`, `operation_id`, `access_id` | Revoke the selected share and close its matching connection. This does not replace `release_control` for an MCP session. |

The server schema permits omitted `device_id` on `share.*` only for legacy single-phone credentials. Account connections require it; always supply the intended phone's current ID. Uncertain sharing operations require `share.status` and an explicit unresolved outcome if necessary, not a replacement mutation.

## Receipts and limits

Inspect `isError`, `structuredContent.error_code`, receipt `state`, `retry_safe`, and any nested `result`. `submitted_to_device` / `ui_outcome: "not_evaluated"` proves no UI outcome. Verify the screen and any relevant terminal job result before reporting success.

For uncertain operations follow the skill's original-ID recovery workflow; transport success does not authorize replay. On `session_ended`, never reuse the session. On `operation_conflict` or `operation_not_found`, check the original session/ID/payload without hiding uncertainty under a new ID. `account_device_limit_reached` stops queued acquisitions without automatic retry or credential switching.

Current defaults: 180 ordinary calls/minute per credential, a separate shared 60/minute for `release_control` and `operation.status`, and device-action limits of 2/second and 60/minute per grant. `file.upload_status` and `operation.status` are exempt from the device-action quota, not their tool-call allowance. New acquisitions are limited to 12/minute per lease and 60/minute per user. Honor live limits and `retry_after_ms`, `retry_after_seconds`, or HTTP `Retry-After`.

The account cap is 16 concurrent phones across all clients and credentials; stopping/isolating sessions still count. Requests are limited to 64 KiB. Screenshots have a maximum edge of 1280 pixels and decoded size of 2 MiB. Idle sessions normally expire after five minutes; always explicitly release on completion, cancellation, or blockage and confirm closed/drained. See [parallel control](parallel-control.md) for per-phone state and shared dispatch budgets.
