# CloudHandset MCP tool reference

Setup kit **0.1.0** · Server interface checked **2026-10-10** against `server/mcpToolSchemas.ts` and `server/mcpServer.ts`, with execution semantics from `agentControlService.ts` and the device services.

These are the server's 12 tools. Muse must discover their live schemas after compatible authentication; this reference does not establish that Muse can call them. The only OAuth scope is `device:control`. There is no read-only scope. Only `list_devices` and `observe` carry the server's top-level read-only hint; treat every other tool, including the mixed-purpose `device_tool`, as potentially consequential and keep host approvals enabled.

## Common inputs and results

- `device_id`, `session_id`, `observation_id`, `upload_id`, `app_id`, and `access_id` are UUIDs obtained from service results. Never invent a phone or session ID.
- `operation_id` is 1–64 ASCII letters, digits, underscores, or hyphens. Use a new ID per new intended mutation; retain the original ID and payload for resolving uncertainty. Reusing an ID with changed arguments causes `operation_conflict`.
- In the tables, **S** means `session_id`; **M** means `session_id` + `operation_id`; **O** means M + `observation_id`. These are abbreviations for documentation, not literal JSON fields. Unlisted input fields are rejected.
- Coordinates are integers in the current screenshot's pixel space, bounded by its actual width and height; the schema also caps each coordinate at 16384. The server scales them to the control surface. Do not rescale on the client.
- Observations expire after at most 30 seconds and become invalid after a session mutation. Serialize actions and observe again before the next coordinate/text action.
- Results include text and `structuredContent` metadata. `observe` also returns a native MCP `content` image block (`image/png` or `image/jpeg`); only metadata appears under `structuredContent.image`. There is no audio result.
- Operation receipts can include `operation_id`, `session_id`, `action`, `state`, `evidence`, `error_code`, `job_id`, `result`, `retry_safe`, and `ui_outcome`. `submitted_to_device` and `ui_outcome: "not_evaluated"` do not prove task completion. Inspect the actual resulting screen and any relevant job result.

## The 12 tools

| Tool | Inputs | Result and effects |
| --- | --- | --- |
| `list_devices` | `{}` | Reads the phone authorized by this credential: `devices` with IDs, display/model details, lease/grant expiry, `automation_enabled`, `supported`, and `busy`. Does not acquire control. |
| `acquire_control` | `device_id`, `operation_id` | Reserves exclusive control. Check `acquired: true` and `state: "active"`; retain `session_id`, `control_epoch`, expiry, and capabilities. Busy writers are never evicted. |
| `observe` | S; optional `after_operation_id` | Captures a fresh image with `observation_id`, capture/expiry times, image/control dimensions, and orientation. `after_operation_id` attaches the receipt for an existing operation in this session; it is not a guarantee that its business outcome succeeded. |
| `tap` | O + `x`, `y` | One screen tap; operation receipt. |
| `swipe` | O + `start_x`, `start_y`, `end_x`, `end_y`, `duration_ms` (integer 50–5000) | Screen swipe; operation receipt. |
| `input_text` | O + nonempty `text` (at most 4096 UTF-8 bytes) | Types into the focused field using the clipboard path. Does not clear or submit the field; operation receipt. |
| `press_key` | M + `key`: `HOME`, `BACK`, `RECENTS`, `POWER`, `VOLUME_UP`, or `VOLUME_DOWN` | Navigation, power, or volume change; operation receipt. No observation ID input. |
| `release_control` | S | Stops and drains this writer. Require `closed: true`, `state: "closed"`, and `closed_evidence` confirming drain, such as `bridge_execution_drained`. Authorization remains valid. `stopping` or `isolating` is unresolved cleanup. |
| `gesture` | O + `points` (2–512 objects) | Touch trajectory. Each point contains `pointerId` (integer 0–9), `phase` (`down`, `move`, `up`), integer `x`, `y`, and `at_ms` (integer 0–5000). Supply valid ordered pointer lifecycles; operation receipt. |
| `scroll` | O + `x`, `y`, `deltaX`, `deltaY` (each delta −10000 to 10000) | Scroll at a visible location; operation receipt. |
| `key_event` | M + `code`, `phase` (`down` or `up`); optional boolean `shiftKey`, `altKey`, `ctrlKey`, `metaKey` | Physical key event; operation receipt. Codes: `KeyA`–`KeyZ`, `Digit0`–`Digit9`, `Enter`, `NumpadEnter`, `Backspace`, `Delete`, `Escape`, `Tab`, `Space`, and four `Arrow*` keys. Release held keys when done. |
| `device_tool` | `action` + the exact inputs below | Mixed read and write capabilities. No arbitrary shell, arbitrary URL fetch, or arbitrary APK installation. |

