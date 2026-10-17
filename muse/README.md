# CloudHandset for Meta Muse

Setup kit **0.1.2** · Updated **2026-10-18**

This version adds [independent multi-phone control](PARALLEL_CONTROL.md) and a paced `parallel` adapter command. Each account may control up to 16 Android phones at once across every client and credential. Workers must be 1–16; a batch covering more than 16 distinct phones is rejected before dispatch, with no automatic splitting. The 16-phone limit is backed by separate service capacity checks; the Muse-host run below used two phones.

Use this kit to prepare a Custom Connector for **Meta Muse, the personal agent**. It contains connection instructions, a Python MCP adapter, and a tool reference. It is not a Muse Code configuration, a native importable plugin, or a Meta-approved directory listing.

**Current compatibility:** in a 2026-10-10 account check, Muse reported no native entry point for registering an arbitrary remote MCP server. Its Custom Connector uses PKCE `S256`, callback `https://agent.meta.ai/api/hatch/oauth/callback`, and public client ID `cloudhandset-muse`. CloudHandset registered that client on 2026-10-10 and supports its omitted `resource` parameter while keeping authorization bound to the fixed MCP endpoint. The supplied adapter uses Muse's official credential helper. A live account check completed OAuth, official skill scaffolding, discovery of all 12 tools, phone listing, acquisition, one JPEG observation opened with `muse.read`, and confirmed control release. No screen actions were performed. This is a single-account connection check, not a claim about every Muse version or business workflow.

CloudHandset MCP is available to active customers for their own valid Android phone leases. Authorization covers either the phone selected during login or the current and future Android phone leases explicitly approved by the user. There is no fixed test account or required test phone. Other clients' successful connections do not establish Muse compatibility.

## Validation scope — 2026-10-18

A two-phone run in Muse's own host covered parallel acquisition and observations, explicit normalized-coordinate taps with visible results on both phones, clipboard write/read, and closed/drained release for both sessions. One phone received two consecutive 4,694,656-byte Demo MP4 uploads, reported at 28 seconds each, with the original completion operation succeeded and the active-session check passed before the next file. Muse inspected two videos in Gallery. These timings describe this run, not a speed guarantee.

Some navigation-bar taps on the other phone were accepted but produced no visible change; an in-app back tap succeeded. That isolated behavior remains unexplained. Upload timeout/unknown-result recovery was not triggered in this live run. The separate service test used 1, 4, 8, and 16 phones for 120 seconds per level; it does not establish native 16-phone Muse app workflows.

## Install through Muse chat

Follow the bundled [installation guide](SETUP.md): extract the ZIP and attach its six files to Muse. For a new connection, complete the official form with client ID `cloudhandset-muse` and an empty client secret. Reuse an existing ready connection and keep its private binding.

Before replacing an existing adapter, verify the official helper import in the current Muse runtime and keep a backup of the working adapter. The current official helper path was checked in Muse on 2026-10-18: `/opt/muse/skills/custom-connector-setup/bin/dynamic_credentials.py`. The adapter uses that path first and falls back to the previous official path only when the current file is absent. Missing, unloadable, or incompatible helpers and unavailable credentials return distinct errors before dispatch. Keep the existing private connector binding, place `upload_file.py` beside `cloudhandset.py`, and add `PARALLEL_CONTROL.md` to the skill's instructions. See [SETUP.md](SETUP.md) for migration checks and [TOOLS.md](TOOLS.md) for exact arguments, explicit coordinate conversion, and parallel calls.

On 2026-10-11, the supplied 0.1.1 scripts completed a real 4,694,656-byte MP4 upload from Muse: one binary PUT, completion confirmed, the Android file checksum verified, and control released with `bridge_execution_drained`. The observed begin-to-completion time was 25.567 seconds in that single-account check; transfer speed depends on the host and network.

## Upload completion and recovery

The 0.1.2 adapter sends each file once, then uses a 120-second query budget for the original completion operation by default. Reads check an absolute deadline between available chunks, so a continuous stream cannot extend that budget; a final silent in-flight read can take up to 30 additional seconds to time out. `submitted_to_device` or `running` is not completion. Success requires the matching session, upload and operation IDs, `result.state=succeeded`, the expected byte count, and the generated Android path. A final `file.upload_status` read checks that the same session remains active. `upload_complete=true` records the transfer result; `can_start_next_upload=true` and `session_checked_active=true` apply only at that final check, not indefinitely.

If the deadline expires, the result remains pending and the command exits nonzero. Keep `session_id`, `upload_id`, `complete_operation_id`, and `expected_size`; use `upload-status` in [SETUP.md](SETUP.md) to continue read-only verification. Unknown results, missing operation records, or a closed session do not trigger another PUT or a new upload ID. A transfer already proven complete stays marked complete even when the final active-session check fails. The adapter never starts the next file automatically.

