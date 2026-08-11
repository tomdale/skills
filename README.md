# tdx

My personal agent skills and lightweight workflow helpers. These are written for my own workflow and public by default — you're welcome to reuse them, but I make no promises they fit yours.

## Skills

- [abstraction-boundaries](skills/abstraction-boundaries/SKILL.md) — Find APIs and module boundaries operating at the wrong level of abstraction and refactor them into a cleaner shape.
- [commit](skills/commit/SKILL.md) — Commit the current work as one coherent change, or propose logical groups when the tree contains unrelated changes.
- [cruft](skills/cruft/SKILL.md) — Audit a codebase for low-value compatibility code, stale defensive layers, and glue that no longer has a real consumer.
- [documentation-comments](skills/documentation-comments/SKILL.md) — Write or review documentation comments that explain intent names and types can't express.
- [exec-summarizer](skills/exec-summarizer/SKILL.md) — Summarize technical material for an executive reader who wants substance with minimal overhead.
- [fix-pr-checks](skills/fix-pr-checks/SKILL.md) — Diagnose and fix failing GitHub PR checks for the current branch.
- [interactive-shell](skills/interactive-shell/SKILL.md) — Interact with programs that require a real terminal or PTY, like REPLs and prompt-driven CLIs.
- [iterm2-python-api](skills/iterm2-python-api/SKILL.md) — Write and debug iTerm2 Python automation scripts for windows, tabs, sessions, and event handlers.
- [lawyerify](skills/lawyerify/SKILL.md) — Generate a lawyer-oriented Word document overview of the current PR for legal or compliance review.
- [minify-prompt](skills/minify-prompt/SKILL.md) — Compress agent memory and instruction files (CLAUDE.md, SKILL.md, system prompts) for maximum information density.
- [narrative](skills/narrative/SKILL.md) — Turn the current branch's diff into narrative prose suitable for a PR description or comment.
- [pr-feedback](skills/pr-feedback/SKILL.md) — Draft and post GitHub PR review feedback with user approval at each step.
- [recap](skills/recap/SKILL.md) — Summarize prior Codex work for a directory from local session transcripts.
- [refactoring](skills/refactoring/SKILL.md) — Aggressively refactor TypeScript codebases toward a greenfield-quality module layout.
- [ship-pr](skills/ship-pr/SKILL.md) — Branch, commit, push, and open a GitHub pull request for the current work.
- [tui-development](skills/tui-development/SKILL.md) — Build, test, and debug terminal user interfaces.
- [walkthrough](skills/walkthrough/SKILL.md) — Guide a reviewer through a checked-out PR by grouping the diff into conceptual units.

## Install

### Individual skills (any agent)

Use [skills](https://github.com/vercel-labs/skills) to install only the skills you want — it supports Claude Code, Codex, Pi, Cursor, and more:

```sh
# List available skills
npx skills add tomdale/skills -l

# Install specific skills
npx skills add tomdale/skills -s refactoring -s ship-pr

# Install globally instead of project-level, for specific agents
npx skills add tomdale/skills -s refactoring -g -a claude-code -a codex
```

Or symlink a skill directory into your agent's skills path manually:

```sh
ln -s "$PWD/skills/refactoring" ~/.agents/skills/refactoring
```

### Claude Code (all skills)

```sh
/plugin marketplace add tomdale/skills
/plugin install tdx
```

### Codex (all skills)

```sh
codex plugin marketplace add tomdale/skills
codex plugin add tdx@skills
```

### Pi (all skills)

```sh
pi install git:github.com/tomdale/skills
```
