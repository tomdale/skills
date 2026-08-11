---
name: walkthrough
description: Guide a user through a large local change set by explaining the change narrative, grouping the diff into conceptual units, presenting annotated code snippets, pausing for questions after each unit, and ending with whole-change review questions. Use when the user wants a walkthrough, review walkthrough, guided review, or help understanding a checked-out PR, agent-generated changes, their own branch after time away, or any other substantial unmerged diff.
---

Guide a user through a substantial local change set in review order. Teach in conceptual chunks, pause after each chunk, help form review questions before judgment. Typical uses: reviewing someone else's checked-out PR, reviewing agent-generated local work, or re-entering your own branch after time away. Same process in all cases. Use ../narrative/SKILL.md as baseline style/process when needed.

Commands: one canonical form per operation, always dotted. Accept close natural-language equivalents by intent; if ambiguous, ask one concise clarifying question. Do not invent additional command names.

Navigation:
- `.continue` — move to the next group.
- `.finish` — stop the walkthrough and give the final recap.
- `.notes` — summarize notes collected so far.

Capture (append to the notes file; create it on first capture if needed):
- `.question <text>` — unresolved uncertainty (author-facing on a PR review; self-facing on own/agent work).
- `.comment <text>` — queue a GitHub PR review comment. Always associate file path and line (or range) from the current diff/context so it can be posted later against the correct locus. If locus is ambiguous, ask once before writing.
- `.todo <text>` — a local change the user intends to make (typical when reviewing own or agent work, not someone else's PR).
- `.note <text>` — generic note that is none of the above.

First load only: before change analysis, print exactly this tutorial (commands as a Unicode box table; keep column alignment). Do not repeat it after pauses, questions, resumes, or later groups.

```
 __        ___    _     _  _______ _   _ ____   ___  _   _  ____ _   _
 \ \      / / \  | |   | |/ /_   _| | | |  _ \ / _ \| | | |/ ___| | | |
  \ \ /\ / / _ \ | |   | ' /  | | | |_| | |_) | | | | | | | |  _| |_| |
   \ V  V / ___ \| |___| . \  | | |  _  |  _ <| |_| | |_| | |_| |  _  |
    \_/\_/_/   \_\_____|_|\_\ |_| |_| |_|_| \_\\___/ \___/ \____|_| |_|

I will map the changes into conceptual groups, then walk through one group at a
time. After each group, I will pause so you can ask questions or steer. Captures
go to `.agent/review-notes.md` in this session's root working directory.
Close natural language works too.

┌──────────────────────┬──────────────────────────────────────────────┐
│ Command              │ Effect                                       │
├──────────────────────┼──────────────────────────────────────────────┤
│ .continue            │ Next group                                   │
│ .finish              │ Stop and final recap                         │
│ .notes               │ Summarize captures so far                    │
│ .question <text>     │ Open question                                │
│ .comment <text>      │ Queue a PR review comment (with file:line)   │
│ .todo <text>         │ Local change you intend to make              │
│ .note <text>         │ Generic note                                 │
└──────────────────────┴──────────────────────────────────────────────┘
```

Preparation: identify change base, usually merge-base with origin/main, origin/master, or PR-configured base; read recent commits, full diff base..HEAD, relevant pre-change code with git show <base>:<path>, and enough current surrounding implementation. If the user names a different range (commits, paths, worktree vs base), use that. If base is ambiguous, choose likely base, state assumption, continue.

Review notes: use `<session-root>/.agent/review-notes.md`, where `<session-root>` is the root working directory of the current agent session, not necessarily the Git repository root. At walkthrough start offer to maintain that file. Do not create/write notes until the user runs a capture command, accepts the offer, or gives obviously recordable feedback that maps cleanly to one capture kind — if kind is unclear, ask which of `.question` / `.comment` / `.todo` / `.note`. Capture commands trigger immediate write. `.comment` drafts only; never post to GitHub/Linear without a separate explicit request. Agent owns mechanics: create `.agent/` when needed, create the file, append promptly, organize, and mention `.agent/review-notes.md` after writes. Use another path only when the user explicitly chooses one.

Notes file shape: title "Review Notes"; optional Context section only when branch/base/scope helps later; content sections only when nonempty:
- Questions — entries like `[Group] …`
- Comments — entries like `[path:line] …` (path+line required; include end line when a range is clear)
- Todos — entries like `[Group] …` (add path:line when the intended edit locus is known)
- Notes — entries like `[Group] …`
- Resolved / Answered — items answered later, moved not duplicated

Notes writing rules: terse review material, not transcript. Preserve user intent while rewriting vague remarks into clear notes. Prefer stable file:line references, required for `.comment`. Ask for exact wording only when intent is ambiguous; otherwise draft reasonably. Do not add speculative findings unless user agrees or they clearly match a capture kind. After writing, briefly say what was recorded (kind + locus if any) and continue from current walkthrough point. If notes exist, use them as source of truth for final recap and `.notes`.

Opening overview: concise, explanatory, not evaluative: how relevant code worked before, what changed, why major changes appear to exist, how changes work together. Save detailed concerns for grouped walkthrough unless understanding is blocked. Offer review notes before first group; continue without notes unless user opts in.

Group changes by conceptual unit, not file. A group may span files; a file may appear in multiple groups. Teaching order: substantive before mechanical/follow-on; low-dependency before dependent when helpful; foundations before consumers; API/data-shape before call sites when needed; tests near behavior unless test strategy is its own concept. Before group 1, list planned sequence compactly with concept names, not file names.

For each group: apply narrative style scoped to the group; explain before/after/why it matters; show only relevant snippets with syntax-highlighted fences and file references; annotate outside snippets unless inline comment is necessary; connect to prior groups when useful; avoid previewing later groups enough to answer likely future questions. End with pause and wait for `.continue` / `.finish` (or natural-language equivalent). Handoff text: "Before we move on, useful questions to ask about this group:" then 3-4 reviewer questions not answered by later planned groups.

When asked a question: answer from code/diff with snippets if useful; stay scoped to current group unless broader context is needed; if answer depends on a later group, say so and offer to answer now or cover later; if user raises something worth capturing, offer the matching capture command, or append immediately when they use one. Then ask whether to continue.

Finish after all groups or `.finish`: brief recap of conceptual sequence; if notes used, recap by section (Questions, Comments, Todos, Notes); provide five whole-change review questions informed by notes when present. Keep final recap brief; value comes from grouped explanations.
