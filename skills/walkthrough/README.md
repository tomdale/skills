# walkthrough

Walk through changes grouped by concept, pausing after each group so you can
capture notes and questions as you go.

Useful when the diff is bigger than what you can hold in your head:

- Reviewing a checked-out GitHub PR
- Reviewing changes an agent just made
- Coming back to your own branch after time away

## Approach

Two things get in the way of understanding a large diff:

- It's not clear where to start, or in what order to review each file.
- Agents make it easy to go down time-consuming rabbit holes, which gets in the
  way of understanding the diff as a whole.

This skill provides a workflow that addresses both. Instead of diving into files
at random, it groups the diff into conceptual groups and walks them in an order
that builds understanding. You can queue questions or concerns as they come up rather
than derailing mid-stream, so you finish with a big-picture understanding and a
list of items to follow up on.

## Getting started

Have the files to review checked out, then ask:

> Guide me through this PR for review.

> Walk me through the changes you just made.

> I haven't looked at this branch in a week. Walk me through it.

## Workflow

You move through these phases in order:

1. **Overview**: set the stage before any deep dive
   1. **Intro**: how things worked before, what the diff is doing, how the
      pieces fit
   2. **Outline**: the ordered list of change groups you will review
2. **Review**: for each group:
   1. **Narrate**: hear that group explained as a short story
   2. **Pause**: clarify or queue notes, then continue or finish
3. **Finish**: recap, then work through what you queued

### Overview

Before the main review loop, you'll see:

**Intro.** You learn how this area of the code worked before, what the diff is
trying to do, and how the main pieces fit together. This is orientation, not a
verdict: enough to follow the rest of the walkthrough without deciding yet
whether the approach is good or bad.

**Outline.** You see the ordered list of change groups you will walk through.
Each group bundles related edits by concept, not by file; one group may span
files. That list is the route for the Review loop that follows.

### Review

This is the main loop. For each group on the outline, you get a short story of
that slice of the diff, then a pause for you to respond before moving on.

**Narrate.** You hear how this part of the code worked before, what the diff
changed, and why it matters, with relevant snippets woven into the story.

**Pause.** You can ask a quick clarifying question, or queue something for later
so you don't lose it. Prefer queuing over chasing every thread now. When you are
ready, `.continue` starts the next group; `.finish` stops early and jumps to the
recap.

| Command            | Effect                          |
| ------------------ | ------------------------------- |
| `.continue`        | Next group                      |
| `.finish`          | Stop and recap                  |
| `.notes`           | Summarize the notes file        |
| `.question <text>` | Capture a question to ask       |
| `.todo <text>`     | Capture a change or fix to make |

`.question` only writes the question down. It does not start an investigation.

### Finish

You get a short recap of what the review covered, then you are prompted to work
through what you captured.

- **Questions**:
  - Often, early questions will be implicitly answered later in the review, and
    can be discarded.
  - Otherwise, you can pass remaining questions to your agent to answer.
- **Todos**:
  - You can assign todos for the agent to perform immediately, or clean them up
    and turn into a plan for another agent to execute.

## PR review

When you ask for a PR review or a checked-out branch is an active GitHub PR, you
still run the same Overview → Review → Finish loop. What changes is what you
queue along the way and what happens at the end.

| Command            | Effect                                |
| ------------------ | ------------------------------------- |
| `.continue`        | Next group                            |
| `.finish`          | Stop and recap                        |
| `.notes`           | Summarize the notes file             |
| `.question <text>` | Capture a question to ask             |
| `.comment <text>`  | Capture a PR comment                 |

The goal at the end is a draft PR review you can submit. At `.finish`:

- Questions the agent can answer from the code alone get resolved locally.
- Remaining questions and `.comment` items become inline notes when they belong
  to a specific location; otherwise they go in the main review body.
- Nothing is posted until you approve.
