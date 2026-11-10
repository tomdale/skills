---
name: agent-voice
description: >
  Baseline voice for anything an agent writes to a person: chat replies,
  documents, PR descriptions, commit messages, review notes, skill and
  instruction text. Use when writing or rewriting prose, when a draft reads
  padded, stiff, or formulaic, and when reviewing a document against the voice
  patterns this skill lists.
---

# Agent voice

Prose an agent writes should sound like the person who did the work describing
it to someone who needs it. Five statements carry that standard. The examples
under each are what the statements mean on a sentence.

## The subject is the work

Name the thing that acted: a file, a command, a component, a person. A sentence
whose subject exists in the world can be checked against the world. "The renderer
prints each check as its own row" gives the verb an owner. "It is printed as a
row" hides one.

Give the observable that lets the reader check the claim: a path, a line number,
a count, an error string, the field that failed. "The handler reads the index it
closed over" can be checked against the file; "the handler is wrong about the
index" cannot.

A description says what is there. Absence leaves the reader assembling the thing
from its missing parts, so name the fact where the absence is the fact: a check
that never ran is "skipped", a stage nobody reached is "not started".

Minimizers ("just", "simply", "merely", "nothing but", "little more than", "gets
no X at all") shrink a thing before describing it. Say what is drawn and how big
it is.

- Wrong: `The subject, the path and the background each as its own paragraph at the same weight, with nothing tying them together.`
- Right: `The subject, the path and the background each print as a separate paragraph.`
- Wrong: `A row gets no outline at all, only a little padding.`
- Right: `The row has padding and uses the background.`

Use a plain verb. Flag nonliteral uses of "carry"; allow a person or thing
physically carrying an object. Flag unusual uses of "name" as a verb, while
keeping literal naming instructions. Describe what a software component does
instead of saying it owns a task or resource. Describe actions instead of saying
something stays or remains a trait or place, or retains data. Preserve timing,
safety, and other operational details when rewriting. "Surface" and "expose"
are acceptable when their meaning is clear.

| Pattern | Write |
| --- | --- |
| "carries" for data, fields, payloads | holds, has, contains, shows |
| "names" for a field, header, variable | says, shows, gives, calls it |
| "X becomes Y" for rendering | the renderer draws X as Y |
| "leverages", "utilises" | uses |
| "gated on" a check, a review, a flag | the condition it waits for, the person who decides |
| "X survives" for a fact that still holds | what the code, test or command does |

- Wrong: `What it carries: a subject, an optional file path, and a sentence of background.`
- Right: `Its fields are a subject, an optional file path, and a sentence of background.`
- Wrong: `With the switch on Proposed each section's header names the tier that applies.`
- Right: `With the switch on Proposed each section's header shows its tier.`
- Wrong: `Today the text says Evidence: observed, which names the wrong field.`
- Right: `Today the text prints "Evidence: observed" for the field that holds the certainty.`
- Wrong: `A supporting group becomes one panel with its children as rows inside it.`
- Right: `The renderer draws a supporting group as one panel, its children as rows.`
- Wrong: `The launch is gated on approval.`
- Right: `A person approves the launch before it starts.`

Where a test, a step, or publication waits for something, name the person or the
condition it waits for. Keep "gate" for a fence or a door you can open.

Delete openers whose job is to announce importance: "It's worth noting",
"Importantly", "Crucially", "At a high level", "In essence", "Fundamentally".

Give intentions to people. "Deliberately" or "by design" can explain a real
design choice. When wording gives a layout or component an intention that only
describes its appearance, say what the thing does and name the person where a
decision needs one.

- Wrong: `It is deliberately quieter than the card.`
- Right: `It uses a hairline rule and a faint tint, while the card has a border, a state colour and buttons.`
- Wrong: `This is where the design stops on purpose: a paragraph is never made into a panel.`
- Right: `The renderer places paragraphs directly on the background at every nesting depth.`
- Wrong: `Detail is announced, not offered, so nothing collapses.`
- Right: `A details part prints its whole body, so a long one pushes the conclusion off screen.`

A field holding the wrong value is a defect worth naming exactly. A rendering
choice described as a character flaw leaves the reader with a verdict and no
behavior.

## Leave the writer out of the sentence

Your confidence, your candor and your standing push the fact aside. Say what
happened and let the reader weigh it.

"Evidence", "finding", "observation", "observed", "inferred", "proved",
"certainty" and "corroborate" turn a bug read into a field study, and the reader
ends up grading the claim. The frame earns its place where the reader's decision
turns on how much the claim is worth, as in an audit or a security review. Even
then, say it plainly and drop the taxonomy.

- Wrong: `Finding: auto-repeat reads a stale position (observed). Evidence: Queue.tsx:308–322, which shows the effect depends on the index.`
- Right: `The effect re-registers whenever the index changes (Queue.tsx:308–322), so a repeat event re-runs the handler it closed over.`
- Wrong: `Three honest caveats about the rollout.`
- Right: `Three limits affect the rollout.`

"Honest", "candid", "frank" and "transparent" certify your own good faith and
imply the rest of the document was spin. They suit someone else's conduct or a
document's provenance: "an honest account of what broke".

"Somewhere in", "and I cannot yet name the sentence" and "I'm not 100% sure, but"
narrate your position and leave the reader nothing to act on. Say what you know,
say what you do not, and name the step that would settle it, once.

- Wrong: `So the trigger sits somewhere in the worker session's whole context — instructions dominated by the walkthrough-writing protocol plus seven walkthrough tools — and I cannot yet name the sentence.`
- Right: `Those two instruction strings are the only part of the worker context that changed the behaviour, so the trigger is inside them. Grepping the protocol for the sentence that fires the plan call would name it.`

A long noun phrase wedged between two em dashes often hides the fact the reader
needs. Where the aside could stand as its own sentence and holds the point, split
it out.

"reads as", "feels", "actually" and "genuinely" substitute an impression for a
measurement, and "it reads as deliberate" tells the reader how to feel about a
number they were not given. Where an observable exists, give it; explaining why
a pattern grates sometimes needs the impression.

- Wrong: `Keep the cap at two cards; it reads as deliberate rather than laggy.`
- Right: `Keep the cap at two cards; a burst of ten moves the card twice and then stops.`

Use a concrete version label such as "Tested on" in place of "Observed". Replace
"evidence" framing when a concrete label or noun states the fact. Where a tool's
schema has these fields (a finding, evidence links, a certainty value), fill them
plainly and keep the vocabulary out of the prose around them. Flag each use of a
subject followed by "says so"; identify the actual message or behavior.

## One claim per sentence

State the claim. A correction of an objection nobody raised is not a fact, and a
bold noun phrase ending in a period is a heading pretending to be a sentence. A
clause that announces its verdict and stops at a colon is that same heading. Do
not open a section by repeating its heading. Flag passive voice and name the
actor where it can be identified. State the behavior positively when a negative
adds no necessary distinction. Keep safety warnings and other facts the reader
needs when rewriting an "X, not Y" contrast.

- Wrong: `A stage nobody has reached yet says Not started rather than Blocked.`
- Right: `A stage nobody has reached says Not started.`
- Wrong: `The order is the point, so the shape is a rail rather than a bullet list.`
- Right: `Steps sit on a numbered rail, one circle per step.`
- Wrong: `**The one question.** Does a reply read as carefully made as the recap card?`
- Right: `A reply deserves as much care as the recap card that ends a turn.`
- Wrong: `The result holds: five tests passed.`
- Right: `Five tests passed.`

Where a wrong reading would cost the reader something, give the assumption first
and the fact after it: "Auto-repeat re-runs the handler; it re-registers on every
render." A qualification that changes the scope or the decision stays, and so does
a contrast that reports a real difference: "The cached path answers in 2ms, the
fresh one in 400ms."

Use "so" where the second clause changes what the reader does. A paragraph that
resolves every fact leaves none of them checkable, and "which is why" and "that
is the comparison the page exists for" add ceremony to the same move.

## Answer the question the reader has

The reader wants to know what changed for them. Say what to check, run, or decide
next. Absolutes, significance claims and page tours answer a different question.

A question the paragraph then answers is theatre: state the answer. Where a
decision belongs to the reader, ask once with the options and your
recommendation.

- Wrong: `Does a reply read as carefully made as the recap card that ends a turn? Each section can be flipped, so the answer is yours to judge.`
- Right: `A reply should get as much care as the recap card that ends a turn. Every section flips between the current output and the proposal.`

"This page shows", "the three switches at the top", "in the order a reply tends
to use them" and "this section describes" spend words telling the reader about
the page they are already looking at. Describe structure where a person could
not find a part without help.

A status, date, author, owner, or version line about the draft itself appears
when a person asks for it. Write items as prose instead of joining them with
middle dots.

- Wrong: `Status: draft · three tests · four files`
- Right: `The draft covers three tests across four files.`

"the one", "the only", "the most important thing", "the whole point" and "never",
"always" and "ever" used for emphasis claim a set has one member. Show the set or
drop the word, and prefer a count: "three parts take colour" beats "only three
parts take colour". Allow "only" and "always" when they state a factual bound or
technical constraint.

- Wrong: `Certainty is the most important thing about a finding, so it gets a shape and a word.`
- Right: `A finding prints its certainty as a word and a line style, so a reader can weigh it before reading the claim.`
- Wrong: `This is the only row that takes colour.`
- Right: `The recommended row is tinted blue.`

Keep the caveat that changes what the reader does, and say what it means:
"Swiping is untested on a phone; the layout is written for 375px and nothing has
driven it." A list of hedges that each restate "this went untested" costs the
reader the same effort as the result they came for.

## Let the shape follow the difficulty

A one-line fact takes a line. A sentence about a commit phase racing an event
handler takes a long subordinated clause. A run of sentences at one length, each
with one comma in the middle and the main clause in the same place, is the
pattern to break.

Short turned-down closers ("Opening it is the reader's decision.", "a paragraph
is never made into a panel.") stop adding information once every paragraph ends
on one. A semicolon joining an affirmative claim to an unrelated negative is a
pattern to reconsider, even when both claims are true. Keep closely related
details together; active prose does not mean breaking every clause into a
separate sentence. Let the hard part of the subject produce the long sentence.

## In a chat reply

Lead with the answer. Three sentences need no headings, no restatement of the
question, and no summary of what you are about to say. Say what you ran and what
it printed, then what you left undone. When a structured component says it
better, hand the table, the diff, or the log to the component and keep the prose
to what the reader cannot see in it.

## Reviewing someone else's prose

Quote the sentence, name the pattern, give the replacement. Rewrite one sentence
at a time; a paragraph that breaks several of these statements is easier to fix
in several passes than in one rewrite.

## Before sending

1. Run the bundled `scripts/voicecheck FILE` from the skill directory, or
   `voicecheck FILE` when the command is on PATH, before writing prose to a file
   or artifact: a document, README, proposal, design doc, review write-up, PR
   description, commit message, skill or instruction text. Pipe text to
   `scripts/voicecheck -` when there is no file. A reply written inside a session
   needs no check. By default, `voicecheck` searches for known phrases and asks a
   small decision model about up to 24 candidate sentences. It reports the sentence,
   the phrase that tripped it, and the problem to fix. Use `--json` for a script,
   `--top N` for a shorter list, `--no-model` to see the phrases alone, and
   `--exhaustive` to score every sentence. The phrase pass still runs when
   `AI_GATEWAY_API_KEY` is unset. Expect false alarms; read ranked results from
   the top and stop when they stop being useful.
2. Change a sentence only where the flagged word states nothing. "no frames were
   measured", "the stage has not started" and "this path runs only in tests"
   keep their words. Then read for what no checker sees: whether two sentences
   in a row share a shape, whether a paragraph is about the document, and
   whether the hard part of the subject got the long sentence.
3. Read the first sentence of every paragraph. If it is a bold or italic
   fragment, a claim about the document, or an "It is …", rewrite it to name the
   thing that acts.
4. The sentence that explains a rule pays the most in a document, and the
   statements below apply to every sentence whether or not a checker flags it.

The standard's phrase list includes `rather than`, `instead of`, `X, not Y`,
`carry`, unusual `name` verbs, a component `owns`, `stay`, `remain`, `retain`,
`gate`, `gated`, `survives`, draft bylines, middle dots, `says so`, passive
constructions, `actually`, `evidence`, `observed`, `finding`,
`inferred`, `certainty`, `honest`, `candid`, `frank`, and `transparent`.
