# iPhone neighborhood-events design audit

## Basis and decisions

The app’s primary outcome is finding nearby events. This audit treats the statements in [interface.md](interface.md) as verified specification evidence, not as observed runtime behavior. All five findings below are directly supported by that file. Ranking is a review judgment based on interference with that outcome; frequency, affected-user counts, and production severity are unknown.

Use an events-first entry point, stable navigation, unobscured event information, and explicit action states. Keep merchandise available as a secondary destination. These are framework-agnostic decisions; they require no Apple SDK.

Guidance was read from the installed package in this order: root `apple-hig/SKILL.md` → `subskills/apple-hig-getting-started/SKILL.md` → its `references/designing-for-ios.md` → `references/design-principles.md`. The family routes directly to these articles and contains no separate topic procedure for this review. No additional component-specific implementation is prescribed here.

## Ranked verified findings

| Rank | Evidence from interface.md | Effect and principle | Correction and acceptance check |
| --- | --- | --- | --- |
| 1 — High | “Launch opens an unrelated merchandise page” | The first screen diverts people from nearby events. **Purpose** focuses on the valuable outcome; **Agency** takes people directly to content. | On a fresh ordinary launch, show Discover with nearby-event content or an actionable location-selection state. No merchandise step is required. Verify launch reaches that state directly. |
| 2 — High | “opaque decoration obscures event times” | Essential information for choosing an event is unavailable. **Simplicity** calls for readily available essentials; **Delight** allows character without distracting from tasks. | Place event time in the content layer; decoration must neither cover it nor intercept its controls. Verify complete date/time remains readable in every supported layout and text-size configuration. |
| 3 — High | “navigation labels change after each tap” | People cannot reliably recognize destinations or understand where they are. **Familiarity** calls for consistent equivalent controls; **Flexibility** calls for predictable controls and preserved context. | Keep destination identity, label, and order stable. Change only selection state as navigation occurs. Verify repeated navigation preserves labels and returns to the same destination and prior browsing context. |
| 4 — Medium | “actions give no pending/success feedback” | People cannot tell whether an action is processing or completed and may repeat it. **Familiarity** explicitly calls for progress and change feedback. | For asynchronous actions, expose pending, success, and failure states associated with the initiating action. Prevent duplicate submissions while pending. Verify delayed completion, successful completion, failure, and retry. Failure/retry behavior is a proposed completeness requirement, not an observed defect. |
| 5 — Medium | “promotional content receives greater prominence than events” | The hierarchy privileges a secondary commercial task. **Purpose** and **Simplicity** support prioritizing the core outcome and a recognizable hierarchy. | Put the event heading, discovery controls, and event results before optional promotion in reading and interaction order. Give promotions lower emphasis and no blocking presentation. Verify the first content region serves event discovery, including when results are empty. |

