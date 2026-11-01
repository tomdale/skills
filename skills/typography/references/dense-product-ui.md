# Dense product UI

Applies to text that people operate or scan inside an application at about 11–14px: app chrome, panels, inspectors, tables, menus, forms, and chat or agent reply columns. Design-system values below were read from each system's source tokens or live CSS on 2026-11-01.

## Constraints that set the numbers

Body size floor. Reading speed is roughly constant above an x-height of about 0.2° of visual angle and falls sharply below it (Legge & Bigelow 2011, the critical print size). On a 14" MacBook Pro at default scaling (1 CSS px ≈ 0.2mm), Inter (x-height 0.546em) gives:

| Size | 40cm | 50cm | 60cm |
| --- | --- | --- | --- |
| 11px | 0.17° | 0.14° | 0.12° |
| 12px | 0.19° | 0.15° | 0.13° |
| 13px | 0.20° | 0.16° | 0.14° |
| 14px | 0.22° | 0.18° | 0.15° |
| 16px | 0.25° | 0.20° | 0.17° |

So 13px prose is at or below the point where reading slows at laptop distances, and 11–12px suits glanceable text: labels, numbers, timestamps. Set wrapped prose at 13px or larger, and when a surface holds continuous reading (a chat column), offer 14px and 15px density settings. Recompute with the actual font's x-height; a smaller x-height lowers every value.

Dark mode. Dark-on-light outperforms light-on-dark in proofreading, and the gap grows as characters get smaller (Piepenbrock, Mayr & Buchner 2013, 2014). In dark themes keep prose at 7:1 or above, keep secondary text at 4.5:1 or above, avoid weights below 400, and lighten strokes with `GRAD` rather than by dropping contrast. On `#111111`, 4.5:1 starts near `#808080` and 7:1 near `#a0a0a0`; `#666666` is 3.3:1 and fails.

Measure. The panel sets the measure, and small type makes a given column relatively wide. At 13px, Inter averages about 6.1px per character in English prose, so a 400px column holds about 66 characters and a 480px column about 79. Cap prose width near 50ch with Inter (its `ch`, the width of "0", is about 1.35 average characters), and give long measures the looser line height.

## Single-line and wrapped text are different styles

Every mature dense system keeps a tight line height for single-line UI text and a looser one for wrapped prose at the same size:

| System | Single-line | Wrapped |
| --- | --- | --- |
| Vercel Geist | Label 13/16, Label 14/20 | Copy 13/18, Copy 14/20 |
| IBM Carbon | `body-compact-01` 14/18 (≤4 lines) | `body-01` 14/20 |
| Adobe Spectrum | Component M 14/18 | Body 1.5× |
| Apple macOS | Body 13/16 (controls) | (no prose style; Body is tuned for controls) |

Use about 1.2–1.3 for single-line text and 1.4–1.55 for wrapped text. Any element that can wrap uses the wrapped style.

## How dense systems rank text

They name more roles than sizes and rank with weight. Apple macOS Headline and Body are both 13/16, Bold vs Regular, and Footnote, Caption 1, and Caption 2 all use 10pt. Polaris `heading-sm` and `body-md` are both 13/20. Carbon `label-01` and `helper-text-01` are identical. Primer's small title is body-large size in semibold. A dense screen usually needs four to six sizes: one below body, body, and two or three heading steps.

## Reference values

