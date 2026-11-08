---
name: eradicate-ui-slop
description: >
  Remove the tells that mark UI as agent-built: middot chains, eyebrows, pills,
  nested cards, gradients, mono metadata, invented claims, and hedging copy
  such as "local" or "simulated". Use for any UI, HTML mockup, wireframe,
  prototype, component, landing page, or Markdown whose layout is the
  deliverable, before writing it and again before showing it; and when asked
  to review UI for slop, or when a design looks generic, templated, or
  AI-generated. Every result must pass the bundled fast-model checker on its
  source and screenshots.
---

# Eradicate UI slop

These patterns mark UI as agent-built at a glance, and readers who spot them stop trusting the rest of the work. Remove each one by deleting it or by restructuring the information it stood in for. Most slop is chrome filling the space where a decision about the information should have been, so deletion is the default fix.

A cousin of a tell is the same tell. `·` swapped for `|`, `/` or `—`, a pill swapped for a tinted span, an eyebrow swapped for a small bold label, and a card swapped for a hairline box all fail the same rule.

## How the rules work

Every rule below has a bold name, which the checker uses in its reports, and one of three types:

- Banned: remove it wherever it appears.
- Only when: allowed under the stated condition and banned otherwise.
- Required: the artifact must have it.

A rule of any type yields only to these exceptions:

1. The user asked for that pattern in this artifact.
2. You are editing an existing product that already uses that exact pattern in that exact place. Match it there; do not spread it. A design-system document that permits a pattern does not license new uses of it.
3. You are reproducing third-party chrome exactly, such as a host app's own header or a platform's native controls. Content you write inside that chrome gets no exception.

"Compact", "conventional", "scans well" and "fits the aesthetic" are not exceptions. Mark each kept pattern in source on its line with `slop-ok: <exception number> <reason>`; the checker skips marked lines. Mark a waived Required rule the same way on the file's root element or first style rule, naming the rule. In your reply, list the exceptions you took.

## Content: what goes on the screen

Required:
- **Requested fidelity.** Build at the fidelity asked. A rough wireframe is grey boxes, real labels and plain system type, with no colour, shadow, icon or theme polish.
- **Real content.** Use the product's nouns, realistic names and realistic sample data. Sample values for fields the brief defines, such as a run's age or a file count, are content and need no exception.

Banned:
- **Placeholder content.** Lorem ipsum, Acme, Jane Doe, "Project Alpha".
- **Invented claims.** Numbers that assert performance, adoption or results: `10x faster`, `18–38% more space`, user counts, uptime, ratings, testimonials, logo strips. Show a claim only when it comes from real data you were given.
- **Provenance words** that describe the artifact or its data rather than a product concept: local, locally, synthetic, simulated, mock, fixture, sample, inert, stand-in, placeholder, illustrative, playground, design study, prototype. Product terms that contain these words, such as a git "local branch" or an audio "sample rate", stay. Wrong: `Save locally`, `Rename local thread…`, `Local playground · simulated BB host`. Right: `Save`, `Rename thread…`, and no sidebar note.
- **Reassurance** about side effects: `Nothing is sent to an agent or saved in BB.`
- **Not-X hedges** that define a thing by what it isn't: `These test container layouts, not device behavior`. State what it is, or delete the sentence.
- **Authenticity claims**: `Real row-action reveal`, `the actual component`. Show the component.
- **Implementation asides** and bug notes: `uses a floating Radix portal`, `Stepper's keyboard handler does not check its disabled prop`. File the bug; keep the screen about the reader's task.
- **Process residue**: empty logs and placeholders such as `No local actions yet` that exist only to show the mockup works.
- **Help text**: permanent tips and paragraphs explaining how the UI works. They cover for labels and layout that do not explain themselves, so change the screen. Field input formats, required legal or safety disclosures, and consequences of destructive actions stay.

Caveats about what is simulated, missing or broken go in your chat reply.

## Copy: how it is worded

Banned:
- **Middot chains.** `·`, `•` or `&middot;` joining facts of different kinds into one line at one weight. Delete what the reader does not need, put the primary fact in the sentence, and give each secondary fact its own position: a right-aligned column, a second line, a tooltip.
  - Wrong: `Running · 1m` on every row of an "Active" section. Right: `1m` in a right-aligned column; the heading already says the run is active.
  - Wrong: `Reviewing · 39f36ab · 2 suggestions · 1 failed`. Right: `Vercel Agent is reviewing 39f36ab.` with `One of 2 suggestions couldn't be posted.` on its own line.
- **Separator glyphs.** Pipes, slashes and bullets doing a middot's job. `BB thread / simulated context` is a middot chain.
- **Em dashes** anywhere in UI copy: readers take them as the signature of model-written text. Use a period, a colon, or a second line.
- **Label-and-count capsules**: `Concerns · 1`, a `Part 1 of 3` pill. Put the count in a sentence or heading, or delete it.
- **Repeated status**: a status word on each row that repeats the group heading.
- **Tagline formulas**: `Fast. Simple. Secure.`, `One repository. A worktree for every agent.`, `X, reimagined`, `Built for Y`, `Everything you need to Z`, `Meet X`, and the words supercharge, unlock, seamless, effortless, powerful, elevate, empower.
- **Implementation vocabulary** in place of outcomes: "preparing the review", "reconciling findings", "syncing state". Say what the reader gets: "Adding comments to your pull request."
- **Arrow links**: arrows and chevrons appended to links and buttons, `Learn more →`, `View all ›`.
- **Emoji** as icons or in headings, including ✨ for AI and 🚀 for launch.

