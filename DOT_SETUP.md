# First phone check with Dot

Complete the connection and skill installation in [DOT_INSTALL.md](DOT_INSTALL.md) first. The installed plugin should show one connected CloudHandset app and one android-phone skill.

Send this to Dot:

> Use my authenticated CloudHandset tools directly to list my Android phones. Let me choose one if needed. Acquire the selected phone, inspect its actual current screen image and describe it, then release control and confirm the writer is closed and drained. This is a screen check only: do not click, type, install, change network settings, or reboot. If tools, login, or a usable image are unavailable, report the missing prerequisite and any unresolved control session. Do not claim success from tool discovery or command submission alone.

You may include the phone's displayed name in the request. Dot should match it against the current device list. A successful check means Dot inspected the real image and confirmed release. For later tasks, specify the action you want and when Dot should stop.

## Control and recovery

- An occupied phone must remain with its current operator. Do not take over automatically.
- After an action, inspect a fresh image to verify the result. Submission alone does not confirm the intended screen change.
- If an action times out, keep its original operation ID, check its status, and observe the associated result. Do not replay an action whose outcome is unknown, especially when `retry_safe` is false.
- On completion, interruption, or error, release held inputs and phone control. Confirm release is closed and drained; otherwise report cleanup as unresolved.
- If a person takes control, stop operating the phone until they explicitly resume the task and a fresh check confirms availability.
- If authorization expires, reconnect through the independent login window. If the phone lease expires, renew it before requesting control.

## Optional local fallback prompt

Use this only when you have enabled Dot access to an online computer with the CloudHandset Codex plugin installed and authenticated:

> Create a local Codex task on my connected computer using the installed `cloudhandset:cloudhandset-phone` skill and existing CloudHandset connection. List my Android phones and let me choose one if needed. Inspect the selected phone's real screen and describe it, then release control and confirm the writer is closed and drained. Do not click, type, install, change network settings, or reboot. Wait for the task result and identify which executor inspected the image. Report missing prerequisites or unresolved control. Do not install a duplicate MCP server or copy credentials.

The computer must remain online for this route. Dot must wait for the local result before reporting completion; creating the task is not completion. The same control and recovery rules apply.
