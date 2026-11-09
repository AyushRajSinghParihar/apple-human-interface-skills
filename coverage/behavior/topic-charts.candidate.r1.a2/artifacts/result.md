# Medical appointment chart audit

Scope: macOS; framework-agnostic review of `interface.md`. The supplied prose is the interface evidence, not a rendered chart. “Verified” below means explicitly stated in that specification. The task is to compare daily nonnegative appointment totals accurately. Capacity utilization cannot be determined without a capacity denominator.

## Ranked verified findings

Priority reflects this review's assessment of task impact, not an Apple severity scheme.

| Rank | Verified problem and effect | Correction and source support |
|---|---|---|
| 1 — High | Bars begin at 48, exaggerating 50 versus 54. Length is no longer proportional to the daily total and can mislead planning. | Begin all bars at zero on a shared linear scale. Bars suit accumulated daily quantities; zero makes their lengths comparable. [Charts: Marks and Axes](https://developer.apple.com/design/human-interface-guidelines/charts#Axes). |
| 2 — High | No textual values or accessibility description. Exact totals and the comparison have no supplied nonvisual equivalent. | Show exact counts persistently, provide a concise chart overview and accessible per-observation values. A summary alone does not replace value access. [Charts: Enhancing accessibility](https://developer.apple.com/design/human-interface-guidelines/charts#Enhancing-the-accessibility-of-a-chart), [Charting data: Best practices](https://developer.apple.com/design/human-interface-guidelines/charting-data#Best-practices). |
| 3 — High | Red/green series have no other distinction. Series identity disappears for people who cannot distinguish those hues. | Pair each actual series name with a stable pattern, such as solid versus diagonal hatch, in marks and legend; include the name with each value. Color can remain supplemental. [Charts: Color](https://developer.apple.com/design/human-interface-guidelines/charts#Color), [Color: Inclusive color](https://developer.apple.com/design/human-interface-guidelines/color#Inclusive-color). |
| 4 — Medium | Axes are unlabeled, obscuring the variables and unit. | Label X “Date” with explicit dates and Y “Appointments per day” with integer ticks. Add a descriptive title and date range. [Charts: Anatomy and Descriptive content](https://developer.apple.com/design/human-interface-guidelines/charts#Descriptive-content). |

Ranks 2 and 3 can block access entirely. Rank 1 affects the central magnitude comparison for everyone relying on bar lengths. No contrast failure, missing keyboard implementation, or misleading series *name* is verified: those details were not supplied.

## Corrected representation and decisions

Retain bars because the supplied task compares accumulated daily counts. For multiple series on a date, use adjacent bars sharing zero; do not stack potentially overlapping totals or assume they are additive. Keep chronological dates and a stable series order. Actual dates, series identities, whether 50 and 54 belong to different dates or series, and aggregation provenance remain unknown. Resolve them from the real data before release; do not ship invented labels.

Title: “Daily appointment totals”, with the actual date range. Do not title this “Capacity utilization” or infer spare slots, overload, staffing needs, or a safe capacity threshold. These are product/data decisions, not HIG rules. If capacity is later supplied, define its unit and matching date/series scope before comparing it with totals.

Use a shared Y range of 0–60 for the worked 50/54 example, ticks every 10 appointments. This upper limit is a proposed readable headroom choice, not a measured capacity or an Apple requirement. For other data, select a rounded upper bound at or above the maximum; preserve zero. Use the same range for simultaneous comparable panels, and explain scale changes across views. Do not use a broken axis or replace bars with a narrowly bounded line just to magnify this difference.

Place each exact count above its bar. Include an adjacent plain-text value list for every observation: explicit date, actual series name, count and unit. Keep the list available without hover or selection. A zero is a recorded count and must read “0 appointments”; a missing observation reads “Not available” and must not render as zero. An empty dataset reads “No appointment data available.” These missing/empty states are proposed robustness requirements, not observed defects.

Use semantic foreground/background roles appropriate to the host framework; map to macOS adaptive roles where available without requiring NSColor or another Apple SDK. Keep explanatory text neutral and series color separate from action accents. Supply light, dark and increased-contrast treatments if colors are custom, and retain patterns and names in all appearances. No numeric palette or contrast result is asserted. [Color: Best practices and macOS](https://developer.apple.com/design/human-interface-guidelines/color#macOS).

Accessible overview: chart type, purpose, date range, X meaning, Y meaning and bounds, followed by an objective takeaway. Without an implemented Audio Graphs facility, explicitly include the axis bounds. Expose each observation with date, series meaning and exact appointment count. Follow chronological date then stable series order; avoid duplicate announcements of decorative ticks where the equivalent information is already exposed. Do not announce identities as “red” and “green.” No Audio Graphs support is assumed. [Charts: Accessibility](https://developer.apple.com/design/human-interface-guidelines/charts#Enhancing-the-accessibility-of-a-chart).

No controls or interactions are described in the supplied interface, so none can be verified or mapped as an observed button, picker or menu. Value access in this correction requires no chart gesture. If interactive inspection is added, define reachable keyboard focus, pointer and assistive navigation to the same values in the same order, with a visible focus indication and no hover-only facts. Chart-level guidance supports these checks; actual keyboard behavior remains untested. [Charts: Best practices](https://developer.apple.com/design/human-interface-guidelines/charts#Best-practices).

## Worked before/after

The two supplied counts form a comparison example; their dates and series membership are not known.

| Property | Before, as specified | After, proposed |
|---|---|---|
| Values | 50 and 54 appointments, not printed | “50 appointments” and “54 appointments” printed and available as text |
| Baseline | 48 | 0 |
| Relative visible lengths on a linear scale | 50 − 48 = 2; 54 − 48 = 6; ratio 3:1 | 50 and 54; ratio 1.08:1 |
| Example plot height of 240 units | Upper bound unknown; absolute heights cannot be computed | With 0–60 domain: 200 and 216 units tall |
| Comparison | Magnitude exaggerated | Difference = 4 appointments; 54 is 8% higher than 50 |
| Identity/context | Unlabeled axes; hue-only series | Actual date and series name, unit, stable pattern, matching legend |

Example overview wording, after binding real labels: “Daily appointment totals. Bar chart. Horizontal axis: dates [actual range]. Vertical axis: appointments per day, 0 to 60. [Actual observation label] has 54 appointments, 4 more than [actual comparison label] at 50.” Bracketed text is a specification placeholder, not production copy. Do not say “increased” unless the real dates establish time order; do not sum the two values without confirming disjoint groups.

```text
require each observed count is a nonnegative integer
require real date and series identity for every observation
observed = records with known counts
upper = roundedReadableBound(max(observed.count))  // 60 for example
if all known counts are zero: upper = positiveReadableBound()
domain = [0, upper]
for date in chronological order:
    for series in stable order:
        if count is missing:
            expose date, series.name, "Not available"; draw no quantity bar
        else:
            bar.height = plotHeight * count / upper
            bar.baseline = zero
            bar.pattern = stablePattern(series)
            show count and expose date, series.name, count, "appointments"
render overview, labeled axes, named/patterned legend, plain-text values
```

## Acceptance checks and status

**Passed — specification inspection and arithmetic:** The supplied platform, count unit, nonnegative domain and four findings are traceable to `interface.md`. The worked arithmetic is 6/2 = 3, 54/50 = 1.08, 54 − 50 = 4 and 4/50 = 8%. The proposed example heights are 240 × 50/60 = 200 and 240 × 54/60 = 216. These are mathematical checks, not a rendering test.

**Failed — supplied interface specification:** Zero-baseline proportional bars; labeled axes/units; series distinction independent of hue; persistent exact values and accessible description. Each fails explicitly in the supplied prose. The corrected contract addresses each; no implemented fix has been tested.

**Not executed — acceptance tests for the eventual implementation:**

- With real 50/54 records, confirm a shared 0–60 scale, visible zero tick and counts, correct dates/series and 1.08 height ratio within rendering tolerance. No bar is clipped. With totals above 60, the upper bound expands without truncation.
- Remove hue or view in grayscale: every series remains identifiable from names and patterns. Verify legend-to-mark mapping and stable encodings across views.
- Inspect accessible structure: overview contains type, purpose and bounds; every real observation exposes its date, named series, count and unit in chronological/series order. Then test with macOS VoiceOver and Accessibility Inspector. A text spec does not prove spoken order.
- Reach all essential values using keyboard and assistive navigation. If selection exists, verify the same detail through pointer and keyboard, visible focus, and no hover-only information.
- At narrow window sizes and at least 200% text enlargement, preserve titles, dates, values and series identity through reflow; the plain-text alternative remains usable. [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).
- Measure actual foreground/background contrast in light, dark and Increase Contrast appearances using a contrast calculator; record inputs and results under the applicable text-size guidance. Verify macOS user accent changes do not erase meaning. No measurements are possible from “red/green” alone.
- Exercise zero, all-zero, missing, empty and long-label fixtures; distinguish missing from zero and keep labels readable. Confirm actual aggregation and series relationships before generating comparisons or totals.

## Evidence and routing limits

Read the installed root `apple-hig/SKILL.md`, the Content family and Charts procedure, and searched `references/topic-index.md` before completing the route. Also read Patterns → Charting data and Foundations → Accessibility and Color procedures, each before its supporting reference. All paths were resolved within `.agents/skills/apple-hig/`; each file was read in its own shell command. Supporting articles read: `content/references/charts.md`, `patterns/references/charting-data.md`, and `foundations/references/{accessibility,color}.md` under their respective `subskills/apple-hig-*` directories.

The official links above identify the sources represented by installed local snapshots; they were not fetched. No web, screenshot, source implementation, dataset beyond the supplied counts, GUI, device, SDK compilation, contrast measurement or accessibility execution was used. No visual example was supplied, so screenshot/media inspection was inapplicable. This review does not establish clinical validity, actual capacity, native rendering, or accessibility conformance. The output is a corrected specification and test contract, not an executed application.
