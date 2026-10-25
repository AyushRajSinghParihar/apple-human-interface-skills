---
name: apple-hig-charts
description: Use when designing, reviewing, or adapting a chart's marks, scales, annotations, selection, or accessible data representation.
---

# Make the chart answer its question

Read [the chart guide](../../references/charts.md). The workflow below is application advice; distinguish its recommendations from the documented platform behavior.

Inspect the actual dataset and chart artifact, target platform, audience question, and requested create/review/adapt mode. Record units, missing observations, bounds, series, and any aggregation. Do not infer data accuracy from a screenshot or report invented outliers.

Choose marks from the comparison: bars for comparable quantities, lines for ordered time trends, points for individual observations/relationships. Decide scale and baseline together: bar lengths normally require zero; a meaningful variation far above zero can justify a bounded line scale with explicit bounds. Use fixed limits for inherently bounded quantities and dynamic limits only when their changing frame will remain understandable. Show the takeaway in words before requiring exploration.

Implement the chart or produce a concrete mark/axis/label specification; in review, attach corrections to the affected series, axis, or interaction. Add units, dates, and objective accessible values. Distinguish series beyond color and keep stacked segments separable. If tiny marks are hard to select, enlarge the interaction region or let selection scrub the plot. Define logical keyboard/assistive traversal and grouped detail for dense data. On watchOS, favor a glance and move extensive exploration to an available companion; do not promise Audio Graphs from an arbitrary framework merely because Swift Charts supplies defaults.

**Worked transformation:** Before: a monthly electricity chart uses truncated bars, unexplained red/green series, and no units. Decision: comparing consumed quantities requires honest lengths and noncolor identification. After: zero-baseline bars labeled in kWh, patterned/labelled household versus solar series, and a written monthly total; exact values are available through plot selection and accessible descriptions.

Deliver the edited artifact plus its question, scale rationale, and accessible overview. Verify against real rows, missing values, narrow widths, and selected points. Fail for misleading bar lengths, unlabeled units/bounds, lost series meaning without color, or critical facts available only by touch. Separate inspected accessibility structure from device/VoiceOver/Audio Graphs execution.

For analysis and dataset framing load [charting-data](../../../apple-hig-patterns/.topics/apple-hig-charting-data/SKILL.md); for broader access failures load [accessibility](../../../apple-hig-foundations/.topics/apple-hig-accessibility/SKILL.md).
