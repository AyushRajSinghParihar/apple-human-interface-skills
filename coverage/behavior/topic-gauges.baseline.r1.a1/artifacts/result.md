# Watch hiking battery gauge audit

This is a specification review of `interface.md`, targeting watchOS. Findings are verified against the supplied description, not an observed running interface. Priority reflects potential misunderstanding during a hike; it is not a measured risk score.

## Ranked findings and decisions

| Rank | Verified observation | Effect | Decision and basis |
|---|---|---|---|
| 1 — High | Unknown battery data is displayed as a real zero. | A missing estimate is indistinguishable from a valid depleted battery reading. | Represent unavailable data explicitly; never substitute zero. This is an audit decision applying the status family's honesty principle and the gauge's numerical-range meaning, not an explicit unknown-state rule in the gauge article. |
| 2 — High | Green is the only safety cue. | People who cannot distinguish the color lose the cue; a battery percentage alone cannot establish whether a hike is safe. | Remove the implied safety assessment. Show a textual battery state and use color only as reinforcement. Accessibility guidance explicitly pairs color with text, shape, or icons. Any future hike-sufficiency assessment needs separate validated inputs and policy. |
| 3 — Medium | No concise title or description. | People lack a clear statement of what is being measured. | Use “Battery estimate” as the visible title and accessible name. Gauges guidance calls for concise descriptions of the value. |
| 4 — Medium | No percentage unit. | The numerical value's scale is ambiguous. | Display and speak the percent unit, for example “62%” and “62 percent.” This is a concrete application of the gauge-description guidance; the article does not prescribe a literal percent sign. |
| 5 — Medium | No endpoint labels. | People cannot readily interpret the range or position. | Label the endpoints “0%” and “100%,” and include the range in accessible semantics. Gauges guidance asks for concise descriptions of both endpoints and notes that styles differ in which labels they show. |

Ranks 3–5 jointly establish the gauge's meaning. Correct them together rather than treating lower rank as optional.

## Corrected behavior

Use a read-only capacity gauge spanning 0–100 percent. A linear track is a proposed layout, not a watchOS requirement. Keep the title, current value, and endpoint labels readable together; allow the group to grow vertically with text enlargement. The gauge is a value within a range, not task-completion progress.

Known data displays a bounded fill, the percentage, endpoint labels, and the text “Estimated battery remaining.” Green may remain decorative but must not mean “safe to finish.” Unknown data displays “Battery estimate unavailable” and no current fill or numeric position. Endpoint labels may remain to identify the scale, but no marker may imply zero. A real zero remains “0%,” with “Estimated battery depleted”; do not infer the physical device has shut down.

Framework-agnostic specification:

```text
Input = Known(percent: finite number in [0, 100]) | Unavailable

normalize(raw):
    if raw is missing, nonnumeric, nonfinite, or outside [0, 100]:
        return Unavailable
    return Known(raw)        // zero is valid; never use a truthiness check

render(state):
    title = "Battery estimate"
    range = ["0%", "100%"]
    if state is Unavailable:
        currentValue = none
        fill = none
        status = "Battery estimate unavailable"
        accessibleSummary = "Battery estimate, unavailable"
    else:
        valueText = localeFormatPercent(state.percent)
        fill = state.percent / 100
        currentValue = valueText
        status = "Estimated battery depleted" if state.percent == 0
                 else "Estimated battery remaining"
        accessibleSummary = "Battery estimate, {spoken percentage}, " +
                            "range 0 to 100 percent, {status}"

    expose one coherent read-only accessible group
    avoid duplicate announcements from decorative track and labels
    never announce Unavailable as numeric zero
```

Input validity and unavailable-state handling are proposed product contracts. Reject invalid values instead of silently clamping them into credible readings. If rounding is needed, define and test a formatting policy that does not turn a small positive estimate into a depleted-state claim. The same estimate must drive both visual and accessible output. This specification introduces no arbitrary low-battery threshold, remaining-hours prediction, or route-safety calculation.

