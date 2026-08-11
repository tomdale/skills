# Codex CLI Skills Reference

Source: `codex-rs/core-skills/src/`, `codex-rs/skills/src/`
Verified: installed `codex-cli 0.144.4` and current first-party source/docs available at review time

## Anatomy of a Skill

```
my-skill/
  SKILL.md              # required
  agents/
    openai.yaml         # UI metadata (optional but recommended)
  scripts/              # executable helpers (Python, Bash, Node, etc.)
  references/           # docs loaded on demand, not eagerly
  assets/               # templates, icons, static files
```

## SKILL.md Format

### Frontmatter (YAML)

```yaml
---
name: my-skill             # required, ≤64 chars, lowercase-hyphenated
description: |             # required, ≤1024 chars
  What the skill does AND when to use it. Both belong here.
  The body is only loaded after the skill triggers, so put all
  trigger conditions and "when to use" context in description.
  Short-description is in metadata, not displayed to user by default.
metadata:
  short-description: "One-liner for UI chips"  # optional, ≤1024 chars
---
```

Only `name` and `description` are read by Codex to decide whether to trigger a skill.
Do not put trigger conditions only in the body—they will not be seen before triggering.

### Body (Markdown)

Free-form Markdown instructions. Loaded completely once the skill is invoked.
Keep concise; context window is shared with everything else in the session.

### Field Limits

| Field | Max |
|-------|-----|
| `name` | 64 chars |
| qualified name (with namespace) | 128 chars |
| `description` | 1024 chars |
| `short-description` | 1024 chars |
| `default_prompt` (agents/openai.yaml) | 1024 chars |

## agents/openai.yaml (UI Metadata)

```yaml
interface:
  display_name: "Human-Readable Name"
  short_description: "One-liner for skill chips/lists."
  default_prompt: "What should happen when skill is activated."
  icon_small: "assets/icon-small.png"
  icon_large: "assets/icon-large.png"
  brand_color: "#FF6600"

dependencies:
  tools:
    - type: "mcp"
      value: "my-mcp-server"
      description: "Required MCP server"
      transport: "stdio"
      command: "npx -y @org/mcp-server"

policy:
  allow_implicit_invocation: true   # default true
  products: []                      # restrict to specific products
```

Generate/update with the `skill-creator` bundled skill or:
```bash
scripts/generate_openai_yaml.py <path/to/skill-folder> \
  --interface display_name="My Skill" \
  --interface short_description="Brief description"
```

## Skill Discovery

Discovery happens per-session (cached by CWD). Codex walks each root concurrently
(up to 8 root scans simultaneously, 32 skill loads per root at a time, max 2,000
dirs per root). Hidden directories are skipped.

### Discovery Roots (full detail)

1. **Repo (`.codex/skills/`)** — at git project root; requires trusted directory.
2. **Repo (`.agents/skills/`)** — in each dir between CWD and project root (walks upward).
3. **User (`$HOME/.agents/skills/`)** — preferred cross-harness user skills location.
4. **User (`$CODEX_HOME/skills/`)** — deprecated but still scanned for backward compat.
5. **System (`$CODEX_HOME/skills/.system/`)** — extracted from binary at startup.
6. **Admin (`/etc/codex/skills/`)** — admin-managed.
7. **Plugin-contributed roots** — added at User scope when plugins are installed.

On this machine: `$HOME/.agents/skills/` is symlinked from `~/.pi/agent/skills/`.

### Namespace Resolution

When multiple roots contain skills with the same name, skills are namespaced with a
plugin-prefix or root-based qualifier. The qualified name is used in invocation.

## Context Budget

```
DEFAULT_SKILL_METADATA_CHAR_BUDGET = 8,000 chars
SKILL_METADATA_CONTEXT_WINDOW_PERCENT = 2%
MAX_DEFAULT_CONTEXT_SKILL_DESCRIPTION_CHARS = 1,024 chars
```

If total name+description text exceeds budget:
1. Descriptions are truncated to fit (with `...` suffix).
2. If still over budget, all descriptions are removed.
3. A warning is injected: "Skill descriptions were shortened..."

Mitigation: disable unused skills via `[[skills.config]]` entries.

## Invocation Triggers

1. **Explicit mention**: user writes `$SkillName` or plain text matching the name.
2. **Description match**: task clearly matches description (model decides).
3. **Implicit invocation**: running a script from `scripts/` dir (detected by command parse).

Skills are **not** carried across turns unless re-mentioned. Multiple matching skills
can be used in one turn; model chooses minimal covering set.

## How Skills Are Read (Progressive Disclosure)

1. At session start, Codex injects skill names + descriptions into context.
2. When a skill triggers, the model reads `SKILL.md` fully before acting.
3. The model then reads referenced files (`references/`, `scripts/`) as needed per instructions.
4. Subagents may perform task work, but the main agent must read skill instructions itself.

## Creating a Skill with the Bundled `skill-creator`

The bundled `skill-creator` system skill guides skill creation. Invoke it in Codex:
> "Create a new skill for [topic]" — Codex will invoke `skill-creator` automatically.

Or manually:
```bash
python3 "$CODEX_HOME/skills/.system/skill-creator/scripts/init_skill.py" \
  --name my-skill \
  --description "What it does and when to use it" \
  /path/to/skills/dir
```

## Validating a Skill

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py ./my-skill/
```

Checks: YAML frontmatter format, required fields, name length rules.

For a repo-local smoke test, place the skill under `.agents/skills/<name>/` or `.codex/skills/<name>/` and run `codex exec` normally.

## Bundled System Skills (verify against the installed version)

Extracted to `$CODEX_HOME/skills/.system/` at startup:
- `skill-creator` — guide for creating skills
- `skill-installer` — installs skills from remote sources
- `plugin-creator` — guide for creating plugins
- `review-agent` — code review workflows
- `openai-docs` — queries OpenAI documentation
- `imagegen` — image generation workflows

Disable with: `[skills.bundled] enabled = false` in `~/.codex/config.toml`.
