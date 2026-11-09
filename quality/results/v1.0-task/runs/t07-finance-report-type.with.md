Replace the 9 pt thin font with system typography, render headings as live text, and let the report reflow as text grows.

The following is a proposed product specification, informed by Apple’s [Typography](https://developer.apple.com/design/human-interface-guidelines/typography) and [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) guidance.

| Role | iOS, at default text size | macOS, baseline | Treatment |
|---|---|---|---|
| Report title | Title 1, 28 pt | 22 pt Bold | Live text; wraps |
| Section heading | Title 2, 22 pt | 17 pt Semibold | Live text with heading semantics |
| Table column heading | Headline, 17 pt | 13 pt Semibold | Sentence case; labels may wrap |
| Body and table values | Body, 17 pt Regular | 13 pt Regular | Primary readable content |
| Notes and sources | Footnote, 13 pt Regular | 11 pt Regular | Essential financial qualifications remain body size |
| Totals and key findings | Body, Semibold | 13 pt Semibold | Weight and spacing distinguish emphasis |

Use SF through system font APIs, with automatic tracking and natural line metrics. Use comfortable leading for paragraphs; avoid tight leading for passages of three or more lines. The macOS sizes above are product choices.

**Resizing and financial formatting**

- **iOS:** Use semantic text styles that follow every Dynamic Type size, including accessibility sizes, and honor Bold Text. The point sizes above are reference values, not fixed sizes.
- **macOS:** Use native font APIs and provide a persistent report text-size control supporting at least 200%. macOS does not provide Dynamic Type.
- **Layout:** Allow headings, labels, and rows to grow. When columns no longer fit, switch to stacked label–value rows, preserving period, currency, and column associations. Never shrink essential values to fit or truncate their digits.
- **Numbers:** Use tabular, monospaced digits rather than making all text monospaced. Align amounts to the trailing edge, or decimal separator where needed. Keep column widths stable during updates and reserve space for expected digits, signs, currency, and separators. Recalculate widths when text size changes.
- **Emphasis:** Replace all-caps paragraphs with sentence case and selective semibold phrases. Use a short descriptive heading for an important passage. Preserve standard acronyms and currency codes.

**Acceptance checks**

| Check | Pass condition |
|---|---|
| Default readability | Body renders at 17 pt on iOS and 13 pt on macOS with Regular weight; no thin 9 pt report text remains. |
| Heading replacement | Every heading is live, localizable text with appropriate heading semantics; no heading depends on an image. |
| iOS enlargement | At every Dynamic Type size, with Bold Text off and on, all labels, complete amounts, notes, and actions remain readable and reachable. |
| Mac enlargement | At 100%, 150%, and 200% report text size, including the smallest supported window, content reflows without clipping or overlap. |
| Numeric stability | Updates such as `111.11 → 888.88` preserve digit positions. `999.99 → 1,000.00` preserves the alignment anchor and neighboring columns without clipping. |
| Financial edge cases | Negative amounts, accounting parentheses, large totals, localized separators, and supported currencies retain every character and clear units. |
| Hierarchy and emphasis | Titles, sections, body, and notes remain distinguishable at enlarged sizes; no paragraph uses all caps for emphasis. |
| Accessible reading | VoiceOver identifies headings and associates each financial value with its row label, period, and currency. |
| Appearance | Text remains legible in light and dark appearances and with Increase Contrast; emphasis never depends on color alone. |

Based on your brief, the current design fails readability, heading presentation, enlargement, numeric stability, and emphasis checks. The revised specification’s runtime checks have **not been executed**.