## Worked before / after

The before column reflects supplied behavior; the exact layout and wording were not supplied. The known-data values below are synthetic fixtures, not sensor evidence.

| Input | Before | After |
|---|---|---|
| Unknown | Real zero displayed; green is the only safety cue; no title, unit, or endpoints. | “Battery estimate” / “Battery estimate unavailable.” No fill or numeric current value. Accessible summary: “Battery estimate, unavailable.” |
| Known 62 | Unitless value, no title/endpoints, green-only safety meaning. | “Battery estimate” / “62%” / “Estimated battery remaining”; track filled to 62%, endpoints “0%” and “100%.” Accessible summary includes 62 percent and the range. No safety claim. |
| Known 0 | Visually indistinguishable from unknown data. | “Battery estimate” / “0%” / “Estimated battery depleted”; empty capacity track, range labels present. Accessible summary includes zero percent and the depleted estimate. |

## Acceptance checks

These are checks to perform, not execution results.

- Feed missing, null, nonnumeric, nonfinite, negative, and greater-than-100 inputs: show unavailable, without a zero value, current marker, or numeric accessibility value.
- Feed 0, 62, and 100: show 0%, 62%, and 100%, with corresponding empty, 62%-filled, and full tracks. Unknown → known zero → unknown must preserve their distinct text and semantics.
- With all color removed, the measured quantity, unit, endpoints, and availability remain understandable. No state claims the hike is safe.
- Inspect the accessibility representation: one coherent read-only group conveys name, known percentage and range, or unavailability; decorative elements do not repeat it. Verify the actual spoken result with VoiceOver when a watch build exists.
- At watchOS text enlargement of 140%, verify the title, value, state, and endpoints remain legible without essential truncation or overlap on supported watch sizes. This percentage comes from the local accessibility guide; no layout has yet been rendered.
- Measure text contrast using actual chosen colors and sizes, including applicable appearance and Increase Contrast settings. Apply the local guide's scoped contrast guidance; no current contrast failure can be verified without visual values.
- Test localized percentage formatting, spoken units, and longer translated labels. Confirm layout can expand instead of suppressing meaning.

## Evidence and limits

Read order: installed root `apple-hig/SKILL.md`; supplied `interface.md`; status family `SKILL.md`; exact-component entries in `references/topic-index.md`; foundations family `SKILL.md`; then the routed `gauges.md` and `accessibility.md` source guides. Both selected families route directly to article references; they specify no additional topic procedure. All package paths were resolved under `.agents/skills/apple-hig/`, and each file was read in its own shell command.

Local guidance consulted:

- [Status procedure](.agents/skills/apple-hig/subskills/apple-hig-status/SKILL.md): gauge meaning and honest status.
- [Gauges source guide](.agents/skills/apple-hig/subskills/apple-hig-status/references/gauges.md), corresponding to [Apple Gauges — Best practices](https://developer.apple.com/design/human-interface-guidelines/gauges#Best-practices): concise value and endpoint descriptions. The local guide states no additional watchOS rule. Its macOS green-fill and threshold details were not transferred to watchOS.
- [Accessibility source guide](.agents/skills/apple-hig/subskills/apple-hig-foundations/references/accessibility.md), corresponding to [Apple Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision): redundant color cues, meaningful VoiceOver descriptions, text enlargement, and contrast evaluation.

Official links identify the sources; they were not opened. The installed package describes a dated, derived English HIG snapshot, not an SDK reference or independently verified current Apple manual. No web access was used.

No screenshot, code, sensor data, runtime, device, SDK, GUI, or accessibility execution was supplied or performed. Typography, contrast, geometry, clipping, touch behavior, actual semantics, update timing, estimate accuracy, and supported watch sizes remain unverified. The pseudocode and acceptance checks are a reviewable correction specification, not an implemented or tested app. No battery threshold or route-safety policy can be validated from the supplied evidence.
