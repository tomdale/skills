---
name: design-ui
description: >
  Design UI that fits its product, content and reader: rank the real content,
  lay it out in that order, build every state, and verify the render. Reference
  docs cover research, concepts, redesigns and critiques. Use before creating,
  extending or redesigning a page, screen, component, HTML mockup, prototype,
  landing page, or Markdown whose layout is the deliverable; when a design
  looks generic or would fit any other product; and when asked to critique a
  design. Load eradicate-ui-slop with it; that skill lists the tells to remove
  and their exceptions.
---

# Design UI

Generic UI happens when you pick a layout before you know the content. Work from the content out, so every visual decision comes from this reader, this content or this product.

Load eradicate-ui-slop too; its rules apply at every step. Set type with the typography skill. For animation or other time-based behaviour, use the prototyping-ui-motion and verifying-motion skills.

## Choose the work

Run the core steps for every task except a critique. Some tasks also load docs from references/:

| Task | Also load |
| --- | --- |
| Small change to an existing screen | nothing |
| New screen, new visual direction, or making a design less generic | research.md, concept.md |
| Redesign of an existing screen | research.md, concept.md, redesign.md |
| Critique only | critique.md, instead of the core steps |

Skip research.md when the user gives you a reference to match, and concept.md when they give you a layout.

For a small change, step 1 covers only the content and states you're changing, and step 2 fits them into the existing layout.

Save notes and screenshots in task storage, and summarise them in your reply.

## Core steps

### 1. Learn the job and the content

- **Reader and task.** Name the reader, the task they come to this surface for, and how often they do it. A glance at status, close reading and repeated expert work each want a different density.
- **Content inventory.** List every fact the screen shows, its kind (name, time, count, status), and its realistic and extreme values (the longest name, zero items, 500 items, an error message). Get real data from the product, its fixtures or the user. If you don't know the content and it would change the design, ask.
- **Ranking.** Rank the facts by what the reader needs first and cut what they don't need. The ranking becomes the hierarchy.
- **States.** List the states in scope: empty, loading, partial, error, success, no permission, and the transitions between them.
- **Existing product.** If the screen already exists, open it in its host, screenshot the states you'll change, and read its components, tokens and spacing in source. Keep the product's existing decisions unless the user says otherwise.

Then run research.md and concept.md if you loaded them.

### 2. Compose

Lay out the content in rank order, starting from concept.md's layout if you have one:

- **Hierarchy.** Position, then size, then weight, then colour: the top-ranked fact gets the most prominent position.
- **Grouping.** Group with space and alignment: less space inside a group than between groups, from one spacing scale.
- **Alignment.** Few shared edges, and columns for facts readers compare across rows.
- **Density.** Screens for repeated expert use show more per line; occasional flows show one decision at a time.
- **Copy.** Headings name the section in the reader's terms, buttons name their effect ("Delete 3 branches"), and errors say what happened and what to do next.

### 3. Build

- **Components.** Use the product's components, tokens and typeface. Write a new one only when none fits, in the product's style.
- **Colour.** Use the product's palette. Without one, use neutrals and one accent with one job, such as the primary action or the selection. Use semantic colours only for state.
- **States.** Build every state from step 1 and the extreme content, not only the main path.
- **Access.** Make focus order follow reading order and give every control an accessible name.

### 4. Verify

1. **Render** in the surface it ships to, in each theme it supports and at each width it is used at, with typical and extreme content. Screenshot each. For a small change, cover only what it affects, and compare against your step 1 screenshots to catch regressions.
2. **Squint** at each screenshot. The eye should land on the top-ranked fact first and then follow the ranking; where it doesn't, fix position and size before adding emphasis.
3. **Exercise** it: tab through every control, read the accessibility tree for names and roles, trigger each state, and check that every number, status and promise on the screen matches real product behaviour.
4. **Run reference checks** from any docs you loaded.
5. **Remove slop** with eradicate-ui-slop's build procedure on the source and screenshots.
6. **Repeat** until these checks pass and further changes would only be taste.

### 5. Report

Say which themes, widths and states you checked and which you didn't, and include what each loaded doc asks you to report.
