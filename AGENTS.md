# Repository Guidance

## Skills and extensions: choose the correct location

This repository contains both distributable plugin skills and repo-local development skills. Keep them separate.

### `skills/` — plugin-distributed skills

Put a skill under `skills/<name>/SKILL.md` when it is part of the `tdx` plugin and should be distributed through the Codex or Claude Code plugin manifests.

Use this location for:

- Personal workflow skills intended to be loaded by the installed plugin.
- Skills that are complete enough to be part of the plugin's public surface.
- Supporting references, scripts, and assets that the distributable skill needs.

Requirements:

- Keep the skill self-contained and reusable outside this checkout where practical.
- Use lowercase, hyphenated directory names.
- Update plugin metadata or documentation only when the plugin's distributable contents actually change.
- Do not put harness-specific authoring notes here unless they are themselves an intentional plugin feature.

The plugin manifests point at this directory. Anything added here may become part of the plugin's installed surface.

### `.agents/skills/` — repo-local development skills

Put a skill under `.agents/skills/<name>/SKILL.md` when it is supporting work performed in this repository and must not be included in the `tdx` plugin.

Use this location for:

- Guides for developing Codex CLI, Claude Code CLI, Pi, or other harness integrations.
- Repository-maintenance instructions and local engineering workflows.
- Comparative or experimental skills that are useful to contributors but are not plugin features.
- Harness-specific references, API notes, and compatibility research.

These skills are discovered as repo-local skills by harnesses that support `.agents/skills/`, but they are intentionally excluded from `skills/` and must not be added to the plugin manifests merely because they exist here.

### Other locations

- `.codex-plugin/`: Codex plugin metadata only; do not place skill bodies here.
- `.claude-plugin/`: Claude Code plugin metadata only; do not place skill bodies here.
- `.agents/plugins/`: Codex marketplace metadata only.
- `scripts/`: shared executable helpers used by multiple skills; a helper needed only by one skill may live in that skill's `scripts/` directory.

## Decision rule

Before creating a skill, ask:

1. Is this a capability users should receive when they install the `tdx` plugin?
   - Yes: use `skills/`.
2. Is this guidance for contributors developing, testing, or comparing agent harnesses in this repository?
   - Yes: use `.agents/skills/`.
3. Is it both?
   - Keep the portable user-facing capability in `skills/` and put harness-specific development guidance in `.agents/skills/`. Do not duplicate content without a clear reason; link conceptually through references where appropriate.

When moving a skill between locations, check the plugin manifests and `skills/README.md` so repo-local material does not accidentally become distributable—or vice versa.
