---
name: eradicate-ui-slop
description: >
  Strip the tells that make agent-built UI look machine-made: middot chains,
  pills, eyebrow labels, cards in cards, gradients, mono metadata, emoji icons,
  invented numbers, and disclaimers inside mockups.
  Load before writing any UI, HTML mockup, wireframe, prototype, component,
  landing page, or Markdown whose layout is the deliverable (a bot's GitHub
  status comment, a rendered report), and again before showing it. Also use
  when a design looks generic, templated, AI-generated, or sloppy, or when
  asked to review UI for slop. Includes a scanner for the tells visible in
  source.
---

# Eradicate UI slop

These patterns mark UI as agent-built at a glance, and readers who spot them stop trusting the rest of the work. Every pattern in this file is banned in anything you produce or touch, except under the four exceptions below.

Remove a tell by deleting it or by restructuring the information it stood in for. Most slop is chrome filling the space where a decision about the information should have been, so deletion is the default fix. Swapping a tell for a cousin repeats it: `·` becomes `|`, `/` or `—`; a pill becomes a tinted span; an eyebrow becomes a small bold label; a card becomes a box with a hairline border.

## Exceptions

A banned pattern stays only when one of these holds:

1. The user asked for that pattern in this artifact.
2. You are editing an existing product that already uses that exact pattern in that exact place. Match it there; do not spread it.
3. You are reproducing third-party chrome exactly, such as GitHub's own timeline header. Content you write inside that chrome gets no exception.
4. The scanner matched something that is not the pattern, such as a monospace rule for a real code block or a `/` inside a file path.

"Compact", "conventional", "scans well", "fits the aesthetic" and "the design system allows it" are not exceptions. In source, mark each kept hit on its line with `slop-ok: <exception number> <reason>`. In your reply, list the exceptions you took.

## Scope and fidelity

- Build at the fidelity asked. A rough wireframe is grey boxes, real labels and plain system type, with no colour, shadow, icon or theme polish.
- Keep commentary out of the artifact: no "Simulation only", "illustrative", "stand-in", "design study", "not the real X", or legends explaining the mockup. Caveats go in your chat reply.
- Write no permanent help text, tips or explainer paragraphs about how the UI works: they cover for a screen whose labels and layout do not explain themselves. Change the screen. Field input formats, required legal or safety disclosures, and consequences of destructive actions stay.
- Use real content: the product's nouns, actual names and realistic data. Lorem ipsum, Acme, Jane Doe and "Project Alpha" are banned.

## Copy and punctuation

Middot chains. `·`, `•` and `&middot;` joining metadata pack facts of different kinds into one line at one weight. Decide what each fact is for. Delete what the reader does not need, put the primary fact in the sentence, and give each secondary fact its own position: a right-aligned column, a second line, a tooltip.

- Wrong: `Running · 1m` on every row of an "Active" section.
- Right: `1m` in a right-aligned column; the section heading already says the run is active.
- Wrong: `Reviewing · 39f36ab · 2 suggestions · 1 failed`
- Right: `Vercel Agent is reviewing 39f36ab.` with `One of 2 suggestions couldn't be posted.` on its own line.

Pipes, slashes, bullets and em dashes used as separators follow the same rule. `BB thread / simulated context` is a middot chain with a different glyph.

Also banned:

- Em dashes anywhere in UI copy, not only as separators: readers take them as the signature of model-written text. Use a period, a colon, or a second line.
- Label-and-count capsules such as `Concerns · 1` or a `Part 1 of 3` pill. Put the count in a sentence or heading, or delete it.
- Counts in headings such as `ACTIVE (3)` when the rows are visible. Keep a count only for collapsed or paginated content.
- A status word on each row that repeats the group heading.
- Tagline formulas: `Fast. Simple. Secure.`, `X, reimagined`, `Built for Y`, `Everything you need to Z`, `Meet X`, and the words supercharge, unlock, seamless, effortless, powerful, elevate and empower.
- Implementation vocabulary in place of outcomes. "Preparing the review", "reconciling findings" and "syncing state" describe the machine. Say what the reader gets: "Adding comments to your pull request."
- Invented numbers: percentages, `10x faster`, `18–38% more space`, user counts, uptime, ratings, testimonials, logo strips. Show a number only when it comes from real data you were given.
- Arrows and chevrons appended to links and buttons: `Learn more →`, `View all ›`.
- Emoji as icons or in headings, including ✨ for AI and 🚀 for launch.
- Title Case Buttons And Headings. Use sentence case.

