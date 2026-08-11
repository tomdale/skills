---
name: codex-cli-development
description: Research, configure, and extend the OpenAI Codex CLI (codex-rs). Use when working on Codex skills, plugins, MCP servers, config layers, hooks, exec policy, sandboxing, or non-interactive (exec) mode. Also use when diagnosing skill discovery, invocation, or context-budget issues in Codex sessions.
metadata:
  internal: true
---

# Codex CLI Development

Authoritative sources: [github.com/openai/codex](https://github.com/openai/codex) (raw GitHub
works with curl; use `curl -sL "https://raw.githubusercontent.com/openai/codex/main/..."` for
source) and [developers.openai.com/codex](https://developers.openai.com/codex) (JS SPA, browser
only). **Verified against the installed `codex-cli 0.144.4` and current first-party source/docs available at review time.** Written in Rust (`codex-rs`). Version-sensitive details must be checked with the installed binary and its `--help` output.

## Installation

```sh
curl -fsSL https://chatgpt.com/codex/install.sh | sh   # macOS/Linux
npm install -g @openai/codex
brew install --cask codex
```

Auth: `codex login` (ChatGPT account) or `CODEX_API_KEY=<key>`.

## Key CLI Subcommands

`exec`/`e` (non-interactive; see [references/exec-noninteractive.md](references/exec-noninteractive.md)) · `review` · `mcp` · `plugin` · `mcp-server` (Codex as MCP server)
· `doctor` · `apply`/`a` · `resume` · `fork` · `sandbox` · `update` · `completion`

Default (no subcommand): interactive TUI.

## Config System

Config file: `~/.codex/config.toml`. `$CODEX_HOME` defaults to `~/.codex`.
Full field list: [references/config-reference.md](references/config-reference.md).

**Layer stack** (highest precedence wins):
`admin (MDM)` → `system (/etc/codex/)` → `cloud (enterprise)` → **`user (~/.codex/)`** →
`profile (~/.codex/<name>.config.toml)` → `cwd` → `tree (.codex/ in parents)` → `repo (.codex/ at git root)` → `runtime (CLI flags)`

Project-local layers (cwd/tree/repo) **cannot** set: `openai_base_url`, `model_provider`,
`model_providers`, `notify`, `profile`, `otel`, `chatgpt_base_url` (security boundary).
Untrusted directories have their config loaded but disabled.

Minimal example:
```toml
model = "o4-mini"
approval_policy = "on-request"   # untrusted | on-request (default)
sandbox_mode = "read-only"       # read-only | workspace-write | danger-full-access
instructions = "Always use TypeScript strict mode."
```

## Skills

Skills are `SKILL.md` files loaded into Codex's context. See [references/skills.md](references/skills.md).

**Discovery roots** (scanned in this priority order):

| Scope | Paths |
|-------|-------|
| Repo | `.codex/skills/` at project root; `.agents/skills/` in dirs from CWD up to project root |
| User | `$HOME/.agents/skills/` (preferred); `$CODEX_HOME/skills/` (deprecated, still scanned) |
| System | `$CODEX_HOME/skills/.system/` (bundled skills, extracted from binary at startup) |
| Admin | `/etc/codex/skills/` |

Plugin-contributed skill roots also appear at User scope.

**SKILL.md frontmatter:**
```yaml
---
name: my-skill         # required, ≤64 chars
description: |         # required, ≤1024 chars – primary trigger; include WHEN to use here
  The body is loaded only after triggering, so all trigger context must be in description.
---
```

Optional: `agents/openai.yaml` (UI metadata), `scripts/`, `references/`, `assets/` dirs.

**Invocation**: named explicitly by user (`$SkillName` or plain mention), or task matches description,
or a script from the skill's `scripts/` dir is executed. Not carried across turns unless re-mentioned.

For repo-local skills, use a discovered `.agents/skills/<name>/` or `.codex/skills/<name>/` directory. Test selection through the normal interactive or `codex exec` flow.

**Context budget**: 2% of context window (≈8,000 chars) for all skill name+description text combined.
Descriptions are truncated or dropped if budget is exceeded. Disable unused skills to recover budget.