Acquire only a user-selected phone for an authorized task. A list-only request must not acquire it. A first connection check uses only list, acquire, observe, release. If the model cannot inspect the image, do not perform visual actions. When finished, canceled, or blocked, release held inputs and attempt `release_control`; report unconfirmed closure.

## `device_tool` actions

All rows require the literal `action` shown. “Read” describes the action's intended device effect, not its OAuth permissions or top-level tool hint. Device-backed reads still require a control session where S is listed. Except for catalog and share-status reads, results normally arrive inside an operation receipt's `result`.

| Action | Inputs after `action` | Effect and result |
| --- | --- | --- |
| `clipboard.read` | S | Read. Returns `available` and `text`, or `available: false` with a reason. A timeout does not prove the clipboard is empty. |
| `clipboard.write` | O + `text` (at most 16384 UTF-8 bytes); optional boolean `paste` | Writes clipboard and optionally pastes. Requires a fresh observation even when `paste` is false. |
| `display.rotate` | M | Rotates display and changes its generation. Obtain a new image before another visual action. |
| `device.open_settings` | M | Opens Android Settings. Receipt alone does not verify the displayed screen. |
| `media.status` | S | Read. Returns media mode, on-demand observation mode, and control readiness. |
| `media.recover` | M | Requests media recovery; a `recovering` result is not proof of restored images. Observe afterward. |
| `media.set_mode` | M + `mode`: `webrtc` or `jpeg` | Changes media mode where supported. Still uses on-demand image observations; does not create a continuous video or audio feed for the model. |
| `file.upload_begin` | M + `name`, `size`, `sha256` | Starts staging. Name: 1–160 characters, nonblank, no slash/backslash/control characters. Size: integer 1–31457280 bytes (30 MiB). SHA-256: 64 lowercase hex characters. Retain returned `upload_id`/`job_id` and progress. |
| `file.upload_chunk` | M + `upload_id`, integer `offset` ≥ 0, base64 `data` | Adds a chunk: at most 32768 decoded bytes and 44000 encoded characters. Use returned progress and the correct offset. |
| `file.upload_complete` | M + `upload_id` | Completes and verifies the staged upload, then transfers it to the phone. Inspect result/progress; it is a mutation. |
| `file.upload_status` | S + `upload_id` | Read. Returns upload progress/status without adding file content. |
| `file.upload_cancel` | M + `upload_id` | Cancels the staged upload; inspect the returned state. |
| `apps.list` | No other inputs | Read. Returns `apps` with `id`, `name`, and `package_name` from the service catalog, not the phone's entire installed-app inventory. No session required. |
| `apps.install` | M + `app_id` from the catalog | Installs a catalog app and returns installation evidence/result. Does not accept an arbitrary APK URL. |
| `operation.status` | S + the original `operation_id` | Read. Retrieves a session operation receipt and refreshes job progress where applicable. Does not replay the action. It cannot query grant-scoped sharing operations. |
| `airplane.get` | S | Read. Returns airplane-mode status. |
| `airplane.set` | M + boolean `enabled`, `confirmed: true` | Changes connectivity. Require the user's authorization; `confirmed: true` is an input assertion, not a substitute for permission. |
| `device.restart` | M + `confirmed: true` | Restarts the phone and may interrupt access. Require the user's authorization. Never use it to clear an unknown operation. |
| `share.status` | No other inputs | Read. Returns current share IDs, permissions, and expiry/revocation metadata. No session required. |
| `share.create` / `share.regenerate` | `operation_id`, `permission`: `view` or `control`, `duration`: `24h`, `7d`, or `lease` | Grant-scoped mutation, no session. Both replace existing active shares and stop their matching connections before issuing a new link. Link expiry is capped by grant/lease access. Treat returned `url` as a credential. |
| `share.revoke` / `share.take_back` | `operation_id`, `access_id` from share status | Grant-scoped mutation, no session. Revokes the specified share and closes its matching share connection. Check returned `closed`/`state`; this is not a replacement for releasing an MCP session. |

