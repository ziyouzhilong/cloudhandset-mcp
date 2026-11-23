---
name: cloudhandset-phone
description: Use the CloudHandset MCP connection when the user asks to list, view, or operate their leased CloudHandset Android phones.
---

Use the tools discovered under the plugin's `cloudhandset_phone` MCP server in Antigravity. If the server requires sign-in, direct the user to its Authenticate control. Keep passwords, verification codes, OAuth codes and tokens out of chat. Keep Antigravity tool approvals enabled.

Follow the [phone workflow](references/phone-workflow.md). Refresh `list_devices` for each task. A list-only request ends there. Match the requested phone to its returned `device_id`; clarify ambiguous names and respect a busy phone's operator.

1. Acquire control with a fresh `operation_id`; continue only after `acquired: true` and `state: "active"`. Retain the session and operation IDs. Recover a lost acquisition response only with the identical request and original ID.
2. Inspect the image content returned by `observe`. If Antigravity exposes only metadata or an unreadable image, stop visual actions and release. Use the original screenshot's pixel coordinates and the observation ID where the live tool requires it. Inspect a fresh image after each action.
3. Keep one operation in flight per phone. On an unknown write result, query `device_tool` with `operation.status` and the original ID, then observe if active. Never replay an uncertain write. For `share.*`, supply the intended device ID and use `share.status` to resolve uncertainty. Keep share links private.
4. On user take-back, respect draining and wait for the phone to become available. Acquire a fresh session only for the authorized task. On an explicit automation stop, wait for the user's resumption request and supported verification.
5. On completion, cancellation, or failure, release any held inputs and call `release_control` with only the session ID for each session acquired here. Report what was visibly verified and whether closure and writer drain were confirmed.

For multiple phones, use [parallel control](references/parallel-control.md). For a requested upload, follow [file upload](references/file-upload.md) using this skill's `scripts/upload_file.py`. Run the helper relative to this skill directory and pass its one-use ticket privately on stdin. If private ticket transfer or local file access is unavailable, report the limitation.
