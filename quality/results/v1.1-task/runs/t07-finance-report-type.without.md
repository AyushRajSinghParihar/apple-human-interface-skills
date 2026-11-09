Use semantic text styles that scale with the person’s text-size settings. The specification below applies to iOS and macOS; point sizes are defaults, not fixed limits.

| Element | Revised type specification |
|---|---|
| Report title | Live text, system `.largeTitle`, bold. Allow wrapping. |
| Section headings | Live text, `.title2`, semibold. Use sentence case and expose heading semantics to accessibility. |
| Subheadings | Live text, `.headline`. Use sentence case. |
| Body and explanatory text | System `.body`, regular. Default is 17 pt on iOS and 13 pt on macOS. |
| Table labels and values | System `.body`, regular. Use semibold for totals. Apply monospaced digits to numeric values and align numeric columns to the trailing edge. |
| Supporting notes | System `.footnote`, regular. Keep essential financial information at body size. |
| Emphasis | Use short, sentence-case phrases in semibold, supported by spacing or a descriptive heading. Reserve all caps for established abbreviations such as USD. |

On iOS, use Dynamic Type throughout, including accessibility sizes. On macOS, use semantic system styles and respect supported system text-size settings; provide report zoom or text-size controls where needed. If retaining a custom font, choose a readable regular weight and scale it through platform text metrics.

Remove fixed text heights. Let labels and values wrap or rows grow. At larger sizes, adapt dense tables into stacked label–value rows or provide horizontal scrolling with clear row and column context. Keep full financial values visible, including signs, currency, decimal places, and units.

Monospaced digits prevent digit-width jitter. Keep column widths stable during updates as well; right alignment alone does not prevent movement when content changes width.

Acceptance checks:

- **Hierarchy:** Titles, sections, body, notes, and totals are distinguishable through size, weight, and spacing. Headings remain selectable, searchable text.
- **Scaling:** Test every iOS Dynamic Type size, including the largest accessibility size, and supported macOS text sizes and report zoom levels. No text clips, overlaps, or becomes inaccessible.
- **Financial accuracy:** Test long values, negative amounts, zero, currencies, and localized separators. Every sign, digit, decimal, and unit remains available.
- **Stable updates:** Update values repeatedly, including `111.11 → 888.88` and `999.99 → 1,000.00`. Numeric columns remain anchored, with no digit-width jitter or neighboring-column movement.
- **Accessibility:** VoiceOver identifies headings and reads table values with their row labels, column labels, and units.
- **Emphasis:** No full paragraphs use all caps. Important information remains identifiable without relying on color alone.