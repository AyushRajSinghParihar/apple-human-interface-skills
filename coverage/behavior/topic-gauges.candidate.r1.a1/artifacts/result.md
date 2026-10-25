# Hiking battery gauge review

This is a specification audit of `interface.md` for an in-app watchOS battery estimate. The only supplied interface evidence is its written description; “verified” below means explicitly stated there, not observed on a device. The task is to understand remaining battery while hiking. No implementation changes or Apple SDK are assumed.

## Ranked verified findings

| Rank | Observed problem and effect | Decision and source support |
|---|---|---|
| 1 — High | Unknown battery data displays as a real zero. A hiker cannot distinguish unavailable information from an empty battery. | Model unknown separately; display “Estimate unavailable,” with no numeric value or capacity fill. A genuine measured zero remains `0%`. This is an application correctness decision supported by the installed gauge procedure’s unknown-input and honest-value checks; the HIG article establishes a gauge as a numerical value within a range. [Gauges, Anatomy](https://developer.apple.com/design/human-interface-guidelines/gauges#Anatomy). |
| 2 — High | Green is the only safety cue. People who cannot distinguish the color lose that meaning; the supplied data also provides no basis for calling a hike safe. | Remove the safety claim pending a validated domain model. Show battery quantity in words and numbers independently of color. If validated warning states are later added, give each a visible text label and equivalent accessible state. HIG says to pair essential color signals with words, shapes, or glyphs. [Color, Inclusive color](https://developer.apple.com/design/human-interface-guidelines/color#Inclusive-color), [Accessibility, Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |
| 3 — Medium | No concise title/description, percentage unit, or endpoint labels. The number and track lack quantity and range context. | Use “Battery estimate,” `42% remaining`, and endpoints `0% · Empty` / `100% · Full`. Supply concise descriptions of the current value and both endpoints in the semantic model as well. HIG recommends descriptions of value and endpoints; visibility varies by gauge style. Visible endpoint labels here are a design choice, not a universal requirement. [Gauges, Best practices](https://developer.apple.com/design/human-interface-guidelines/gauges#Best-practices). |

Ranking reflects misleading hiking decisions before missing explanatory context. No contrast, font-size, geometry, or spoken-output defect is verified by this brief.

## Corrected behavior and decisions

- **Quantity:** estimated remaining battery charge, expressed as percent of capacity, not estimated hiking duration or probability of safe completion. The brief specifies percentage; confirm the producer’s unit contract before integration. Do not convert a time estimate into percent without a defined model.
- **Scale:** fixed, linear 0–100 percent. A continuous capacity fill runs from empty to full; it is not task-completion progress. No gradients, safety bands, or arbitrary low-battery threshold are introduced.
- **Visible structure:** title, current value or availability message, continuous track when known, and endpoints. Keep essential wording available in compact layouts; permit a stacked arrangement rather than truncating units or states.
- **Color roles:** primary text for title/value/endpoints, secondary text for explanatory availability content, neutral track and distinguishable capacity fill. Use adaptable semantic equivalents in the chosen framework. Green may decorate capacity only if it conveys no additional safety meaning. Custom colors need appropriate appearance and increased-contrast variants. Actual contrast remains unmeasured. [Color, Best practices and System colors](https://developer.apple.com/design/human-interface-guidelines/color#Best-practices).
- **Semantics:** expose one coherent read-only gauge description containing name, value, range, and availability; the drawn track must not create duplicate information. This is a proposed semantic contract, not evidence of current VoiceOver behavior. Do not expose an unavailable gauge as numeric zero or as an adjustable control.
- **Freshness:** accept “current” only from a producer with an explicit freshness policy. The brief provides neither timestamps nor a freshness interval. Until that contract exists, do not invent a cutoff or imply that a cached value is current. Invalid, failed, absent, or producer-marked stale data use the unavailable state. A later fresh sample restores the numeric state.

The local gauge article specifies no additional watchOS rule. Its green capacity default and tiered threshold discussion are scoped to **macOS level indicators**, so they do not justify green safety semantics on this watch. This is an in-app gauge review; no complication/widget surface is supplied.

### Framework-agnostic state contract

```text
Input = Missing | Failed | Stale | Current(percent)
// Producer owns units and freshness; Current must mean current evidence.

present(input):
  title = "Battery estimate"
  endpoints = ["0% · Empty", "100% · Full"]
  if input is not Current(p) or p is not finite or p < 0 or p > 100:
    return {
      title, endpoints,
      message: "Estimate unavailable",
      track: hidden, numericValue: absent,
      semantics: "Battery estimate. Estimate unavailable. Range: 0 percent,
                  empty, to 100 percent, full."
    }
  displayed = roundToWholePercent(p)  // no extra decimal precision
  return {
    title, endpoints,
    message: displayed + "% remaining",
    track: capacity(fillFraction = displayed / 100),
    numericValue: displayed, minimum: 0, maximum: 100,
    semantics: "Battery estimate. " + displayed + " percent remaining.
                Range: 0 percent, empty, to 100 percent, full."
  }
```

Whole-percent rounding is a proposed display policy, not an Apple requirement or a claim about sensor accuracy. It must not feed safety classification. Reject out-of-range input instead of silently clamping it into a believable measurement. Known → unavailable removes the old numeric fill immediately; unavailable → known restores it from the new sample. No simulated reading or spinning progress indicator is needed.

## Worked before/after

The following numbers are synthetic examples, not sensor readings.

| Input | Before, per supplied description | Corrected output |
|---|---|---|
| Unknown | Real zero displayed, no unit/title/endpoints; green is the only safety cue | **Battery estimate** / **Estimate unavailable**; no numeric value or capacity fill; `0% · Empty` and `100% · Full` remain range context. Accessible contract reports unavailable, never “zero percent.” |
| Current 42% | Numeric value lacks percentage unit and explanatory labels; safety depends on green | **Battery estimate** / **42% remaining**; capacity track filled 42%; labeled endpoints. Semantic description includes quantity, value, and range. No claim that 42% is enough to finish the hike. |
| Current 0% | Visually conflated with unknown | **Battery estimate** / **0% remaining**; empty track with labeled range. Numeric zero is preserved as a known value. |

## Acceptance checks and status

**Passed — static review only:** read the supplied brief; mapped the only supplied component to Gauges; followed the installed root → Status → Gauges procedure → guide route, searched the topic index, and read Foundations → Accessibility and Color procedures before their guides. The proposed contract distinguishes zero from unknown, specifies units/endpoints, and supplies noncolor meaning. These are document properties, not implemented behavior.

**Failed — supplied specification:** unknown/zero distinction; noncolor safety meaning; quantity/unit and endpoint context. These failures are verified by the explicit statements in `interface.md`.

**Not executed — implementation acceptance:**

| Check to execute against an eventual implementation | Pass condition |
|---|---|
| Minimum and maximum | Current `0` yields `0% remaining` with empty capacity; `100` yields `100% remaining` with full capacity; both retain range descriptions. |
| Midpoint and display mapping | Current `42` yields `42% remaining` and 0.42 fill; fill and displayed number use the same rounding policy. |
| Invalid/unknown inputs | Missing, failure, stale, nonfinite, `-1`, and `101` yield unavailable with no numeric value/fill; none become zero or an apparent full battery. |
| Transitions | Current 42 → Missing removes 42 and its fill; Missing → Current 0 restores genuine zero; Current 0 → Current 100 restores full capacity. |
| Noncolor meaning | In monochrome, readers can identify the quantity, value, range, and unavailability. No safety meaning disappears with hue. |
| Compact watch layout and resizing | At supported watch sizes and 140% text enlargement, title, units, endpoints, and availability remain readable without clipping; reflow as necessary. The local accessibility guide states 140% for watchOS. [Accessibility, Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |
| Contrast and appearances | Record actual foreground/background pairs and calculator results; test applicable appearances and Increase Contrast. Use the local guide’s scoped contrast table rather than claiming blanket conformance; test outdoor legibility on hardware separately. [Accessibility, Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |
| Assistive output | On a supported Apple environment, verify the actual gauge reading includes name, current value/availability, and range without duplicate decorative readings; unavailable never announces numeric zero. |

## Evidence limits

Only `interface.md` and installed local instructions/guides were used. Official links identify the guidance behind decisions; no web pages were fetched. The installed articles are dated 2026-10-25 and are local application guidance, not SDK documentation or independently verified runtime evidence.

No screenshot, source implementation, sensor reading, device, GUI, runtime, or accessibility execution was supplied or performed. Therefore contrast ratios, actual label placement, compact fit, assistive announcements, hardware comfort/legibility, SDK availability, and compilation remain unverified. No battery accuracy, remaining-time, safety threshold, or freshness interval can be validated from the evidence. The corrected behavior above is a reviewable specification awaiting implementation and execution of its checks.
