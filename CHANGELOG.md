# Changelog

## 2026-10-18 — Dot 0.2.4 and Muse 0.1.2

- Add independent cross-phone workflows with ordered steps per phone, separate images/results, bounded dispatch, and independent cleanup after partial failures. Account-wide simultaneous control is limited to 16 phones across all clients and credentials.
- Dot follows the host's native parallel facility when available. Muse adds a finite, explicitly paced `parallel` command, without automatic action retries or hidden extra coordinators.
- Repair Muse official-helper compatibility and preflight diagnostics; reject incorrect read/release fields before dispatch; convert explicit normalized coordinates once using the matching current observation; verify the original upload completion with bounded read-only continuation.
- Keep existing valid OAuth and private connector bindings. Retain the published Codex 0.1.3 package and checksum.
- Validation scope: Service capacity was checked at 1, 4, 8, and 16 phones for 120 seconds per level. Dot 0.2.4 was installed in the existing cloud plugin; Codex exercised its existing authenticated Dot connection with two concurrent phone sessions, separate screen checks, Settings/Home actions, and closed/drained release. Muse's own host exercised two phones in parallel, explicit normalized-coordinate taps, clipboard write/read, and two consecutive 4,694,656-byte Demo MP4 uploads on one phone, reported at 28 seconds each. Both uploads completed with the active-session check passed, both videos were inspected in Gallery, and both phone sessions were closed and drained. These were two-phone client checks, not native 16-phone app-workflow tests. Upload recovery after an unknown result was not triggered. Some navigation-bar taps on one Muse test phone produced no visible change despite acceptance; an in-app back tap worked. That isolated behavior remains unexplained.

## 2026-10-11 — Codex 0.1.3, Dot 0.2.3 and Muse 0.1.1

- Include the shared fast uploader: one binary transfer from the agent host, followed by the original CloudHandset upload writer and separate final completion checks. The 30 MiB limit is unchanged.
- Keep existing OAuth connections and private bindings when upgrading. Document account-scope authorization for current and future eligible Android phone leases; existing single-phone grants require explicit opt-in.
- Include both Python files in Muse's five-file kit and Codex 0.1.3 in Dot's optional local fallback.
- Publish four unbound archives, English installation and upgrade steps, and unified SHA256SUMS. Earlier release assets remain available.
- Validate the same 4,694,656-byte Demo MP4 through the web, Codex, the Dot connection exercised by Codex, and Muse's own host, including Android checksum/media-index checks and closed/drained release. Dot's autonomous model and app publication were not tested.

## 2026-10-10 — CloudHandset for OpenAI Dot 0.2.2

- Add the exact authenticated `device_tool` file-upload fields, 30 MiB file limit, ordered 32 KiB chunks, rate pacing, and checks for asynchronous completion.
- Document source-file reading, SHA-256 verification, recovery using the original operation ID, and confirmed control release.
- Explain the `Download/CloudHandset` destination and how to check the intended Android media picker after a media-index request. A completed transfer does not establish publication.
- Add upgrade instructions that reuse the customer's existing connection and replace the skill through **Upload new version**. Refresh stale MCP tool schemas before uploading.
- Publish unbound setup and plugin archives with SHA256SUMS. Existing Codex, Dot 0.2.1, and Muse release assets remain available.


## 2026-10-10 — Muse installation guide

- Add a five-step English chat-based installation guide with copyable prompts, connection form values, and the first screen check.
- Link the guide from the repository and Muse overview. Published 0.1.0 ZIP files and checksums are unchanged.

## 2026-10-10 — CloudHandset for Meta Muse 0.1.0

- Add a separate setup kit for Meta Muse's personal agent, using a Custom Connector and Python MCP adapter with Muse's credential helper.
- Include setup prompts, the 12-tool reference, and rules for choosing a phone, inspecting images, resolving unknown operations, and confirming release.
- Pass a real connection and screen check in one Muse account: OAuth, the official connector scaffold, discovery of all 12 MCP tools, listing the authorized phone, acquiring control, the model reading an actual screenshot, and closed/drained release. Taps, text input, and app workflows were not tested.
- Keep the package free of customer credentials and account-bound configuration. This is not a native plugin import or a Meta-approved directory listing.
- Keep the Codex 0.1.2 and Dot 0.2.1 downloads and checksums unchanged. Their GPT-6.1 Sol-or-more-capable requirement applies to Codex/Dot phone operation; Muse uses its host-provided model.

## 2026-10-09 — Public download packages

### CloudHandset for Codex 0.1.2

- Distribute the local plugin marketplace, registered MCP connection configuration, and `cloudhandset-phone` skill.
- Document installation, independent account verification, the manual MCP alternative, first-use screen checks, expiry, and removal.
- Guide agents to use fresh screenshots, verify visible results, resolve uncertain operations without replaying them, and release control.

### CloudHandset for Dot 0.2.1

- Distribute an unbound setup kit for each customer's own CloudHandset connection.
- Document the static OAuth client settings, per-account app-ID binding, and generation of the skill archive for ChatGPT Plugins.
- Include the `android-phone` skill, first-use prompts, and CloudHandset for Codex 0.1.2 for the optional local execution route.
- Keep account-bound archives separate from the public package.

### Shared documentation

- Provide English customer installation guides and download checksums.
- Explain the authorization limit of 30 days, the earlier lease-expiry limit, and customer handback behavior.
- Clarify that these packages do not provide audio, a public one-click marketplace listing, or a guaranteed background task runner.

This release covers the downloadable client packages and their documentation; client versions are tracked separately.
