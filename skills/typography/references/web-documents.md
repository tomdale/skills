# Web documents

Applies to text people came to read continuously: essays, articles, documentation pages, reports, rendered long-form Markdown, and the prose sections of marketing pages. The goal is typography a book designer would accept: comfortable size and measure, an even texture, correct punctuation and figures, and hierarchy that guides without shouting. Browser support below comes from MDN's browser-compat data, read 2026-11-01.

## Size and measure

Body size: 16–21px on desktop. Screens are read from farther away than books, so screen body text is larger than print's 10–12pt (Butterick: 15–25px; Reichenstein, "Responsive Typography: The Basics"). Inter-sized x-heights reach the 0.2° critical print size at 50cm only at about 16px (see the dense supplement's table), and Rello et al. (2016) measured readability and comprehension improving up to 18pt. Use 1rem–1.125rem for documentation and 1.125rem–1.3rem for essays, and leave the root at `font-size: 100%` so the reader's default carries through.

Measure: 60–75 characters per line for a single column (Bringhurst 2.1.2: 45–75 acceptable, 66 ideal). Research is mixed: longer lines can be read faster while medium lines are comprehended better (Dyson & Haselgrove 2001; Dyson 2004). Set `max-width` in `em` or `ch` and check it with real text: `ch` is the width of "0", which in most text faces is wider than the average character, so 60ch usually holds 70–80 characters.

Line height: about 1.45–1.65 for body text at 16–21px, more for long measures, large x-heights, and sans faces; about 1.1–1.3 for headings. Butterick gives 120–145%; documents usually sit at or above his upper bound because screen measures run long. Measured effects of line spacing are small (Rello et al. 2016), so tune by eye with real paragraphs.

## Choosing typefaces

Serif vs sans makes no reliable difference to reading performance on screen (Arditi & Cho 2005 varied serifs alone and found no reading-speed effect; Bernard et al. 2003 found no objective difference between Times and Arial). Choose for voice and for features. Readers also differ: Wallace et al. (2022) found individuals read 35% faster in their fastest of five fonts than their slowest, with no font best for everyone.

A text face for documents has:

- A design for text sizes: moderate stroke contrast, open apertures, and spacing loose enough for 16–20px. An `opsz` axis that covers both text and display sizes is a strong advantage.
- A true italic, real small caps (`smcp`, `c2sc`), oldstyle and lining figures in proportional and tabular widths (`onum`, `lnum`, `pnum`, `tnum`), and fractions (`frac`). Check the font file; many web families omit small caps and oldstyle figures, and some hosted builds strip features.
- Weights you will use: regular, italic, a semibold or bold, and its italic.

Pairing: one superfamily (serif plus matching sans) or one text face plus a sans for headings and interface text, with x-heights close enough that inline mixes look the same size. Use at most two families plus a monospace. Match the monospace x-height with `font-size-adjust` (Chrome 127, Firefox, Safari 16.4) or a fixed 0.9em, measured against the body face.

System fonts are acceptable when performance matters more than voice. Butterick's system-font ranking puts Charter, Iowan Old Style, and Palatino among the tolerable serifs on Apple platforms and Georgia lower.

## Scale and headings

Documents can use larger steps than product UI because headings are fewer and space is available: about 1.2–1.33 per step, with at most three visible heading levels in a page. Butterick objects to doubling body size for emphasis; size, weight, and space together carry a heading.

- Space above a heading exceeds space below it, so the heading belongs to the text it introduces (for example two lines above, half a line below).
- Measure vertical space in units of the body line height (Bringhurst 2.2.2).
- Set headings with `text-wrap: balance` and `hyphens: none`. Tighten display sizes with the font's `opsz` or slight negative tracking; leave text sizes alone.
- Titles in all caps get 5–10% letterspacing (Bringhurst 2.1.6). Do not letterspace lowercase (2.1.7).

Worked scale for an essay, desktop, a text serif with `opsz`, small caps, and oldstyle figures, steps of `2^(1/3)` ≈ 1.26 from 18px:

| Role | Size / LH | Treatment |
| --- | --- | --- |
| Body | 18 / 28 | Regular; oldstyle proportional figures; `text-wrap: pretty`; measure 60–75 characters |
| Heading 3 | 18 / 28 | Semibold or italic, same size as body; 28px above, 7px below |
| Heading 2 | 23 / 28 | Semibold; 56px above, 14px below; `text-wrap: balance` |
| Title | 36 / 42 | Display optical size; 0 to −0.01em |
| Lede or standfirst | 23 / 32 | Regular or italic, below the title |
| Captions, footnotes, sidenotes | 15 / 22 | Regular; secondary colour at 4.5:1 or above |
| Code | matched x-height / 1.5 | Monospace with `font-size-adjust`; no ligatures, no hyphens |
| Small caps for acronyms | inherits | `font-variant-caps: all-small-caps; letter-spacing: 0.05em` |

For documentation at 16px, use steps of `2^(1/4)` ≈ 1.19: 16, 19, 23, 27, with h4 at body size in semibold and code at a matched x-height near 14px.

## Fluid sizing

Documents are where fluid sizing helps: the reader's distance and the column width change together from phone to desktop. Interpolate between two scales at two viewport widths (the Utopia approach) and let headings grow more than body text.

```css
/* Body 16px at 360px wide → 18px at 1280px wide; max/min = 1.125 */
html { font-size: 100%; }
body { font-size: clamp(1rem, 0.951rem + 0.217vw, 1.125rem); }
/* Optional: snap to whole pixels (round(): Chrome 125, Firefox 118, Safari 15.4) */
body { font-size: round(nearest, clamp(1rem, 0.951rem + 0.217vw, 1.125rem), 1px); }
```

