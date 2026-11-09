Use live text, semantic styles, and layouts that grow with the person’s text settings.

| Role | Revised type specification |
|---|---|
| Report title | System **Large Title**, bold. Use once per report. |
| Section heading | System **Title 2**, bold. Use for major sections such as “Cash flow.” |
| Subsection heading | System **Headline**, semibold. |
| Body and explanations | System **Body**, regular. Use the platform default size: typically 17 pt on iOS and 13 pt on macOS. |
| Financial values | Body-sized text with **tabular, monospaced digits**. Right-align amounts; align decimal places where practical. Use semibold for totals. |
| Table labels | Body, regular; semibold for column headings. Allow descriptive labels to wrap. |
| Supporting notes | System **Footnote**, regular, with sufficient contrast. Keep essential financial information at body size. |
| Emphasis | Sentence case with short semibold phrases, descriptive headings, or callouts. Reserve all caps for established abbreviations such as “USD.” |

Use native system text styles rather than forcing identical point sizes across platforms. On iOS, support Dynamic Type through every accessibility size. On macOS, respect system text-size settings where supported and provide report text scaling where needed. If a brand font is retained, use readable regular and semibold weights and scale it through platform text metrics.

Replace image headings with selectable, localizable text and expose their heading level to accessibility. Preserve branding through surrounding graphics.

Let rows and cells grow vertically. At larger text sizes or narrow widths, switch dense tables to a labeled, stacked presentation when needed. Keep every amount, sign, currency, and unit visible. Use horizontal scrolling only where the table’s column relationships need to remain intact.

Acceptance checks:

- **Hierarchy:** Title, section, subsection, body, and notes are visibly distinct on both platforms. VoiceOver identifies headings in a logical order.
- **Readability:** Essential content no longer uses thin 9 pt text. Regular body text remains readable in light and dark appearances.
- **Text scaling:** Test all iOS Dynamic Type sizes, including the largest accessibility size, plus supported macOS text settings and report scaling. No text clips, overlaps, or disappears.
- **Window sizes:** Test narrow iPhone layouts, iPad multitasking, and small macOS windows. Labels wrap and complete values remain accessible without truncation.
- **Stable numbers:** Update values such as `1,111.11` → `8,888.88`. Digits occupy equal widths and amounts retain their trailing alignment. Test negative values, larger digit counts, and localized separators.
- **Table integrity:** Currency, units, signs, decimal precision, and row/column associations remain clear in both table and stacked layouts.
- **Emphasis:** No paragraph relies on all caps or color alone to communicate importance.
- **Live text:** All headings can be selected, searched, localized, and read by VoiceOver.