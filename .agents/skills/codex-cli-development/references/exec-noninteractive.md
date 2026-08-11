# Codex CLI Non-Interactive (Exec) Mode

Source: `codex-rs/cli/src/main.rs`, `codex-rs/exec/`, `codex-rs/exec-server/`
Docs: [developers.openai.com/codex/noninteractive](https://developers.openai.com/codex/noninteractive) (browser required)
Verified: installed `codex-cli 0.144.4` and current first-party source/docs available at review time

## Basic Usage

```bash
# Run a prompt non-interactively (short alias: e)
codex exec "Fix the failing tests in src/"
codex e "Refactor auth.ts to use async/await"

# With approval policy
codex exec --approval-policy untrusted "Generate unit tests for utils.ts"
codex exec --approval-policy danger-full-access "Run the full test suite and fix failures"

# With a specific model
codex exec --model o4-mini "Summarize the recent git log"

# Pipe input
echo "What does this function do?" | codex exec --stdin

# With working directory
codex exec --cwd /path/to/project "Add a README"
```

## Code Review (Non-Interactive)

```bash
codex review
codex review --model o4-mini
```

Runs a structured code review on the current branch diff.
Configured with `review_model` in `config.toml`.

## Key CLI Flags for exec

| Flag | Description |
|------|-------------|
| `--approval-policy` | Override approval policy: `untrusted` \| `on-request` \| `danger-full-access` |
| `--model` | Override model selection |
| `--cwd` | Set working directory |
| `--config` | Inline config key=value overrides |
| `--profile` | Use a named config profile |
| `--stdin` | Read additional input from stdin |
| `--json` | Output events as JSON (for scripting) |

## Exec Policy in Non-Interactive Mode

Non-interactive sessions use the same exec policy as interactive sessions.
Test your policy before running:
```bash
codex execpolicy check "git diff HEAD~1"
```

Set a more permissive policy for automation:
```bash
# In ~/.codex/config.toml or a profile:
approval_policy = "danger-full-access"
sandbox_mode = "workspace-write"
```

Or via profile:
```bash
codex exec --profile ci "Run tests and fix linting errors"
```

Profile config: `~/.codex/ci.config.toml`

## Scripting / JSON Output

```bash
codex exec --json "List all TODO comments" | jq .
```

JSON output streams structured event objects. Pipe to `jq` for filtering.

## Session Resume in Non-Interactive Mode

```bash
# Resume last session
codex exec --resume last "Continue from where you left off"

# Resume specific session
codex exec --resume <session-id> "Continue"
```

## Environment

Non-interactive exec inherits the caller's shell environment unless `shell_environment_policy`
in config restricts it. The sandbox (`CODEX_SANDBOX_NETWORK_DISABLED`, `CODEX_SANDBOX`) env
vars are set inside sandboxed tool calls just as in interactive mode.

## Caveats

- `codex exec` is the primary entrypoint for CI/scripting use cases.
- Approval policy defaults to `on-request` which may pause for human input in automation;
  use `--approval-policy untrusted` or `danger-full-access` for truly headless runs.
- Output format (`--json`) is useful for machine consumption but evolves with releases.
- Some interactive features (session picker, TUI rendering) are unavailable in exec mode.
