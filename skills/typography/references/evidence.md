# Evidence and sources

Typography guidance mixes measurement, standards, type-designer specifications, and practitioner convention. When explaining a recommendation, say which kind supports it.

## What supports each claim

| Claim | Kind of support | Source |
| --- | --- | --- |
| Reading speed is flat above ≈0.2° x-height and falls sharply below it | Measured, many vision-science studies | Legge & Bigelow 2011 |
| 13px text is at or below that point at laptop distances | Derived from the above with stated geometry | dense-product-ui.md |
| Readability and comprehension improve with font size up to ≈18pt | Measured, one eye-tracking study on Wikipedia text | Rello, Pielot & Marcos 2016 |
| Line spacing between 0.8 and 1.8 has small effects | Measured, same study | Rello et al. 2016 |
| Leading should suit face, text, and measure; 120–145%; 1.4–1.55 for body | Practitioner guidance | Bringhurst 2.2.1; Butterick; design systems |
| 45–75 characters per line, 66 ideal | Practitioner guidance; studies mixed (longer lines can read faster, medium lines comprehend better) | Bringhurst 2.1.2; Dyson & Haselgrove 2001; Dyson 2004 |
| Screen body text should be larger than print | Argued from reading distance; consistent with the size research | Butterick; Reichenstein 2012 |
| Dark-on-light beats light-on-dark, more for small text | Measured (proofreading, acuity, pupil size) | Piepenbrock et al. 2013, 2014 |
| Light text on dark looks heavier | Widely reported perception, the basis for grade axes; not quantified in a study found | Google Fonts grade documentation |
| Pure white on black causes halation for astigmatic readers | Asserted; no study found | — |
| Serifs make no reliable difference to reading speed | Measured | Arditi & Cho 2005; Bernard et al. 2003 |
| Different fonts suit different readers | Measured | Wallace et al. 2022 |
| Justification slows reading | Measured only with uneven spacing, short lines, or crude algorithms | Gregory & Poulton 1970; Trollip & Sales 1986; Campbell 1981 |
| Lowercase reads ≈5–10% faster than all caps, through practice | Measured speed; explanation argued from the literature | Tinker 1963 via Larson 2004 |
| Slight letter-spacing increases aid word recognition; large ones hurt | Measured, narrow tasks | Perea et al. 2011; Chung 2002 |
| Larger x-height fonts are more legible at a given body size on screen | Measured (threshold legibility) | Sheedy et al. 2005, via Legge & Bigelow 2011 |
| Ratio scales produce harmony | Asserted | Brown 2011; Bringhurst 3.1.1 argues for a limited scale, not for perceived intervals |
| Size steps below ≈15% do not read as rank at UI sizes | Practitioner heuristic, consistent with Apple and Polaris ranking by weight | — |
| Tracking loosens at small sizes and tightens at large | Type-designer specification for specific fonts | Apple SF Pro tracking table; Inter Dynamic Metrics |
| Contrast, resize, spacing, and target-size thresholds | Normative standard | WCAG 2.2 |
| APCA size and weight thresholds | Draft method, not a standard | APCA documentation; WCAG 3 draft leaves the algorithm undetermined |
| `vw`-based fluid type can fail 1.4.4; max ≤ 2.5× min is sufficient | Demonstrated by measurement and algebra | Roselli 2019; Barvian 2023 |

## Books and guides