Source rules: [Purpose](https://developer.apple.com/design/human-interface-guidelines/design-principles#Purpose), [Agency](https://developer.apple.com/design/human-interface-guidelines/design-principles#Agency), [Familiarity](https://developer.apple.com/design/human-interface-guidelines/design-principles#Familiarity), [Flexibility](https://developer.apple.com/design/human-interface-guidelines/design-principles#Flexibility), [Simplicity](https://developer.apple.com/design/human-interface-guidelines/design-principles#Simplicity), and [Delight](https://developer.apple.com/design/human-interface-guidelines/design-principles#Delight). The local [iOS best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices) also support clear primary content/actions and adaptation to orientation and Dynamic Type. Links identify official sources; they were not opened for this audit.

## Worked before/after

Scenario: someone opens the app to find an event for tonight. Event data and the “Save” action below are illustrative fixtures, not supplied product evidence.

**Before — supported sequence:** launch shows merchandise; navigation labels change when tapped; on reaching events, decoration obscures times and promotion has greater prominence. Any action provides neither pending nor success feedback. The exact labels, number of taps, visual arrangement, and available actions are unknown.

**After — proposed sequence:**

1. Launch opens **Discover**. A stable navigation set could be **Discover · Saved · Shop**; these names and destinations are proposals, not existing requirements.
2. Discover shows the chosen neighborhood and event results first. If location is unknown, show a manual neighborhood choice with an optional location-use action. This avoids making a permission decision a prerequisite for discovery.
3. An illustrative row reads “Community Night Market — Tonight, 6–9 PM — Oak Square.” Its date/time stays fully visible; decorative art occupies a separate region. Promotion follows the event content.
4. Tap the illustrative **Save** action. It changes to **Saving…**, then **Saved** on confirmed success. A failed request shows “Couldn’t save. Try again.” while retaining the event and browsing position. An **Unsave** action makes the change reversible.
5. Navigate to Shop and return. Labels and order remain stable; Discover retains its neighborhood, filters, and scroll position.

Manual location choice, specific navigation names, Save/Unsave, and retained filter/scroll details are design proposals informed by Agency and Flexibility. They are not additional verified findings. If location is requested, explain why at the point of use and collect only what is needed, following [Responsibility](https://developer.apple.com/design/human-interface-guidelines/design-principles#Responsibility).

## Framework-agnostic behavior specification

```text
DESTINATIONS = fixed ordered identities and labels
selectedDestination = Discover on fresh ordinary launch

Discover:
  if no neighborhood is available:
    show neighborhood chooser and optional location-use action
  else:
    show event heading, discovery controls, then results
    if loading: expose loading state
    if empty: show no-results explanation and ways to change discovery inputs
    if failed: preserve inputs and offer retry
  show optional promotion after discovery content
  reserve separate space for decoration; never obscure essential information

navigate(destination):
  retain current destination's browsing state
  select destination without renaming or reordering DESTINATIONS
  restore destination's browsing state

performAsyncAction(event, action):
  if this event/action is pending: ignore duplicate submission
  expose pending state with an understandable label
  submit once
  on confirmed success: expose resulting state and available reversal
  on failure: preserve prior data; expose error and retry
  expose state changes as text and accessible status information,
    without requiring color alone or unexpectedly moving focus
```

Loading, empty, error, accessible-status, and reversal details are proposed supporting behavior. No supplied evidence establishes their current implementation.

## Acceptance checks

These are checks to execute against a future implementation; none has been run here.

- **Launch:** Fresh ordinary launch reaches events or neighborhood selection without entering merchandise. Test direct navigation to Shop separately so the correction does not remove intentional access.
- **Essential content:** With long event names, long time strings, portrait/landscape layouts, and supported Dynamic Type sizes, all essential event information remains readable. Decoration cannot cover it or block interaction. Inspect light and dark appearances.
- **Navigation:** Capture labels and order, visit every destination twice, then compare. Verify selection is identifiable and returning restores the chosen neighborhood and browsing position.
- **Action lifecycle:** Hold a request pending, activate repeatedly, then resolve success or failure. Expect one submission, understandable pending feedback, confirmed result on success, and retained context plus working retry on failure. Check reversal where supported by the action.
- **Hierarchy:** In loaded, loading, empty, and error states, event discovery occupies the primary content region. Promotions never gate access or precede the primary discovery task in reading order.
- **Assistive interaction:** On an actual implementation, check accessible names, reading order, event-time exposure, action-state announcements, and focus preservation using appropriate assistive technology. These remain validation targets, not accessibility conformance claims.

## Evidence limits and remaining principles

Only interface.md and the installed skill instructions/articles were used. No screenshots, source implementation, event dataset, measurements, device, SDK, GUI, simulator, or accessibility execution were supplied or performed. This is a specification audit, not a visual or runtime test report. It cannot establish contrast, touch-target dimensions, actual text clipping, animation behavior, latency, permission practices, or accessibility conformance.

The eight core principles were considered. Purpose, Agency, Familiarity, Simplicity, and Delight directly inform the verified findings; Flexibility supports predictable navigation and proposed adaptation checks. Responsibility cannot be judged from the supplied evidence. Craft calls for prototyping and testing in real settings: those checks remain outstanding, and no claim about the team's process is justified. Delight does not require removing decoration; the correction preserves character while protecting useful content.

The installed references describe themselves as original application guidance based on a dated HIG snapshot, rather than verbatim Apple text. Their retrieval date is 2026-10-25; the principles article lists a June 8, 2026 source revision. No current-web verification or independent media review is claimed. Recommendations preserve the guidance's qualitative scope: the proposed navigation names and priority ordering are product judgments, not universal Apple mandates.