| System (version) | Small → body | Headings | Tracking | Fits dense UI because / breaks because |
| --- | --- | --- | --- | --- |
| Apple macOS HIG (page updated 2025-12-16) | 10/13 Footnote, Captions; 11/14 Subheadline; 12/15 Callout; 13/16 Body | 13/16 Headline Bold; 15/20; 17/22; 22/26; 26/32 | SF Pro: +0.12pt at 10, 0 at 12, −0.08pt at 13, −0.15pt at 14 | Ranks by weight with 1pt fit steps; body line height suits controls, too tight for prose; no Dynamic Type on macOS |
| Shopify Polaris (`polaris-tokens` 9.4.2, archived) | 11/12, 12/16, 13/20 body, 14/20 | 12/16, 13/20, 14/20 semibold (650); 20/24, 24/32, 30/40, 36/48 bold | 0 to 14; −0.2px at 20–24, −0.54px at 36 | Inter at 13/20 with weights 450/550/650/700 is the closest analogue to a dense web app |
| Vercel Geist (live CSS) | Label 12/16, 13/16, 14/20; Copy 13/18, 14/20 ("most commonly used"), 16/24 | Heading 14/20 … 72/72, semibold | Headings −0.02em at 14–20, −0.04em at 24–32, −0.06em at 40+ | Label/Copy split and heading tracking transfer well; 13 and 14 both as body invite one-pixel adjacency |
| IBM Carbon (`@carbon/type` 11.70) | 12/16 label and helper; 14/18 compact; 14/20 body | 14/18 … 54/64; large productive headings in Light (300) | +0.32px at 12, +0.16px at 14 (IBM Plex) | Compact/long split; Plex-specific tracking; light large headings are thin on dark |
| Adobe Spectrum (design data 2026-06-17) | 10, 11, 12 (1px steps), 14 component, 16 body | 1.125 ratio from 14, rounded; heading LH ≈1.3 → 1.15 | 0em (Adobe Clean) | Component vs reading sizes; weak heading contrast from a small ratio |
| Material 3 (material-web `v0_192`) | 11/16 Label S, 12/16, 14/20 Body M | 14/20 … 57/64 | +0.4–0.5px at 11–12, +0.25px at 14 (Roboto) | Mobile-first 14–16sp; Roboto-only tracking; no 13px step |
| Tailwind (v4.3.3) | 12/16, 14/20, 16/24 | 18, 20, 24, 30, 36, 48+ | Flat em tokens independent of size | No 13px step, so dense products drift into arbitrary `text-[13px]` values |

Copy the structure (roles, the single-line/wrapped split, weight ranking) and recompute numbers for your font.

## Worked scale: 13px dark-mode chat column

Constraints: dark theme; reply column 400–520px; model-written Markdown with paragraphs, lists, up to six heading levels, inline and block code, tables, paths, timestamps, badges, and buttons; Inter 4 (variable, `opsz` 14–32, `tnum`, `zero`, no real small caps) with `ui-monospace` for code.

Upward steps from `13 · 2^(i/5)`: 14.93 → 15, 17.15 → 17, 19.70 → 20, 22.63 → 23. A reply heading above 17px competes with app titles, so 20 and up belong to the app chrome scale. Below body the ratio gives 11.3 and 9.9; metadata takes 12px instead (read in passing, separated by colour), and 11px is kept only for optional uppercase or tabular micro labels.

| Token | Role | Size / LH | Weight | Tracking | Notes |
| --- | --- | --- | --- | --- | --- |
| `text-body` | Prose, list items | 13 / 20 | 400 | 0 | `text-wrap: pretty`; max-width ≈50ch |
| `text-label` | Buttons, tabs, menu items, single-line values | 13 / 16 | 400 | 0 | `nowrap` with truncation; anything that wraps uses `text-body` |
| `text-heading-3` | h3–h6 in replies, card titles | 13 / 20 | 600 | 0 | Space above 16px, below 4px |
| `text-heading-2` | h2 in replies | 15 / 20 | 600 | 0 with `opsz`; −0.01em without | `text-wrap: balance`; space above 20px, below 8px |
| `text-heading-1` | h1 in replies, panel section titles | 17 / 22 | 600 | 0 with `opsz`; −0.015em without | `text-wrap: balance`; not the page `<h1>` |
| `text-meta` | Timestamps, model name, path captions, helper text | 12 / 16 | 400 | 0 | Secondary colour ≥4.5:1; `tabular-nums` for times and durations |
| `text-code` | Inline and block code | 12 / 20 inline, 12 / 18 block | 400 | 0 | Mono 1px smaller matches the sans x-height (Geist pairs Label 14 with Mono 13); blocks scroll horizontally |
| `text-numeric` | Table numbers, counters, token and cost counts | inherits | inherits | 0 | `tabular-nums`; right-align columns |
| `text-micro` (optional) | Badges, `kbd`, uppercase eyebrows | 11 / 14 | 500 | +0.06em uppercase | Three words or fewer; pad to 24px if clickable |

