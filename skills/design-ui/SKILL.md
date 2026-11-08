---
name: design-ui
description: >
  Design UI that fits its product, content and reader: inventory and rank the
  real content, compose from that ranking, build every state in scope, and
  verify the render, with reference research, concept exploration, redesign
  baselines and critique in task-specific references. Use before creating,
  extending or redesigning a page, screen, component, HTML mockup, prototype,
  landing page, or Markdown whose layout is the deliverable; when a design
  looks generic or would fit any other product; and when asked to critique a
  design. Load eradicate-ui-slop with it; that skill lists the tells to remove
  and their exceptions.
---

# Design UI

Generic UI comes from choosing a layout before knowing the content: the agent reaches for a structure that fits any product and fills it in. The core steps below make every visual decision answer something specific about this reader, this content or this product.

Load eradicate-ui-slop alongside this skill; its rules constrain every step. Set type with the typography skill. For animation or other time-based behaviour, use the prototyping-ui-motion and verifying-motion skills.

## Choose the work

Every task except critique runs the core steps. Load the references its type adds, before step 1, and run them where the core steps call for them:

| Task | Add |
| --- | --- |
| Change or extend an established screen within its existing design | nothing |
| New surface, open visual direction, or making a design less generic | references/research.md, references/concept.md |
| Redesign of an existing screen | references/research.md, references/concept.md, references/redesign.md |
| Critique only, changing nothing | references/critique.md, which runs parts of the core steps in place of all of them |

A reference to match, supplied by the user or the brief, replaces research.md, and a composition they fix replaces concept.md; skip that reference and work within what the user gave.

For a change to an established screen, scope step 1 to the content and states the change touches, and step 2 to placing that content within the screen's existing composition.

Keep notes from each step and screenshots in task storage, and summarise them in your reply.

## Core steps

### 1. Learn the job and the content

- **Reader and task.** Name the reader, the task they come to this surface for, and how often they do it. A glance at status, close reading and repeated expert work each want a different density.
- **Content inventory.** List every fact the screen shows, its kind, realistic values and its extremes (the longest name, zero items, 500 items, an error message). Get real data from the product, its fixtures or the user. Ask when the content is unknown and would change the design.
- **Ranking.** Rank the facts by what the reader needs first and cut what they don't need. The ranking becomes the hierarchy.
- **States.** List the states in scope: empty, loading, partial, error, success, no permission, and the transitions between them.
- **Existing product.** When there is one, open the current screen in its host, screenshot the states you will change, and read its components, tokens and spacing in source. The product's existing decisions are fixed unless the user opens them.

Now run whichever of research.md and concept.md the task loaded and nothing replaced, in that order. concept.md ends with a chosen composition.

### 2. Compose

Lay out the ranked content, or refine the composition concept.md chose:

- **Hierarchy.** Position, then size, then weight, then colour: the top-ranked fact gets the most prominent position.
- **Grouping.** Less space inside a group than between groups, taken from one spacing scale. Space and alignment do the grouping.
- **Alignment.** Few shared edges, and columns for facts readers compare across rows.
- **Density.** Screens for repeated expert use show more per line; occasional flows show one decision at a time.
- **Copy.** Headings name the section in the reader's terms, buttons name their effect ("Delete 3 branches"), and errors say what happened and what to do next.

### 3. Build

- **Components.** Use the product's components, tokens and typeface. Add a component only when none fits, written in the product's idiom.
- **Colour.** Use the product's palette. With none, start in neutrals, give the accent one job, such as the primary action or the selection, and use semantic colours only for state.
- **States.** Build every state from step 1 and the content extremes alongside the main path.
- **Access.** Make focus order follow reading order and give every control an accessible name.

### 4. Verify

1. **Render** in the surface it ships to, in each theme it supports and at each width it is used at, with typical and extreme content. Screenshot each. For a change to an established screen, cover the themes, widths and states the change affects, and compare each with the screenshot from step 1 to catch regressions.
2. **Squint** at each screenshot. The eye should land on the top-ranked fact first and then follow the ranking; where it doesn't, fix position and size before adding emphasis.
3. **Exercise** it: tab through every control, read the accessibility tree for names and roles, trigger each state, and check that every number, status and promise on the screen matches real product behaviour.
4. **Run the loaded references' checks**: concept.md's swap test and reference comparison, redesign.md's baseline comparison.
5. **Remove slop** with eradicate-ui-slop's build procedure on the source and screenshots.
6. **Repeat** after each fix pass. Stop when these checks pass and further changes would be taste.

### 5. Report

State which themes, widths and states you checked and which you didn't, plus what each loaded reference asks you to report.
