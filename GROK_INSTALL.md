# Install CloudHandset for Grok Bot

Use this guide for xAI **Grok Bot**, not ordinary Grok chat or the xAI model API.

1. Download [CloudHandset for Grok Bot 0.1.1](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/download/plugins-2026.10.23/cloudhandset-grok-bot-plugin-0.1.1.zip), verify [SHA256SUMS](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/download/plugins-2026.10.23/SHA256SUMS), and extract it.
2. Follow the connector prompt in [SETUP.md](grok-bot/SETUP.md). Reuse a working CloudHandset connection. The endpoint is `https://device.cloudhandset.com/mcp`, public client ID `cloudhandset-grok-bot`, scope `device:control`, and client secret is empty.
3. Click the Connect card returned by Grok Bot. Complete your own login in the separate CloudHandset window and choose account or single-phone scope. Do not send your password, verification code, or callback URL to chat.
4. Supply the skill and its reference text from the extracted package as described in SETUP.md. Save one self-contained personal skill named `cloudhandset-phone`, then ask Grok Bot to load it by name. If the loader reports a missing backing file, follow the exact-path repair in the guide. For uploads, also supply `scripts/upload_file.py` from the skill folder and verify its checksum before using it.
5. Ask Grok Bot to list your phones. Select one available Android phone, view its current screenshot, and release control before starting a larger task.

First screen-check prompt:

```text
Load cloudhandset-phone by name and use my authenticated CloudHandset connector.
List my Android phones and let me choose one if I have not selected one yet.
On that available phone, acquire control, inspect the actual screenshot,
describe what you see, then release control and confirm closed and drained.
Do not tap, type, upload, install, share, change networking, or restart the phone.
```

The supported setup is **custom MCP plus a personal skill**. The ZIP is a source and setup package, not a direct Grok Bot catalog import; this GitHub release is not a marketplace listing. Use the skill by name. The private-skill menu and persistence after a host restart are not verified. See [compatibility and supported validation scope](grok-bot/README.md) before relying on a particular workflow.

Uploads require Python 3.9+ and the included helper on the Bot's computer. The helper performs one binary transfer, and the agent must check the original completion operation and release control. A completed upload does not establish visibility in a media picker or publication in an app.

Existing Codex, Dot, and Muse installations need no changes. Keep valid connections and account-bound skills private.
