Replace the 9 pt thin font with a readable system type hierarchy, render headings as text, and let the report grow with the reader’s text size.

**Revised type specification**

Use the system font on both platforms. The sizes below are proposed default design tokens; iOS sizes scale with Dynamic Type rather than remaining fixed. Semantic text styles provide the basis for this scaling. [Apple’s scaling guidance](https://developer.apple.com/documentation/uikit/scaling-fonts-automatically)

| Role | iOS default | macOS default | Treatment |
|---|---|---|---|
| Report title | Large Title, 34 pt | 26 pt | Bold; sentence case |
| Section heading | Title 2, 22 pt | 20 pt | Semibold; live text with heading semantics |
| Subheading | Headline, 17 pt | 15 pt | Semibold |
| Body and table values | Body, 17 pt | 13 pt | Regular |
| Supporting notes | Footnote, 13 pt | 11 pt | Regular; essential information stays body-sized |
| Totals and key figures | Body, 17 pt | 13 pt | Semibold; spacing or a rule reinforces grouping |

- **Scaling:** Support every iOS Dynamic Type size, including accessibility sizes. On macOS, support applicable system text-size preferences and provide report text enlargement. Scale spacing and row heights with text; avoid fixed-height text containers and shrinking text to fit.
- **Headings:** Replace heading images with native text. Preserve wording, localization, selection, and accessibility heading navigation.
- **Financial tables:** Use tabular digits, such as SwiftUI’s `.monospacedDigit()`, with trailing or decimal alignment. Keep column widths stable during updates; tabular digits alone do not prevent movement when values gain digits. Use consistent currency and precision rules. [Apple’s digit-spacing API](https://developer.apple.com/documentation/swiftui/view/monospaceddigit())
- **Large-text layout:** Wrap labels and increase row height. When columns no longer fit, use stacked records with explicit labels, or an accessible horizontally scrollable table where comparison requires columns. Keep complete amounts, signs, currencies, and units visible.
- **Emphasis:** Replace all-caps paragraphs with sentence-case text. Use short semibold phrases, headings, and spacing. Reserve capitals for conventional abbreviations such as USD; never rely on color alone.

**Acceptance checks**

- [ ] Title, sections, body, notes, and totals are visibly distinguishable on both platforms; no report text uses thin weight or the former 9 pt body style.
- [ ] Every heading is live text, localizes correctly, and appears in VoiceOver heading navigation.
- [ ] At every iOS text size, including the largest accessibility size, no content clips, overlaps, or becomes inaccessible. Repeat with Bold Text enabled.
- [ ] On macOS, test the smallest supported window and maximum supported text enlargement; all report content remains reachable and readable.
- [ ] Long labels and large, negative, zero, and fractional amounts remain complete. Test supported locales with different currency placement and separators.
- [ ] During repeated value updates, column boundaries and decimal anchors remain stable, including transitions such as `999.99 → 1,000.00`.
- [ ] At large text sizes, each value retains an unambiguous row label, column label, currency, and unit; VoiceOver conveys those relationships.
- [ ] No paragraph uses all caps for emphasis. Hierarchy and emphasis remain understandable in grayscale.