# Changelog

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