- Robert Bringhurst, *The Elements of Typographic Style*, 4th ed. (2012). Rules cited by number are quoted in Richard Rutter's adaptation, [The Elements of Typographic Style Applied to the Web](http://webtypography.net/).
- Richard Rutter, [*Web Typography*](https://book.webtypography.net/) (2017).
- Matthew Butterick, [*Practical Typography*](https://practicaltypography.com/): [key rules](https://practicaltypography.com/summary-of-key-rules.html), [line spacing](https://practicaltypography.com/line-spacing.html), [hyphenation](https://practicaltypography.com/hyphenation.html), [curly quotes](https://practicaltypography.com/straight-and-curly-quotes.html), [system fonts](https://practicaltypography.com/system-fonts.html), [websites](https://practicaltypography.com/websites.html).
- Tim Brown, [More Meaningful Typography](https://alistapart.com/article/more-meaningful-typography/) (2011) and [*Flexible Typesetting*](https://abookapart.com/products/flexible-typesetting) (2018).
- Jason Santa Maria, [*On Web Typography*](https://abookapart.com/products/on-web-typography) (2014).
- Ellen Lupton, *Thinking with Type*, 3rd ed. (2024).
- Spencer Mortensen, [The typographic scale](https://spencermortensen.com/articles/typographic-scale/).
- Oliver Reichenstein, [Responsive Typography: The Basics](https://ia.net/topics/responsive-typography-the-basics) (iA, 2012).
- [Tufte CSS](https://edwardtufte.github.io/tufte-css/); Gwern Branwen, [Sidenotes in web design](https://gwern.net/sidenote).

## Design systems (values read 2026-11-01)

- Apple [HIG Typography](https://developer.apple.com/design/human-interface-guidelines/typography).
- Material 3 [type scale tokens](https://m3.material.io/styles/typography/type-scale-tokens); [material-web `v0_192`](https://github.com/material-components/material-web/blob/main/tokens/versions/v0_192/_md-sys-typescale.scss).
- IBM Carbon [type sets](https://carbondesignsystem.com/elements/typography/type-sets/); [`@carbon/type` styles](https://github.com/carbon-design-system/carbon/blob/main/packages/type/src/styles.ts).
- Adobe Spectrum [typography](https://spectrum.adobe.com/page/typography/); [design data tokens](https://github.com/adobe/spectrum-design-data/blob/main/docs/markdown/tokens/typography.md).
- Shopify Polaris [typography](https://polaris.shopify.com/design/typography); [`polaris-tokens` font](https://github.com/Shopify/polaris/blob/main/polaris-tokens/src/themes/base/font.ts) and [text](https://github.com/Shopify/polaris/blob/main/polaris-tokens/src/themes/base/text.ts).
- Vercel [Geist typography](https://vercel.com/geist/typography).
- Tailwind [`theme.css`](https://github.com/tailwindlabs/tailwindcss/blob/main/packages/tailwindcss/theme.css).
- GitHub [Primer primitives](https://github.com/primer/primitives/blob/main/src/tokens/functional/typography/typography.json5).
- Inter [Dynamic Metrics (archived)](https://d.rsms.me/inter-website/v3/dynmetrics/).

## Research

- Legge & Bigelow (2011), [Does print size matter for reading?](https://jov.arvojournals.org/article.aspx?articleid=2191906) *Journal of Vision* 11(5):8.
- Rello, Pielot & Marcos (2016), [Make It Big!](https://dl.acm.org/doi/10.1145/2858036.2858204) CHI '16.
- Piepenbrock, Mayr, Mund & Buchner (2013), *Ergonomics* 56(7), [doi:10.1080/00140139.2013.790485](https://doi.org/10.1080/00140139.2013.790485); Piepenbrock, Mayr & Buchner (2014), [*Human Factors* 56(5)](https://journals.sagepub.com/doi/abs/10.1177/0018720813515509).
- Dyson & Haselgrove (2001), *IJHCS* 54, [doi:10.1006/ijhc.2001.0458](https://doi.org/10.1006/ijhc.2001.0458); Dyson (2004), How physical text layout affects reading from screen, *Behaviour & Information Technology* 23(6).
- Arditi & Cho (2005), Serifs and font legibility, *Vision Research* 45(23), doi:10.1016/j.visres.2005.06.013.
- Bernard, Chaparro, Mills & Halcomb (2003), [*IJHCS* 59(6)](https://dl.acm.org/doi/abs/10.1016/S1071-5819(03)00121-6).
- Wallace et al. (2022), [Towards individuated reading experiences](https://dl.acm.org/doi/10.1145/3502222), *ACM TOCHI* 29.
- Gregory & Poulton (1970), [Even versus uneven right-hand margins](https://www.tandfonline.com/doi/abs/10.1080/00140137008931157), *Ergonomics* 13(4); Trollip & Sales (1986), [Readability of computer-generated fill-justified text](https://doi.org/10.1177/001872088602800204), *Human Factors* 28(2); Campbell (1981), [A note on right-justification techniques](https://www.tandfonline.com/doi/abs/10.1080/00140138108924885), *Ergonomics* 24(8).
- Larson (2004), [The science of word recognition](https://www.microsoft.com/en-us/research/wp-content/uploads/2021/06/Larson-2005-the-science-of-word-recognition.pdf).
- Chung (2002), [letter spacing and reading speed](https://iovs.arvojournals.org/article.aspx?articleid=2200181), *IOVS* 43(4); Perea, Moret-Tatay & Gómez (2011), *Acta Psychologica* 137(3), [doi:10.1016/j.actpsy.2011.04.003](https://doi.org/10.1016/j.actpsy.2011.04.003).

## Standards and support

- WCAG 2.2 Understanding: [1.4.1](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html), [1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [1.4.4](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html), [1.4.12](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html), [2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html).
- [WCAG 3.0 draft](https://www.w3.org/TR/wcag-3.0/); [APCA Easy Intro](https://git.apcacontrast.com/documentation/APCAeasyIntro.html).
- [MDN browser-compat-data](https://github.com/mdn/browser-compat-data) for every support version quoted.
- Adrian Roselli, [Responsive Type and Zoom](https://adrianroselli.com/2019/12/responsive-type-and-zoom.html); Maxwell Barvian, [Addressing Accessibility Concerns With Using Fluid Type](https://www.smashingmagazine.com/2023/11/addressing-accessibility-concerns-fluid-type/); [Utopia](https://utopia.fyi/).
- [Google Fonts grade axis documentation](https://googlefonts.github.io/gf-docs/Grade/).
