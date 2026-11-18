# CloudHandset for Codex

> Includes the [shared task workflow](plugin/skills/cloudhandset-phone/references/phone-workflow.md) and three app guides for observing, acting and checking the result. A tool receipt alone does not establish task completion.

Package version: **0.1.5**. Requires a Codex version that supports plugins. The earlier release installation was checked with Codex CLI **0.162.0-alpha.2**; check the installed version and start a new conversation after upgrading.

Connect Codex to the Android phones covered by your active CloudHandset leases. Access is limited to your own account and the scope you approve during verification. Existing and newly provisioned phones use the same connection setup; a phone must finish provisioning and have a valid lease before it is available to you. Nothing from this package needs to be installed on the phone.

This package contains a local plugin marketplace, the CloudHandset plugin, its MCP connection, and the `cloudhandset-phone` skill with suggested prompts. It contains no credentials and does not grant access by itself.

## Install the plugin

**Required model for phone operation:** Select **GPT-6.1 Sol or a more capable model** in your agent before asking it to operate the phone. This requirement applies to phone operation, not plugin installation.

In a Codex conversation in **Work mode**, upload the plugin ZIP and ask Codex to install it for you. Complete your own CloudHandset login in the separate verification window when prompted.

### Manual installation

Unzip `cloudhandset-codex-plugin-0.1.5.zip` into a location you will keep. In your interactive terminal, change to its `cloudhandset-codex` folder, then run:

```sh
codex plugin marketplace add .
codex plugin add cloudhandset@cloudhandset
codex plugin list
codex mcp get cloudhandset
codex mcp login cloudhandset
```

If installation already completed verification, an additional login is unnecessary. Open a new Codex conversation after installation. If your Codex version has no `plugin` command, update to a version that supports it or use the manual MCP connection below.

An existing manual `cloudhandset` connection with the same endpoint and OAuth client ID can be retained. Do not create duplicate server names, copy credentials, or remove a working login just to install the skill. Check any conflicting configuration before changing it.

This is a local distributable plugin, not a listing in the public Codex plugin directory. It uses Codex's supported `.codex-plugin/plugin.json` compatibility format so the MCP connection can retain the registered OAuth client ID. Official reference: [Build plugins](https://developers.openai.com/plugins/build/plugins).

## Upgrade an existing installation

Keep your working CloudHandset OAuth connection. Extract the 0.1.5 ZIP into a permanent folder. From its `cloudhandset-codex/` directory, replace the old local marketplace source and reinstall the plugin:

```sh
codex plugin marketplace remove cloudhandset
codex plugin marketplace add .
codex plugin add cloudhandset@cloudhandset
codex plugin list
```

Confirm version **0.1.5**, refresh the connection's tools, and open a new conversation. These commands update the plugin source; do not log out or create another MCP connection. If a conflicting installation is reported, inspect it before changing unrelated configuration.

## Fast file upload

Version 0.1.3 adds a packaged Python uploader. Attach a file and ask Codex to upload it to your chosen Android phone using the fast upload workflow, verify completion and the returned path, then release control. The host sends one binary transfer; CloudHandset reuses its original upload writer. The limit is 30 MiB. See [file-upload.md](plugin/skills/cloudhandset-phone/references/file-upload.md). A completed transfer does not publish the file in an app.

## Prompts and skill discovery

The plugin supplies suggested prompts and enables implicit discovery of `cloudhandset-phone` for CloudHandset phone requests. Discovery depends on the host and task; installation does not mean the Agent will open a phone in every conversation. Use the skill explicitly when needed:

> Use $cloudhandset-phone to list my Android phones, let me choose one if needed, inspect its screen, and release control.

For an actual task:

> Use $cloudhandset-phone on my selected Android phone to complete this task: [describe the task]. Verify the result on screen and release control when finished.

The skill guides device selection, login recovery, fresh screenshots, serialized actions, uncertain-operation checks, and release. A list-only request stops at the list. Customer handback stops Agent control until the user asks to resume. No always-on hooks or background task runner are installed.

## Manual MCP connection (alternative)

Skip this setup if the plugin or a previous setup already supplies the connection. Use your own interactive terminal and check first:

```sh
codex mcp get cloudhandset
```

If it does not exist, add it:

```sh
codex mcp add cloudhandset --url https://device.cloudhandset.com/mcp --oauth-client-id cloudhandset-codex
```

If verification does not start automatically, run:

```sh
codex mcp login cloudhandset
```

## Verification window

If the connection already exists, check its URL and client ID before changing it. You can alternatively merge the two sections in the included `config.toml` into your Codex configuration. Do not replace your entire `~/.codex/config.toml` or overwrite unrelated MCP services.

Do not add `oauth_resource` or `--oauth-resource`: Codex discovers the resource from the server metadata, and an additional value can create a duplicate parameter in the tested version.

