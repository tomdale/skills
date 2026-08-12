# review-agent-changes

A quality gate for a batch of agent-generated changes **before you ship it**. It
is an audit of the implementation an agent just produced — not a GitHub PR
review, and not a review of someone else's committed work.

This README is a user guide. The agent-facing instructions live in
[SKILL.md](SKILL.md); the per-topic contracts live in
[lenses/](lenses/). If you are choosing whether to run this skill, read on.

## When to use it

Run this before shipping agent-produced implementation work. It is worth it when
you want a second, systematic pass for:

- behavioral and regression risk, not just "does the test pass"
- tests that only prove the absence of a removed API or mock the wrong layer
- unshipped "compatibility shims" the agent keeps alive for a shape it invented
  earlier in the same session and never merged
- readability and house style vs. the repository's own conventions (not taste)
- safety concerns: destructive ops, security, privacy, concurrency, rollout

Typical invocations:

- "audit these agent-generated changes"
- "review the implementation before shipping"
- "run a change audit on the current branch"
- "look for issues in the current changes before I merge"

**Not** for drafting or posting GitHub review feedback — use the `pr-feedback`
skill for that. And by default the audit never edits your files; only apply
fixes if you explicitly ask.

## What it does

1. **Establishes the comparison.** It resolves a base revision (preferring the
   merge base or default branch) and tells you in the result what it compared.
2. **Reads context.** Repository guidance (`AGENTS.md`, `CLAUDE.md`,
   contribution guides, design-system/CLI-UX docs) plus the complete diff and
   nearby unchanged code, so findings use real local precedent rather than
   generic best practice.
3. **Selects lenses.** It runs the core lenses on any substantive change and
   adds specialist lenses only where the diff has a real target — it will not
   run a lens just because one exists.
4. **Dispatches and synthesizes.** Independent lenses run in parallel when
   subagents are available; overlapping findings are deduplicated, speculative
   ones rejected, and the survivors are reported as **High / Medium / Low**
   priorities.
5. **Reports clean lenses** explicitly, separates required fixes from optional
   follow-ups, and says plainly when the audit found nothing — it will not
   manufacture nits.

## The lenses

Core lenses run on any substantive implementation change:

- **Behavior and regression risk** — traces changed behavior through real
  callers, error paths, and state transitions.
- **Readability and house style** — naming, layering, utilities, output, and
  abstractions measured against local precedent, not taste.
- **Tests and validation** — distinguishes behavioral coverage from mock-only or
  implementation-detail tests; checks negative paths.
- **Change scope** — the diff is coherent, complete, and free of unrelated churn
  or abandoned work.
- **Documentation and durable context** — flags text that preserves
  implementation-session details instead of durable runtime or architectural
  context.
- **Compatibility and cruft** — removes shims protecting unshipped intermediate
  shapes rather than real consumers.

The specialist lenses are switched on only when the diff touches their domain:
**CLI UX and machine output**, **data safety**, **dependency
boundaries**, **API contracts**, **concurrency and idempotency**, **security and
secrets**, **data policy**, **observability**, **accessibility
and interaction design**, **performance and resource use**, and **configuration
and rollout safety**.

Overlapping lenses are bundled into one reviewer so a finding is reported
exactly once — `data-safety` and `data-policy` are split by action guardrails vs.
retention/privacy policy, and `compatibility` decides whether an unshipped shim
deserves to exist.

## What you get out

A consolidated report that starts with the base/head comparison and selected
lenses, then lists findings by priority. Each finding includes:

- priority and `path:line`
- a concise title
- concrete evidence and the repository precedent it rests on
- impact on this implementation
- the smallest remedy that preserves the intended change

It ends with the clean lenses, validation already observed (and what is still
recommended), and optional follow-ups.

## What makes it trustworthy

The skill is deliberately conservative about inventing problems. Findings must
be **traceable to the diff and a real consumer or contract**; generic
best-practice claims with no local precedent, and findings contradicted by an
intentional requirement, are rejected in synthesis. A document-only change gets
documentation and change-scope lenses, not a mechanical pass through concurrency
and performance. A clean result is a valid and expected outcome.
