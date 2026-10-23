# CloudHandset for Grok Bot

Version **0.1.1** — private custom-MCP and personal-skill integration verified for single-phone observation, basic actions, a small text-file upload, and release; **not published to the marketplace**.

Use xAI's Grok Bot to inspect and operate your leased CloudHandset Android phones through the existing remote MCP service. The plugin contains a Cursor-format manifest, native MCP configuration, a phone-operation skill, and a Python file uploader. Phone tools run on CloudHandset; no app is installed on your Android phone.

CloudHandset has applied and verified the dedicated public OAuth client `cloudhandset-grok-bot`. Real Grok Bot OAuth completed with the registered callback and exact resource; the strict service checks validated PKCE S256 and public-client authentication without a secret. Each user still needs their own CloudHandset login and authorization. This package targets Grok Bot, a separate product from the ordinary Grok chat app and the xAI model API.

## Connect

Follow [SETUP.md](SETUP.md). Private acceptance uses a custom remote MCP connector and an equivalent personal skill based on the bundled [phone instructions](skills/cloudhandset-phone/SKILL.md), with reference text inlined. In Grok Bot 0.75.3, `AddCustomMcp` prepared the connector. `UpdateSkill` saved the skill's catalog entry but did not create the `SKILL.md` file required by its loader; updating the same entry again did not resolve that gap. Writing the self-contained skill at the loader's explicitly reported path and copying the supplied helper to its `scripts/upload_file.py` made loading by name work. Two reads in the same turn and a subsequent-turn read succeeded without another save or repair.

Ask the Bot to load `cloudhandset-phone` by name. Private-skills settings, `/` selection, and persistence after a restart have not been verified. Saving a catalog entry alone does not install the backing file or uploader.

The ZIP is a distribution and review candidate. The inspected host's `InstallPlugin` accepts a stable catalog plugin ID, not an attached ZIP or local path. This candidate has no marketplace listing or catalog ID; custom MCP plus a personal skill must not be reported as a catalog plugin installation.

| Setting | Value |
| --- | --- |
| MCP endpoint / OAuth resource | `https://device.cloudhandset.com/mcp` |
| Transport | Streamable HTTP |
| Client ID | `cloudhandset-grok-bot` — service registration applied and verified |
| OAuth | Authorization Code, PKCE S256, public client, no secret |
| Scope | `device:control` |
| Verified Grok Bot cloud callback | `https://www.cursor.com/agents/mcp/oauth/callback` |

The client requests only your eligible leases. Choose your intended account or single-phone scope during verification. Account scope covers current and future eligible leases, but does not authorize tasks on every visible phone. Authorization lasts at most 30 days, with each phone limited by its effective lease. Expiry requires a new login; no refresh token is issued. Old single-phone connections do not expand automatically.

## Use

- “List my CloudHandset Android phones.”
- “Show the screen of the phone I selected, describe it, then release control.”
- “Upload this attached video to the selected Android phone's Downloads folder.”
- “Perform this task on these two named phones, and report the result and release status of each.”

The skill discovers the actual tool schemas, inspects real MCP images before visual actions, tracks each phone separately, and checks the result before reporting success. Uncertain operations retain their original IDs and are not replayed. Sessions must be closed and drained when work ends. The account limit is 16 simultaneous phones across all clients and credentials; availability and service limits still apply.

Uploads require the bundled Python 3.9+ helper and a file-specific ticket, not an OAuth token. The verified setup received the unchanged helper through a chat attachment and copied it into the personal skill's `scripts/upload_file.py`. Use a supported host file/execution flow to place the helper and requested file on Grok Bot's cloud computer and verify their paths and the helper checksum; otherwise report uploads as unavailable. Maximum supported size is 30 MiB, although large-file behavior has not been accepted in Grok Bot. Upload completion and visibility in an Android app are separate checks. The extracted distribution contains the workflow at `skills/cloudhandset-phone/references/file-upload.md`; the packager adds this shared reference and the helper.

## Validation and distribution

The manifests follow the documented Cursor plugin and static-OAuth configuration. Official support confirms Grok Bot uses these plugin MCP definitions. The build verifies its explicit file list and produces SHA-256 checksums.

Private acceptance with Grok Bot 0.75.3 verified the dedicated OAuth connection, discovery of 12 tools, and personal-skill loading by name after its backing files were supplied. The skill and uploader were readable again in a later turn without rewriting them. On one explicitly selected Android phone, the model viewed native PNG/JPEG screenshots and release was confirmed closed and drained.

Basic actions on the same phone passed HOME, opening Android Settings, BACK navigation, a tap on search using a fresh image, visibly verified text input, clearing the search, and returning HOME. Actual screenshots established the outcome; `submitted_to_device` alone was not the success criterion.

A small plain-text file upload passed through Grok Bot's native MCP connection and the existing uploader with one binary PUT. The original completion operation reached `succeeded`, and the resulting byte count and destination path were verified. Final release was closed and drained, with no remaining control writer. These checks used only one phone.

**Multiple-phone operation, media-picker visibility, large files, failure recovery, connectivity changes, restart, and sharing remain untested in Grok Bot.** These results do not establish successful execution of every discovered tool, comprehensive end-to-end acceptance, or catalog plugin installation. Private-skills UI selection and persistence after a restart also remain unverified. Existing Codex, Dot, or Muse acceptance does not establish Grok Bot results. Version 0.1.0 remains a separate historical candidate; these findings belong to 0.1.1.

Do not treat the ZIP as a Grok Bot “Import ZIP” format. It is a distributable plugin source tree and a source of text for the private setup path. Record custom-MCP connection, personal-skill persistence, and any later catalog-plugin installation separately. Cursor IDE local loading tests can inspect the files but do not install or authenticate the cloud Bot. This client registration allows only the cloud callback, so IDE localhost authentication is outside its scope.

## Official references

- [Grok Bot computer and apps](https://docs.x.ai/grok-bot/computer-and-apps)
- [Add a custom MCP through chat](https://forum.cursor.com/t/grokbot-custom-connectors/169965/5)
- [Grok Bot supports plugin MCP definitions](https://forum.cursor.com/t/grok-bot-cursor-cloud-agents-not-respecting-mcpservers-optional-field/173273/6)
- [Cursor plugin format](https://cursor.com/docs/reference/plugins) and [static OAuth configuration](https://cursor.com/docs/mcp)
- [Grok Bot cloud callback](https://forum.cursor.com/t/grok-bot-cloud-mcp-oauth-leaves-env-asana-client-id-unsubstituted/168404/14)
- [Grok Bot skills](https://docs.x.ai/grok-bot/skills-routines-and-automations)

References checked on 2026-10-23. A provider-specific static-client issue remained reported in the [official October 11 thread](https://forum.cursor.com/t/grok-bot-cloud-mcp-oauth-leaves-env-asana-client-id-unsubstituted/168404/16). Verify the actual CloudHandset connection; do not assume every host version handles the settings identically.
