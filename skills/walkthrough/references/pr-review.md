# PR review mode

Read this reference before starting whenever the user asks for a PR review or
GitHub pull request review, asks to prepare or post review feedback, mentions
inline review comments, author questions, a PR URL or number, or the checkout
metadata identifies an active GitHub PR.

## Entry requirements

PR review mode is an intended outcome, not just a tone. Before beginning the
walkthrough, establish whether there is a viable review target:

- an active PR associated with the checkout;
- a PR URL or number supplied by the user; or
- enough repository metadata to identify the target.

If the user asks for a PR review but no target is available, do not begin a
long walkthrough silently. Explain that you can continue by preparing standalone
feedback, but cannot attach or post it automatically. Ask the user to choose:

1. switch to the local workflow; or
2. continue in PR review mode and prepare a draft for later use.

If the user chooses PR review mode without a target, state the limitation again
briefly and continue only with the user's confirmation.

If the directory is not a Git repository and the user has not supplied a PR,
patch, or comparison baseline, ask for one before claiming to review changes.

Explicit user intent wins over repository state. If the user asks for a local,
self, or agent review, use the local workflow even when the branch also has an
open PR. If the user asks for a PR review, use this mode after the target check.
If there is no explicit intent, an active PR selects this mode; otherwise use the
local workflow.

## First-load tutorial

Use the PR variant of the first-load tutorial. Print the ASCII banner, explain
that the session will group the diff, outline the order, narrate one group at a
time, and pause after each group. Tell the user that captures go to
`.agent/review-notes.md` and that questions and comments will be turned into a
draft review at the end.

Print this command table:

```text
┌──────────────────────┬──────────────────────────────────────────────┐
│ Command              │ Effect                                       │
├──────────────────────┼──────────────────────────────────────────────┤
│ .continue            │ Next group                                   │
│ .finish              │ Stop and final recap                         │
│ .notes               │ Summarize the notes file                     │
│ .question <text>     │ Capture a question to ask                     │
│ .comment <text>      │ Capture a PR comment                          │
└──────────────────────┴──────────────────────────────────────────────┘
```

When saving a question, comment, or other capture, include the relevant file
path and line or range from the current diff when known. Keep that metadata in the
notes without making the user provide it as part of the command. If a comment has
no stable locus, save it as review-body feedback instead of inventing a line.

## Captures during the walkthrough

- `.question <text>` captures an author-facing question and keeps the session
  moving. Do not investigate it immediately. At the end, answer it from local
  artifacts when possible; leave it for the author when the answer is unknowable.
- `.comment <text>` captures concise review feedback. Attach the relevant file
  path and line or range when the feedback belongs to a specific diff location.
  Preserve comments without a valid location for the review body.
- `.todo` is not a normal PR review capture. Accept it only for an explicitly
  personal follow-up.
- `.note` remains available for generic context but is not part of the first-load
  command table.

Do not automatically capture the questions offered at each pause. Capture only
when the user uses a command or clearly asks to record something.

## Finish and draft review

At `.finish`, provide:

1. a brief recap of the conceptual sequence;
2. a recap of the nonempty notes sections; and
3. an open-questions pass.

For each queued question, inspect local artifacts such as the code, diff, tests,
commits, and PR description or body. Record answers and move answered questions
to `Resolved / Answered`. Do not invent answers for questions that require the
author's intent or information unavailable locally.

Then offer to prepare a draft GitHub PR review:

- unresolved `.question` items become author questions or review-body material;
- `.comment` items with a valid location become inline comments;
- `.comment` items without a valid locus go in the review body.

Surface stale, invalid, or ambiguous locations for confirmation rather than
guessing. Preview the complete draft before any external action. Never submit,
post, or otherwise send the review without a separate explicit request.
