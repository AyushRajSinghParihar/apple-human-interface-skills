# Revised activity summary interaction specification

Design deliverable for watchOS and iOS, based on `interface.md`. No SDK or executable application is assumed. The task is to check one person's daily system activity and a distinct app-owned weekly goal.

## Decisions and source support

1. **Keep the familiar system Activity element unchanged.** Reject purple recoloring and reordered rings. Preserve the supplied system order, colors, proportions, opacity and rendering; do not add shadows, gradients, filters, cropping or masks. Place on black with outer clearance at least the inter-ring gap. A circular enclosure uses the container's corner radius. Identify the person explicitly, for example “Alex · Today.” Adapt surrounding layout instead of branding the rings. [Activity rings — Best practices](https://developer.apple.com/design/human-interface-guidelines/activity-rings#Best-practices), [HealthKit — Activity rings](https://developer.apple.com/design/human-interface-guidelines/healthkit#Activity-rings).
2. **Separate daily system measures from the weekly app goal.** Below the daily section, place a heading “Your weekly goal,” a date range, numeric progress, and a straight horizontal filled track. Purple may distinguish this app-owned track, subject to measured contrast; it never recolors the system element. No concentric or circular weekly graphic. This is a product design choice applying the separation rule. Supply value, units and endpoints. [Activity rings](https://developer.apple.com/design/human-interface-guidelines/activity-rings#Best-practices), [Gauges — Best practices](https://developer.apple.com/design/human-interface-guidelines/gauges#Best-practices).
3. **Replace inappropriate wheelchair copy through a metric contract.** For a confirmed wheelchair activity mode with a verified system roll-hours measure, label that measure “Roll” and show its hours, including in spoken output. Never simply rename a Stand value to Roll, infer mode from an avatar, or convert pushes into hours. If the adapter cannot establish the measure, show “Hourly activity unavailable” in the text summary and omit any unsupported metric value. Request no disability declaration just to view the summary. This is a proposed inclusive product requirement: the supplied local Activity/HealthKit guides describe Stand but do not establish wheelchair mode, Roll terminology, calculation or API support. Verify these before release; do not patch system artwork to simulate support.
4. **Completion means a recorded activity goal was met.** Use “Daily goal met” or “Weekly goal met,” scoped to the specific measure. Delete the proposed clinical-outcome inference. No “recovered,” “health improved,” or equivalent badge follows from closing a ring. This is an evidence constraint and product decision, not a clinical rule established by HIG. The HealthKit procedure expressly separates UI work from evidence of medical efficacy.
5. **Preserve platform variation.** watchOS uses the supplied three-ring presentation. iOS may legitimately show three rings when paired or a single approximate Move ring without a Watch; historical records may differ. Do not synthesize missing rings or reinterpret an unpaired Move estimate as wheelchair pushes. [Activity rings — iOS](https://developer.apple.com/design/human-interface-guidelines/activity-rings#iOS).

## Screen and interaction contract

Reading order on both platforms:

1. Page heading “Activity summary.”
2. “Alex · Today” and the explicit local calendar date.
3. Unmodified system activity element, when legitimately available; adjacent text gives each supplied metric's name, actual, goal and unit. Daily and weekly values always have separate periods.
4. “Your weekly goal,” inclusive start/end dates, “2 of 3 sessions,” then a linear track with endpoints “0 sessions” and “3 sessions.” At completion add “Weekly goal met.”
5. “Weekly goal details” button. Details show the same period, counted session records and counting rule; a Back action returns to the same summary state.

The weekly metric is not supplied in the brief. For this concrete specification, choose **completed wheelchair workout sessions**, target **3 per week**, with no minimum duration or intensity implied. An adapter must supply a stable session ID, explicit wheelchair workout classification and completed status. Count each qualifying session once, on its completion date within the displayed week. Exclude canceled, in-progress and unclassified sessions. State this rule in details. Do not claim this is a recommended fitness prescription. Target editing, workout recording, notifications and sharing are outside this summary's scope.

Use the person's configured calendar/time zone for explicit week boundaries; default to a displayed Monday–Sunday week only when no preference exists. Evaluate membership as start-inclusive/end-exclusive instants. Recalculate when the date, zone, target or source records change; never combine different people's data. A corrected/deleted session can decrease progress and remove the completed state. A new week starts a new total without changing past records.

**iOS:** stack sections in portrait; landscape may place them side by side when readable, retaining heading order and daily/weekly separation. Keep details reachable in the middle/lower content area. Preserve system Back navigation. Returning from another app restores selected date, week and scroll position. [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices).

**watchOS:** prioritize today's system summary and a compact “This week · 2 of 3 sessions” line. Details are one labeled activation away; enlarged content can continue vertically. The Watch remains useful with locally available data when the phone is unreachable. Wrist lowering and interruption preserve context; resumption refreshes freshness before claiming current values. No complication, notification or custom Always On surface is introduced. Crown scrolling, wrist-state rendering and system presentation are implementation verification items, not capabilities claimed here. [Designing for watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices).

## Framework-agnostic data/state model

```text
Daily = {personID, date, zone, freshness, availability,
         systemPresentationHandle?, verifiedMetricRows[], activityMode}
Weekly = {personID, start, endExclusive, zone, target,
          uniqueCompletedQualifyingSessions[], freshness, availability}
Availability = loading | available | unavailable | error

on open/resume/date-change:
    retain selected period and navigation context
    request current permitted data through an adapter
    evaluate Daily and Weekly independently

if current data available:
    show timestamp and supplied values
    use system presentation only if adapter supports authentic rendering
else if previously available snapshot remains permitted:
    show dated snapshot marked "Last updated [time]" / "May be out of date"
    do not present it as today's confirmed completion
else:
    show "Activity data unavailable"; do not draw empty rings as zero

weekly when available and target > 0:
    actual = count(distinct qualifying session IDs in period)
    trackFill = clamp(actual / target, 0, 1)
    display actual + " of " + target + " sessions"  // may exceed target
    completion = actual >= target
weekly when target absent or invalid:
    show "Weekly goal not set"; omit track and completion
weekly when unavailable:
    show "Weekly progress unavailable"; omit track and completion
```

Loading uses “Updating activity…” without inventing values. Errors retain a labeled Retry action; unavailable data is not necessarily a known authorization denial. If the user elects to connect activity data, explain its summary purpose, request only needed access through the platform authorization flow when available, and recheck access on use. Do not add conflicting permission switches or repeatedly prompt after unavailable reads. Keep the independently available weekly section usable. [HealthKit — Privacy protection](https://developer.apple.com/design/human-interface-guidelines/healthkit#Privacy-protection).

If no authentic system renderer is available in the chosen stack, use the labeled text summary and state “Activity rings unavailable here.” Do not counterfeit a purple or approximately correct system graphic. Delivery of the authentic ring surface remains an integration dependency.

## Accessible presentation

Use text for every metric, unit, completion state and freshness message, so color and ring closure carry no exclusive information. Preserve prescribed ring colors; if associated colored labels lack contrast, add an equivalent readable neutral text summary outside the ring container rather than recoloring the rings. Measure actual foreground/background combinations in light, dark and Increase Contrast appearances. Use readable platform text defaults as the starting point (iOS 17 pt; watchOS 16 pt). Preserve essential content at 200% text on iOS and 140% on watchOS through vertical reflow. Give buttons at least 44 × 44 pt activation areas on both platforms as this specification's chosen target; do not shrink them to force a single screen. [Accessibility — Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

Expose headings and one grouped text item per metric: e.g. “Roll, 8 of 12 hours, today.” Expose the weekly track as a read-only value with its purpose, actual, goal and endpoints; it is not an adjustable slider. The details button's name is “Weekly goal details.” Keep graphical rings out of duplicate reading order only if their full information is already exposed in adjacent accessible text. Refresh values without moving focus; retain focus on the details button on return. No celebratory animation or audio is required. [VoiceOver — Descriptions and Navigation](https://developer.apple.com/design/human-interface-guidelines/voiceover#Descriptions).

## Worked before → after

**Before, supplied proposal:** purple system rings in changed order, wheelchair users seeing Stand, and completion presented as proof of a clinical outcome. The brief supplies no screenshot, exact reordered sequence, metric values or clinical claim wording.

**After, illustrative fixture, not observed user data:** Alex, wheelchair mode verified by the adapter, today: Move 420/500 kcal; Exercise 30/30 min; Roll 8/12 hours. Show the authentic three-ring system summary in its standard order and colors, black clearance intact. Text says “Exercise · 30 of 30 min · Daily goal met”; Roll remains incomplete. There is no clinical success statement.

Below a separated weekly heading, display “Oct 19–25, 2026 · 2 of 3 sessions,” endpoints 0 and 3 sessions, and a track filled two thirds. Opening details lists the two distinct completed session IDs and the counting rule. Adding a third qualifying session changes this section to “3 of 3 sessions · Weekly goal met.” It does not alter daily rings. A fourth session reads “4 of 3 sessions” with a full track. Revoking availability removes unsupported current claims, rather than displaying zero activity.

## Acceptance checks and audit status

**Passed — static specification checks:** read `interface.md`; explicitly read the installed root skill, selected family routes, topic procedures before their source guides, and searched the topic index. The revised contract rejects recoloring/reordering, separates daily/weekly periods, identifies one person, constrains completion language, handles legitimate iOS ring variation, and gives wheelchair-label and unavailable-data rules. These passes establish document coverage only.

**Failed — supplied proposal against the revised contract:** purple system rings; altered system order; clinical-outcome inference; Stand copy for the intended wheelchair treatment. These are described proposal defects, not measured runtime failures. Wheelchair terminology remains source-limited as noted above.

**Not executed — implementation acceptance scenarios:**

| Scenario | Required observable result |
|---|---|
| Authentic ring rendering on each platform | Standard system order/colors/opacity/proportions, black background, margin ≥ inter-ring gap, no clipping/overlap at supported sizes |
| Wheelchair mode / other mode / unknown mode | Verified Roll hours shown as Roll; other mode retains source semantics; unknown mapping never silently relabels Stand or invents Roll |
| iOS paired, unpaired, mixed historical dates | System-supplied three/single-ring variation retained; missing measures not fabricated |
| Zero, 2/3, 3/3, 4/3 weekly sessions | Fill 0, 2/3, 1, 1; true numeric totals retained; completion only at ≥ goal |
| Duplicate, canceled, deleted and boundary sessions | Count rule applied once per ID; corrections decrease total; week boundaries use displayed zone |
| Invalid target, missing data, loading, error, changed access | No false zero/completion; independent sections remain usable; Retry works without repeated authorization prompts |
| Weekly completion or daily ring closes | Only scoped activity-goal language appears; no clinical outcome inferred or redundant system notification generated |
| iOS rotation, 200% text; watchOS 140% text | Essential labels, units, periods and controls reflow without loss; daily/weekly separation remains clear |
| VoiceOver and applicable assistive input | Read in specified order, current values spoken once, details reachable/activatable, Back restores focus; no precision gesture required |
| Actual colors and control geometry | Contrast measured in light/dark/Increase Contrast; chosen 44 × 44 pt activation areas verified on iOS/watchOS |
| Interrupted app / lowered wrist / disconnected phone | Context retained, freshness represented accurately; available Watch summary remains useful independently |

## Evidence limits

Only supplied local text and installed instructions were consulted; no web access was used. Official links above are citations from the installed snapshot, not live verification. Sources are local summaries dated/retrieved October 25, 2026, not SDK documentation or clinical validation. No screenshots, executable implementation, real data, authorization flow or renderer were supplied. No device, SDK compilation, GUI, contrast measurement, accessibility execution, Crown response, wrist behavior, pairing behavior or medical efficacy was tested. The wheelchair mapping and session-goal definition are explicit product decisions requiring integration validation; local guidance does not resolve Roll API details. An authentic ring adapter and verified wheelchair metric mapping are release dependencies for the full treatment; the text fallback is fully specified without assuming Apple SDK availability.
