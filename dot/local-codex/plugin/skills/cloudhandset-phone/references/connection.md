# Connect CloudHandset in Codex

## Account connection and newly added phones

When the CloudHandset verification page offers **Current and future Android phone leases**, choose it to authorize this connection for the account's eligible phones, including phones added during the fixed 30-day connection. Each phone remains limited by its effective lease. Existing single-phone connections do not expand automatically; reconnect once to opt in. **Only one selected Android phone** keeps the previous single-phone scope. Account access does not clear an explicit automation stop. Ordinary customer take-back preserves authorization; once the customer leaves or disconnects and the phone is available, acquire a new session with the existing connection.

Call `list_devices` again after adding a phone and at the start of each task. Select the returned `device_id`; never reuse a different phone's session. For `device_tool` actions named `share.*`, supply that `device_id` explicitly. A valid account connection can return an empty list when it has no eligible leases.

The plugin supplies the `cloudhandset` MCP connection at `https://device.cloudhandset.com/mcp` with the registered public OAuth client ID `cloudhandset-codex`. It contains no account credentials. No software from this package is installed on the Android phone.

1. Check `codex mcp get cloudhandset`. If an older manual connection already exists, preserve it when it uses the same URL and OAuth client ID. Do not add duplicate servers under new names or replace unrelated configuration.
2. If the connection is absent, check that the CloudHandset plugin is installed and enabled with `codex plugin list`. For a manual setup instead, run `codex mcp add cloudhandset --url https://device.cloudhandset.com/mcp --oauth-client-id cloudhandset-codex` in the user's interactive terminal.
3. To authenticate or renew access, use `codex mcp login cloudhandset`. The account owner completes the independent English verification window. Never supply credentials on the user's behalf or ask for secrets in chat.
4. Open a new Codex conversation after connection changes. If the tools are still unavailable, report the missing connection instead of pretending to inspect the phone. Explicitly invoke `$cloudhandset-phone` when needed.

The OAuth window selects only phones covered by the user's own active leases. A localhost callback is handled by Codex; the phone service remains on the public CloudHandset endpoint. Do not manually add `oauth_resource` or `--oauth-resource`; native discovery provides it. Do not attempt dynamic client registration or reuse another client's credentials.

Authorization lasts up to 30 days and ends earlier with the selected phone's effective lease. No refresh token is issued. On authorization expiry, stop actions and complete a new login. An expired lease must first be renewed; login alone cannot restore it. Customer take-back ends the current session while preserving valid authorization. Respect the customer's control and any draining state; after the phone becomes available, an already authorized task may acquire a new session with the existing connection. Never replay interrupted or uncertain actions. An explicit automation stop remains paused until the user requests resumption and completes supported verification. Background runs are not guaranteed to open a verification window automatically.

## Switching accounts

Release control before switching. Use `codex mcp logout cloudhandset`, then `codex mcp login cloudhandset`, and let the owner sign in to the intended account in the verification window. Do not remove the plugin or require website revocation just to switch accounts.

In Codex 0.163.0-alpha.11.2, a running conversation can retain the old credential after terminal login succeeds. Open a new conversation using the same connection, or use the host's supported MCP reload on its existing runtime. `config/mcpServer/reload` is the tested host protocol method; it is not a shell command. Never start another app-server and claim that it refreshed the user's desktop.

Discard the old task's device, session and observation IDs. Call `list_devices` again and verify the intended phone from that actual result. If the list still belongs to the old account, stop phone actions and check the exact connection name and local/remote environment. Do not claim that the account changed based on login success, and do not reuse a previous tool result or extract credentials to force a switch.

Release control before signing out, disabling, or removing the plugin. `codex mcp logout cloudhandset` clears local credentials; it does not revoke the server-side grant or prove that another process has released control. If immediate server-side revocation is needed, contact CloudHandset support. Do not extract tokens as a workaround.
