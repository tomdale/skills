---
name: walkthrough
description: Guide a user through a substantial local changeset as a conceptual, paused narrative walkthrough. Use for GitHub PR review or local/self/agent-originated work: explain the change story, group the diff into teachable units, capture review feedback or follow-up work, and finish with mode-appropriate next steps.
---

Guide a user through a substantial local changeset in conceptual review order. Teach in focused chunks, pause after each chunk, and help the user understand the implementation before making judgments. Use `../narrative/SKILL.md` as the baseline style and process when needed.

Default **workflow** is local review (own branch, agent-generated work, resumed work). Primary captures: `.question`, `.todo`.

## Mode selection

Infer the workflow before the tutorial and opening overview from the request and checkout context.

If the user asks for a PR review or GitHub pull request review, asks to prepare or post review feedback, mentions inline review comments, author questions, a PR URL or number, or the checkout metadata identifies an active GitHub PR, read `references/pr-review.md` before starting. That reference contains the PR-specific entry checks, tutorial, captures, and finish behavior.

Otherwise use the default local workflow. Explicit user intent wins over repository state: a request for local, self, or agent review stays local even if the branch also has an open PR. If PR intent is present but no review target is available, follow the reference's early-choice procedure rather than beginning a walkthrough that cannot meet the user's expected outcome.

If intent remains ambiguous and no active PR resolves it, ask once whether this is a GitHub PR review or a local walkthrough. Do not ask again after the workflow is set.

## Commands

One canonical dotted form per operation. Accept close natural-language equivalents by intent; if ambiguous, ask one concise clarifying question. Do not invent additional command names.

Navigation:

- `.continue` — move to the next group.
- `.finish` — stop the walkthrough and give the final recap.
- `.notes` — summarize the notes file.

Capture (always append to the notes file; create on first capture):

- `.question <text>` — capture an open question in the notes file and keep moving. The purpose is to queue uncertainty so the walkthrough stays focused instead of branching into every rabbit hole. Do not deep-investigate on capture; resolution happens at finish (see Finish). Attach the relevant file path and line or range from the current diff when known. Keep that metadata in the notes without presenting it as a user-facing requirement.
- `.comment <text>` — capture review feedback when the user explicitly requests PR review behavior. Read `references/pr-review.md` for its location and finish rules. When saving any capture, attach the relevant file path and line or range from the current diff when known. Keep that metadata in the notes without exposing it as a command requirement.
- `.todo <text>` — **Local primary.** Capture a change or fix the user intends to make after the walkthrough. Attach the relevant file path and line or range from the current diff when known. Keep that metadata in the notes without presenting it as a user-facing requirement.
- `.note <text>` — generic context, observation, or reminder. Available in either mode but not shown in the first-load table; use when the user clearly wants a non-question/non-comment/non-todo capture.

`.comment` is always draft-only. Never post a GitHub review, inline comment, or other outbound feedback without a separate explicit user request.

## First-load tutorial

On first load only, before change analysis, print exactly the local tutorial below. Do not repeat after pauses, questions, resumes, or later groups. Do not include `.note` in the table.

If `references/pr-review.md` was loaded, print that reference's PR tutorial instead.

For the default local workflow, print:

```text
 __        ___    _     _  _______ _   _ ____   ___  _   _  ____ _   _
 \ \      / / \  | |   | |/ /_   _| | | |  _ \ / _ \| | | |/ ___| | | |
  \ \ /\ / / _ \ | |   | ' /  | | | |_| | |_) | | | | | | | |  _| |_| |
   \ V  V / ___ \| |___| . \  | | |  _  |  _ <| |_| | |_| | |_| |  _  |
    \_/\_/_/   \_\_____|_|\_\ |_| |_| |_|_| \_\\___/ \___/ \____|_| |_|

I will group the diff into related changes, outline the review order, then
narrate one group at a time. After each group, I will pause so you can respond or
capture follow-ups. Captures go to `.agent/review-notes.md` in this session's root
working directory.
Local workflow. Capture questions and changes or fixes as you go; we resolve what
we can at the end. Close natural language works too.

┌──────────────────────┬──────────────────────────────────────────────┐
│ Command              │ Effect                                       │
├──────────────────────┼──────────────────────────────────────────────┤
│ .continue            │ Next group                                   │
│ .finish              │ Stop and final recap                         │
│ .notes               │ Summarize the notes file                     │
│ .question <text>     │ Capture a question to ask                 │
│ .todo <text>         │ Capture a change or fix to make           │
└──────────────────────┴──────────────────────────────────────────────┘
```

## Preparation

