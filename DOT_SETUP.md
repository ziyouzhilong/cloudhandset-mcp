# First phone check with Dot

## Account connection and newly added phones

When the CloudHandset verification page offers **Current and future Android phone leases**, choose it to authorize this connection for the account's eligible phones, including phones added during the fixed 30-day connection. Each phone remains limited by its effective lease. Existing single-phone connections do not expand automatically; reconnect once to opt in. **Only one selected Android phone** keeps the previous single-phone scope. Account access does not clear an explicit automation stop. Ordinary customer take-back preserves authorization; once the customer leaves or disconnects and the phone is available, acquire a new session with the existing connection.

Call `list_devices` again after adding a phone and at the start of each task. Select the returned `device_id`; never reuse a different phone's session. For `device_tool` actions named `share.*`, supply that `device_id` explicitly. A valid account connection can return an empty list when it has no eligible leases.

Complete the connection and skill installation in [DOT_INSTALL.md](DOT_INSTALL.md) first. The installed plugin should show one connected CloudHandset app and one android-phone skill.

Send this to Dot:

> Use my authenticated CloudHandset tools directly to list my Android phones. Let me choose one if needed. Acquire the selected phone, inspect its actual current screen image and describe it, then release control and confirm the writer is closed and drained. This is a screen check only: do not click, type, install, change network settings, or reboot. If tools, login, or a usable image are unavailable, report the missing prerequisite and any unresolved control session. Do not claim success from tool discovery or command submission alone.

You may include the phone's displayed name in the request. Dot should match it against the current device list. A successful check means Dot inspected the real image and confirmed release. For later tasks, specify the action you want and when Dot should stop.

## Check two or more phones

Use an account-scope connection and replace the names with phones shown by a fresh device list:

> Use my existing CloudHandset connection to check [PHONE A] and [PHONE B]. Keep one independent sequence per phone. Use your native parallel tool facility for different phones if available, with ordered steps on each phone; otherwise report that you are interleaving calls. Acquire only these available phones, read each current screen image, and report what you see for each. Do not tap, type, scroll, or press keys. Release each acquired session and confirm it is closed and drained. Keep separate results and unresolved cleanup if one phone fails. Do not take over a busy phone or start another agent.

There is an account-wide limit of 16 simultaneously controlled phones, including other clients' sessions. Reject an oversized requested set before dispatch instead of silently splitting it. Reuse valid OAuth; reconnect only for expired access or explicit account-scope opt-in. Follow [PARALLEL_CONTROL.md](PARALLEL_CONTROL.md) for pacing and recovery.

## Control and recovery

- An occupied phone must remain with its current operator. Do not take over automatically.
- After an action, inspect a fresh image to verify the result. Submission alone does not confirm the intended screen change.
- If an action times out, keep its original operation ID, check its status, and observe the associated result. Do not replay an action whose outcome is unknown, especially when `retry_safe` is false.
- On completion, interruption, or error, release held inputs and phone control. Confirm release is closed and drained; otherwise report cleanup as unresolved.
- If a person takes control, stop phone actions and preserve unresolved operation IDs. After their session ends and the phone is available, an already authorized task can acquire a fresh session with the existing connection. Inspect a new screenshot; do not replay interrupted actions.
- If authorization expires, reconnect through the independent login window. If the phone lease expires, renew it before requesting control.

## Optional local fallback prompt

Use this only when you have enabled Dot access to an online computer with the CloudHandset Codex plugin installed and authenticated:

> Create a local Codex task on my connected computer using the installed `cloudhandset:cloudhandset-phone` skill and existing CloudHandset connection. List my Android phones and let me choose one if needed. Inspect the selected phone's real screen and describe it, then release control and confirm the writer is closed and drained. Do not click, type, install, change network settings, or reboot. Wait for the task result and identify which executor inspected the image. Report missing prerequisites or unresolved control. Do not install a duplicate MCP server or copy credentials.

The computer must remain online for this route. Dot must wait for the local result before reporting completion; creating the task is not completion. The same control and recovery rules apply.
