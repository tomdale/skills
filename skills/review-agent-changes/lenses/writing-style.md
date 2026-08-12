# Prose and Writing Style

Review prose in READMEs, docs, comments, help text, changelogs, examples,
migration notes, and model-facing descriptions for diction that signals
machine generation. Agent prose reads as AI when it adds an attention flag to
a claim the surrounding text already proves, or reaches for an amplifier
metaphor where the concrete thing would carry the point. It should read like a
maintainer asserted a durable fact, not like an assistant proposed a polished
one.

Report a tell when it repeats or when it is a formula rather than the author
holding the point; a single incidental instance in otherwise natural prose is
not a finding. Defer to the repository's own writing conventions where they
exist (some houses use em-dashes deliberately), but treat the patterns below as
machine tells unless local precedent contradicts them.

## Construction tells

- **Em-dash overuse** as a catch-all pause and connector instead of commas,
  periods, or reordering.
- **"X remains <adjective>."** An invariant framed as status rather than
  consequence, e.g. "Defined empty strings remain authoritative." It reads as
  auto-assurance; restate the contract it implies instead.
- **"worth naming" / "worth noting" / "it's important to note"** and similar
  meta-discourse that flags relevance without supplying content.
- **Paired and balanced constructions** ("not only X but Y", "both X and Y",
  stacked three-part parallel lists) used for symmetry rather than logic.
- **Habitual sentence-openers** that transition without relating:
  "Notably," "Additionally," "Moreover," "However," "In other words".

## Word-level tells

These words are overused as semantic amplifiers, not because they are wrong.
Each claims structural weight the argument, not the adjective, should earn.

- `seam`, `seamless` — perfect-join claims pasted loosely over composition.
- `load-bearing` — applied to every important point instead of the single
  structural one.
- `evidence` — a concrete observation renamed to sound more rigorous.
- `lanes` — a concern-separation metaphor repeated where a plain subject
  already says where responsibility sits.
- `delve`, `tapestry`, `landscape`, `myriad`, `testament`, `leverage`, `pivot`,
  `foster`, `unlock`, `crucial`, `navigate`, `siloed`, `robust`, `in the same
  vein`.

Test any instance by deleting the signpost or swapping the amplifier for the
concrete thing it stands for. If the sentence still carries its meaning, the
tell was scaffolding, not prose.