## Visual

- Eyebrows: small uppercase letter-spaced text above a heading (`OVERVIEW`, `PART 1`, `ACTIVE`). Delete it or make the heading say it. Uppercase section labels anywhere count.
- Pills and badges on anything that is not a removable filter tag: counts, metadata, part numbers, "New", "Beta", suggestion chips. Use plain text in the right position.
- Cards: every section in a bordered rounded box, cards inside cards, the three-up icon-title-blurb feature grid, a stat row of big numbers over small labels. Group with spacing, alignment and type. A box goes only around something with its own behaviour, such as an independently saved form, a draggable item, or an embedded preview of another surface.
- Icon tiles: an icon in a tinted rounded square beside each heading or list item.
- Coloured left-border callouts (`border-left: 3px solid` in an accent).
- Gradients on backgrounds, buttons, borders or text (`background-clip: text`); glows; blurred colour blobs; noise overlays; glass panels (`backdrop-filter: blur`).
- Default palettes: Tailwind indigo, violet or purple as the accent (#6366f1, #8b5cf6, #7c3aed, #a855f7); near-black with neon green or cyan for developer tools; warm cream paper with a serif display face and a terracotta or rust accent for anything "thoughtful". Use the product's palette. With none, use neutral greys and one accent taken from the subject.
- Monospace for anything other than code, paths, SHAs and commands. Timestamps, counts, status words and section labels in mono are dressing up as technical.
- Fonts brought in for flavour: Space Grotesk, Instrument Serif, Fraunces, Playfair, DM Serif, Syne, Outfit, Sora, Clash or Cabinet Grotesk, and italic serif captions. Use the product's typeface or the system stack, and set the scale with the typography skill.
- Large radii and soft shadows everywhere (`rounded-2xl`, `shadow-xl`, 16–24px radius). Use one small radius, only on controls and real containers.
- Decorative motion: hover lift (`translateY(-2px)`), hover scale, pulsing status dots, shimmer, fade-in on scroll, animated gradients.
- Fake chrome: macOS traffic-light dots on code blocks, fake browser frames, fake terminal windows.
- The hero formula: giant centred headline, grey subhead, a primary and ghost button pair, a screenshot in a glowing frame, a "Trusted by" strip.
- Text under 11px, more than two grey levels of text, and muted text under 4.5:1 contrast.
- One state encoded three times: a coloured dot, a pill and a word. Use one encoding, plus text when colour alone would carry meaning.
- Keyboard-shortcut hints on controls nobody asked shortcuts for.

## Whole artifact

A standalone page follows the system theme with `color-scheme: light dark` and `prefers-color-scheme` styles, and has no theme toggle unless asked. The page and every component on it share that theme. Text columns have a max width and the page has margins.

## Procedure

1. Before writing UI, list what the reader must know and do on this screen, in priority order. Build only that, using the lists above as constraints.
2. Run the scanner on every file you created or changed: `python3 <this skill's directory>/scripts/slop-scan.py <files or directories>`. It reads HTML, CSS/SCSS/Less, JSX/TSX/MDX, Vue, Svelte, JS/TS and Markdown, reports unsupported files you name directly (directory walks skip unsupported types and node_modules, dist, build, out, coverage, vendor and dot-directories silently), prints `file:line rule excerpt` for each hit, and exits 1 if any unmarked hit remains. It sees source patterns only; step 4 covers the rest.
3. Fix every hit by deleting or restructuring, then rerun. Finish when it prints `clean`; it skips lines marked `slop-ok:`.
4. Render the result where readers will see it and screenshot it: pages and components with the browser tools in light and dark at the real container width; GitHub Markdown through `gh api markdown` in a page using GitHub's styles, or in a draft on GitHub itself. Check the screenshot against the Visual list for what source text cannot show: card nesting, hero formulas, triple-encoded state, competing emphasis, centred-everything. Fix and rescan.
5. Report the final scanner output and the exceptions taken.

When asked only to review existing UI, run the scanner and render the UI as in steps 2 and 4, skip the fixing and rescanning, and report each hit with the fix you would make.
