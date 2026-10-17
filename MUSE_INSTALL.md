# Install CloudHandset in Meta Muse

Version **0.1.2** uses Meta Muse's Custom Connector and a dedicated skill in Muse's execution environment. Download the setup kit and let Muse install it through chat. It is not a native plugin import or a Muse Code configuration.

## Upgrade an existing connection

Download [cloudhandset-muse-setup-0.1.2.zip](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/download/plugins-2026.10.18/cloudhandset-muse-setup-0.1.2.zip), verify [SHA256SUMS](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/download/plugins-2026.10.18/SHA256SUMS), and attach the ZIP or all six extracted files to your existing Muse conversation. Send:

```text
Upgrade my existing CloudHandset skill to 0.1.2 using the attached files. First verify the current official credential helper and back up the working adapter and skill instructions. Keep the existing Custom Connector, private credential binding, and valid OAuth authorization. Install cloudhandset.py and upload_file.py side by side in the existing executable directory, and update TOOLS.md and PARALLEL_CONTROL.md references in the skill. Run import, compile, and --help checks without phone actions. Do not create another connection or repeat authorization while the existing access is valid. Report the installed version, paths, and check results.
```

The upgrade adds parallel control and four repairs: current official credential-helper compatibility and clear preflight errors; exact read/release argument checks; explicit optional coordinate conversion; and bounded verification of an upload's original completion operation. Screenshot pixels remain the default. Normalized coordinates are accepted only when explicitly requested with the current observation's actual image dimensions and matching session/observation IDs. See [TOOLS.md](muse/TOOLS.md).

## 1. Download the six-file kit

Choose the named [Muse setup ZIP](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/download/plugins-2026.10.18/cloudhandset-muse-setup-0.1.2.zip) from the [release](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/tag/plugins-2026.10.18), not GitHub's Source code archive. The `cloudhandset-muse/` folder contains `README.md`, `SETUP.md`, `TOOLS.md`, `PARALLEL_CONTROL.md`, `cloudhandset.py`, and `upload_file.py`.

You need a CloudHandset account with an active Android phone lease and a Muse account with Custom Connectors and its execution environment. The connection flow has been used in Safari. Nothing from the kit is installed on your Android phone.

## 2. Give the files to Muse

Open [Muse](https://muse.ai/), attach all six files, and send:

```text
Follow the attached SETUP.md to install CloudHandset using your official Custom Connector and a dedicated skill. Reuse an existing working connection if one exists. Otherwise verify the actual connector requirements, show the official connection form, and wait for me to authorize it. After authorization, install cloudhandset.py and upload_file.py together and reference TOOLS.md and PARALLEL_CONTROL.md from the private skill. Do not acquire or operate a phone yet.
```

Muse must use its current official credential helper. The registered configuration uses `cloudhandset-muse`, public-client authentication `none`, PKCE S256, and the exact callback `https://agent.meta.ai/api/hatch/oauth/callback`. If the current host requires different values, report the mismatch before continuing. Detailed settings and staged prompts are in [SETUP.md](muse/SETUP.md).

## 3. Complete the official connection form

Click the **Connect** entry Muse returns. Enter client ID **`cloudhandset-muse`** and leave the client secret empty. Continue to the separate CloudHandset verification page and sign in there. Choose **Current and future Android phone leases** if this connection should cover the account's eligible phones, or **Only one selected Android phone** for one phone. An existing single-phone authorization requires a normal reconnect to opt in to account scope; package upgrades do not expand it automatically.

Enter passwords and verification codes only on the verification page, and let the browser finish the callback. Do not paste credentials, tokens, complete callback URLs, or authorization links into chat. If the Connect card is missing, ask Muse to show the form for the same connector. If an embedded browser blocks the callback, start a fresh connection from Muse in Safari.

## 4. Finish installation and list phones

After authorization completes, send:

```text
Authorization is complete. Finish the CloudHandset installation with your current official connector setup procedure and the six supplied files. Keep the account-bound configuration private. Discover the live tools and list my eligible Android phones with their names and availability, then wait before acquiring control.
```

An existing connected provider need not be scaffolded again. Retain its private binding and keep normal host approvals enabled. Command examples use `bin/` or `scripts/`; Muse should substitute the actual adapter path reported during installation and the credential name from its own connector instructions. Keep the two Python files in that same directory. Account-scope access still requires an effective lease for every phone. Ordinary customer take-back preserves authorization; an explicitly stopped automation state is separate.

## 5. Check selected screens

Replace the names with phones returned by the fresh list. For one phone, omit the second name:

```text
Use my existing CloudHandset connection to check [PHONE A] and [PHONE B]. Follow PARALLEL_CONTROL.md: maintain independent sessions and results, run different phones in parallel with explicit workers and shared call budgets, and keep steps on each phone ordered. Acquire only these available phones, actually read each screenshot, and describe each screen. Do not tap, type, scroll, or press keys. Release each session independently and confirm it is closed and drained. Preserve and report partial failures or unresolved cleanup without replaying uncertain actions.
```

The limit is **16 simultaneously controlled Android phones per account**, across all clients and credentials. Worker count does not increase that limit. Muse's `parallel` command runs a finite batch; it does not automatically acquire, operate, or release phones. A successful check requires actual image inspection and separate confirmed release for each phone. Image metadata alone does not prove a screen check.

## Uploads and recovery

The [fast-upload workflow](DOT_UPLOAD.md) sends a file once. Muse 0.1.2 waits within a bounded query budget for the same completion operation and checks the matching byte count and Android path. Pending or unknown results keep the original IDs for read-only `upload-status`; they do not trigger another PUT. `upload_complete` and the final `session_checked_active`/`can_start_next_upload` check are distinct, and no next file starts automatically. Gallery visibility needs its own check when required by the task.

For exact commands, coordinates, argument fields, and errors, use [TOOLS.md](muse/TOOLS.md), [SETUP.md](muse/SETUP.md), and [Support](SUPPORT.md). Reuse valid OAuth; expired authorization or account-scope changes require the normal verification flow.

Current two-phone Muse-host results and remaining limits are recorded in [the Muse overview](muse/README.md#validation-scope--2026-10-18).
