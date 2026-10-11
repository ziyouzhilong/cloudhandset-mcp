# Install CloudHandset in Meta Muse

Use Muse's chat to create a **Custom Connector and a dedicated skill**. The setup ZIP contains the files Muse needs; it is not a one-click native plugin import. This guide is for **Meta Muse, the personal agent**, not Muse Code.

## Upgrade from 0.1.0

Attach the new 0.1.1 ZIP or its five extracted files to your existing Muse conversation and send:

```text
Upgrade my existing CloudHandset skill to 0.1.1 using these files. Back up the installed files, retain the existing official Custom Connector credential binding, and install cloudhandset.py and upload_file.py side by side in its bin directory. Update TOOLS.md and the skill references to use the fast upload command. Check imports and --help without operating a phone. Do not create another connection or repeat OAuth while the existing authorization is valid. Report the installed version and paths.
```

Reuse that connection for later tasks. The uploader sends one binary transfer and checks final phone completion separately. See the [file-upload guide](DOT_UPLOAD.md). For a new installation, follow the steps below.

## Before you start

You need a CloudHandset account with an active lease for an assigned Android phone, and a Muse account with Custom Connectors and its execution environment. Use Safari for the connection flow verified with this release. Muse uses its host-provided model; you do not need to select GPT inside Muse.

## 1. Download and extract

Download [cloudhandset-muse-setup-0.1.1.zip](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/download/plugins-2026.10.11/cloudhandset-muse-setup-0.1.1.zip) from the [Muse release](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/tag/plugins-2026.10.11), and check it against [SHA256SUMS](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/download/plugins-2026.10.11/SHA256SUMS). Choose the named setup ZIP, not GitHub's Source code archive.

Extract the ZIP. The `cloudhandset-muse/` folder contains:

- `README.md`
- `SETUP.md`
- `TOOLS.md`
- `cloudhandset.py`
- `upload_file.py`

## 2. Give the files to Muse

Open [Muse](https://muse.ai/) in Safari. Attach all five extracted files to your conversation and send:

```text
Please follow the attached SETUP.md to install the CloudHandset Custom Connector and dedicated skill for me. First verify the connection requirements and show the official connection form, then wait for me to complete authorization. After connection, install the supplied cloudhandset.py and upload_file.py side by side, and bind the skill using your official credential helper. Reuse an existing working connection instead of creating a duplicate. Do not acquire or operate a phone yet.
```

Muse should check its actual connector capabilities and use the configuration in `SETUP.md`. If its callback or authentication requirements differ, have it report the mismatch before continuing.

## 3. Connect your CloudHandset account

Click the **Connect** entry Muse returns. In the hosted form:

| Field | Value |
| --- | --- |
| Client ID | `cloudhandset-muse` |
| Client Secret | Leave empty |

Continue to the separate CloudHandset verification page, sign in, and choose your access scope. Choose **Current and future Android phone leases** to include eligible phones added during this fixed authorization, or **Only one selected Android phone** for access to one phone. Existing single-phone connections do not expand automatically: reconnect once to opt in, then refresh the tools and call `list_devices` again. Each phone still requires an effective lease; account scope does not resume a manually paused phone. Enter passwords and verification codes only on that page. Let the browser complete the callback; do not paste codes, tokens, or complete authorization links into chat.

If the Connect card is no longer visible, ask Muse to show the form again for the same CloudHandset connector. If an embedded browser blocks the callback, complete a fresh connection from Muse in Safari rather than copying the blocked authorization URL.

## 4. Finish the skill installation

After the connection completes, send:

```text
Authorization is complete. Please finish installing the CloudHandset skill according to SETUP.md, using your official connector scaffold and the supplied cloudhandset.py, upload_file.py and TOOLS.md (install both Python files in the same bin directory). Keep the account-bound skill private. First discover the tools and list my authorized phone. Report its name and availability, then wait for me before acquiring control or checking the screen.
```

Muse installs the script in its own execution environment. You do not need to run Python on your computer or install anything on the Android phone. Keep normal host approvals enabled. If Muse asks to contact `device.cloudhandset.com` for this check, review the request and use **Allow once**. If a request times out, wait for its outcome and follow `SETUP.md`; do not repeatedly resend uncertain operations.

## 5. Check the screen

Once Muse has listed your phone, replace the placeholder below with its actual name and send:

```text
Use CloudHandset to check [MY PHONE NAME]. Acquire control, inspect its current screenshot and describe what you see, then release control and confirm it is closed. This is a screen check only; do not tap, type, scroll, or press keys.
```

A successful check means Muse actually reads the returned image and confirms release with `closed: true`, `state: closed`, and drain evidence. After that, give Muse a specific phone task when you want it to act.

## Help and limits

- Detailed connector configuration and recovery: [SETUP.md](muse/SETUP.md).
- Available tools and operation rules: [TOOLS.md](muse/TOOLS.md).
- Connection overview and verified scope: [Muse README](muse/README.md).
- Help with a mismatched callback or failed connection: [Support](SUPPORT.md).

Authorization lasts up to 30 days; each phone requires an effective lease, and single-phone access ends no later than that lease. Expiry requires fresh verification. One account completed a real connection, screenshot-read, and release check with this release; taps, text input, and app workflows were not part of that check. The package does not provide audio, guaranteed background execution, or a Meta-approved directory listing.
