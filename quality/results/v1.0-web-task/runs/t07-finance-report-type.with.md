Replace the 9 pt thin face with a semantic system-font hierarchy, render headings as text, and let the report reflow as text grows.

**Revised type specification**

The following sizes are proposed report defaults. iOS values describe the default Dynamic Type setting; production text must scale. Apple recommends legible weights, semantic styles, and platform-appropriate sizing. [Typography guidance](https://developer.apple.com/design/human-interface-guidelines/typography)

| Role | iOS | macOS | Treatment |
|---|---|---|---|
| Report title | Title 1, 28 pt | 22 pt | Bold; live text |
| Section heading | Title 2, 22 pt | 17 pt | Semibold; live text |
| Subsection / table header | Headline, 17 pt | 13 pt | Semibold |
| Narrative / row label | Body, 17 pt | 13 pt | Regular |
| Financial value | Body, 17 pt | 13 pt | Regular, tabular digits |
| Total / key result | Body, 17 pt | 13 pt | Semibold, tabular digits |
| Notes / reporting period | Footnote, 13 pt | 11 pt | Regular; essential disclosures retain body size |

- **Font:** Use the platform system font through native font APIs. Keep system tracking and natural line heights; use relaxed leading for long narrative passages. A retained custom font must provide legible weights, scaling, and equivalent accessibility behavior.
- **Headings:** Replace heading images with localized text and expose heading semantics to accessibility services.
- **Emphasis:** Use sentence case and selective semibold phrases. Give important findings a short heading and separate paragraph. Reserve capitals for established acronyms and currency codes.
- **Numbers:** Use tabular digits, right-aligned numeric columns, and consistent precision within each column. Align decimal separators where comparison requires it. Keep column widths stable during updates, reserving space for signs, separators, currency, and expected maximum values.
- **Expansion:** Allow headings and labels to wrap and rows to grow. Preserve complete amounts, signs, units, and periods. When columns no longer fit, switch to stacked, labeled records or an accessible scrollable table with clear header associations. Never shrink essential text to fit.
- **Platform sizing:** On iOS, support every Dynamic Type size and Bold Text. macOS has no Dynamic Type; provide a persistent report text-size control supporting at least 200%, with matching reflow. [Typography](https://developer.apple.com/design/human-interface-guidelines/typography), [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

**Acceptance checks**

| Check | Pass condition |
|---|---|
| Hierarchy | Title, sections, body, totals, and notes remain distinguishable at default and enlarged sizes. No thin 9 pt body text remains. |
| Live text | Every heading is rendered as text, scales cleanly, and exposes its heading role. |
| iOS enlargement | At every Dynamic Type size, including the largest accessibility size, with Bold Text on and off: no essential text clips, overlaps, or disappears. |
| macOS enlargement | At default, 150%, and 200% report text size, including the minimum supported window width: all content and actions remain reachable. |
| Value integrity | Large amounts, negative values, parentheses, currency symbols, percentages, and long localized labels remain complete and correctly associated. |
| Update stability | Repeated updates such as `111.11 → 888.88` and `999.99 → 1,000.00` keep column boundaries and numeric alignment anchors stationary. |
| Emphasis | No paragraphs use all caps for emphasis; key findings remain identifiable without relying on color. |
| Reading access | VoiceOver reads headings, row labels, column periods, amounts, currencies, and negative signs in meaningful order. |
| Readability | Check actual devices at normal reading distances, in light/dark appearances and Increase Contrast; all text meets the product’s measured contrast target. |

These are proposed acceptance criteria. The supplied description establishes the existing defects; implementation and runtime checks have **not been executed**.