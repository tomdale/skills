---
name: typography
description: >
  Design or review a typographic system: type scales, font sizes, line height,
  letter-spacing, weights, figures, wrapping, and text hierarchy for the web.
  Use when choosing or fixing text styles for a product UI or a long-form web
  document, when sizes have been picked by eye, when hierarchy looks muddy or
  near-identical sizes compete, or when asked for a type scale, design tokens
  for text, or world-class reading typography. Routes to a dense product UI
  supplement or a web document supplement by scenario.
---

# Typography

A type scale is a short list of named text styles, each a complete bundle of size, line height, weight, tracking, figure style, and wrapping behavior, assigned to a role the content has. Sizes are one property of a style, and two roles may share a size. This skill gives the method that applies to every surface; the supplements give the numbers and techniques for each scenario.

## Route by scenario

Classify each region of the surface by its reading task, then read the matching supplement before choosing values.

- Dense product UI: text people operate or scan in passing, set at about 11–14px, with density as a constraint. App chrome, dashboards, inspectors, tables, chat and agent reply columns, panels, menus. Read [references/dense-product-ui.md](references/dense-product-ui.md).
- Web documents: text people came to read continuously, set at about 16–21px. Articles, essays, documentation pages, reports, rendered long-form Markdown, landing-page prose. Read [references/web-documents.md](references/web-documents.md).
- Mixed surfaces: a docs site has app chrome around a document column; an app may open a full-page reader view. Use the product supplement for the chrome and the document supplement for the reading column, and keep the two scales separate, sharing only family, colour roles, and weights.

A chat reply column is dense product UI even though it holds prose: it sits inside an app, at app sizes, beside controls. Offer a larger density setting rather than switching it to document sizes.

[references/evidence.md](references/evidence.md) records which recommendations rest on measurement, which on standards, and which are convention, with sources. Consult it before presenting a guideline to a user as research.

## Method

1. Read the real content, the font, and any existing tokens. Measure the font rather than assuming: x-height as a fraction of the em, average character width, which OpenType features exist (`tnum`, `onum`, `smcp`, `c2sc`, `zero`, `frac`), and which variable axes (`wght`, `opsz`, `GRAD`). fontTools reads these from the font file. Two fonts at the same `font-size` can differ visibly in apparent size.
2. Inventory roles from the content: body, single-line labels, metadata, heading levels actually used, code, numerals, captions, micro labels. Count only roles that occur.
3. Assign each distinction to a channel. Rank (heading vs body, heading levels) uses weight and size steps of roughly 15% or more. Primary vs secondary uses colour. Prose vs code uses family. Micro labels use case and tracking. Wrapped vs single-line uses line height. A size step smaller than about 15% does not read as rank; sizes 1px apart may coexist only when another channel already separates their roles.
4. Choose sizes. Fix the body size from the supplement. Generate heading candidates above it with a ratio, for example `f = body · 2^(i/5)` (≈1.149 per step, the ratio inside the classic printer's scale) or a larger ratio for documents. Round to whole pixels. Set the bottom of the scale from the legibility floor and the smallest role, not from the ratio; a ratio's values below body are rounded away.
5. Complete each style: a size/line-height pair, weight, tracking for this font at this size, figure style, wrapping, and spacing above and below. Store line heights as pairs with sizes, not one global ratio.
6. Write tokens in `rem` so the user's default font size and zoom scale the whole system. Give each role its own token even when two roles share metrics.
7. Verify with the checks below and the supplement's checks, on real content, in every supported theme and container width.

## Mechanics that apply everywhere

Line height depends on typeface, text, and measure: larger x-height, longer lines, and continuous reading need more; single-line labels and large headings need less. The ratio falls as size rises.

Tracking follows a per-font curve: looser below a font's design size, tighter above it. Fonts with an `opsz` axis apply much of this through optical size, and `font-optical-sizing: auto` is the browser default, so start at `letter-spacing: 0` and adjust after looking. Tracking values from a design system belong to that system's font; do not copy them across fonts. Letterspace all-caps and small caps 5–10%; leave lowercase alone.

Weight: rank needs a visible step, usually 400 to 600 for headings. Keep text at 400 or heavier below 16px. Weight changes glyph width unless the font has a `GRAD` axis, so bolding on hover or selection reflows neighbours; use grade, colour, an indicator, or reserved width. Light text on a dark background looks heavier than the same weight on light; lower `GRAD` where available, or avoid heavier-than-400 Regular mappings in dark mode.

Figures: tabular (`font-variant-numeric: tabular-nums`) where digits align in columns or change in place; proportional in prose. Set the figure style explicitly; fonts differ in their defaults.

Wrapping: `text-wrap: balance` for headings and short blocks (Chromium balances up to 6 lines); `text-wrap: pretty` for paragraphs (Chrome 117, Safari 26, ignored by Firefox); `overflow-wrap: anywhere` where long URLs, paths, or identifiers meet narrow columns. Never hyphenate code, URLs, or headings.

Contrast and accessibility (WCAG 2.2, the normative standard): 4.5:1 for normal text, including metadata and placeholders; 3:1 for large text, which starts at 24px regular or 18.67px bold. Text must reach 200% under zoom (1.4.4) and survive user overrides of line height 1.5, paragraph spacing 2×, letter spacing 0.12em, and word spacing 0.16em without clipping (1.4.12); fixed-height boxes with `overflow: hidden` are the usual failure. Click targets need 24×24 CSS px or equivalent spacing (2.5.8); inline links are exempt. WCAG sets no minimum font size. APCA thresholds are a useful second opinion, but APCA is not a standard.

Fluid sizing with `clamp()` and `vw` or `cqi`: viewport terms shrink as users zoom, which can stop text from doubling. Include a `rem` term, keep max ≤ 2.5× min, and test at 200% and 400% zoom. The supplements say where fluid sizing belongs.

## Verify

- Rank test: set every size to the body size in dev tools. If the structure still reads, rank lives in weight and colour, and the other sizes only fit text into place.
- Inventory test: list every `font-size`, `line-height`, and `letter-spacing` in the built CSS and remove values outside the token set.
- Zoom and default-size test: zoom to 200%, then set the browser default font size to 20px; all text grows in both.
- Spacing test: apply the 1.4.12 overrides and check that nothing clips.
- Contrast test: every foreground/background pair in every theme, including secondary, disabled, placeholder, link, and code backgrounds.
- Content test: render real content with the longest strings, every heading level in use, tables, code, and numbers, at the narrowest and widest supported containers. Specimen pages hide the failures.

Report the role inventory, the scale as a table, and which choices follow evidence, standards, or convention.