Polling defaults to five seconds per command. One coordinator must share the 60/minute `operation.status`/release allowance across all uploads and reserve room for release. For 16 simultaneous waiters, use at least 40-second intervals and account for initial checks and other calls; separate processes do not combine their local budgets. Honor longer server retry delays. File completion does not itself verify gallery visibility.

## Detailed setup

1. Paste **Stage 1** from [SETUP.md](SETUP.md) into Muse. It asks Muse to establish its actual connection capabilities before attempting login.
2. Give CloudHandset the non-secret client ID, exact registered callback URI, authentication method, and any connector requirements that Muse can verify. Do not send a complete authorization or callback URL containing `code`, `state`, or other session values.
3. Continue to **Stage 2** only after CloudHandset confirms registration and the host can perform the required flow. Enter account credentials only in the independent CloudHandset verification window.
4. List the authorized phone first. Acquire it only when the user has selected it and requested the connection check. The first check is **list → acquire → observe → release**, with no screen actions.

See [TOOLS.md](TOOLS.md) for the current server interface and operation rules. This reference describes the CloudHandset service. Discover the live schemas in each connected account before using them; the connection check does not validate every tool or action.

## Connection requirements

| Setting | Required value or verification |
| --- | --- |
| Connection name | CloudHandset |
| MCP endpoint and OAuth resource | `https://device.cloudhandset.com/mcp` — no trailing slash |
| Transport | Remote Streamable HTTP |
| OAuth flow | Authorization Code with PKCE `S256` |
| Scope | `device:control` |
| Token endpoint authentication | `none` — public client, no client secret |
| Registered client ID | `cloudhandset-muse` |
| Registered callback URI | `https://agent.meta.ai/api/hatch/oauth/callback` |
| Dynamic client registration | No DCR endpoint is supplied |

There is no separate read-only OAuth scope. Tool read/write classifications are operational guidance, not narrower token permissions. If Muse requires DCR, a client metadata document, a secret, or another flow, report that requirement and stop until CloudHandset confirms a supported configuration. Do not invent a callback, reuse another client's ID or localhost callback, pass website cookies, share tokens, or weaken callback validation.

Authorization lasts at most **30 days** and never beyond the effective phone lease. Expiry requires fresh verification; automatic Muse login prompts have not been verified. Releasing control leaves the authorization valid. Customer take-back ends the current Agent session while preserving valid authorization. After the customer leaves or disconnects and the phone is available, an already authorized task can acquire a new session with the same connector, without signing in again. Inspect a fresh screenshot and do not replay interrupted actions.

## What counts as a successful connection check

Report these outcomes separately:

- OAuth completed using the registered client and callback.
- `list_devices` returned the user's selected, authorized Android phone.
- Muse actually read the PNG/JPEG image returned by `observe` and described visible content. Tool discovery or image metadata alone is insufficient.
- `release_control` confirmed `closed: true`, `state: "closed"`, and closure evidence confirming the writer was drained, such as `bridge_execution_drained`.

If the image is unavailable, stop visual actions and release control. If release is unconfirmed, report the unresolved session. CloudHandset MCP provides no audio. It does not grant background execution independently of the host.

For support, provide the Muse version, timestamp and timezone, connection stage, error code, non-secret registration details, image result, and release result. Share session/operation/observation IDs privately when needed. Do not publish credentials, tokens, authorization links, share links, or private screenshots.

## Package contents

`cloudhandset-muse-setup-0.1.2.zip` contains only `README.md`, `SETUP.md`, `TOOLS.md`, `PARALLEL_CONTROL.md`, `cloudhandset.py`, and `upload_file.py` under `cloudhandset-muse/`. It includes no credentials or guessed import manifest. The Python script runs inside Muse's execution environment with its official credential helper; see the installation steps in [SETUP.md](SETUP.md).

Maintainers build it from the development repository root with:

```sh
python3 scripts/packageMuseConnector.py
```

The independent package command produces the six-file setup ZIP, `manifest.json`, and `SHA256SUMS`. Validation results above apply to their stated versions, hosts, phone counts, and workflows.

## Official references

- [Meta: How Muse works with Connectors](https://www.meta.com/help/artificial-intelligence/1687253048996149/) describes asking Muse to create a Custom Connector.
- [Muse Connector Platform](https://muse.ai/platform/docs) provides connector platform guidance.

The public guides reviewed for this kit do not establish the exact Muse callback, client identity, PKCE behavior, or MCP image support required here. The callback and PKCE observations above come from the actual 2026-10-10 authorization request. Use verified host behavior and confirmed service registration before continuing the conditional setup.