Enter your CloudHandset account email, password and, if enabled, two-step verification code only in the **English verification window opened by Codex**. The CloudHandset website console has no separate Agent/MCP authorization page. Choose **Current and future Android phone leases** to include eligible phones added during this fixed authorization, or **Only one selected Android phone** for access to one phone. Existing single-phone connections do not expand automatically: reconnect once to opt in, then refresh the tools and call `list_devices` again. Each phone still requires an effective lease; account scope does not resume a manually paused phone. No active lease means no phone access.

A successful login may return to a `127.0.0.1` callback handled by Codex on your computer; the MCP service remains at `https://device.cloudhandset.com/mcp`. Do not share passwords, codes, tokens, cookies or full callback URLs in chat or configuration files.

Open a new Codex conversation after login and confirm that the CloudHandset tools are available. Keep Codex's approval protections enabled and review tool requests when prompted.

## First use

Ask Codex to run `list_devices`, acquire control of your selected Android phone, call `observe`, describe the actual screenshot, and call `release_control`. Confirm that release reports the control session closed and drained. Check this basic connection before requesting further actions.

Use one control action at a time for each phone. If it is busy, do not take over another session. If an action's outcome is unknown, check the original operation ID and observe again; do not issue the same action under a new ID. If no usable screenshot is returned, do not guess where to tap. Always release control when finished.

CloudHandset MCP does not provide audio.

## Expiry and taking control back

Authorization lasts **up to 30 days**. Each Android phone is accessible only while its effective lease is valid; single-phone authorization ends no later than that lease. CloudHandset does not issue refresh tokens. If access expires, you receive a `grant_expired` or `401` response, or Codex asks you to authenticate, stop actions and run:

```sh
codex mcp login cloudhandset
```

Complete verification, open a new conversation using the connection, and start again with `list_devices`. Do not replay actions whose outcomes were unknown before expiry. Reauthentication cannot extend an expired phone lease, and a background task is not guaranteed to open a login window automatically.

Taking the phone back ends the current Agent session and preserves valid authorization. Respect the customer's control and wait until the phone is available. An already authorized task may then acquire a new session with the same connection and inspect a fresh image; never replay an uncertain action. An explicit automation stop keeps control paused until the user requests resumption and completes the supported verification flow.

## Switch CloudHandset accounts

Release any phone control first. In the same local environment used by Codex, run:

```sh
codex mcp logout cloudhandset
codex mcp login cloudhandset
```

Sign in to the new CloudHandset account. Then open a **new Codex conversation** and ask it to actually call `list_devices`. Confirm the returned phones belong to the new account before requesting control. Switching accounts does not require removing the plugin or revoking access in the CloudHandset website.

**Codex 0.163.0-alpha.11.2:** an existing conversation's MCP connection can keep using the previous account's in-memory credential after those terminal commands succeed. A native-runtime test reproduced this with both default and file credential storage. New conversations read the new credential; reloading MCP connections also updates the original conversation. Do not treat “Successfully logged in” or a remembered device list as proof that an existing conversation switched accounts. If a fresh call in a new conversation still returns old devices, check that the terminal and desktop use the same execution environment and connection name; do not keep repeating login or operate the old phone.

For host integrations, the tested same-conversation recovery is `config/mcpServer/reload` on the **already running app-server**, followed by a fresh `list_devices` call. This is an app-server protocol method, not a terminal `codex mcp` subcommand. Starting a separate app-server does not refresh the desktop's existing connection. The CloudHandset plugin cannot change Codex's native logout/login implementation.

## Sign out or remove the connection

Release control and stop conversations using the connection, then run:

```sh
codex mcp logout cloudhandset
```

To uninstall the plugin:

```sh
codex plugin remove cloudhandset@cloudhandset
```

If you also created a manual MCP configuration, remove that separately when no longer needed:

```sh
codex mcp remove cloudhandset
```

These commands target only the named connection. **Codex logout removes local credentials; it does not revoke the CloudHandset server-side grant.** Other running processes may still have credentials in memory. For immediate revocation, contact CloudHandset support and confirm that the server-side authorization has been revoked and control has drained. Do not extract or copy tokens to perform revocation yourself.

Client behavior can change after upgrades. Official references: [Codex MCP commands](https://github.com/openai/codex/blob/main/codex-rs/cli/src/mcp_cmd.rs) and [OAuth credential storage](https://github.com/openai/codex/blob/main/codex-rs/rmcp-client/src/oauth.rs).

## Verify your connection

Installing the plugin does not authenticate your account or connect a phone by itself. Complete your own first-use screen check after login, verify the observed result of each requested action, and confirm control has been released. Keep the extracted plugin folder available while it is installed.
