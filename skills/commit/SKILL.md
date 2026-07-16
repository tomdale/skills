---
name: commit
description:
  Commit the current work using a repository-aware Git workflow. Automatically
  creates one commit for a coherent change or proposes confirmed logical groups
  when the working tree contains unrelated changes. Use when asked to commit,
  stage and commit, save work, or create commits.
---

Commit the current work without pushing. Read and follow the applicable
repository and project instructions before making any Git decision. Local
`AGENTS.md`, `CLAUDE.md`, and other project-specific instructions override this
skill, including branch, staging, signing, hook, and commit-agent policies.

## Use a Git worker when available

When the harness provides subagents, use one for repository inspection and Git
execution so the primary conversation receives a compact result instead of
large status, diff, and command transcripts. First resolve and run the bundled
`../../scripts/commit-context.sh` relative to this skill directory in one tool
call, passing the target repository path when needed. Define the worker just in
time from the adjacent `code-committer.md` reference. Use the harness's native
subagent mechanism; the reference defines the worker's responsibilities and
return contract, not harness-specific invocation syntax.

If no subagent facility is available, perform the same workflow directly.

## Workflow

1. Inspect the working tree, index, untracked files, current branch, recent
   commit style, and applicable local instructions.
2. Stop if there is nothing to commit.
3. Decide whether all requested changes are one coherent logical change.
4. If they are coherent, execute one commit.
5. If they are unrelated:
   - Return a concise proposed grouping with files and rationale.
   - Ask the user to confirm or adjust it before changing the index.
   - After confirmation, execute one commit per approved group.
6. For each commit, stage only files or hunks belonging to that group. Never
   use broad staging such as `git add .`, `git add -A`, or `git commit -am`.
7. Follow repository commit conventions. Otherwise use a concise Conventional
   Commit subject in imperative mood, no longer than 72 characters, and explain
   intent rather than implementation trivia in the body.
8. Keep staged and unstaged changes that are outside the approved group intact.
   Isolate each subsequent group carefully rather than assuming the index is
   clean.
9. Do not push, amend existing commits, or modify files as part of commit work
   unless local instructions or the user explicitly require it.
10. Return only a compact summary: outcome, commit SHA and subject for each
    commit, final working-tree status, and concise errors or ambiguities.

When a worker reports an ambiguity, conflict, or grouping proposal, bring only
that concise information to the user. Do not reproduce raw Git output unless
needed to explain a failure.
