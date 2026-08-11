# Codex CLI Configuration Reference

Source: `codex-rs/config/src/config_toml.rs`
Verified: installed `codex-cli 0.144.4` and current first-party source/docs available at review time

## Top-Level Fields (`ConfigToml`)

### Model / Inference

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `model` | string | – | Model override (e.g. `"o4-mini"`) |
| `review_model` | string | – | Model used by `/review` |
| `model_provider` | string | – | Key from `model_providers` map |
| `model_context_window` | i64 | – | Context window size in tokens |
| `model_auto_compact_token_limit` | i64 | – | Auto-compaction threshold |
| `model_auto_compact_token_limit_scope` | enum | – | `full` or `suffix` |
| `model_instructions_file` | absolute path | – | Points to a file for model instructions |

### Approval & Sandbox

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `approval_policy` | enum | `on-request` | `untrusted` \| `on-request` \| fine-grained object |
| `sandbox_mode` | enum | `read-only` | `read-only` \| `workspace-write` \| `danger-full-access` |
| `sandbox_workspace_write` | object | – | Fine-grained workspace-write config |
| `allow_login_shell` | bool | `true` | Allow model to request login shells |
| `auto_review` | object | – | Guardian auto-reviewer policy instructions |
| `approvals_reviewer` | enum | – | Where approval requests escalate to |

### Instructions

| Field | Type | Notes |
|-------|------|-------|
| `instructions` | string | Injected into system prompt (user-level) |
| `developer_instructions` | string | Developer-facing instructions |
| `include_permissions_instructions` | bool | Include permissions in system prompt |
| `include_apps_instructions` | bool | Include apps instructions |
| `include_collaboration_mode_instructions` | bool | Include collab mode instructions |
| `include_environment_context` | bool | Include env context |
| `compact_prompt` | string | Custom compaction prompt |

### Project Docs (AGENTS.md)

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `project_doc_max_bytes` | usize | `32768` (32 KB) | Max bytes from AGENTS.md |
| `project_doc_fallback_filenames` | list of strings | `[]` | Filenames to try if AGENTS.md missing |

### Skills

```toml
[skills]
include_instructions = true    # include skills block in system prompt

[skills.bundled]
enabled = true                 # enable/disable system/bundled skills

[[skills.config]]
name = "skill-name"            # select by name
enabled = false

[[skills.config]]
path = "/abs/path/to/SKILL.md" # select by path
enabled = false
```

### MCP Servers

```toml
[mcp_servers.my-server]
command = "npx"
args = ["-y", "@org/mcp-package"]
env = { MY_VAR = "value" }
timeout_ms = 30000
approval_mode = "auto"         # auto | prompt | writes | approve

# HTTP/SSE transport
[mcp_servers.remote-server]
url = "https://example.com/mcp"

# OAuth
[mcp_servers.oauth-server]
url = "https://example.com/mcp"
[mcp_servers.oauth-server.auth.oauth]
client_id = "..."
```

### Plugins

```toml
[plugins.my-plugin]
enabled = true

[plugins.my-plugin.mcp_servers.some-server]
approval_mode = "prompt"
```

### Marketplaces

```toml
[marketplaces.openai-bundled]
last_updated = "2025-01-01T00:00:00Z"
last_revision = "abc123"
```

### Hooks (inline in config.toml)

```toml
[hooks.PreToolUse]
# See hooks-reference.md for full structure
```

### Other

| Field | Type | Notes |
|-------|------|-------|
| `history` | object | Session history settings |
| `tui` | object | TUI display settings |
| `shell_environment_policy` | object | Shell env var passthrough policy |
| `notify` | list of strings | Notification targets |
| `tool_output_token_limit` | usize | Token budget for tool outputs |
| `sqlite_home` | path | SQLite state DB directory |
| `log_dir` | path | Log file directory |
| `hide_agent_reasoning` | bool | Default false; hide reasoning in UI |
| `model_providers` | map | Custom model provider configs |
| `orchestrator.skills.enabled` | bool | Toggle skills at orchestrator level |
| `orchestrator.mcp.enabled` | bool | Toggle MCP at orchestrator level |

## Requirements / Admin Enforcement (`requirements.toml`)

Admin-only overrides using the same config path structure but under:
- Unix: `/etc/codex/requirements.toml`
- Windows: `%ProgramData%\OpenAI\Codex\requirements.toml`

Set `allow_managed_hooks_only = true` in `requirements.toml` to block user/project hooks
while keeping managed (admin) hooks active.

## Project-Local Config Denylist

These fields are ignored in cwd/tree/repo config layers for security:
`openai_base_url`, `chatgpt_base_url`, `apps_mcp_product_sku`, `model_provider`,
`model_providers`, `notify`, `profile`, `profiles`, `otel`,
`experimental_realtime_webrtc_call_base_url`, `experimental_realtime_ws_base_url`

## Trust

Project configs from untrusted directories are loaded but not applied.
Set trust explicitly:
```toml
# .codex/config.toml in the project
trust_level = "trusted"   # or "untrusted"
```

Or via CLI: `--trust` flag.

## Config Schema

JSON schema available at: `codex-rs/core/config.schema.json`
Regenerate with: `just write-config-schema` (from `codex-rs/`)
