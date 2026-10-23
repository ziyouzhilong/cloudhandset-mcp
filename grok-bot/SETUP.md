# Set up CloudHandset in Grok Bot

Version 0.1.1: the dedicated CloudHandset OAuth client is registered and its real Grok Bot OAuth flow has been verified. Private acceptance in Grok Bot 0.75.3 passed one selected phone's screen observation, basic navigation/tap/text-input actions, a small plain-text upload, and closed/drained release. Multiple-phone operation, media-picker visibility, large files, failure recovery, connectivity changes, restart, and sharing remain untested in Grok Bot. Use the existing Grok Bot connector if one is already working; do not duplicate it or replace its private binding. No CloudHandset password, token, cookie, or authorization code belongs in chat or these files.

## 1. Prepare the connector

Use a custom MCP connection plus a personal skill for private acceptance. The ZIP is a distribution and review candidate, not a Grok Bot installer. In the inspected host, `InstallPlugin` requires a stable catalog plugin ID and does not accept an attachment, ZIP, or local path. This candidate has no catalog ID. Copy this prompt directly into a Bot chat:

```text
Prepare CloudHandset as a custom remote MCP connector in this Grok Bot account.

Endpoint and OAuth resource: https://device.cloudhandset.com/mcp
Transport: Streamable HTTP
Public client ID: cloudhandset-grok-bot
Scope: device:control
Flow: Authorization Code with PKCE S256
Token endpoint authentication: none; no client secret
Authorization endpoint: https://device.cloudhandset.com/oauth/authorize
Token endpoint: https://device.cloudhandset.com/oauth/token
No DCR endpoint and no refresh token grant.
Verified cloud callback: https://www.cursor.com/agents/mcp/oauth/callback

Use your actual current connector tools to prepare this connection. The inspected host exposes AddCustomMcp; follow its live schema. The bundled mcp.json is documented Cursor plugin configuration, not the payload for a host connector tool. Do not invent tool argument names or call InstallPlugin with a ZIP or path. Use the literal public client ID, not a Mac environment variable or another client's identity.

First check that your current flow uses the registered static public client, S256, and the exact resource. Report only the non-secret client ID, exact callback URI, PKCE method, scopes, and whether resource is sent. Do not print full authorization/callback URLs, code, state, or credentials. Do not acquire or operate a phone during preparation. If your actual flow differs from the registered settings, report the specific mismatch and stop authentication; do not substitute a secret, token, cookie, DCR service, or localhost callback.
```

CloudHandset's applied registration uses the cloud callback verified in the real authorization flow. The exact resource was present, and the strict service validated S256 and token-endpoint authentication `none`. `allowOmittedResource` remains false: if another host flow omits `resource`, report it for a narrowly scoped service review. Existing client exceptions do not apply to this client.

## 2. Login and save the personal skill

Ask Grok Bot to show its Connect/Authenticate card. Complete CloudHandset verification in the independent browser window. Choose the intended account or single-phone scope. This does not authorize work on all listed phones. A missing card can be reopened with the host's supported reconnect flow. If the provider reports an invalid client or callback, stop and check the registration; avoid repeated login attempts.

Extract the candidate ZIP outside the catalog-install flow. Provide the text from `skills/cloudhandset-phone/SKILL.md`, with the contents of its `references/tools.md`, `references/parallel-control.md`, and `references/file-upload.md` inlined as named sections. Ask Grok Bot to save one self-contained personal skill with the same instructions and safety boundaries, replacing relative reference links with those section names. Saving only the main text with unresolved file links is incomplete. Supply the unchanged `scripts/upload_file.py` from the extracted skill as a separate chat attachment if uploads are needed.

Ask the Bot to load `cloudhandset-phone` by name with its `Skill` tool. In the inspected host, `UpdateSkill` saved the catalog entry but left the backing `SKILL.md` absent; updating the same entry again did not create it. If the loader reports that exact missing-file condition, use the host's supported file/execution tools to write the self-contained skill at the path explicitly reported by the loader. Preserve the existing skill ID. Do not guess a Mac, Cursor IDE, or cloud installation path, and do not delete/recreate the skill merely to repair the missing file.

For uploads, copy the attached helper to `scripts/upload_file.py` beneath that actual skill directory, verify its SHA-256 against the distribution manifest, and confirm the host can run it with Python 3.9+. The helper and requested upload file must both exist on the Bot's computer. If the host cannot place or execute them, report that gap instead of claiming uploads are installed.

Load the skill again and read back the instructions, inlined reference sections, and helper path. After the missing files were supplied, two loads in the same turn and another load in a later turn succeeded without saving or repairing them again. This verifies loading across turns, not persistence after restart. Private-skills settings and `/` selection have not been verified as usable; invoke the skill by name. Attach the connected CloudHandset app with `@` when needed. The first screen check below does not need the uploader.

A custom MCP plus this equivalent personal skill is the private acceptance path, not a catalog plugin installation. A future catalog installation requires a published entry and its stable plugin ID; do not infer that a team repository import, a local ZIP, or Cursor IDE loading installs the plugin into Grok Bot. The team must permit the endpoint. This candidate has not been published.

## 3. First connection check

Ask Grok Bot:

```text
Load my personal skill cloudhandset-phone by name and use my authenticated
CloudHandset connector.
First discover its actual tools and list my eligible Android phones. If I have
not already selected one, ask me to choose. On that selected available phone,
acquire control, observe and actually inspect the returned PNG/JPEG image,
describe two visible details, then release control. Do not tap, type, upload,
install, share, change networking, or restart the phone in this check.

Save the session ID as soon as acquisition returns. Release that same session
even if observation fails, and report closed=true, state=closed, and writer
drain evidence separately. If an acquire response is lost, recover it with the
same request and original operation ID. Never create a new acquisition ID to
hide uncertainty. If image content cannot be viewed, say so; metadata and
base64 text alone do not establish visual acceptance.
```

Record OAuth success, the selected phone, actual model image visibility, and confirmed closed/drained release separately. The private check passed this sequence on one explicitly selected phone: 12 tools were discovered, the model viewed the returned native image, and release was closed and drained. Tool discovery or a ZIP checksum alone does not establish phone acceptance.

Separately authorized checks on that same phone passed HOME, opening Android Settings, BACK navigation, a fresh-image tap on search, visibly verified text input, clearing the search, and returning HOME. Actual images supported the outcome; `submitted_to_device` alone did not.

Once the helper is installed, follow the saved upload workflow for a requested file. The accepted small plain-text transfer used native MCP to obtain its file-specific ticket and the existing helper for one binary PUT. Check the original completion operation for terminal `succeeded` and verify its byte count and returned destination path; PUT success alone is insufficient. Final release was closed and drained with no remaining writer.

These are limited single-phone checks. Multiple-phone operation, media-picker visibility, large files, failure recovery, connectivity changes, restart, sharing, and other tool behaviors require their own authorized checks. They do not establish catalog installation, restart persistence, or comprehensive end-to-end acceptance.

For troubleshooting, provide the host version, timestamp/timezone, failing stage, error code and non-secret client settings. Keep session receipts and screenshots private. Host approvals stay enabled. CloudHandset has no audio or arbitrary shell tool.