Only when:
- **Heading counts** such as `Active (3)`: only for collapsed or paginated content.

Required:
- **Casing**: follow the product's or platform's casing convention, and use one style throughout.

## Structure: grouping and emphasis

Banned:
- **Eyebrows**: small uppercase or letter-spaced labels above a heading (`OVERVIEW`, `PART 1`, `Components`). Delete them or make the heading say it. Uppercase section labels anywhere count.
- **Card nesting**: cards inside cards, a bordered rounded box around every section.
- **Feature grids**: the three-up icon, title and blurb grid.
- **Stat rows**: big numbers over small labels.
- **Icon tiles**: an icon in a tinted rounded square beside each heading or list item.
- **Single-side borders**: a thick border on one edge of a panel or callout, in an accent or a neutral grey. On a rounded box it bends into the corners and tapers to a point (`border-left: 3px solid var(--border)` with `border-radius`). Delete it; separate the region with spacing.
- **Triple encoding**: one state shown by a coloured dot, a pill and a word. Use one encoding, plus text when colour alone would carry meaning.
- **Hero formula**: giant centred headline, grey subhead, a primary and ghost button pair, a screenshot in a glowing frame, a "Trusted by" strip.
- **Centred everything**: body copy, lists and sections centred by default.

Only when:
- **Boxes**: a bordered or filled container only around something with its own behaviour, such as an independently saved form, a draggable item, a code block, or an embedded preview of another surface. Group everything else with spacing, alignment and type.
- **Pills and badges**: only for a state label in a list where state must scan at a glance, a user-applied label or tag, a filter chip, or a counter on a tab or nav item, and at most one per row. Metadata, part numbers, label-and-count capsules and a decorative "New" are plain text in the right position.

## Type

Banned:
- **Flavour fonts** brought in for character: Space Grotesk, Instrument Serif, Fraunces, Playfair, DM Serif, Syne, Outfit, Sora, Clash or Cabinet Grotesk, and italic serif captions. Use the product's typeface or the system stack, and set the scale with the typography skill.

Only when:
- **Monospace**: only for code, paths, SHAs and commands. Timestamps, counts, status words and section labels in mono are dressing up as technical.

Required:
- **Legible text**: 11px or larger, at most two grey levels of text, and muted text at 4.5:1 contrast or better.

## Colour and surface

Banned:
- **Default palettes**: Tailwind indigo, violet or purple as the accent (#6366f1, #8b5cf6, #7c3aed, #a855f7); near-black with neon green or cyan for developer tools; warm cream paper with a serif display face and a terracotta or rust accent for anything "thoughtful". Use the product's palette. With none, use neutral greys and one accent taken from the subject.
- **Gradients and effects**: gradients on backgrounds, buttons, borders or text (`background-clip: text`); glows; blurred colour blobs; noise overlays; glass panels (`backdrop-filter: blur`).
- **Fake chrome**: macOS traffic-light dots on code blocks, fake browser frames, fake terminal windows.

Required:
- **One small radius**, on controls and real containers only. Large radii and soft shadows everywhere (`rounded-2xl`, `shadow-xl`, 16–24px radius) fail it.

## Page

Required:
- **System theme**: a standalone page follows the system theme by default with `color-scheme: light dark` and `prefers-color-scheme` styles. A light/dark switch is fine when System is its default.
- **Shared theme**: the page and every component on it use the same theme. A dark code block or card on a light page fails it.
- **Measure and margins**: text columns have a max width and the page has margins.

## Build procedure

1. Before writing UI, list what the reader must know and do on this screen, in priority order. Build only that, using the rules above as constraints.
2. Render the result in the surface it ships to and screenshot it with the browser tools, in light and dark at each width the surface is used at (for a gallery, each preview width). Render Markdown with the host's own renderer.
3. Check the changed source and the screenshots: `node <this skill's directory>/scripts/slop-check.ts <files, directories, screenshots>`. It sends source files and screenshots in separate batches to a fast model with this file as the rubric and reports every file: its tells, each with location (`line N` or `screenshot`), rule name, quote and fix; `no tells found`; or `no result from the checker` when the model skipped the file or its batch failed, which fails the run. Run `--help` for options. It needs the `pi` CLI. Without it, give a fast-model subagent references/checker.md, this file, and the files, headed `Run: edit` or `Run: review`.
4. A fast model misses tells and invents some. Confirm each hit against the source or screenshot, then fix it by deleting or restructuring. Look at the screenshots yourself for card nesting, hero formulas, triple encoding, competing emphasis and centred-everything layouts.
5. Re-render and re-check the files you changed until every file reports `no tells found`, apart from screenshot tells that match a pattern marked `slop-ok:` in source. The checker keeps reporting those and exits 1, so accept each one yourself and list it with the exceptions. Report the exceptions taken.

## Review procedure

When asked only to review existing UI, run build steps 2 and 3 with `--review`, confirm each hit as in step 4, and change nothing. Treat imported components as part of the artifact and ignore exception 2. Report hits grouped by rule name, each with the fix you would make.
