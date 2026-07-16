# Scripts

Shared helper scripts for the `tdx` plugin live here.

Use this directory for utilities that are reused across multiple skills. Keep
skill-specific helpers next to the skill unless they are reused elsewhere.

## Current Scripts

- `branch-context.sh`: summarize branch/base context before shipping a PR
- `commit-context.sh`: summarize repository instructions and changes before
  committing
- `task_add.js`: append a new task to `.agent/tasks.md`
- `task_get.js`: print the first pending task
- `task_complete.js`: mark the first pending task complete or blocked
- `task_archive.js`: archive a fully completed task file
