# Codex MCP Reference

Source: `codex-rs/config/src/mcp_types.rs`, `codex-rs/cli/src/mcp_cmd.rs`, `codex-rs/codex-mcp/`
Verified: installed `codex-cli 0.144.4` and current first-party source/docs available at review time

## CLI Commands

```bash
# Add a stdio MCP server
codex mcp add <name> -- <command> [args...]
codex mcp add my-server -- npx -y @org/mcp-server

# Add an HTTP/SSE server
codex mcp add <name> --url <url>
codex mcp add my-server --url https://example.com/mcp

# List configured servers
codex mcp list [--json]

# Show a single server
codex mcp get <name> [--json]

# Remove a server
codex mcp remove <name>

# OAuth authentication
codex mcp login <name>
codex mcp logout <name>
```

## Config TOML Structure

### Stdio Transport

```toml
[mcp_servers.my-server]
command = "npx"
args = ["-y", "@org/mcp-package"]

# Optional environment variables
[mcp_servers.my-server.env]
MY_VAR = "value"
SECRET_TOKEN = { name = "MY_TOKEN", source = "local" }   # from local env
REMOTE_VAR = { name = "REMOTE_TOKEN", source = "remote" } # from remote env

# Optional settings
timeout_ms = 30000        # connection timeout
environment_id = "local"  # default "local"; for remote exec environments
```

### HTTP / SSE Transport

```toml
[mcp_servers.remote-server]
url = "https://example.com/mcp"
```

### OAuth Authentication

```toml
[mcp_servers.oauth-server]
url = "https://example.com/mcp"

[mcp_servers.oauth-server.auth.oauth]
client_id = "your-client-id"
```

OAuth tokens stored in system keyring. Use `codex mcp login` / `codex mcp logout` to manage.

### Per-Tool Approval

```toml
[mcp_servers.my-server]
command = "npx"
args = ["-y", "@org/mcp-package"]
approval_mode = "auto"    # default; auto-approve safe calls

# Per-tool overrides
[mcp_servers.my-server.tools.dangerous-tool]
approval_mode = "approve"  # always require user approval
```

**Approval modes:**

| Mode | Behavior |
|------|----------|
| `auto` | Approve automatically (default) |
| `prompt` | Ask user before every call |
| `writes` | Ask user only for write operations |
| `approve` | Always require user approval |

## Env Var Sources

- `source = "local"` (default): pass through from local shell environment
- `source = "remote"`: inject from remote execution environment

## Codex as MCP Server

Run Codex as an MCP server that other clients can connect to:
```bash
codex mcp-server    # stdio transport
```

This exposes Codex's agent capabilities as MCP tools to the connecting client.

## Plugin-Contributed MCP Servers

Plugins can declare MCP servers in their manifest. These are automatically added
to the active server set when the plugin is enabled. Override approval mode:

```toml
[plugins.my-plugin.mcp_servers.server-name]
approval_mode = "prompt"
```

## Limits & Caveats

- MCP connection manager handles reconnection and tool state mutation.
- Prefer using `codex-rs/codex-mcp/src/mcp_connection_manager.rs` abstractions
  when working on MCP tool calls in the codebase.
- OAuth callback port configurable: `mcp_oauth_callback_port` in config.
- OAuth callback URL configurable: `mcp_oauth_callback_url` in config.
- Credential storage mode: `mcp_oauth_credentials_store` (keyring backend).
