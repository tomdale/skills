# Codex CLI Plugin Reference

Source: `codex-rs/plugin/src/manifest.rs`, `codex-rs/cli/src/plugin_cmd.rs`, `codex-rs/core-plugins/`
Verified: installed `codex-cli 0.144.4` and current first-party source/docs available at review time

## CLI Commands

```bash
# Install a plugin
codex plugin add <plugin>@<marketplace>
codex plugin add sample@openai-bundled
codex plugin add sample --marketplace openai-bundled

# List installed / available plugins
codex plugin list [--json]
codex plugin list --available [--marketplace <name>] [--json]

# Remove a plugin
codex plugin remove <plugin>[@<marketplace>]

# Marketplace management
codex plugin marketplace list
codex plugin marketplace add <name> <url-or-path>
codex plugin marketplace remove <name>
codex plugin marketplace refresh [<name>]
```

## Plugin Manifest Structure

A plugin package contains a manifest file (parsed by Codex at install time):

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does.",
  "keywords": ["tag1", "tag2"],
  "paths": {
    "skills": ["skills/my-skill/"],
    "mcp_servers": "mcp-servers.json",
    "apps": "apps.json",
    "hooks": ["hooks/pre-tool.toml"]
  },
  "interface": {
    "display_name": "My Plugin",
    "short_description": "Brief description for the marketplace.",
    "long_description": "Full description shown on plugin detail page.",
    "developer_name": "ACME Corp",
    "category": "productivity",
    "capabilities": ["skills", "mcp"],
    "website_url": "https://example.com",
    "privacy_policy_url": "https://example.com/privacy",
    "terms_of_service_url": "https://example.com/tos",
    "default_prompt": ["What the plugin does when activated."],
    "brand_color": "#FF6600",
    "composer_icon": "assets/icon.png",
    "logo": "assets/logo.png",
    "logo_dark": "assets/logo-dark.png",
    "screenshots": ["assets/screenshot1.png"]
  }
}
```

`paths.skills` is a list of paths to skill directories within the plugin package.
`paths.mcp_servers` can be a path to a JSON file or an inline JSON string.

## Plugin Config in `~/.codex/config.toml`

```toml
# Enable/disable a plugin
[plugins.my-plugin]
enabled = true

# Override MCP server approval for a plugin's MCP server
[plugins.my-plugin.mcp_servers.some-server]
approval_mode = "prompt"
```

## Marketplaces

Plugins are installed from marketplaces (Git repos or local dirs with a marketplace manifest).
Default marketplace: `openai-bundled` (bundled with Codex binary).

Marketplace install root: `$CODEX_HOME/marketplaces/<marketplace-name>/`.
Plugin install root: `$CODEX_HOME/plugins/<marketplace-name>/<plugin-name>/`.

```toml
[marketplaces.openai-bundled]
last_updated = "2025-01-01T00:00:00Z"
last_revision = "abc123def456"
```

## Plugin Capabilities

A plugin can contribute any combination of:
- **Skills** — `SKILL.md` files injected into Codex's skill discovery
- **MCP Servers** — MCP servers automatically started with sessions
- **Apps** — App connector declarations for the ChatGPT apps system
- **Hooks** — Lifecycle event hooks (PreToolUse, PostToolUse, etc.)

## Creating a Plugin

Use the bundled `plugin-creator` system skill:
> "Create a new plugin for [topic]"

Plugin packages are typically distributed as Git repositories or npm packages.
The `codex plugin marketplace add` command registers a marketplace source.

## Plugin ID Format

Plugin identifiers follow `<segment>` rules (lowercase, alphanumeric, hyphens).
Full plugin references use `<plugin>@<marketplace>` syntax.
`validate_plugin_segment()` in `codex-rs/plugin/src/plugin_id.rs` enforces naming rules.

## Caveats

- Plugin installation requires ChatGPT account auth for the default marketplace.
- Validate plugin subcommands and flags with `codex plugin --help` and the relevant subcommand's `--help`; plugin behavior is version-sensitive.
- Plugin resources are authority-bound; skills and MCP servers resolve within the plugin package root.
- Requirements layer (`requirements.toml`) can restrict which marketplace sources are allowed.
- Use `codex doctor` to diagnose plugin install issues.
