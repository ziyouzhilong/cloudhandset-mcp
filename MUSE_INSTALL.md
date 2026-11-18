# Install CloudHandset in Meta Muse

> Release **plugins-2026.11.17**. See [release status and validation limits](RELEASE_STATUS.md).

Setup kit **0.1.4** uses Muse's Custom Connector and a dedicated skill. The unchanged Python adapter reports **0.1.2**; that protocol version is separate from the kit version. This is not native ZIP import or Muse Code configuration.

## Package and permitted installation paths

The [Muse ZIP](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/download/plugins-2026.11.17/cloudhandset-muse-setup-0.1.4.zip) has ten files under `cloudhandset-muse/`: README.md, SETUP.md, TOOLS.md, PARALLEL_CONTROL.md, phone-workflow.md, cloudhandset.py, upload_file.py, and app-guides/android-settings.md, chrome-qa.md and gallery.md. Check [SHA256SUMS](SHA256SUMS). The executable/skill installation has eight files; README and SETUP are reference documents.

Before changing files, identify the actual CloudHandset connector and skill directories and report the intended paths. Install or update only this connector's CloudHandset files and a backup within its confirmed directory; for a new connection, use the dedicated directory returned by the host's normal setup flow. Do not guess a global path.

Do not read or edit global MEMORY.md, daily logs, unrelated chat/history files, other skills, global agent instructions, scheduled tasks, or internal credential stores as part of installation. Use the official credential helper without inspecting or copying credentials. If host instructions require changes outside the confirmed connector/skill directories, stop and report the conflict before changing files.

Preserve the existing connector, private binding, valid OAuth authorization and approved phone scope. Keep explicitly stopped tasks stopped; installation does not resume automation or authorize phone control. Report installed paths, package and adapter versions, and local import/compile/help checks. A phone screen check is a separate user-authorized step.

## Upgrade an existing connection

Attach the complete new ZIP to the existing Muse account. Send:

```text
Upgrade only my existing CloudHandset connector/skill from the attached 0.1.4 kit. First follow SETUP.md's Installation scope: identify the actual directories and intended file paths, and make a backup there. Keep the existing connector, private binding, valid OAuth, approved scope and stopped-task state. Install cloudhandset.py and upload_file.py side by side, plus TOOLS.md, PARALLEL_CONTROL.md, phone-workflow.md and all three app-guides files. Do not modify global MEMORY.md, daily logs, other skills, global instructions, scheduled tasks or credential stores. If a host rule requires broader changes, stop and report it. Run only local import, compile and --help checks. Do not acquire or operate a phone. Report paths, installed file hashes, kit/adapter versions and any unresolved checks.
```

## New connection

Follow [SETUP.md](muse/SETUP.md), including its staged compatibility checks, using the same installation scope above. Use the current official credential helper. Reuse an existing provider when available; otherwise show the normal connector form and wait for the user's authorization.

The registered public client ID is `cloudhandset-muse`, callback `https://agent.meta.ai/api/hatch/oauth/callback`, token authentication `none`, PKCE S256, scope `device:control`. A different actual host flow must be reported rather than guessed. Complete login only in CloudHandset's separate verification window. Never paste passwords, tokens, authorization codes or complete callback links into chat.

Choose account or single-phone scope deliberately; upgrading the package never expands it. Keep account-bound configuration private. The official helper is used, not copied or edited.

## Separate first phone check

When ready, explicitly request a fresh phone list and choose one available phone. Then request acquire, actual screenshot inspection, a description and release with closed/drained confirmation. No tap, typing or upload is needed for that check. If the image is unavailable, stop visual actions. Preserve and report unresolved operations or release instead of retrying unknown writes.

For multi-phone tasks use [parallel control](PARALLEL_CONTROL.md). For uploads, preflight the original file before acquiring control and follow [TOOLS.md](muse/TOOLS.md#fast-upload-011) and [upload instructions](DOT_UPLOAD.md). Pending transfer results retain their original identifiers for read-only status checks.

The new installation-scope paragraph has received local document/package checks, not a new native installation acceptance run. Earlier installation side effects and incomplete host-input evidence are not retroactively resolved by this wording. See [release limits](RELEASE_STATUS.md).