Five sizes (11, 12, 13, 15, 17) across 6px, each tied to a role and a second channel. Densities: 14px gives 12 meta, 14/20 body, 14/18 label, 16/22 h2, 18/24 h1, 13 mono; 15px gives 13, 15/22, 15/20, 17/24, 20/26, 14.

```css
:root {
  --text-body-size: 0.8125rem;  --text-body-lh: 1.25rem;    /* 13/20 */
  --text-label-lh: 1rem;                                     /* 13/16 */
  --text-meta-size: 0.75rem;    --text-meta-lh: 1rem;        /* 12/16 */
  --text-h2-size: 0.9375rem;    --text-h2-lh: 1.25rem;       /* 15/20 */
  --text-h1-size: 1.0625rem;    --text-h1-lh: 1.375rem;      /* 17/22 */
  --text-code-size: 0.75rem;
  --text-micro-size: 0.6875rem; --text-micro-lh: 0.875rem;   /* 11/14 */
}
.reply { font: 400 var(--text-body-size) / var(--text-body-lh) Inter, system-ui, sans-serif; }
.reply :is(p, li) { text-wrap: pretty; overflow-wrap: anywhere; }
.reply h1 { font-size: var(--text-h1-size); line-height: var(--text-h1-lh); font-weight: 600; text-wrap: balance; }
.reply h2 { font-size: var(--text-h2-size); line-height: var(--text-h2-lh); font-weight: 600; text-wrap: balance; }
.reply :is(h3, h4, h5, h6) { font: inherit; font-weight: 600; }
.reply :is(code, kbd, pre) { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: var(--text-code-size); }
.reply pre { line-height: 1.125rem; overflow-x: auto; }
.meta { font-size: var(--text-meta-size); line-height: var(--text-meta-lh); font-variant-numeric: tabular-nums; color: var(--fg-secondary); }
.micro { font-size: var(--text-micro-size); line-height: var(--text-micro-lh); font-weight: 500; }
.micro.caps { text-transform: uppercase; letter-spacing: 0.06em; }
.badge, .button { text-box: trim-both cap alphabetic; }
```

## Techniques specific to dense UI

- Optical centring: `text-box: trim-both cap alphabetic` (Chrome 133, Safari 18.2, Firefox 154) centres button, badge, and pill labels on their visible letters; older browsers fall back to normal leading.
- Icons: size to the label's line box (16px icon with a 13/16 label) and centre on cap height or x-height.
- Uppercase: legitimate for labels of one to three words (eyebrows, calendar day names, status pills, `kbd`) with 5–10% tracking; wrong for sentences and verb buttons.
- Small caps: Inter and Geist have no `smcp`, so `font-variant-caps: small-caps` makes shrunken capitals; set `font-synthesis-small-caps: none` and use uppercase with tracking instead.
- Figures: tabular for timestamps in lists, durations, counters, token and cost counts, diff stats, table columns; slashed zero (`zero`) for hashes in a proportional face.
- Model-written Markdown: map h4–h6 to the h3 style, cap reply headings at about 1.3× body, break long paths with `overflow-wrap: anywhere`, and scroll code blocks horizontally.
- Fluid sizing: product chrome uses discrete density settings (compact, default, comfortable) switched by a root custom property. Viewport width does not track reading distance, and interpolated sizes produce values nobody reviewed. Containers choose between discrete styles with `@container`, not interpolated sizes.

## Traps

- Several sizes within 2px doing the work of hierarchy. They read as mistakes; rank with weight and steps of 15% or more.
- Copying Material's or Carbon's positive small-size tracking onto Inter, SF Pro, or Geist.
- A muted grey that fails 4.5:1 on the dark surface.
- 13/16 used for wrapped prose, or 13/20 used for single-line controls.
- Bold-on-select in a font without `GRAD`, shifting the row.
- Treating the platform minimum (macOS 10pt, iOS 11pt) as a reading size.
- Arbitrary one-off sizes (`text-[13px]`, `font-size: 12.5px`) that bypass the tokens.

## Extra checks

- Render a reply holding six heading levels, a 120-character path, a wide table, a code block, and a timestamp list at the narrowest and widest column.
- Compare 13px, 14px, and 15px densities on the same reply.
- Check every secondary, placeholder, and disabled colour against the darkest and lightest surfaces it sits on.
