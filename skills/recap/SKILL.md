---
name: recap
description: Summarize prior work by Claude Code, Codex, and Pi for the current directory and its child directories. Use when the user asks to recap, summarize, reconstruct, review, or understand what work has happened in a repo or directory.
---

# Recap

Summarize prior agent work in the current directory tree. Cover Claude Code,
Codex, and Pi sessions; do not limit the recap to one harness.

## Workflow

1. Use Memex when it is installed. It indexes Claude Code, Codex, and Pi
   transcripts behind one session/search interface and preserves source and
   working-directory metadata.

   Refresh the index incrementally, without embeddings unless semantic search
   is needed:

   ```bash
   memex index --no-embeddings
   ```

   Memex honors `CLAUDE_CONFIG_DIR` for Claude Code history. If the history
   tree contains projects that should never enter the local index, configure
   `exclude_paths` in `~/.memex/config.toml` or use repeatable `--exclude`
   globs for a one-off refresh:

   ```bash
   memex index --no-embeddings --exclude '~/path/to/private/**'
   ```

   Find sessions associated with the current repository:

   ```bash
   memex sessions --cwd . --limit 100 --json-array
   ```

   The results include `source`, `session_id`, `cwd`, `git_root`, timestamps,
   message counts, and a resume command. Group sessions by source and project,
   then fetch promising sessions with:

   ```bash
   memex session <session_id>
   ```

   Use `memex search` for focused follow-up searches. Prefer exact or hybrid
   searches and constrain them to this project or a selected session:

   ```bash
   memex search "query" --cwd . --limit 20
   memex search "query" --session <session_id> --sort ts --limit 50
   ```

   Use `--source claude`, `--source codex`, or `--source pi` when comparing a
   particular harness. Use `--role assistant` to find narrative outcomes and
   `--role tool_result` to investigate command failures. Add `--include-agents`
   to indexing when Claude Code subagent work is relevant. Memex 0.13.0 also
   supports newer sources such as Grok and modern OpenCode SQLite transcripts;
   include them only when they are relevant to the requested recap.

2. If Memex is unavailable or does not contain the needed history, use the
   bundled fallback for Codex and Pi transcripts:

   ```bash
   /path/to/this/skill/scripts/codex-session-recap --excerpt
   ```

   Resolve the script path relative to this skill directory. The fallback
   scans `${CODEX_HOME:-$HOME/.codex}/sessions` for Codex rollout JSONL files
   and `${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}/sessions` for Pi JSONL files.
   It includes sessions whose recorded cwd is the current directory or a child
   directory. It does not cover Claude Code.

3. Read the returned session records or digests and produce a concise recap.
   Group related sessions by theme or project area rather than dumping a
   chronological transcript. Prefer concrete outcomes, files changed,
   commands, decisions, and unresolved work. Identify the harness when it
   matters, and mention uncertainty when excerpts are incomplete.

## Important details

- Do not assume an indexed session belongs to this checkout solely because its
  project name matches. Confirm its `cwd` or `git_root` matches the current
  directory or a descendant.
- Avoid exposing transcript secrets, credentials, tokens, private keys, or
  other sensitive session material in the recap.
- Use session paths or resume commands only when they help the user follow up.
- Memex supports more sources than this skill requires; at minimum, include
  Claude Code, Codex, and Pi in the recap.
- Memex 0.11+ excludes transcript paths at discovery time, before content is
  indexed. Prefer `exclude_paths` for durable trust boundaries rather than
  trying to filter sensitive content after indexing.