File transfers, installations, connectivity changes, restarts, and sharing require task-specific authorization. Sharing can expose control and disconnect an existing recipient. A share link is issued only in the original successful result; a retained receipt does not redisplay the credential. For an uncertain share mutation, read `share.status` and ask the service to resolve any remaining ambiguity. Do not generate another share operation or claim success because a session `operation.status` lookup is unavailable.

## Errors and retries

Tool failures use `isError: true` and/or `structuredContent.error_code`; HTTP authentication failures may instead return an HTTP error. Inspect receipt state and `result` as well. Do not assume a successful transport means the phone task succeeded.

| Signal | Required response |
| --- | --- |
| Lost `acquire_control` response | Retry only the identical acquire request with its original ID to recover the session. Do not create new acquisition IDs in a loop. |
| Timeout, lost mutation response, `unknown`, or `retry_safe: false` | Retain the original ID. For session actions, query `operation.status`; then call `observe` with `after_operation_id` if the session remains active. Do not replay. If unresolved or ended, stop mutations, attempt permitted cleanup, and report uncertainty. |
| `rejected_before_dispatch` / `canceled_before_dispatch` with `retry_safe: true` | No dispatch occurred. Correct the cause and re-observe before a new intended action; keep the rejected receipt. Reusing its ID retrieves the old receipt rather than executing a corrected payload. |
| `invalid_arguments`, `invalid_action_input`, `invalid_coordinates` | Check the live schema and current image geometry. Do not guess coordinates or reuse a changed payload under the same ID. |
| `observation_stale` | Capture and inspect a fresh image before a new intended action. |
| `device_busy`, `action_busy`, `stop_pending` | Do not evict a writer or bypass isolation. Resolve the existing operation, wait as appropriate, or report the blocked state. |
| `control_paused` | Respect the customer's takeover. Resume only at the user's request through fresh verification. |
| HTTP 401, `invalid_grant`, `grant_expired`, `grant_revoked`, `access_ended`, `assignment_changed` | Stop actions. Recheck lease/authorization and use fresh verification only when appropriate; never bypass with cookies or old credentials. Attempt release when permitted and report unconfirmed cleanup. |
| `session_ended` | Do not reuse the session. Report unresolved prior operations; if a new task is authorized, list the phone and acquire a new session only after availability is confirmed. |
| `capture_failed`, `invalid_device_image`, `capability_not_supported` | Report the missing capability or image. Stop visual actions and release the session; do not substitute invented screen state. |
| `operation_conflict` / `operation_not_found` | Check the original ID, session, and payload; never use a new ID to hide uncertainty. |
| `rate_limited` / HTTP 429 | Respect `retry_after_seconds` or `Retry-After` (normally 60 seconds). Avoid polling loops. A rate-limit response does not authorize replay of an earlier uncertain operation. |

The server's idempotence hint describes deduplication, not permission to replay mutations. Associate an observation with the original operation and distinguish dispatch, device receipt, visible result, task completion, and released control.

## Limits

Current defaults are **180 ordinary tool calls/minute per credential**, with a separate shared allowance of **60/minute** for `release_control` and `operation.status`. Device observations and most session actions share stricter persisted limits of **2/second and 60/minute per grant**; `file.upload_status` and `operation.status` are exempt from that device-action quota, but still consume their applicable tool-call allowance. New acquisition IDs are limited to **12/minute per lease and 60/minute per user**. Authentication failures are limited separately. Deployments can override the ordinary tool-call limit; always honor the returned delay.

Requests are capped at 64 KiB. Screenshots have a maximum edge of 1280 pixels and a decoded size limit of 2 MiB. An idle session is normally released after five minutes; explicit cleanup is still required when a task ends.
