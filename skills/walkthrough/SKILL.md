---
name: walkthrough
description: "Guide a user through a substantial local changeset as a conceptual, paused narrative walkthrough. Use for GitHub PR review or local/self/agent-originated work: explain the change story, group the diff into teachable units, record review feedback or follow-up work, and finish with mode-appropriate next steps."
---

Walk through a substantial local changeset in teachable conceptual groups. Explain before/after/why, pause between groups, and help the user understand before judging. Use `../narrative/SKILL.md` for baseline style/process when useful. Default: local review; records `.question`, `.todo`.

Mode: explicit PR intent (PR/GitHub review, feedback, inline comments, PR URL/number) selects PR mode; explicit local/self/agent intent overrides an active PR. Otherwise, before any tutorial, determine whether checkout has an active PR: run `gh pr view --json number` or `gh pr list --head "$(git branch --show-current)" --state open`; an active PR selects PR mode. Read `references/pr-review.md` before the PR tutorial. Use local mode only after that check finds no PR. If still unresolved, ask once: GitHub PR review or local walkthrough? PR mode without a viable target follows the reference's early-choice procedure.

Commands: canonical dotted forms only; accept unambiguous natural-language equivalents, otherwise ask once. Navigation: `.next` next group, `.finish` final recap, `.notes` summarize notes. Each command writes to notes lazily: `.question <text>` records an open question; `.todo <text>` local change/fix; `.comment <text>` only when PR behavior is requested; `.note <text>` generic context. Attach current-diff path and line/range when known, without requiring user syntax. `.comment` is draft-only: never send external review feedback without separate explicit request.

First load: determine mode first, before printing any introduction, command, or tutorial text. Then briefly say that the walkthrough will group and explain the diff, then pause after each group; recorded items go to `<session-root>/.agent/review-notes.md`. Print exactly this Markdown table in either mode:

| Command | Action |
| --- | --- |
| `.next` | Continue to the next change group |
| `.finish` | Stop the walkthrough and show the recap |
| `.notes` | Review all recorded questions and actions |
| `.question <text>` | Record a question to resolve at finish |
| `.todo <text>` | Record a local action to complete first |

In PR mode, include this final row after `.todo`: `| `.comment <text>` | Record draft PR feedback for later |`. Do not repeat the introduction after pauses, recorded items, or resumes.
Preparation: find the base (normally merge-base with `origin/main` or `origin/master`), then inspect recent commits, full `base..HEAD` diff, pre-change code (`git show <base>:<path>`), and enough current context to explain accurately. Honor a user-specified range/path/base; if base is ambiguous, choose the likely one, state it, continue. PR checks/baselines are in the reference. Local mode needs no PR.

Notes: path `<session-root>/.agent/review-notes.md`, where session root is not necessarily repo root. At start offer to maintain it; write/create `.agent/` only after an item is recorded, an accepted offer, or clearly classifiable feedback. If unclear, ask for `.question`/`.comment`/`.todo`/`.note`. Write items immediately, tersely preserving intent; do not investigate a recorded question mid-walkthrough. Title `Review Notes`; optional context; nonempty sections only: `Questions`, `Comments`, `Todos`, `Notes`, `Resolved / Answered`. Label each item with group and known location. After writing, briefly confirm kind/locus and resume. In local mode `.comment`/`.note` require explicit request.

Opening: concise, explanatory, non-evaluative account of prior behavior, change, apparent reason, and how major pieces connect. Offer notes before group 1. Outline compact concept names (not files). Order groups by dependency and substance: foundations/API/data shape before consumers; mechanical follow-ons later; tests with behavior unless strategy merits a group. Each group uses only relevant syntax-highlighted snippets with file references; annotate outside snippets unless inline is needed; connect prior groups; do not spoil later groups. Pause for `.next`/`.finish`; offer 3–4 useful current-group questions. Answer short unblocking questions; for tangents suggest `.question`; if later-group dependent, offer answer now, later, or as a recorded question, then ask whether to continue.

Finish after all groups or `.finish`. PR reference controls PR record order: todos before questions, comments, or review drafting. Otherwise: briefly recap sequence and nonempty notes; resolve recorded questions from code/diff/tests/commits/PR body, record answers in `Resolved / Answered`, leave unknowable questions open; offer remaining-question investigation and `.todo` edits or plan. Never offer a GitHub review solely because notes exist. Keep recap brief; act on recorded comments or questions only after user opts in.