Identify the change base, usually the merge-base with `origin/main`, `origin/master`, or the PR-configured base. Read recent commits, the full `base..HEAD` diff, relevant pre-change code with `git show <base>:<path>`, and enough current surrounding implementation to explain the change accurately. For PR-specific target checks and baselines, follow `references/pr-review.md`.

If the user names a different range, commits, paths, worktree state, or base, use that instead. If the base is ambiguous, choose the likely base, state the assumption, and continue.

Do not require an active PR for the local workflow. PR target checks happen before the walkthrough when the PR reference is loaded.

## Review notes

Use `<session-root>/.agent/review-notes.md`, where `<session-root>` is the root working directory of the current agent session, not necessarily the Git repository root.

At walkthrough start, offer to maintain that file. Do not create or write it until the user runs a capture command, accepts the offer, or gives obviously recordable feedback that maps cleanly to one capture kind. If kind is unclear, ask which of `.question` / `.comment` / `.todo` / `.note`. Capture commands write immediately. Create `.agent/` lazily when needed. Use another path only when the user explicitly chooses one.

The notes file is the source of truth for `.notes` and finish recaps. Terse structured review material, not a transcript. Preserve intent while rewriting vague remarks clearly. Do not add speculative findings unless the user agrees or they clearly match a capture kind. After each write, briefly say what was recorded (kind + locus if any), then return to the current walkthrough point. Do not start investigating a freshly captured `.question` mid-walkthrough.

Title `Review Notes`; optional `Context` only when branch/base/scope/mode helps later. Content sections only when nonempty:

- `Questions` — `[Group] …`
- `Comments` — review feedback, with the relevant location attached when known; feedback without a stable location goes in review-body material
- `Todos` — `[Group] …`, with the relevant location attached when known
- `Notes` — `[Group] …`, with the relevant location attached when known
- `Resolved / Answered` — items resolved later, moved not duplicated

### Capture guidance

**`.question` (both modes):** Always queue immediately. Do not try to fully answer before writing. The point is to stay on the conceptual walkthrough; deep answers wait until finish. Label by current group when known.

When PR intent triggers `references/pr-review.md`, follow that reference for `.question`, `.comment`, and PR finish behavior.

**Default workflow (local):**

- `.question` — parked clarification for later (user or agent).
- `.todo` — actionable local edit after the walkthrough.
- `.comment` / `.note` — only when explicitly requested; do not offer PR review creation in this mode.

## Opening overview

Concise, explanatory, not evaluative: how relevant code worked before; what changed; why major changes appear to exist; how changes work together. Save detailed concerns for grouped walkthrough unless understanding is blocked. Offer review notes before the first group; continue without notes unless the user opts in.

## Grouping and teaching order

Group by conceptual unit, not file. A group may span files; a file may appear in multiple groups.

Order: substantive before mechanical/follow-on; low-dependency before dependent when helpful; foundations before consumers; API/data-shape before call sites when needed; tests near behavior unless test strategy is its own concept.

Before group 1, show the outline as a compact sequence of concept names, not file names.

For each group: narrative style scoped to the group; before/after/why it matters; only relevant syntax-highlighted snippets with file references; annotate outside snippets unless inline is necessary; connect to prior groups when useful; avoid previewing later groups enough to answer likely future questions. End with pause; wait for `.continue` / `.finish` (or natural-language equivalent).

At each pause, offer three or four useful questions to ask about the current group. Do not capture these prompts automatically; capture one only when the user uses a command or clearly asks to record it.

When the user asks a live question mid-walkthrough: give a brief answer if it unblocks understanding of the current group; if it would pull the session into a long tangent, suggest `.question` to park it for the end. Stay scoped to the current group unless broader context is required. If the answer depends on a later group, say so and offer to answer now, cover later, or park with `.question`. Then ask whether to continue.

## Finish

Finish after all groups or `.finish`.

Always:

1. Brief recap of the conceptual sequence.
2. Notes recap by nonempty section when notes were used.
3. **Open questions pass:** list parked `.question` items. Resolve questions that local artifacts can answer by exploring the code, diff, tests, commits, or PR description/body when present. Record each answer briefly and move it to `Resolved / Answered`; leave unknowable questions unresolved.

Then mode-specific handoff:

If `references/pr-review.md` was loaded, follow its finish and draft-review instructions.

**Default workflow (local):**

- After the open-questions pass, offer to pass remaining questions to the agent for answers from local artifacts.
- Offer to work through `.todo` items as local edits or a concrete implementation plan.
- Do not offer to create or file a GitHub PR review merely because notes exist.

Keep the finish recap brief; value came from the grouped walkthrough. Act on captures only after the user opts into the offered next step.
