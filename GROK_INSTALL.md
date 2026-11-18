# Install CloudHandset for Grok Bot

> Release **plugins-2026.11.17**. See [release status and validation limits](RELEASE_STATUS.md).

Use this guide for Grok Bot, not ordinary Grok chat or a model API. Version **0.1.3** is a custom MCP plus personal-skill setup kit, not a catalog entry.

1. Obtain the [Grok Bot ZIP](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/download/plugins-2026.11.17/cloudhandset-grok-bot-plugin-0.1.3.zip), verify [SHA256SUMS](SHA256SUMS), and extract it.
2. Follow [SETUP.md](grok-bot/SETUP.md). Reuse the existing working CloudHandset connector and skill ID. The public client ID is `cloudhandset-grok-bot`; client secret is empty. Complete any necessary authorization in the separate CloudHandset window.
3. Update only that skill's files. Supply its SKILL.md, all references including phone-workflow.md and three app guides, and scripts/upload_file.py. Preserve relative directories, or inline all referenced Markdown sections only when the host requires it. Do not leave broken reference links.
4. Load the existing skill by name and verify saved contents. If the host reports a missing backing file, use only its reported path and supported recovery flow. Do not recreate a working connector or modify credential stores.
5. Report installed paths and version before phone use. Keep explicitly stopped tasks stopped. A screen check needs the user's selected phone and separate authorization.

```text
Load cloudhandset-phone by name and use my existing authenticated connection.
List my Android phones and let me select one if needed. On that available phone,
acquire control, inspect the actual screenshot, describe it and release control.
Confirm closed and drained. Do not tap, type, upload, install, share, change
networking or restart the phone. Report missing prerequisites and unresolved results.
```

Preserve valid OAuth and approved account/single-phone scope during upgrades. A new package does not widen permissions. Keep host approvals enabled and account-bound files private. Uploads require the real file and the packaged helper; verify size/SHA before acquiring control. No retries of unknown transfers are permitted.

Personal-skill persistence after a host restart and catalog installation are not certified. See [package details](grok-bot/README.md), [release limits](RELEASE_STATUS.md) and [Support](SUPPORT.md).