Keep a `rem` term in every formula and the max at or below 2.5× the min, so text still reaches 200% under zoom (Barvian 2023), then test at 200% and 400% zoom in a 1024px and a 1600px window (Roselli 2019).

## Paragraphs, rag, and hyphenation

- Mark paragraphs with an indent of at least one en (Bringhurst 2.3.2, commonly 1em) or with space between them, never both. The opening paragraph after a heading is set flush (2.3.1).
- Set ragged right by default (2.1.3). Justify only with `hyphens: auto`, a correct `lang` attribute, a measure of at least about 60 characters, and a check of the result in each target browser. Studies that found justification slower traced the cost to uneven word spacing on short lines and crude spacing algorithms (Gregory & Poulton 1970; Trollip & Sales 1986; Campbell 1981 found proportional spacing faster than both).
- `hyphens: auto` needs `lang` (Chrome 55, Firefox 43, Safari 17). Leave at least two letters before a break and three after (Bringhurst 2.4.1): `hyphenate-limit-chars: 6 2 3` (Chrome 109, Firefox 137, not yet in Safari). Avoid more than three hyphenated lines in a row (2.4.3). Do not hyphenate headings, URLs, email addresses, or code.
- `text-wrap: pretty` on paragraphs. WebKit improves the rag across the whole paragraph; Chromium adjusts only the last four lines; Firefox ignores it.
- `orphans` and `widows` affect only paged and multi-column layout and Firefox ignores them; on screen, `text-wrap: pretty` handles one-word last lines.

## Microtypography

- Curly quotes and apostrophes, with the apostrophe pointing down even at the start of a word (’70s). En dashes for ranges, em dashes for breaks, a real ellipsis, × for dimensions, primes for feet and inches. Convert at build time with a tested converter (SmartyPants or equivalent) and never inside code.
- One space after a sentence (2.1.4). Non-breaking spaces between a number and its unit and in short expressions (2.4.6).
- Kerning and common ligatures stay on (browser defaults); discretionary ligatures stay off; ligatures off in code.
- Figures: oldstyle proportional in running text when the face has them; lining figures with capitals (3.2.1); tabular lining in tables.
- Acronyms in spaced small caps when the face has real small caps (3.2.2); otherwise leave them in capitals rather than synthesising small caps.
- Emphasis in italics; bold for rare strong emphasis; underline only for links.
- Hang opening quotation marks and list markers into the margin. `hanging-punctuation` works only in Safari, so use a negative `text-indent` or `::marker` positioning elsewhere.

## Links, notes, and block elements

- Links: an underline plus colour. Tune it with `text-decoration-thickness` and `text-underline-offset` (Chrome 87–89, Firefox 70, Safari 12.1) and keep `text-decoration-skip-ink: auto`. Colour alone needs 3:1 against surrounding text plus a non-colour cue on focus and hover (WCAG 1.4.1, technique G183).
- Notes: sidenotes beside the text on wide screens and toggled or end notes on narrow ones (Tufte CSS switches at 760px). Keep notes at a readable size (15px against an 18px body), not caption-tiny.
- Block quotations: extra lead before and after (2.3.3), set off by indent or a rule, with the opening quotation mark hung.
- Lists: markers hung or aligned consistently with the text edge; list text at body size and line height.
- Tables: tabular lining figures, numbers right-aligned, minimal horizontal rules, header alignment matching the column.
- Code blocks: monospace at matched x-height, line height about 1.5, horizontal scroll, no hyphenation.
- Figures and captions: caption style from the scale, set directly below the figure, at the text measure.
- Initial letters: `initial-letter` (Chrome 110, Safari with prefix, not Firefox) as progressive enhancement only.

## Dark mode for documents

Light text on dark looks heavier, so lower `GRAD` or keep weights at 400, and keep body contrast high (7:1 or above) because dark-on-light outperforms light-on-dark for reading (Piepenbrock et al. 2013, 2014). Off-white body text on a near-black background is common practice; the claim that pure white on black causes halation for astigmatic readers is widely repeated and unmeasured.

## Loading fonts without reflow

Serve WOFF2, subset to the scripts in use, and prefer one variable file over several statics. Use `font-display: swap` or `optional`, and give the fallback matching metrics with `@font-face` `size-adjust` (Chrome 92, Firefox 92, Safari 17), `ascent-override` (Chrome 87, Firefox 89, not yet in Safari stable), or `font-size-adjust`, so text does not shift when the webfont arrives.

## Traps

- Body text set in product sizes (13–14px) on a reading page.
- A column wider than about 80 characters because `max-width` was set in `px` for one font.
- Default browser headings at about 2× body, or more than three visible heading levels.
- Justified text without hyphenation, or on a narrow mobile column.
- Straight quotes, hyphens for dashes, double spaces, smart quotes inside code.
- Synthetic small caps, synthetic bold or italic from a family without those files (`font-synthesis: none` exposes missing styles during development).
- Fluid formulas built from `vw` alone.
- Relying on `orphans`/`widows` for screen layout.

## Extra checks

- Read a full real article at the narrowest phone width, a laptop width, and a wide desktop; count characters per line in each.
- Inspect the rag and hyphenation in every target browser with the page's real `lang`.
- Search the rendered text for straight quotes, `--`, `...`, and double spaces outside code.
- Confirm each OpenType feature the CSS requests exists in the served font file.
- Zoom to 200% and 400% at two window widths and confirm text doubles.
