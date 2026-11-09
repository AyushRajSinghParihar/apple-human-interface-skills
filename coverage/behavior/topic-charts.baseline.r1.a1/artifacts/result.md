# Medical appointment chart audit

Scope: macOS; specification review of [interface.md](interface.md). The task is to compare daily nonnegative appointment totals accurately. No screenshot, executable interface, dataset, dates, series definitions, or capacity limit was supplied. Findings below are verified against the supplied specification, not a running interface.

## Ranked findings and decisions

Ranks reflect likely impact on interpreting the counts; they are audit judgments, not Apple severity ratings.

| Rank | Verified finding and effect | Correction and source basis |
|---|---|---|
| 1 — High | Bars start at 48, exaggerating 50 versus 54 appointments. Length is an unreliable representation of relative totals. | Keep bars for daily accumulated quantities; use a linear count axis starting at 0. The Charts guidance says a zero baseline makes bar lengths comparable. This decision follows the mark and task; it is not a rule that every chart must start at zero. [Charts: Marks and Axes](https://developer.apple.com/design/human-interface-guidelines/charts#Axes). |
| 2 — High | No textual values or accessibility description: exact counts and the comparison are unavailable through the supplied nonvisual representation. | Show exact values and a short objective takeaway. Provide a chart description and accessible observations with date, meaningful series name, count, and unit. Without Audio Graphs, describe chart type, axis meanings, and bounds explicitly. [Charts: Descriptive content and accessibility](https://developer.apple.com/design/human-interface-guidelines/charts#Enhancing-the-accessibility-of-a-chart). |
| 3 — High | Red/green is the only series distinction. People unable to distinguish those colors cannot reliably identify series. | Pair color with distinct patterns and explicit series labels; make the legend match both encodings. Use meaningful series names rather than color names. [Charts: Color](https://developer.apple.com/design/human-interface-guidelines/charts#Color); [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |
| 4 — Medium | Axes are unlabeled, leaving the categories and measured quantity unclear. | Label the count axis “Appointments per day” and the category axis “Date” when dates are confirmed; show explicit dates and familiar ticks. Label the series directly or supply a legend. [Charts: Anatomy](https://developer.apple.com/design/human-interface-guidelines/charts#Anatomy), [Axes](https://developer.apple.com/design/human-interface-guidelines/charts#Axes). |

These issues compound: accessible numbers alone do not repair misleading visual lengths, and a zero baseline alone does not identify series or dates.

## Corrected behavior specification

Framework-agnostic design decisions:

- Use the title “Daily appointment totals.” Do not describe utilization, remaining slots, overload, or available capacity until a documented capacity denominator and compatible scope are supplied. This is a data-integrity decision, not a separate HIG violation proven by the input.
- Require each production observation to include an explicit date, a stable series identifier, a meaningful series label, and a nonnegative integer count. Do not infer dates, series meanings, or chronological order from the two supplied numbers.
- Plot grouped bars when multiple series share a date. Give each series a consistent pattern, color, and labeled legend entry. Put the exact count adjacent to each bar; retain it in a visible text table if space is constrained. Do not make hover or selection the sole route to values.
- Start the count scale at 0. Choose a rounded upper bound at least as large as the maximum count, using familiar intervals. Use 0–60 with ticks every 10 for the worked example. Use a nonzero upper bound for an all-zero dataset. Never map missing data to zero; show an explicit unavailable state.
- Provide a persistent takeaway and an accessible chart overview followed by observations in date order, then consistent series order within each date. Include the same information in a visible table with Date, Series, and Appointments columns. Avoid duplicating decorative ticks in assistive traversal when the overview and observations already convey them.
- If inspection controls are introduced, support predictable keyboard focus and operation, not pointer-only hover. No interaction is necessary to read this small comparison. Consider Audio Graphs where the chosen implementation supports them; no Apple SDK is assumed or required by this specification. [Charts: Best practices](https://developer.apple.com/design/human-interface-guidelines/charts#Best-practices).

Illustrative pseudocode:

```text
validate observations: date, seriesId, seriesLabel, integer count >= 0
if no observations: show “No appointment totals available”; do not draw zero bars
maxCount = maximum(observation.count)
axisMin = 0
axisMax = roundedBound(maxCount)  // >= maxCount; > 0 even if all counts are zero
barHeight(count) = plotHeight * count / axisMax
render count axis, dated category labels, pattern-and-color series legend
render bars with exact count labels
render objective takeaway and visible data table
expose overview(chart type, axis meanings, bounds, takeaway)
expose observations(date, series meaning, count + “appointments”)
```

## Worked before/after

The values are supplied; their dates and series associations are not. “Observation A/B” below are audit placeholders only, not proposed production labels.

| | Before: baseline 48 | After: baseline 0, upper bound 60 |
|---|---|---|
| Observation A: 50 | Visible length = 50 − 48 = 2 | Height = 50/60 = 83.33% of plot |
| Observation B: 54 | Visible length = 54 − 48 = 6 | Height = 54/60 = 90% of plot |
| Apparent ratio | 6/2 = 3× | 54/50 = 1.08× |

Corrected visible takeaway: “The two reported daily totals are 50 and 54 appointments, a difference of 4 appointments. 54 is 8% higher than 50.” This does not assert a time trend or a capacity shortfall.

Accessible overview for this limited example: “Bar chart comparing two reported daily appointment totals. Category axis: observations; dates and series meanings were not supplied. Count axis: appointments per day, from 0 to 60. Totals are 50 and 54 appointments; difference 4.” Individual entries: “Observation A, 50 appointments”; “Observation B, 54 appointments.” Production content must replace these placeholders with actual dates and meaningful series names before release.

## Acceptance checks

These are implementation acceptance criteria, not claims of executed tests.

1. With counts 50 and 54, the axis starts at 0, ends at 60, and shows ticks 0, 10, …, 60. Bar heights have ratio 1.08 within rendering tolerance, with exact labels 50 and 54; the text difference is 4 and relative increase is 8% using 50 as denominator.
2. With confirmed data, the title, axis meanings, explicit dates, units, and meaningful series names are visible. No unsupported capacity or trend claim appears. Missing dates or series meanings are surfaced for correction rather than invented.
3. In grayscale and with colors indistinguishable, every series remains identifiable by pattern and labels, including the legend. Check the rendered result for pattern legibility; passing cannot be inferred from this document.
4. Reading visible text or the accessible representation yields all counts and the main comparison without hover. The accessible overview states chart type, axes, and bounds when Audio Graphs are absent. Observations traverse in logical order, without redundant decorative tick announcements.
5. On a macOS implementation, manually verify VoiceOver output and any keyboard interaction. Verify text enlargement to 200% preserves readable labels, values, and table access; check light/dark appearance and Increase Contrast using measured contrast. These broader checks follow [Accessibility: Vision and Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision); no contrast or sizing defect is verified by the supplied text.
6. Empty data shows an unavailable state; zero is represented as a true zero with a readable value; missing counts remain missing; negative counts fail validation. Larger valid totals expand the upper bound without clipping and preserve the zero baseline. These are proposed robustness checks.

## Evidence and limits

Read the installed root `apple-hig/SKILL.md` first, then routed to `subskills/apple-hig-content/SKILL.md` and its `references/charts.md`. Also read `subskills/apple-hig-foundations/SKILL.md` and its `references/accessibility.md`; consulted the root `references/topic-index.md` for exact topic paths. These families route directly to article references and supplied no additional topic procedure. All paths resolve inside `.agents/skills/apple-hig/`; each file was read in a separate shell command.

The local Charts snapshot is dated 2026-10-25; Accessibility records retrieval on 2026-10-25. Official links above identify the source guidance; they were not browsed or independently reverified. Shared chart guidance applies here; the local Charts article states no separate macOS rules. No Swift Charts behavior, SDK availability, or automatic accessibility support is assumed.

Only the specification and installed instructions were inspected. No screenshot, device, GUI, SDK, accessibility tree, VoiceOver session, contrast measurement, or rendered layout was tested. Actual font size, palette contrast, clipping, focus behavior, legend presence, data provenance, and capacity semantics remain unverified. The worked arithmetic was checked from the supplied numbers; the remaining acceptance checks require implementation evidence.
