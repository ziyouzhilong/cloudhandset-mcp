# Support

For account, lease, connection, billing, or immediate authorization revocation assistance, contact CloudHandset through [the official website](https://www.cloudhandset.com).

For installation, start with the [Codex guide](CODEX_INSTALL.md), [Dot guide](DOT_INSTALL.md), or [Muse guide](muse/README.md). Dot also has a [first phone check](DOT_SETUP.md); Muse has [setup prompts](muse/SETUP.md) and a [tool reference](muse/TOOLS.md).

For Dot file uploads, install or upgrade to **0.2.2**, refresh the existing connection's MCP tools, and follow the [file-upload reference](DOT_UPLOAD.md). Confirm the original complete operation reached `succeeded` and retain its returned path. If a video is absent from a photo picker, reopen the picker after any media-index request; Files/Downloads is an alternative only when the app offers it. Do not repeat a verified transfer just because the picker has not refreshed. Contact website support if the file is still unavailable.

Muse 0.1.0 uses a Custom Connector and a Python adapter inside Muse's execution environment. **A single-account connection and screen check passed on 2026-10-10**, covering OAuth, connector setup, tool discovery, authorized phone listing, acquisition, an actual screenshot read by the model, and closed/drained release. Taps, text input, and app workflows were not tested. When reporting a Muse issue, distinguish authentication, tool discovery/calls, image visibility, and control release. GitHub package publication is separate from Meta Connector directory review or approval.

For a documentation or package issue, [open a GitHub issue](https://github.com/ziyouzhilong/cloudhandset-mcp/issues/new). Include:

- The package and client version.
- Your operating system and the installation step that failed.
- The expected result and a redacted error message.

Public issues are visible to everyone. Do not include passwords, verification codes, tokens, cookies, complete OAuth callback URLs, account-bound plugin archives, generated Muse credential-helper files, private phone screenshots, or personal account details. Use website support for account-specific problems. Report suspected credential exposure or security issues privately through website support.

## Release phone control first

Ask the agent to release control and confirm that the session is closed and drained before disconnecting or removing a plugin. If release cannot be confirmed, report the unresolved session through support.

Removing a plugin or signing out locally does not necessarily revoke a server-side authorization. For immediate revocation, ask support to confirm that authorization has been revoked and control has drained.

For Muse installation, follow the [five-step guide](MUSE_INSTALL.md). Attach the four extracted files to Muse chat, complete its official connection form, then let Muse install the dedicated skill.
