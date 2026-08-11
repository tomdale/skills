# walkthrough

Walk through a **local changeset** one conceptual group at a time, pausing after
each so you can ask questions and take notes before forming judgment.

Useful when you need to understand code changes where the diff is bigger than
what you can hold in your head at once:

- Reviewing someone else's checked-out GitHub PR
- Reviewing a large change an agent just made locally
- Coming back to your own branch after time away

## Getting started

Have the branch (or other change range) checked out, then ask something like:

> Walk me through these changes.

> Guide me through this PR for review.

> I haven't looked at this branch in a week — walk me through it.

## Walkthrough session lifecycle

1. **Overview** — A short, non-evaluative picture of how the relevant code
   worked before, what changed, and why the pieces fit together.
2. **Map** — Changes grouped by _concept_, not by file. You'll see the planned
   sequence before the first group.
3. **Walk** — One group at a time: before/after, why it matters, and only the
   relevant snippets.
4. **Pause** — A few questions worth asking about that group, then it waits for
   you.
5. **Finish** — A brief recap of the conceptual sequence, plus whole-change
   review questions. If you kept notes, those are folded in.

## Commands

One canonical command per operation, always dotted. Close natural language is
accepted too, but these are the names to learn:

### Navigation

| Command | Effect |
| --- | --- |
| `.continue` | Next group |
| `.finish` | Stop and give the final recap |
| `.notes` | Summarize captures so far |

### Capture

Captures append to `.agent/review-notes.md` in the session root (created on
first use).

| Command | Effect |
| --- | --- |
| `.question <text>` | Open question (for the PR author, or for you) |
| `.comment <text>` | Queue a GitHub PR review comment, with file path and line |
| `.todo <text>` | Local change you intend to make |
| `.note <text>` | Generic note |

`.comment` only drafts — nothing is posted to GitHub until you ask separately.
The skill attaches path and line from the current diff context so a later post
lands on the right locus.

Ask ordinary questions anytime (no command needed). Answers stay scoped to the
current group unless broader context is needed; if something depends on a later
group, you'll be told and can choose to cover it now or later.

## Tips

- **Capture as you go.** Get through the overview first; act on comments and
  todos after `.finish`.
- **Pick the right capture kind.** `.comment` for PR feedback, `.todo` for
  edits you'll make locally, `.question` for unresolved uncertainty, `.note`
  for everything else.
- **Name a range if needed.** By default it uses the branch vs its merge-base
  (usually `main`/`master`). You can point it at specific commits, paths, or
  "what you just changed."
