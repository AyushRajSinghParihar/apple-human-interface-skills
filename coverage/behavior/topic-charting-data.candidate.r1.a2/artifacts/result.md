# Monthly household energy: revised interaction specification

## Scope and decisions

Target: iPadOS; framework-agnostic design contract, with no Apple SDK dependency. The task is to understand monthly change and inspect exact readings. Source: `interface.md`, which supplies January 210 kWh, February 220 kWh, March 225 kWh, April missing, and May 610 kWh after heating installation. No year, meter provenance, installation date, or evidence of causation is supplied. Preserve month names without inventing a year. Treat the values as supplied monthly energy quantities, not cumulative meter readings; confirm that interpretation before connecting a real data feed.

Replace the pie chart with a chronological line-and-point chart. Months are ordered observations, rather than meaningful shares of a complete whole. Connect January–February–March; leave a gap through April and show May as an isolated point. Do not interpolate April, substitute zero, or draw a March–May connector. This preserves both the available trend and its uncertainty. Familiar lines and points support time trends and individual observation inspection. [Charts: Marks](https://developer.apple.com/design/human-interface-guidelines/charts#Marks)

Lead with a short, supported story, then allow inspection of the same chart. Keep metric, month order, marks, and wording consistent across overview and selection. This applies the guidance to start simply and reveal detail without changing the representation. [Charting data: Designing effective charts](https://developer.apple.com/design/human-interface-guidelines/charting-data#Designing-effective-charts)

## Initial presentation

Display these elements in order:

1. Title: **Monthly household energy**. Period: **January–May · kWh**.
2. Takeaway: **May recorded 610 kWh, up 385 kWh (171.1%) from March, the previous available reading. April is missing.**
3. Supporting context: **January to March rose from 210 to 225 kWh (+15 kWh, 7.1%). May is the highest of the four recorded months.**
4. Chart, followed by persistent month detail. Initial selected month is May.
5. Evidence note: **Heating was installed before the May reading. These readings alone do not establish why usage changed.**

These are product copy decisions derived from the supplied data, not quotations or mandated HIG wording. A written takeaway supplies the main conclusion before exploration. [Charts: Descriptive content](https://developer.apple.com/design/human-interface-guidelines/charts#Descriptive-content)

Chart contract:

- X axis: five equally spaced calendar-month slots, January through May, including April. Visible short labels Jan, Feb, Mar, Apr, May; full names in detail and accessible values.
- Y axis: **Energy (kWh)**, linear 0–700 kWh, labeled ticks at 0, 100, …, 700. Use subdued horizontal reference lines. Keep this range fixed during selection; future periods require a separate scale decision. Zero provides context for the large observed difference; this is a design choice, not a requirement for all line charts. [Charts: Axes](https://developer.apple.com/design/human-interface-guidelines/charts#Axes)
- Filled circular points at all four known readings; straight segments only between adjacent known months. No smoothing or area fill. Use one series labeled by the title, without a redundant color legend.
- April has no quantitative mark. Place **April: no reading** beneath its slot, outside the numeric plotting region. Its inspectable slot remains present.
- Place **Heating installed before May reading** beside May with a leader to that observation, not at an invented installation date. In compact layouts move the annotation below the plot, retaining its month reference.
- Selected observation has an outline ring plus the persistent detail heading; April selection highlights its slot without creating a point. Meaning must survive removal of color. [Charts: Color](https://developer.apple.com/design/human-interface-guidelines/charts#Color)

## Interaction and state contract

Selection is inspection only; no editing, modal presentation, or navigation is needed. Detail stays below the plot and never disappears on a timer. The chart remains visible when space permits. Each detail has a full month heading, reading or missing status, comparison, and relevant context.

```text
rows = [(January,210), (February,220), (March,225),
        (April,null), (May,610)]  // values in kWh
selected = May

select(month):
    selected = month
    show detail for month; update selection outline/slot
    preserve plot bounds, month order, and scroll context

comparison(month):
    if value is null: return "No reading; change unavailable."
    previous = nearest earlier month with a known value
    if none: return "No earlier reading in this period."
    delta = value - previous.value
    percent = delta / previous.value * 100 if previous.value != 0
    name previous month explicitly
    if calendar gap: label "previous available reading";
                     explain intervening missing month
    otherwise: label "from [previous month]"
    round percentage to one decimal only for display
```

Tap or pointer-click anywhere in a month's vertical plot band to select it, including April. Optional dragging across bands scrubs selection; retain the final selection on release and do not steal a vertical page-scroll gesture. Inspection must not depend on dragging or precise point targeting. Provide five labeled month selectors below the plot, each with at least a 44 × 44 pt activation area, wrapping as needed. Selecting a month through any input produces the same detail. Expanded hit regions and predictable navigation follow [Charts: Best practices](https://developer.apple.com/design/human-interface-guidelines/charts#Best-practices); 44 × 44 pt is the local guide's iPadOS default control size, adopted here as the design target rather than its smaller minimum. [Accessibility: Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility)

Month selectors expose a selection role/state and names such as “March, 225 kilowatt-hours” and “April, no reading.” Keyboard focus follows January→May; Enter/Space selects. No focus trap or custom shortcut that overrides system navigation. Selection updates detail without relocating focus. Assistive input can reach and activate every selector; plot scrubbing is supplementary.

The chart has a concise accessible description: “Monthly energy, line and points. January through May; energy axis zero to 700 kilowatt-hours. April missing; line stops at March. May is 610 kilowatt-hours.” The written takeaway and labeled month selectors provide both summary and access to every value; a single image description is insufficient. Do not assume automatic Audio Graphs support. [Charts: Enhancing accessibility](https://developer.apple.com/design/human-interface-guidelines/charts#Enhancing-the-accessibility-of-a-chart)

At narrow iPad window widths, keep all five month slots and move annotation/detail below the plot. If labels cannot fit, retain short axis labels and full names in the selectors/detail; never shrink essential text to force a fit. At 200% text enlargement, wrap supporting text and selectors and allow vertical scrolling without hiding data or actions. No animation is required. Contrast must be measured in the eventual implementation, including light, dark, and increased-contrast treatments. These are acceptance requirements, not measured results. [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision)

## Worked before/after

**Before, as described:** a pie chart shows months and hides April. It obscures chronology and makes the missing month invisible. No screenshot or interaction evidence establishes any additional defect.

**After, on entry:** the chart shows points at 210, 220, 225, a labeled April gap, and 610. May detail reads:

> May · 610 kWh  
> +385 kWh (+171.1%) from March, the previous available reading.  
> April has no reading, so May's change from April is unavailable.  
> Heating installed before May reading; cause of change unconfirmed.

Select April: detail becomes **April · No reading. Change unavailable.** The missing month stays on the axis. Select March: **March · 225 kWh. +5 kWh (+2.3%) from February.** Select January: **January · 210 kWh. No earlier reading in this period.** Return to May: same bounds and May detail, without losing context.

Arithmetic: February–January = +10 kWh (+4.8%); March–February = +5 (+2.3%); March–January = +15 (+7.1%); May–March = +385 (+171.1%). Do not describe the last comparison as month-over-month, extrapolate an annual trend, or present the four readings' sum as the January–May total. No weather, household, tariff, or heating-use breakdown supports further attribution.

## Acceptance checks and evidence limits

**Passed — specification/data inspection:** all five supplied months are represented; null differs from zero; units are retained; calculations above match the supplied numbers; March–May comparison names the gap; annotation avoids a causal assertion; overview and detail retain the same metric and scale. This is static specification evidence only.

**Failed — supplied current description:** April is hidden and the pie representation does not directly serve the stated chronological comparison task. This finding is limited to the text in `interface.md`.

**Not executed — implementation acceptance:**

- Render the fixture: four points, only two connecting segments, no April point, five month slots, bounds 0–700. Select each month and verify the exact details and calculations above.
- Tap bands, click, scrub, and use keyboard selection: all resolve to identical month state; scrolling remains usable; no tooltip is the sole source of a fact.
- Test narrow iPad windows and 200% text enlargement: no essential clipping, lost selectors, obscured marks, or annotation collisions; inspect actual target geometry and spacing.
- On supported Apple hardware, test VoiceOver, Full Keyboard Access, Switch Control, and pointer/touch input from overview to every month's detail. Confirm names, selected state, logical navigation, and perceivable detail updates without unwanted focus movement. Use Accessibility Inspector where available.
- Measure foreground/background contrast in light/dark and increased-contrast configurations; check selection and missingness without color. Do not infer conformance from semantic color names.

Only local files were used. Route read: installed root → Patterns / Charting data and Content / Charts → their supporting guides; Foundations / Accessibility → its supporting guide. The topic index was searched before finalizing the route. Official links above identify the source sections represented by the installed snapshot; they were not fetched or independently verified. No device, SDK, GUI, rendering, assistive-technology, or accessibility execution occurred. This specification neither proves implementation feasibility in a particular framework nor claims accessibility conformance.
