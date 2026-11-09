# Watch workout summary — Always On specification

Platform: watchOS on hardware supporting Always On. This contract applies while the summary is eligible to remain visible as the frontmost app; it does not promise indefinite background visibility or refresh. Respect system Always On and privacy settings. If Always On is unavailable or disabled, allow the system to turn the display off and restore the same summary on activation.

## Task and scope

Let the wearer glance at a completed workout's recorded duration and return to its private heart-rate history when actively viewing. Treat this as a completed-workout summary, not a live recording screen. Workout identity, recorded values, selected history range, and scroll position survive wrist-state changes. No new collection, permissions, sharing, or storage behavior is introduced.

## Active and dimmed pair

Use the same vertical structure in both states: summary heading, recorded-duration row, heart-rate-history region, and a small status line. Preserve each region's frame and the current viewport; do not scroll to the top on wrist down or raise. Any existing controls retain their positions and use an unavailable appearance while dimmed.

| Region | Active / wrist up | Always On / wrist down |
| --- | --- | --- |
| Heading | “Workout summary” | Same heading, secondary emphasis |
| Primary metric | “Recorded duration” and the recorded value, including units | Same value and units, legible and stationary; this completed-workout metric does not tick |
| Heart-rate region | Recorded history for the selected range; show gaps as missing data rather than inventing samples | Replace all samples, axes, heart-rate numbers, averages, peaks, and revealing chart shapes with a neutral placeholder in the same frame: “Heart-rate history hidden” |
| Status | “Recorded data” when final; “Summary updating” only while reconciliation is actually pending; “Update unavailable” after a failed attempt | “Recorded data” when final, otherwise “Updates on wrist raise”; never label cached data live |

Recorded duration is the deliberately retained personal metric because it supplies useful workout context with less exposure than detailed heart-rate history. Do not infer that all workout metrics are safe to expose. If system privacy restrictions require more redaction, substitute “Workout summary” for the duration value in the same row. If duration is absent, show “Not recorded” in either state. Hide unavailable heart-rate data with “No heart-rate data” in the active history region; wrist down still uses the neutral privacy placeholder.

## Appearance and motion

Remove the repeating second-by-second pulse in both states: a completed summary has no live heartbeat to communicate. On wrist down, let any in-flight appearance transition settle using supported system motion, then remain still. Do not replay historical pulses or animate incoming samples. With Reduce Motion enabled, switch directly to the stable state without decorative movement.

Use a predominantly dark background, subdued secondary labels and fills, and minimal large color areas in Always On. Replace the maximum-brightness requirement with system-managed dimming; do not force brightness or simulate dimming by making the primary metric unreadable. Keep text and units discernible. The privacy placeholder must replace the sensitive rendering at dimmed-state entry, before any optional cosmetic transition; do not fade private history through the dimmed state.

## Transitions and freshness

1. **Active → dimmed:** retain workout identity, history selection, scroll position, and recorded data; apply redaction immediately; settle motion and reduce secondary emphasis. Do not initiate a per-second timer or polling loop for this presentation.
2. **While dimmed:** use the last confirmed recorded summary. No refresh is required for a completed summary. If a pending summary receives a permitted system-delivered update, coalesce it into a single subtle value replacement without animation or layout movement. Do not claim a guaranteed cadence. Keep heart-rate content redacted regardless of updates.
3. **Wrist raise or system activation by tap → active:** restore normal hierarchy and the same task context in place; show private history only when system privacy/access conditions permit. Restore controls to their active appearance. This change in detail and emphasis is the clear return-to-active cue; add no splash screen, pulse, or artificial delay.
4. **Refresh pending on activation:** display the last recorded values with “Summary updating,” reconcile when execution is available, and replace only confirmed values. If reconciliation fails, retain recorded values and show “Update unavailable”; never extrapolate heart rate, fabricate gaps, or silently imply freshness. A fully recorded summary needs no refresh spinner.
5. **Interruption or rapid wrist changes:** the latest system state wins. Cancel obsolete transitions; do not queue animations or lose selection. A wake gesture activates the view and must not also invoke an underlying action.

## Acceptance contract

- Compare active/dimmed views for the same workout and viewport: region frames, control positions, history selection, and scroll position remain stable.
- Lower the wrist during motion and during an update: no private heart-rate values or chart silhouettes remain visible; the display settles without recurring motion.
- Withhold all dimmed refresh opportunities: recorded duration remains truthful and useful; pending data says “Updates on wrist raise.” No simulated seconds or live claim appears.
- Raise the wrist with a pending, successful, and failed refresh: active emphasis and permitted detail return in place, with accurate status and no fabricated samples.
- Exercise missing duration/history, stronger system privacy restrictions, disabled Always On, interruption, rapid wrist changes, and Reduce Motion. Confirm the corresponding fallback above and no accidental action on wake.
- On supported Watch hardware, verify primary-metric readability in actual dimming, privacy at transition boundaries, wake behavior, and lack of recurrent animation. These are required implementation checks, not evidence supplied by this document.

## Guidance basis

The stable layout, redaction, useful retained context, subdued detail, infrequent updates, and settling motion follow [Always On — Best practices](https://developer.apple.com/design/human-interface-guidelines/always-on#Best-practices). Glance scope and continuity follow [Designing for watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices). Truthful recorded summaries follow [Workouts](https://developer.apple.com/design/human-interface-guidelines/workouts#Best-practices). Exposure minimization follows [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices); interruptible, reduced motion follows [Motion](https://developer.apple.com/design/human-interface-guidelines/motion#Best-practices). These links identify the official sources of the installed local guidance; they were not fetched. Exact retained fields, copy, and refresh rules above are product decisions applying that guidance.
