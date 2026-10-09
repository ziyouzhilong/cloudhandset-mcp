# CloudHandset for Meta Muse

Setup kit **0.1.0** · Updated **2026-10-10**

Use this kit to prepare a Custom Connector for **Meta Muse, the personal agent**. It contains connection instructions, a Python MCP adapter, and a tool reference. It is not a Muse Code configuration, a native importable plugin, or a Meta-approved directory listing.

**Current compatibility:** in a 2026-10-10 account check, Muse reported no native entry point for registering an arbitrary remote MCP server. Its Custom Connector uses PKCE `S256`, callback `https://agent.meta.ai/api/hatch/oauth/callback`, and public client ID `cloudhandset-muse`. CloudHandset registered that client on 2026-10-10 and supports its omitted `resource` parameter while keeping authorization bound to the fixed MCP endpoint. The supplied adapter uses Muse's official credential helper. A live account check completed OAuth, official skill scaffolding, discovery of all 12 tools, phone listing, acquisition, one JPEG observation opened with `muse.read`, and confirmed control release. No screen actions were performed. This is a single-account connection check, not a claim about every Muse version or business workflow.

CloudHandset MCP is available to active customers for their own valid Android phone leases. Each authorization is bound to the phone selected during login. There is no fixed test account or required test phone. Other clients' successful connections do not establish Muse compatibility.

## Start here

1. Paste **Stage 1** from [SETUP.md](SETUP.md) into Muse. It asks Muse to establish its actual connection capabilities before attempting login.
2. Give CloudHandset the non-secret client ID, exact registered callback URI, authentication method, and any connector requirements that Muse can verify. Do not send a complete authorization or callback URL containing `code`, `state`, or other session values.
3. Continue to **Stage 2** only after CloudHandset confirms registration and the host can perform the required flow. Enter account credentials only in the independent CloudHandset verification window.
4. List the authorized phone first. Acquire it only when the user has selected it and requested the connection check. The first check is **list → acquire → observe → release**, with no screen actions.

See [TOOLS.md](TOOLS.md) for the current server interface and operation rules. This reference describes the CloudHandset service. Discover the live schemas in each connected account before using them; the connection check does not validate every tool or action.

## Connection requirements

| Setting | Required value or verification |
| --- | --- |
| Connection name | CloudHandset |
| MCP endpoint and OAuth resource | `https://device.cloudhandset.com/mcp` — no trailing slash |
| Transport | Remote Streamable HTTP |
| OAuth flow | Authorization Code with PKCE `S256` |
| Scope | `device:control` |
| Token endpoint authentication | `none` — public client, no client secret |
| Registered client ID | `cloudhandset-muse` |
| Registered callback URI | `https://agent.meta.ai/api/hatch/oauth/callback` |
| Dynamic client registration | No DCR endpoint is supplied |

There is no separate read-only OAuth scope. Tool read/write classifications are operational guidance, not narrower token permissions. If Muse requires DCR, a client metadata document, a secret, or another flow, report that requirement and stop until CloudHandset confirms a supported configuration. Do not invent a callback, reuse another client's ID or localhost callback, pass website cookies, share tokens, or weaken callback validation.

Authorization lasts at most **30 days** and never beyond the effective phone lease. Expiry requires fresh verification; automatic Muse login prompts have not been verified. Releasing control leaves the authorization valid. A customer's handback pauses agent control; resume only when the user requests it and completes fresh verification.

## What counts as a successful connection check

Report these outcomes separately:

- OAuth completed using the registered client and callback.
- `list_devices` returned the user's selected, authorized Android phone.
- Muse actually read the PNG/JPEG image returned by `observe` and described visible content. Tool discovery or image metadata alone is insufficient.
- `release_control` confirmed `closed: true`, `state: "closed"`, and closure evidence confirming the writer was drained, such as `bridge_execution_drained`.

If the image is unavailable, stop visual actions and release control. If release is unconfirmed, report the unresolved session. CloudHandset MCP provides no audio. It does not grant background execution independently of the host.

For support, provide the Muse version, timestamp and timezone, connection stage, error code, non-secret registration details, image result, and release result. Share session/operation/observation IDs privately when needed. Do not publish credentials, tokens, authorization links, share links, or private screenshots.

## Package contents

`cloudhandset-muse-setup-0.1.0.zip` contains only `README.md`, `SETUP.md`, `TOOLS.md`, and `cloudhandset.py` under `cloudhandset-muse/`. It includes no credentials or guessed import manifest. The Python script runs inside Muse's execution environment with its official credential helper; see the installation steps in [SETUP.md](SETUP.md).

Maintainers build it from the development repository root with:

```sh
python3 scripts/packageMuseConnector.py
```

The independent package command writes the ZIP, `manifest.json`, and `SHA256SUMS` to `output/mcp-muse-20261010/0.1.0/`. The live connection check above is separate from packaging. Publishing this kit does not submit a connector to Meta or validate arbitrary phone tasks.

## Official references

- [Meta: How Muse works with Connectors](https://www.meta.com/help/artificial-intelligence/1687253048996149/) describes asking Muse to create a Custom Connector.
- [Muse Connector Platform](https://muse.ai/platform/docs) provides connector platform guidance.

The public guides reviewed for this kit do not establish the exact Muse callback, client identity, PKCE behavior, or MCP image support required here. The callback and PKCE observations above come from the actual 2026-10-10 authorization request. Use verified host behavior and confirmed service registration before continuing the conditional setup.
