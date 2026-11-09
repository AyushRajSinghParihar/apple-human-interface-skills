# Finance report text specification

Platforms: iPhone (iOS) and Mac (macOS). The reading task is to identify the report and period, scan section totals, compare financial values, and read explanations. Preserve all report data, signs, currencies, precision, and update behavior. This specification replaces the former thin 9 pt custom font, image headings, clipping, shifting figures, and all-caps paragraphs. No implementation framework is supplied or prescribed.

## Text roles

Use the system font through platform font facilities, with automatic optical sizing/tracking. Render every heading as real text rather than an image. Keep heading strings available to accessibility and text resizing. Use sentence case for prose and headings; retain conventional acronyms and currency codes. Emphasize short meaningful phrases with semibold, rather than capitalizing whole paragraphs.

| Role | iPhone at default Large Dynamic Type | Mac at 100% report text size |
|---|---|---|
| Report title | Title 1, 28 pt, emphasized | System 22 pt Bold |
| Section heading | Title 2, 22 pt, emphasized | System 17 pt Semibold |
| Metric label / body explanation | Body, 17 pt Regular | System 13 pt Regular |
| Section total | Body, 17 pt emphasized | System 13 pt Semibold |
| Financial value | Body, 17 pt Regular; totals emphasized | System 13 pt Regular; totals Semibold |
| Period, units, source, update time | Footnote, 13 pt Regular | System 12 pt Regular |

The iPhone sizes are reference values, not fixed layout constraints: use semantic styles at every supported Dynamic Type category. Mac sizes are product choices; use standard system fonts and keep native controls at appropriate standard-control sizes. Do not treat the HIG minima (11 pt iOS, 10 pt macOS) as body targets. Use normal system leading, with loose leading for explanations of three or more lines. Maintain hierarchy through role, weight, grouping, and spacing as text grows.

## Enlargement and reflow

On iPhone, follow all Dynamic Type categories including the largest accessibility category; honor Bold Text without freezing fonts to the reference sizes. On Mac, provide a persistent Report text size setting from 100% to 200%, in 25% steps, scaling every report role proportionally; retain the selected value when reopening the report. macOS has no Dynamic Type. These are distinct platform accommodations.

Use content-sized heights. Titles, labels, and explanations wrap without line limits in the vertically scrolling report. Place period and update time on separate lines when needed. Keep content inside safe regions and the visible scrollable viewport. Do not shrink fonts, clip essential content, or use ellipses to fit financial values.

In a comparison layout, align labels at the leading edge and numeric columns at the trailing edge, with explicit period and currency/unit headers. Measure using the current font, weight, formatted data, and available content width. If all columns plus their labels and gaps cannot fit without truncation, switch the whole section to stacked records: metric label, then one labeled period/value pair per line, then explanation. Preserve record order and data across the transition. Re-evaluate on resize, text-setting change, and data updates; do not choose the arrangement solely from device type.

Within a stacked record, move a value below its period label if needed. If a single formatted value still exceeds the line width at the chosen size, give that value an independently horizontally scrollable, selectable full-text region with a visible overflow cue; keep its label and currency/unit context visible. Never split the digits into ambiguous wrapped fragments. This is a last-resort full-value route, not a replacement for normal reflow.

## Stable financial figures

Use tabular-width numerals in the system face for financial columns, preserving proportional text for prose. Keep consistent decimal precision within each metric as defined by its data format; retain signs and currency/unit context. Do not round, abbreviate, or change precision simply to fit.

Use a shared trailing anchor and stable column widths across updates. Reserve width for the widest formatted value in the metric's declared range, including sign, separators, currency, and decimal places. If no range is supplied, retain the largest width encountered for the current report session. If new data exceeds the reservation, grow the column or reflow the section without clipping; never compress the font. Tabular digits stabilize equal-length changes, while the trailing anchor and width reservation handle changing digit counts. Do not animate digit positions horizontally.

Use primary semantic text color for body, headings, and amounts; secondary text color only for supporting detail. Hierarchy must remain clear without color. Gains/losses retain explicit signs or descriptive wording even if color is added. Measure actual contrast in light/dark and Increase Contrast configurations before release; no contrast result is established by this document.

## Acceptance contract

1. All report headings are text; title, sections, body, values, and supporting detail follow the role table. No body text uses Thin or the former 9 pt style; paragraphs use sentence case.
2. On iPhone test every Dynamic Type category with Bold Text off/on; on Mac test every report-size step, including 200%. All data and context remain reachable, hierarchy persists, and rows grow without overlap.
3. Exercise content viewport widths of 320, 390, 600, and 1000 pt where the platform permits, plus intermediate resizing. These are product test fixtures, not Apple device support claims. Check short and long labels, explanations of at least three lines, negative values, and long currency-formatted amounts. Comparison layouts switch to labeled stacks before collision; the full-value overflow route works if needed.
4. Repeatedly update an amount from 1,111.11 to 8,888.88, then 999.99 to 1,000.00, and include a negative amount. Equal-length digits keep equal advances, trailing anchors stay fixed within the reserved column, neighboring columns stay stable until an explicit reflow, and no sign or digit disappears.
5. In an Apple runtime, verify headings and complete value/context text are exposed to accessibility, and that the reading task and any overflow region work with VoiceOver and keyboard navigation where supported. Record actual results rather than inferring them from this specification.

## Guidance basis

System styles, legible weights, hierarchy, leading, and platform differences follow [Typography — Ensuring legibility, Conveying hierarchy, Using system fonts, Supporting Dynamic Type, and macOS](https://developer.apple.com/design/human-interface-guidelines/typography). Enlargement and preference checks follow [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). Content-sized rows and width-dependent reflow follow [Layout — Adaptability](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability). These links identify the official sources of the installed local guides; they were not fetched for this task. Exact Mac role sizes, size-setting steps, numeric reservations, and test widths are product decisions, not universal Apple requirements.