**Skill config in `~/.codex/config.toml`:**
```toml
[skills]
include_instructions = true   # include skills block in system prompt
[skills.bundled]
enabled = true                # system/bundled skills on/off

[[skills.config]]
name = "unwanted-skill"
enabled = false
[[skills.config]]
path = "/abs/path/to/SKILL.md"
enabled = false
```

## MCP (Model Context Protocol)

See [references/mcp-reference.md](references/mcp-reference.md).

```bash
codex mcp add my-server -- npx -y @org/mcp-server   # stdio transport
codex mcp add my-server --url https://host/mcp       # HTTP/SSE transport
codex mcp list | remove | login | logout
```

Config in `config.toml` under `[mcp_servers.<name>]`. Per-tool approval modes:
`auto` | `prompt` | `writes` | `approve`. Codex exposes itself as MCP server via `codex mcp-server`.

## Plugins

See [references/plugin-reference.md](references/plugin-reference.md).

```bash
codex plugin add sample@openai-bundled
codex plugin list [--available] [--json]
codex plugin remove sample
codex plugin marketplace list
```

A plugin manifest declares skills, MCP servers, apps, and hooks. Installed from configured
marketplaces. Per-plugin control: `[plugins.my-plugin] enabled = false` in `config.toml`.

## Hooks

Lifecycle events: `SessionStart` · `UserPromptSubmit` · `PreToolUse` · `PermissionRequest` ·
`PostToolUse` · `PreCompact` · `PostCompact` · `SubagentStart` · `SubagentStop` · `Stop`

See [references/hooks-reference.md](references/hooks-reference.md).
Admin enforcement: `allow_managed_hooks_only = true` in `requirements.toml` disables user hooks.

## Exec Policy & Sandboxing

Exec policy: prefix-pattern allowlists/blocklists for shell commands. Admin-enforced via
`requirements.toml`. Test rules with `codex execpolicy`.

Sandboxes: macOS → Seatbelt; Linux → bubblewrap; Windows → Windows Sandbox.
`CODEX_SANDBOX=seatbelt` and `CODEX_SANDBOX_NETWORK_DISABLED=1` are set in sandboxed child env.
**Never modify logic guarding those env vars.**

Sandbox modes: `read-only` (default) · `workspace-write` · `danger-full-access`.

## AGENTS.md / Instructions

Codex reads `AGENTS.md` from repo root, `.codex/`, and parent dirs. Max 32 KB (configurable via
`project_doc_max_bytes`). Inline: `instructions = "..."` in `config.toml`. File-based:
`model_instructions_file = "/path/to/file"`.

## Limitations & Portability Caveats

- `developers.openai.com/codex` is a JS site whose URL structure and CLI flags can change; use the rendered first-party docs and raw GitHub source for scripting/curl.
- Bundled skills live inside the binary; disable with `[skills.bundled] enabled = false`.
- `$HOME/.agents/skills/` is shared with Claude Code on this machine (symlinked). Prefer it for cross-harness skills.
- Project-local config cannot override network/provider settings (enforced security boundary).
- Some features (plugins, marketplace) require ChatGPT account auth.
- API surface evolves rapidly; verify field names against the latest release tag before depending on them.
- The older Node CLI in `codex-cli/` is a thin wrapper; `codex-rs` is the active codebase.

## Source References

| File | Topic |
|------|-------|
| `codex-rs/cli/src/main.rs` | CLI subcommands and flags |
| `codex-rs/config/src/config_toml.rs` | Config struct and all fields |
| `codex-rs/config/src/loader/mod.rs` | Layer loading order |
| `codex-rs/core-skills/src/loader.rs` | Skill discovery / roots |
| `codex-rs/core-skills/src/render.rs` | Skill context budget and injection |
| `codex-rs/config/src/mcp_types.rs` | MCP server config types |
| `codex-rs/plugin/src/manifest.rs` | Plugin manifest structure |
| `codex-rs/config/src/hook_config.rs` | Hook events and TOML format |
| `codex-rs/execpolicy/` | Exec policy rules engine |
| `codex-rs/skills/src/assets/samples/` | Bundled system skill examples |
