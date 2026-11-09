# Medical appointment chart audit

Scope: macOS; framework-agnostic review of `interface.md`, which is the sole interface evidence. Findings are verified against that written specification, not a rendered app. The task is to compare daily nonnegative appointment totals accurately and obtain exact counts without relying on color or sight.

## Ranked verified findings

Rank denotes impact on this comparison task, not a clinical risk assessment.

| Rank | Observed evidence and effect | Decision and source |
|---|---|---|
| 1 — High | Bars start at 48 for values 50 and 54. Their encoded lengths are 2 and 6, implying a threefold comparison instead of 1.08-fold. This distorts the main comparison. | Retain bars for totals, start at zero, use one shared linear scale. Zero makes bar lengths comparable; a bounded line scale is an alternative for a different question about variation, not the correction chosen here. [Charts: Axes](https://developer.apple.com/design/human-interface-guidelines/charts#Axes). |
| 2 — High | No textual values or accessibility description. Exact quantities and the chart's meaning have no supplied nonvisual equivalent. | Display exact counts, an objective takeaway, an accessible overview and individual observation values. Do not make exploration the only source of critical facts. [Charts: Descriptive content and accessibility](https://developer.apple.com/design/human-interface-guidelines/charts#Enhancing-the-accessibility-of-a-chart), [Charting data: Best practices](https://developer.apple.com/design/human-interface-guidelines/charting-data#Best-practices). |
| 3 — High | Red/green series have no other distinction. Series identity is lost when hue cannot be distinguished. | Pair actual series names with stable patterns and direct labels; color is supplementary. [Charts: Color](https://developer.apple.com/design/human-interface-guidelines/charts#Color), [Color: Inclusive color](https://developer.apple.com/design/human-interface-guidelines/color#Inclusive-color), [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |
| 4 — Medium | Both axes are unlabeled. Readers cannot establish units or the daily/category frame from the chart itself. | Label Y “Appointments per day (count)” and X “Date”; show explicit dates, series identities, range and numeric ticks. [Charts: Anatomy](https://developer.apple.com/design/human-interface-guidelines/charts#Anatomy). |

## Corrected behavior and decisions

Use title “Daily appointment totals,” not a claim about spare capacity or utilization. Although the request calls this a capacity chart, no capacity limit, booked/available definition, date range, or series meanings are supplied. Counts alone cannot establish those conclusions. This wording is an audit decision grounded in the available evidence, not an additional Apple rule.

Input contract: each observation contains an explicit date, a stable series identifier and human-readable name, and a nonnegative integer count or an explicit missing value. Preserve the source's daily aggregation; do not sum across series unless their relationship is known. Obtain actual dates and series meanings before publishing the chart. “Observation A/B” below are demonstration placeholders, not inferred categories or chronology.

Representation contract:

- Use vertical grouped bars if there are multiple series per date, ordered by date then stable series order. Every bar extends from zero on the same linear Y scale. For the supplied pair, use 0–60 with ticks 0, 10, 20, 30, 40, 50, 60. For other data, choose a readable upper bound at or above the maximum, retain zero and disclose range changes. Sixty is a display bound, not a capacity target.
- Show explicit dates on X, units on Y, series names and counts directly beside or above each bar. Distinguish series with named solid versus hatched fills and a matching key. Do not assign red/green a good/bad meaning without source semantics.
- Map text, background and grid to semantic roles supported by the actual framework; use readable primary text, a quiet background and subordinate grid lines. Map series identity to name plus pattern plus optional color. Custom palettes need light, dark and increased-contrast treatments. Honor the Mac user's accent for interactive controls if any are later added. No RGB values or contrast results are known. [Color: Best practices and macOS](https://developer.apple.com/design/human-interface-guidelines/color#macOS).
- Put the takeaway before the plot. Provide an accessible chart group with title, bar-chart type, axis meanings, displayed bounds, and summary; expose each observation with actual date, meaningful series name and count. Traverse chronologically then by series. Avoid reading redundant decorative ticks when their information is already represented. These are semantic requirements, not SDK API calls.
- Exact values remain visible and accessible without hover, pointer selection or color. If exploration is added, provide equivalent keyboard and assistive navigation with visible focus and consistent details. No existing controls, selection behavior or navigation are supplied, so none are asserted defective.
- At narrow widths or 200% text enlargement, reflow the chart and its labels or supply an equivalent fully labeled textual arrangement; never drop dates, identities or counts. This is a proposed acceptance condition, not a verified layout defect. [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

Framework-independent logic:

```text
validate each row: date and series meaning present; count is integer >= 0 or missing
sort by date, stable series order
baseline = 0
upper = readableBoundAtOrAbove(max(valid counts))   // sample: 60
for each valid row:
    barStart = baseline
    barEnd = row.count
    visibleLabel = date + seriesName + count + " appointments"
    accessibleObservation = {date, seriesName, count, unit: "appointments"}
for each missing row:
    show and expose "Data unavailable"; do not render a zero-height value
if no rows: show "No appointment data" rather than an unexplained empty plot
if all valid counts are zero: use a positive readable upper bound and label each zero
```

Missing/empty/all-zero rules are defensive design proposals; those states are not evidenced in the supplied interface. On update, keep names and pattern assignments stable and communicate changed values accessibly; do not rely solely on animation. Audio Graphs may be considered where the implementation supports them, but this contract does not assume Swift Charts or promise automatic Audio Graphs.

## Worked before/after

The two counts have no supplied dates or series mapping. Compare them as observations A and B only for this worked example.

| Measure | Before: baseline 48 | After: baseline 0 |
|---|---:|---:|
| A count / encoded length in data units | 50 / 2 | 50 / 50 |
| B count / encoded length in data units | 54 / 6 | 54 / 54 |
| B-to-A length ratio | 3.00 | 1.08 |
| Lengths in a 300-unit plot with corrected 0–60 scale | Not applicable | A: 250; B: 270 |

Corrected visible takeaway: “The two supplied daily totals are 50 and 54 appointments, a difference of 4. The larger total is 8% higher than the smaller.” This does not claim an increase over time, a trend, available appointments, or a capacity breach.

Example accessible overview: “Daily appointment totals. Bar chart. Horizontal axis: date; vertical axis: appointments per day, from 0 to 60. The two supplied totals are 50 and 54 appointments, a difference of 4.” Individual records must add the real date and series meaning before release. A summary alone is insufficient for accessing each value.

## Acceptance checks and evidence status

**Passed — static/computed only:** input establishes macOS, daily nonnegative totals and values 50/54. A local arithmetic calculation confirmed lengths 2/6 at baseline 48, ratios 3 and 1.08, difference 4, relative difference 8%, and corrected sample heights 250/270. The proposed sample scale includes both values and zero. These checks validate the worked specification, not a rendering.

**Failed — supplied specification:** zero-baseline bar comparison; labeled axes/units; exact textual values; accessible description; series identification independent of color. These are the verified findings above. Failure is established by the written description only.

**Not executed — implementation acceptance:**

1. Render sample counts with a common 0–60 scale; confirm zero starts, proportional heights, readable ticks, count labels and no clipping. Exercise zero, missing, all-zero and values over 60; missing must remain distinct from zero.
2. Replace placeholders with actual dates and series meanings; verify all labels, overview and observation values against real rows. Confirm no capacity or temporal claim exceeds those rows.
3. Remove hue: names and patterns must still identify every series. Measure actual foreground/background pairs in light, dark and Increase Contrast appearances using a contrast calculator and the local accessibility guide's applicable scope. No measured ratio is available in this audit.
4. At narrow widths and 200% text enlargement, confirm all essential information remains readable and reachable. No concrete window size or typography was supplied.
5. On a supported macOS implementation, use VoiceOver and Accessibility Inspector to confirm overview, objective per-observation values, logical order and lack of redundant ticks. Exercise keyboard, Full Keyboard Access and Switch Control for any interactive exploration; values must remain available without hover. No such runtime test occurred here.

## Evidence limits and instruction trail

Only `interface.md` and installed local guidance were used; no screenshot, source implementation, full dataset, executable app, SDK, GUI, color measurements or assistive-technology output was supplied. No device, Apple SDK, native rendering, VoiceOver or Audio Graphs execution is claimed. Medical context does not establish patient-data exposure or clinical harm, so neither is reported as a verified defect.

Explicitly read the installed `apple-hig/SKILL.md`, then Content and Foundations family routes; entered Charts, Accessibility and Color topic procedures before their respective source guides. Followed the Charts analysis route through the Patterns family and Charting data procedure before its guide. All were resolved within `.agents/skills/apple-hig/` and read one file per shell command. The official links above identify the local guides' sources; no web browsing or fresh verification occurred. The package describes its sources as a dated snapshot, not independently verified SDK documentation. No platform support or SDK feasibility claim is made.
