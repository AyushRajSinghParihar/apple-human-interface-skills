# Revised activity summary specification

This is a framework-agnostic design for the watchOS/iOS dashboard described in `interface.md`. Its task is to let a person check daily system Activity progress alongside a separate weekly companion goal. It does not start or control workouts, edit goals, diagnose conditions, or assess treatment efficacy.

## Decisions and source support

1. **Keep system Activity recognizable.** Replace the proposed purple, reordered rings with the unmodified standard presentation: Move outside, Exercise in the middle, and the system's third activity measure inside. Preserve colors, proportions, opacity and rendering; add no shadows, gradients, masks or branding effects. Use black behind the rings, preferably a rounded enclosing container rather than a circular mask. Leave black clearance outside the outer ring at least as wide as the inter-ring gap. Identify the person as “Your Activity” for the signed-in person's data; never combine people. The installed guide requires standard rendering, individual identity, black background and clearance. The explicit outer-to-inner ordering is this specification's preservation contract, to verify against the supplied system presentation rather than implement as a custom redraw. [Activity rings — Best practices](https://developer.apple.com/design/human-interface-guidelines/activity-rings#Best-practices).

2. **Use wheelchair-appropriate third-measure wording.** For confirmed wheelchair-mode summaries, visible and accessible labels say **Roll**, not Stand. Preserve Move and Exercise. Do not merely relabel Stand measurements as Roll; require a source-confirmed measure mapping for that person and date. For confirmed non-wheelchair summaries, retain Stand. If the mapping is unknown, show “Activity details unavailable” for that measure, never guess from appearance, name, or app audience. This is a product correction informed by inclusive design; the inspected local Activity/HealthKit articles use Stand generically and do not establish Roll units, thresholds, detection rules or API mapping. Verification is a release gate. [Inclusion — Avoiding stereotypes and Accessibility](https://developer.apple.com/design/human-interface-guidelines/inclusion#Accessibility).

3. **Separate completion from clinical outcome.** A closed ring means its recorded daily activity goal was reached. A full weekly bar means the configured app goal was reached. Neither proves improvement, recovery, treatment adherence, risk reduction or another clinical outcome. Use “Daily goal reached” and “Weekly goal reached”; remove any clinical success claim. This is a product evidence boundary, not a claimed medical conclusion or a quoted HIG prohibition. The HealthKit procedure explicitly separates UI work from health accuracy and medical efficacy. [HealthKit](https://developer.apple.com/design/human-interface-guidelines/healthkit).

4. **Give the app goal its own linear treatment.** Put a separate “Your weekly goal” section below daily Activity with a heading, visible separation and a horizontal capacity bar. Purple may brand this bar, subject to measured contrast; never recolor system rings. Show quantity, units, week dates and endpoints. Do not make another concentric ring, substitute weekly values into Activity rings, or duplicate system Activity notifications. The linear choice is a product decision following the guide's separation requirement. [Activity rings — Best practices](https://developer.apple.com/design/human-interface-guidelines/activity-rings#Best-practices), [Gauges — Best practices](https://developer.apple.com/design/human-interface-guidelines/gauges#Best-practices).

## Presentation and interaction contract

Reading order on both platforms:

1. “Your Activity” and selected date, defaulting to today.
2. Standard system ring presentation when available.
3. Text equivalents in system order: measure name, current value, goal, units and completion state. Include only supported measures. For a confirmed wheelchair record, use Move, Exercise, Roll.
4. “Your weekly goal,” explicit date range, numeric progress, linear bar, and completion or remaining amount.
5. Source/freshness information, adjacent to the section it qualifies.

Daily and weekly periods remain explicit. Never imply that closing today's rings completes the weekly goal or vice versa. Values use locale-aware number, date and unit formatting.

**iOS:** Stack the two sections vertically; reflow in portrait, landscape and enlarged text without changing reading order or losing values. Keep the ring clear of wrapping labels. Preserve scroll position and selected date across interruption. Historical system presentations may legitimately contain one or three rings: retain the supplied representation per record, not today's pairing state. Without a paired Watch, the local guide describes an approximate Move-only presentation; identify it as an estimate and do not fabricate Exercise or Roll. [Activity rings — iOS](https://developer.apple.com/design/human-interface-guidelines/activity-rings#iOS), [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices).

**watchOS:** Prioritize today's Activity at wrist raise. Place the short weekly numeric summary immediately after it; vertical scrolling reveals remaining details. Do not compress text to force both sections onto one viewport. Use ordinary platform scrolling, with Crown support where provided by the eventual host; require no custom precise gesture. Wrist lowering or interruption must preserve summary context and must not reset totals. This specification adds no complication, notification, Always On customization or Action button behavior. [Designing for watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices).

**Accessibility:** Rings and bar have adjacent text equivalents; color is never the only means of identifying a measure or completion. Expose each measure's name, value, goal, unit and state in reading order; suppress redundant decorative graphic announcements. Example: “Roll, 8 of 12 hours, daily goal not yet reached,” only when the source confirms these units and semantics. Reflow at least at 200% text on iOS and 140% on watchOS, including wrapping freshness labels. Start from 17 pt iOS and 16 pt watchOS default text. If controls are later added, use the guide's 44 × 44 pt default activation size on both platforms and verify spacing. Measure text contrast in light/dark and Increase Contrast configurations using the local guide's scoped contrast table; standard ring colors remain unchanged, while surrounding text supplies readable equivalents. No added celebration animation or sound is needed. [Accessibility — Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

## Data and state contract

The platform adapter is an interface boundary, not an assumption that an Apple SDK exists here. It supplies standard presentation capability and authorized, person-specific summary data. If standard rendering is unavailable, show the labeled text summary; do not approximate system rings with custom purple arcs.

```text
DailySummary = {
  personId, date, timezone, fetchedAt,
  availability: loading | available | unavailable,
  systemPresentation: optional opaque standard presentation,
  measures: [{ kind, localizedName, current, goal, unit,
               sourceConfirmedMode, estimateFlag }]
}
WeeklyGoal = {
  personId, weekStart, weekEndExclusive, timezone,
  metricDefinition, unit, target, recordedTotal, fetchedAt,
  availability: loading | available | unavailable
}

render daily and weekly independently
if loading: show "Loading Activity…" / "Loading weekly progress…"
if unavailable: show "Activity unavailable" / "Weekly progress unavailable"
  show last-known values only with their original date and freshness label
  never turn missing data into zero, empty rings, or a completion claim
if available:
  reject mismatched person/period/unit and nonfinite or negative values
  if target <= 0 or missing: show value if valid; "Goal unavailable"; no ratio
  otherwise:
    reached = recordedTotal >= target
    visualFill = clamp(recordedTotal / target, 0, 1)
    retain actual total in text even when above target
```

The clamp applies to the app's weekly bar only; do not override standard Activity over-goal rendering. Real recorded zero is displayed as zero and is distinct from unavailable. Refresh updates values in place without moving reading focus. If access changes or refresh fails, label last-known data with its timestamp and “Latest data unavailable”; do not claim it is current or infer a particular permission-denial reason from missing data.

For the worked example only, the weekly metric is minutes in eligible saved wheelchair workouts. Production must define eligible types and use unique source record IDs to avoid counting imports twice. Paused time is excluded; deleted/corrected records recompute the total. Use a displayed calendar week and timezone, with inclusion by session start within that week. This counting policy is a product choice, not HIG or a clinical prescription. Do not derive weekly totals by summing daily ring completion percentages.

Access must be requested only in the context of this feature, for necessary data, with a clear benefit explanation and the platform's standard authorization flow where available. Keep access management in system privacy settings and provide the required privacy-policy disclosure. No unrelated health access is a prerequisite for viewing an independently available weekly goal. [HealthKit — Privacy protection](https://developer.apple.com/design/human-interface-guidelines/healthkit#Privacy-protection).

## Worked before/after

**Before, from the brief:** The dashboard proposes purple system rings in a changed order, wheelchair users see Stand, and a closed ring is treated as proof of a clinical outcome. The app also wants a weekly goal beside familiar Activity.

**After, illustrative fixture rather than observed health data:** For Alex, a confirmed wheelchair-mode three-measure record on 25 October shows standard rings with black clearance and the following text:

- Your Activity · 25 October
- Move: 420 of 400 kcal · Daily goal reached
- Exercise: 24 of 30 min · 6 min remaining
- Roll: 8 of 12 hours · 4 hours remaining
- Your weekly goal · 19–25 October
- Wheelchair workout time: 85 of 100 min · 15 min remaining
- Linear weekly bar: endpoints 0 min and 100 min, fill 85%
- Updated 14:32

The Roll fixture's unit and mapping remain subject to source verification. After another eligible 20-minute saved workout, the weekly total becomes 105 of 100 min, the bar stays full, and the text becomes “Weekly goal reached · 5 min beyond your goal.” Today's Exercise and Roll remain governed by their own source records. No clinical badge or “health improved” claim appears.

## Acceptance checks and status

**Passed — static specification checks:** The revised contract preserves system identity/rendering and clearance, separates weekly progress, corrects wheelchair wording conditionally on verified data, removes clinical inference, specifies period/person boundaries, and distinguishes unavailable from zero. The worked weekly arithmetic is consistent: 85 + 20 = 105; capped fill is 100% with the actual total retained.

**Failed — supplied design/proposal:** Proposed recoloring/reordering conflicts with standard presentation guidance; the reported Stand wording fails the requested wheelchair treatment; treating completion as clinical proof exceeds the evidence supplied. These are brief-level findings, not inspected runtime defects.

**Not executed — implementation acceptance gates:**

| Scenario | Required observable result |
|---|---|
| Confirmed wheelchair/non-wheelchair/unknown mode | Roll/Stand/source-unknown treatment respectively; verify actual measure semantics, localized wording and units before shipping |
| Standard ring rendering | Correct order/colors, black background, margin at least inter-ring gap; no clipping or overlap at all supported sizes |
| No standard renderer | Text summary remains useful; no imitation system rings |
| iOS pairing/history changes | Supported one-/three-ring variations preserved per record; estimates labeled; no invented missing measures |
| Weekly totals 0, 85, 100, 105 against 100 | Fill 0%, 85%, 100%, 100%; true values and explicit completion state retained |
| Missing/invalid target or total | No fabricated completion, division by zero, or misleading empty bar |
| Refresh, denied/unavailable data, access changes | Independent section states, dated cached values, no false zero or claim of current access |
| Week boundary, duplicate import, correction/deletion | Only eligible records in the defined week counted once; recalculation matches counting policy |
| Interruption, wrist lowering, orientation change | Selected date/scroll context retained; no reset or double counting |
| Enlarged text and appearances | Required text/actions remain reachable; contrast measured; ring clearance retained |
| Assistive navigation | Text equivalents read in specified order without duplicate graphics; scrolling and any host controls reachable through supported assistive input |

## Evidence limits and audit

Read `interface.md` and the installed root `apple-hig/SKILL.md` explicitly. Followed family → topic procedure → source reference for Getting started (iOS, watchOS), Status (Activity rings, Gauges), Foundations (Accessibility, Inclusion), Technologies (HealthKit), and Patterns (Workouts). Each instruction/source read used a separate single-file command. Workouts informed the recorded-summary scope and did not justify adding session controls.

Only supplied local files and installed guidance were used; official links above are attribution from those files, not evidence of browsing. These are dated derivative HIG snapshots, not SDK documentation or independently verified current Apple behavior. The inspected sources do not substantiate wheelchair-specific Roll mapping or any clinical outcome. No device, GUI, SDK, HealthKit authorization, sensor, assistive-technology, contrast-calculator or physical-comfort execution occurred. This deliverable is a reviewable specification, not an implemented or clinically validated companion. Wheelchair-user research, localization review and the listed runtime gates remain necessary validation work.
