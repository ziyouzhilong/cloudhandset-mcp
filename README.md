# CloudHandset MCP Plugins

> Release **plugins-2026.11.17**. See [release status and validation limits](RELEASE_STATUS.md).

Connect Codex, OpenAI Dot, Meta Muse or Grok Bot to Android phones covered by your CloudHandset leases. Each customer signs in with their own account. Packages do not contain credentials or grant phone access by themselves.

## Packages

| Client | Release asset | Installation |
| --- | --- | --- |
| Codex 0.1.5 | [Plugin ZIP](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/download/plugins-2026.11.17/cloudhandset-codex-plugin-0.1.5.zip) | [Codex guide](CODEX_INSTALL.md) |
| Dot 0.2.6 | [Setup ZIP](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/download/plugins-2026.11.17/cloudhandset-dot-setup-0.2.6.zip) | [Dot guide](DOT_INSTALL.md) |
| Muse 0.1.4 | [Setup ZIP](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/download/plugins-2026.11.17/cloudhandset-muse-setup-0.1.4.zip) | [Muse guide](MUSE_INSTALL.md) |
| Grok Bot 0.1.3 | [Setup ZIP](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/download/plugins-2026.11.17/cloudhandset-grok-bot-plugin-0.1.3.zip) | [Grok Bot guide](GROK_INSTALL.md) |

The separate [unbound Dot plugin ZIP](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/download/plugins-2026.11.17/cloudhandset-dot-plugin-0.2.6.zip) is also available; most customers should use the setup kit and follow its connection-binding procedure. Choose named assets, not GitHub's automatically generated Source code archives. Verify the five files against [SHA256SUMS](SHA256SUMS); [release.json](release.json) records exact sizes, versions, hashes and publication status.

## Install and upgrade

Codex and Dot phone operation requires GPT-6.1 Sol or a more capable model. Muse and Grok Bot use their host-provided models. Host support for custom connections, execution and actual image inspection is required; a package is not a one-click catalog installation.

Keep an existing working connection, private binding, valid OAuth authorization and approved phone scope. Updating files does not expand a single-phone authorization or resume an explicitly stopped task. Use the host's normal consent flow only when authorization has expired or the user requests a different scope. Never copy credentials between clients.

Install only the named CloudHandset connector/skill files. Muse installation must not edit global MEMORY.md, daily logs, unrelated skills, global agent instructions, scheduled tasks or internal credential stores. Its [installation guide](MUSE_INSTALL.md) and [bundled scope](muse/SETUP.md#installation-scope) define the permitted paths. Stop if the host requires broader changes.

Installation and phone acceptance are separate. After the user selects a phone and requests a check, list, acquire, inspect the actual image and release with closed/drained confirmation. Missing tools, images or unconfirmed release must be reported. Unknown actions retain their original IDs and must not be replayed.

## Task and upload boundaries

The packages include the same task workflow and guides for Settings, designated Chrome test pages and Gallery. These are navigation aids, not proof that every app or host workflow succeeds. Optional semantic UI information is experimental and cannot replace screenshots.

Use [file-upload instructions](DOT_UPLOAD.md) to inspect the real attachment before acquiring control. Require any supplied size/SHA to match exactly. Dot's attachment materialization path has an unresolved original-versus-derived-file boundary; if original bytes cannot be verified, stop before control or upload. Do not repair encoded content or search unrelated history to reconstruct it.

Different phones can progress independently within the account's shared limit of 16 controlled phones; steps on each phone remain ordered. See [parallel control](PARALLEL_CONTROL.md). A completed transfer does not establish media-picker visibility or publication in another app.

CloudHandset MCP provides no audio or arbitrary shell access, and no MCP app-catalog/install actions. The current downgrade evidence concerns the new service with optional semantics disabled; it does not certify older server binaries. Native model-input provenance, all-host cancellation behavior and every app workflow are not fully established. See [validation limits](RELEASE_STATUS.md).

[CloudHandset](https://www.cloudhandset.com) · [Changelog](CHANGELOG.md) · [Support](SUPPORT.md)
