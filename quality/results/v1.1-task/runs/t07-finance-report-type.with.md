Replace the 9 pt thin custom font with semantic system typography, render headings as live text, and let the report reflow as text grows.

**Revised type specification**

Sizes below are baseline points; iOS values refer to the default Large Dynamic Type setting. Use system font APIs rather than embedding SF font files.

| Role | iOS | macOS | Treatment |
|---|---|---|---|
| Report title | Title 1, 28 pt | Title 1, 22 pt | Bold; live text |
| Section heading | Title 2, 22 pt | Title 2, 17 pt | Bold; semantic heading |
| Subsection/table header | Headline, 17 pt | Headline, 13 pt | Platform headline weight |
| Body and table labels | Body, 17 pt | Body, 13 pt | Regular |
| Financial values | Body, 17 pt | Body, 13 pt | Regular, monospaced digits; semibold for totals |
| Supporting notes | Footnote, 13 pt | Callout, 12 pt | Regular; essential explanations stay body size |

These choices follow Apple’s [Typography guidance](https://developer.apple.com/design/human-interface-guidelines/typography); the role mapping is the proposed report design.

- **Headings:** Replace heading images with localized text and expose heading semantics. Keep titles and sections visually distinct at every text size.
- **Emphasis:** Use sentence case with selective semibold or bold words. Replace all-caps paragraphs with normal paragraphs and a short heading when needed. Preserve conventional capitalization for acronyms and currency codes.
- **Reading:** Use system leading and tracking; use looser leading for long or wide passages. Allow paragraphs and labels to wrap without fixed-height containers.
- **Financial alignment:** Enable tabular/monospaced digits, such as SwiftUI’s `.monospacedDigit()`. Align values by decimal separator, or right-align columns with consistent fractional precision. Reserve column width for expected amounts, currency symbols, and negative signs; keep that width stable during updates. Tabular digits alone won’t prevent movement when digit counts change.
- **Enlargement:** On iOS, use Dynamic Type through the largest accessibility size and honor Bold Text. On macOS, provide a persistent report text-size control supporting at least 200%; macOS has no Dynamic Type. Grow rows and stack each row’s labeled values when columns no longer fit. Keep complete amounts together and readable without shrinking or ellipses. This implements Apple’s [accessibility and enlargement guidance](https://developer.apple.com/design/human-interface-guidelines/accessibility).

**Acceptance checks**

All checks are **not done**; no implementation or running app was supplied.

| Check | Pass condition |
|---|---|
| Hierarchy | Title, sections, body, notes, and totals remain distinguishable at default and enlarged sizes. No heading uses an image. |
| iOS text sizes | Test every Dynamic Type category, including the largest accessibility size, with Bold Text off/on. No essential text clips, overlaps, disappears, or shrinks to fit. |
| macOS enlargement | At 100%, 150%, and 200%, including the minimum supported window width, the complete report remains readable and usable. |
| Reflow | At narrow widths and large text, rows grow or become labeled stacks; each amount retains its label, period, currency, and full precision. |
| Updating numbers | Exercise `111.11 → 888.88`, `999.99 → 1,000.00`, and positive-to-negative changes. Column anchors and decimal alignment remain stable; adjacent columns don’t move. |
| Emphasis | No prose paragraph uses all caps for emphasis. Totals and important statements remain identifiable without relying on color alone. |
| Assistive reading | On both platforms, VoiceOver identifies headings and reads each financial value with its row label, period, currency, and sign in a logical order. |
| Legibility | Review on actual devices in light/dark appearance and Increase Contrast. Body text and supporting notes remain readable at normal viewing distances. |