# CloudHandset for OpenAI Dot

Version 0.2.1. Connect Dot to the Android phones covered by your CloudHandset leases, then install the phone-operation skill. Each customer connects their own account. The public download contains no account connection or login credentials.

This is a setup kit, not a one-click public marketplace installation. Your ChatGPT account must support **Create custom MCP server** and **Upload plugin archive**. You also need a CloudHandset account with an active phone lease and Python 3.9 or later. On Windows, replace `python3` in the commands below with `py -3`.

## Get help from Codex

**Required model for phone operation:** Select **GPT-6.1 Sol** in your agent before asking it to operate the phone. This requirement applies to phone operation, not plugin installation.

Alternatively, upload the entire setup ZIP to a Codex conversation in **Work mode** and ask Codex to help you install it. You still need to complete your own account verification; the full setup ZIP is a chat attachment for setup assistance, not the archive to import through ChatGPT Plugins.

## 1. Create your CloudHandset connection

Open [ChatGPT Plugins](https://chatgpt.com/plugins), choose **Add → Create custom MCP server**, and enter:

| Field | Value |
| --- | --- |
| Name | CloudHandset |
| Server URL | `https://device.cloudhandset.com/mcp` |
| Authentication | OAuth |
| Advanced OAuth settings → Registration method | Custom OAuth client / pre-registered client |
| OAuth client ID | `cloudhandset-dot` |
| OAuth client secret | Leave empty |
| Token endpoint authentication method | `none` |
| Scope | `device:control` |
| Displayed callback URL | `https://chatgpt.com/connector_platform_oauth_redirect` |

The displayed callback must match this value exactly. If it differs or the required settings are unavailable, contact CloudHandset support; do not substitute a callback or invent a client secret. The client ID is a public application identifier, not a password.

Create the connection and complete **Verify and connect** in the independent CloudHandset login window. Use your own account there; never paste passwords, verification codes, tokens, or complete OAuth callback URLs into a chat. Authorization lasts at most 30 days and cannot outlast the phone's effective lease. When it expires, reconnect through the login window.

## 2. Bind your copy of the skill

Extract `cloudhandset-dot-setup-0.2.1.zip`. In the extracted `cloudhandset-dot/` folder, find `bind-connection.py` and `plugin/`.

Open the newly created CloudHandset connection's management page and copy its technical app ID. It must have the form `asdk_app_…` or `plugin_asdk_app_…`. Use the real ID from your connection, not the display name or a hosted plugin's `Plugin_…` ID.

From the extracted folder, run this command, replacing the placeholder with that ID:

```sh
python3 bind-connection.py YOUR_CONNECTION_TECHNICAL_ID
```

The script updates `plugin/.app.json` in your extracted copy. It does not log in, transfer credentials, or create another connection.

## 3. Upload and install the bound skill

From the same extracted folder, create the upload archive:

```sh
cd plugin
python3 -m zipfile -c ../cloudhandset-dot-connected.zip plugin.json .app.json skills
```

The archive must contain `plugin.json`, `.app.json`, and `skills/` at its root. **Do not upload the full setup ZIP:** it includes installation instructions and an optional local Codex dependency. Include the hidden `.app.json` file when using a graphical ZIP tool.

At ChatGPT Plugins, choose **Add → Upload plugin archive**, select `cloudhandset-dot-connected.zip`, review the imported plugin, and install/enable it for the account used by Dot. Confirm its page shows **one connected CloudHandset app** and **one android-phone skill**. An uploaded skill with no connected app cannot operate a phone.

Keep the bound folder and `cloudhandset-dot-connected.zip` private: they reference your account's connection. Share only the original, unbound setup kit with other customers. Each customer must create and bind their own connection.

## 4. Start with a screen check

Use the first-use prompt in [DOT_SETUP.md](DOT_SETUP.md). Once the real screen and release are confirmed, describe the phone task and its stopping condition to Dot. A direct cloud connection does not require your personal computer to remain online; it does not promise indefinite or scheduled background execution.

If custom MCP creation or archive upload is unavailable for your account, this cloud installation route is unavailable. A local plugin installation alone does not enable Dot's cloud tools.

## Optional: local Codex fallback

The setup kit includes CloudHandset for Codex 0.1.2 under `local-codex/`. Keep an existing working installation. Otherwise follow `local-codex/README.md` to install it and log in on your computer.

To use that route, allow your Dot access to the computer from its **Computers** settings, keep the computer online with the desktop app open, and explicitly ask Dot to create a local Codex task using the installed `cloudhandset:cloudhandset-phone` skill. Connecting the computer to Codex is separate from allowing Dot access. The local executor inspects phone images; Dot should report that distinction. This route uses the existing local connection and must not copy cloud credentials or add a duplicate MCP server.

Release active phone control before disconnecting or removing a plugin. Removing the skill, disconnecting the app, and revoking an authorization are separate actions.

References: [Dot computers and apps](https://learn.chatgpt.com/docs/dots/computers-and-apps), [Custom MCP connections](https://developers.openai.com/api/docs/guides/custom-mcp-server), [Plugin OAuth](https://developers.openai.com/plugins/build/auth), [Build plugins in ChatGPT](https://learn.chatgpt.com/docs/build-plugins).
