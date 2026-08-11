# Codex CLI Hooks Reference

Source: `codex-rs/config/src/hook_config.rs`
Verified: installed `codex-cli 0.144.4` and current first-party source/docs available at review time

## Hook Events

| Event | When it fires |
|-------|--------------|
| `SessionStart` | Once when a new Codex session begins |
| `UserPromptSubmit` | Each time the user submits a prompt |
| `PreToolUse` | Before any tool call is executed |
| `PermissionRequest` | When Codex requests a permission |
| `PostToolUse` | After any tool call completes |
| `PreCompact` | Before conversation history compaction |
| `PostCompact` | After conversation history compaction |
| `SubagentStart` | When a subagent session starts |
| `SubagentStop` | When a subagent session ends |
| `Stop` | When the session ends |

## TOML Format

Hooks can be configured inline in `~/.codex/config.toml` or in a separate `hooks.toml` file.
Plugin-contributed hooks live in the plugin package.

### Inline in config.toml

```toml
[hooks.PreToolUse]
[[hooks.PreToolUse.matchers]]
# Each event key contains a list of MatcherGroups

[hooks.PostToolUse]
[[hooks.PostToolUse.matchers]]
```

### Separate hooks.toml File

```toml
description = "My project hooks"

[hooks.SessionStart]
# ...

[hooks.state]
# Per-hook state tracking (enabled/trusted_hash)
[hooks.state.my-hook]
enabled = true
trusted_hash = "sha256-abc123..."
```

## MatcherGroup Structure

The hook config uses `MatcherGroup` arrays under each event key. The exact matcher
structure is defined in `codex-rs/config/src/hook_config.rs`.

## Admin Enforcement

Set in `requirements.toml` (admin layer only):
```toml
allow_managed_hooks_only = true
```

When set, user/project/session hook configs are ignored. Only hooks from `requirements.toml`
and other managed config layers remain active. This setting is only effective in
`requirements.toml`; placing it in `config.toml` has no effect.

## Plugin Hooks

Plugins declare hooks in their manifest under `paths.hooks`:
```json
{
  "paths": {
    "hooks": ["hooks/session.toml", "hooks/tool-use.toml"]
  }
}
```

Or inline in the manifest:
```json
{
  "paths": {
    "hooks": [{ "description": "...", "hooks": { "PreToolUse": [...] } }]
  }
}
```

## Hook State

Hooks can have per-instance state stored in config for trust verification:
```toml
[hooks.state.my-hook-id]
enabled = true
trusted_hash = "sha256-..."   # fingerprint for change detection
```

## Hook Source in PluginHookSource

When loaded, hook sources carry:
- `plugin_id` — the owning plugin
- `plugin_root` — filesystem root of the plugin
- `plugin_data_root` — data directory for the plugin
- `source_path` — absolute path to the hook file
- `source_relative_path` — relative path within plugin
- `hooks` — parsed `HookEventsToml`
