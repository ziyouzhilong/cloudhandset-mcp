# Support

For account, lease, connection, billing, or immediate authorization revocation assistance, contact CloudHandset through [the official website](https://www.cloudhandset.com).

For installation, start with the [Codex guide](CODEX_INSTALL.md), [Dot guide](DOT_INSTALL.md), [Muse guide](muse/README.md), or [Grok Bot guide](GROK_INSTALL.md). Dot also has a [first phone check](DOT_SETUP.md); Muse has [setup prompts](muse/SETUP.md) and a [tool reference](muse/TOOLS.md).

For Dot file uploads, install or upgrade to **0.2.4**, refresh the existing connection's MCP tools, and follow the [file-upload reference](DOT_UPLOAD.md). Confirm the original complete operation reached `succeeded` and retain its returned path. If a video is absent from a photo picker, reopen the picker after any media-index request; Files/Downloads is an alternative only when the app offers it. Do not repeat a verified transfer just because the picker has not refreshed. Contact website support if the file is still unavailable.

Muse 0.1.2 uses the official Custom Connector credential helper and an adapter inside Muse's execution environment. When reporting an issue, distinguish local helper or argument checks, authentication, dispatched tool calls, image inspection, upload completion, and release. The parallel workflow preserves per-phone outcomes. An account can control at most 16 phones at once across all clients; adding credentials does not increase that allowance.

For a documentation or package issue, [open a GitHub issue](https://github.com/ziyouzhilong/cloudhandset-mcp/issues/new). Include:

- The package and client version.
- Your operating system and the installation step that failed.
- The expected result and a redacted error message.

Public issues are visible to everyone. Do not include passwords, verification codes, tokens, cookies, complete OAuth callback URLs, account-bound plugin archives, generated Muse credential-helper files, private phone screenshots, or personal account details. Use website support for account-specific problems. Report suspected credential exposure or security issues privately through website support.

## Release phone control first

Ask the agent to release control and confirm that the session is closed and drained before disconnecting or removing a plugin. If release cannot be confirmed, report the unresolved session through support.

Removing a plugin or signing out locally does not necessarily revoke a server-side authorization. For immediate revocation, ask support to confirm that authorization has been revoked and control has drained.

For Muse installation, follow the [five-step guide](MUSE_INSTALL.md). Attach all six extracted files to Muse chat, complete its official connection form, then let Muse install the dedicated skill.

For Grok Bot, distinguish custom MCP authentication, personal-skill loading, file-helper availability, and phone execution. If the skill loader reports a missing file, follow the exact-path recovery in [SETUP.md](grok-bot/SETUP.md). Do not modify internal credential stores or recreate a working OAuth connection to fix a skill file.
