# tdx

Tom Dale's personal agent skills and lightweight workflow helpers.

This repository is personal-first and public by default. The skills are written
for Tom's workflow, but they are kept reusable on a best-effort basis when that
does not make the local workflow worse.

## Layout

- `.codex-plugin/plugin.json`: Codex plugin manifest
- `.claude-plugin/plugin.json`: Claude Code plugin manifest
- `.agents/plugins/marketplace.json`: Codex marketplace entry for this checkout
- `skills/`: personal skills, one directory per skill with a `SKILL.md`
- `scripts/`: shared helper scripts used by multiple skills

## Bundled Skills

- `abstraction-boundaries`: identify and improve weak module boundaries
- `interactive-shell`: run REPLs and prompt-driven CLIs safely
- `tui-development`: build and verify terminal UIs
- `benchmarking`: measure and improve performance methodically
- `cruft`: audit low-value compatibility and glue code
- `documentation-comments`: write and review useful code comments
- `fix-pr-checks`: diagnose and repair failing GitHub PR checks
- `tasks` and `write-task`: manage a portable markdown task queue
- `iterm2-python-api`: write and debug iTerm2 Python scripts
- `exec-summarizer`: compress technical output for executive readers
- `lawyerify`: draft legal-review-oriented PR summaries
- `minify-prompt`: rewrite instruction-heavy files for lower token cost without
  losing meaning
- `narrative`: write PR narratives from branch diffs
- `pr-feedback`: draft GitHub PR review feedback
- `recap`: summarize prior Codex work from local session transcripts
- `refactoring`: redesign TypeScript code toward a greenfield-quality module
  layout, with aggressive decomposition of monolithic files
- `ship-pr`: stage, commit, push, and open a GitHub pull request, using the
  `narrative` skill to draft the PR description
- `walkthrough`: guide reviewers through a checked-out PR

## Notes

The plugin intentionally avoids carrying local-only Codex, Claude, or MCP
configuration. Dotfiles or machine setup should point tools at this checkout and
own local services such as MCP servers.

## Adding A Skill

Create a new directory under `skills/` and add a `SKILL.md` file:

```text
skills/
  my-skill/
    SKILL.md
```

Keep skill names lowercase and hyphenated so they stay consistent with the
rest of the Codex skill ecosystem.
