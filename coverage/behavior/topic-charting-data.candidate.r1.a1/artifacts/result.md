# Monthly household energy: revised interaction specification

## Scope and decisions

Target: iPadOS, using touch, pointer, keyboard, and assistive input. This is a framework-agnostic design contract; no Apple SDK is required. The evidence is the description and five monthly records in `interface.md`, not a running dashboard. No year is supplied; do not invent one.

The question is “How has household energy use changed, and what was each monthly value?” Replace the described pie chart with chronological points and a line connecting only adjacent months with readings. A pie expresses parts of a whole poorly suited to this trend task and obscures the absent month. The revised chart preserves every month, including April.

Use these records without imputation, smoothing, normalization, or aggregation:

| Month | Energy | Context |
| --- | ---: | --- |
| January | 210 kWh | — |
| February | 220 kWh | — |
| March | 225 kWh | — |
| April | Missing | No reading supplied |
| May | 610 kWh | After heating installation |

The line is a visual guide between observations, not a claim about within-month consumption. May is an isolated point because April is missing. Keep May on the same scale; do not cap it or use an axis break.

## Screen and visual contract

Reading order:

1. Title: **Monthly household energy use**. Period: **January–May · kWh**.
2. Persistent takeaway: **May used 610 kWh, 385 kWh (171.1%) more than March, the previous available reading. April’s reading is missing.**
3. Chart, followed by a persistent selected-month detail region.
4. Context: **May reading is after heating installation. These readings alone do not establish why usage changed.**

Use equally spaced January–May positions on the horizontal axis, with all five month names visible. Vertical axis: **Energy use (kWh)**, fixed for this supplied dataset at 0–700, ticks at 0, 100, …, 700. This zero-inclusive frame makes the full size of the May increase visible. Keep this scale unchanged during selection or layout changes. For a future dataset outside this range, recompute a documented zero-inclusive upper bound and update labels and accessible overview together; never silently clip values.

Draw circles at 210, 220, 225, and 610. Connect January–February–March only. At April, show the text **Missing** in a reserved label band aligned with its month, outside the numeric plot: no zero-height point and no connecting bridge to May. Explain visibly: **Gap = missing reading**. Place **After heating installation** beside May or in a keyed note immediately below the chart if space is constrained. Do not invent an installation date or shade a precise installation interval.

Use a single series style. Selection adds an outline and a “Selected” label; neither missingness nor selection depends on color. Keep gridlines subordinate to marks. Detail content stays outside the plot so it cannot cover values. At narrow split-view widths, retain the five positions and reflow notes below; at enlarged text, allow month labels to wrap and increase chart height. Never drop April, abbreviate away units, or truncate the takeaway.

These choices apply [Charts: Marks, Axes, Descriptive content, and Best practices](https://developer.apple.com/design/human-interface-guidelines/charts) and [Charting data: Designing effective charts](https://developer.apple.com/design/human-interface-guidelines/charting-data). The specific bounds, missing-data treatment, and wording are product decisions based on the supplied records, not universal HIG requirements.

## Interaction and state contract

Initial selection is May. Show its detail immediately; selection has no timeout. The chart and detail remain in one view, preserving the same metric, month order, marks, and scale.

Each month has a selectable full-height plot column, including April. Tap or click anywhere in a column to select its month. Optional horizontal scrubbing previews/selects the nearest column, clamped to the five months; ties choose the earlier month. Releasing retains selection. Vertical movement must allow page scrolling; scrubbing must not be necessary to inspect values.

Expose five labeled month selectors aligned with the plot, with iPadOS activation areas at least 44 × 44 pt and no overlap. These are the explicit alternative to scrubbing. A keyboard user can Tab to each selector and activate it with Enter/Space. When a selector has focus, Left/Right moves focus and selection chronologically, stopping at the ends. Preserve normal Tab navigation and system shortcuts. Pointer hover may emphasize a column but does not change persistent selection; clicking does.

Selecting a month updates its outline, selected state, and persistent detail without moving focus or opening a modal. Detail contains the month, exact value or “Reading missing,” context, and a comparison with the previous available reading, explicitly naming that month. Adjacent-month change is unavailable whenever either adjacent reading is missing.

| Selection | Detail comparison |
| --- | --- |
| January | 210 kWh. No earlier reading in this period. |
| February | 220 kWh. Up 10 kWh (4.8%) from January. |
| March | 225 kWh. Up 5 kWh (2.3%) from February. |
| April | Reading missing. Change cannot be calculated. |
| May | 610 kWh. Up 385 kWh (171.1%) from March, the previous available reading. April-to-May change unavailable. After heating installation. |

```text
records = [Jan:210, Feb:220, Mar:225, Apr:null, May:610]
selected = May
for each adjacent pair (a,b):
    drawLine(a,b) only if a.value != null and b.value != null
onSelect(month):
    selected = month
    previous = nearest earlier record with non-null value
    if month.value == null: comparison = unavailable
    else if previous absent: comparison = no earlier reading
    else:
        delta = month.value - previous.value
        percent = 100 * delta / previous.value if previous.value != 0
        label comparison with previous.month and any intervening gap
    render details; round displayed percentages to one decimal
    retain focus and scale; expose updated detail to assistive input
```

## Accessible equivalent

Provide a chart overview: **Monthly household energy use, January through May. Line and point chart. Horizontal axis: months. Vertical axis: energy use, 0 to 700 kilowatt-hours. April is missing; no line crosses the gap.** Follow it with the takeaway and five interactive month elements in chronological order. Each element exposes its month name, exact value with units or missing status, selected state, and selection action. For example: **April, reading missing, select month** and **May, 610 kilowatt-hours, after heating installation, selected**.

The five month selectors supply accessible values even without sight or chart gestures; selection reveals the same comparison details for all inputs. Avoid duplicate traversal of decorative ticks, lines, and circles. Announce committed detail changes politely without moving focus; coalesce scrub updates rather than speaking every pointer movement. No claim is made that these semantics already exist in an implementation.

Use iPadOS 17 pt as the starting text size, support at least 200% enlargement through reflow, and preserve all values and actions. Measure text/background contrast in light and dark appearances and Increase Contrast; do not rely on a proposed palette as evidence. Use immediate selection changes without required animation, sound, or haptics. Audio Graphs may be considered separately if the eventual framework supports them; they are not assumed here. These requirements apply [Charts: Enhancing the accessibility of a chart](https://developer.apple.com/design/human-interface-guidelines/charts) and [Accessibility: Vision, Mobility, Speech, and Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility).

## Worked before/after

**Before, as described:** a pie chart of months hides April. A person sees slices rather than chronological change and cannot tell that a monthly observation is absent. No screenshot or interaction implementation was supplied, so labels, colors, and existing selection behavior are unknown.

**After:** opening the dashboard shows January 210 → February 220 → March 225, a labeled April gap, and May 610 on the same axis. The takeaway supplies the large change immediately. Selecting April shows “Reading missing,” never 0 kWh. Selecting May shows its installation context and the March comparison. Calculation: 610 − 225 = 385 kWh; 385 / 225 × 100 = 171.1% rounded. It does not say “up 171.1% from April” or “heating caused the increase.”

The known readings sum to 1,265 kWh, but that is not a complete January–May total. Do not present it as one. Monthly duration, weather, occupancy, installation timing, and meter accuracy are unavailable; do not infer efficiency, daily usage, cost, or causation.

## Acceptance checks and current evidence

**Passed — static design/data checks:** All five input months appear in this specification; April remains null. The specified line stops at March. The 0–700 scale contains every supplied value. Calculations above and February/March comparisons agree with the supplied values. The same metric and ordering persist from overview to detail. Critical facts have a text route and every month has a specified non-gesture activation route. These are specification checks, not runtime results.

**Failed — supplied design description:** The existing pie-chart representation does not express the requested time trend directly, and hiding April loses material missing-data context. No other implementation defects are established by the brief.

**Not executed — implementation acceptance:**

- Render the five positions and verify January–March connections, isolated May, labeled April gap, bounds, units, and annotation placement. Fail if April becomes zero, disappears, or is interpolated.
- Select all five months through touch, pointer, keyboard, and assistive navigation. Verify the exact detail strings/comparisons, focus retention, endpoint behavior, and identical selected state. Fail if essential detail requires scrubbing or hover.
- At narrow iPad split-view widths and 200% text, verify that labels, takeaway, detail, and controls reflow without loss, overlap, or blocked scrolling; measure the 44 × 44 pt activation regions.
- Verify logical chronological accessibility traversal, names/values/states, committed-update announcements, and absence of duplicate decorative stops with VoiceOver, Full Keyboard Access, Switch Control, and relevant pointer/AssistiveTouch paths on an actual supported environment.
- Measure contrast for actual rendered light/dark/Increase Contrast palettes, check meaning without color, and confirm Reduce Motion preserves identical information and state.

## Guidance provenance and evidence limits

Read locally in route order: installed `apple-hig/SKILL.md`; Content family → Charts procedure → `content/references/charts.md`; Patterns family → Charting data procedure → `patterns/references/charting-data.md`; Foundations family → Accessibility procedure → `foundations/references/accessibility.md`. Paths are relative to `.agents/skills/apple-hig/subskills/` after the root. Procedures were read before their supporting guides. The local guides carry a 2026-10-25 snapshot/retrieval date; official links above identify their sources and were not fetched.

Only supplied local files and installed instructions were used. There was no browser, GUI, device, SDK, accessibility tool, or runtime execution. No native chart defaults, Audio Graphs availability, physical comfort, measured contrast, or assistive-technology behavior has been verified. This deliverable specifies behavior for a later implementation and its acceptance testing; it does not certify an implemented experience.
