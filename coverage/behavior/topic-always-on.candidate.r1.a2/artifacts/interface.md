# Watch workout summary — Always On specification

Platform: watchOS on hardware supporting Always On. Apply this contract while the summary is frontmost and the system permits Always On. Respect system settings; if unavailable or disabled, let the display turn off normally. Do not simulate Always On or request maximum brightness.

## Task and state

Support a brief glance at recorded workout results, with private heart-rate history available on wrist raise. Interpret “summary” as a completed-workout surface, not an active-session timer. Preserve workout identifier, recorded data, save status, selected detail and viewport across wrist transitions. Lowering or raising the wrist must not save, discard, restart or end a workout. Display “Saved” only after confirmed persistence.

No controls or other metric inventory were supplied. Duration and status below are proposed fields, populated only from real recorded data. If the implementation has actions, retain their positions and show unavailable appearances while dimmed; waking must not activate an underlying action.

## Active/dimmed pair

Keep row order and reserved bounds identical. Use a dark background, reduce secondary fills and detail, and keep primary text legible. Let watchOS manage brightness. Hardware readability remains to be validated.

| Field | Active: wrist raised | Always On: wrist lowered |
|---|---|---|
| Header | Workout summary | Same text and position |
| Status | Workout ended; separate Saved, Saving… or Not saved when known | Same truthful status, no animated spinner |
| Recorded duration | Final recorded duration, e.g. 32 min; Not recorded if absent | Same static value, no ticking seconds |
| Heart-rate region | Recorded private history, or Heart-rate history unavailable | Neutral placeholder and Heart-rate details hidden; replace all samples, axes, extrema, averages and value-bearing graphics within the same bounds |
| Data status | Recorded summary · updated 10:42, using last successful data timestamp; Summary unavailable if no snapshot | Same absolute timestamp or unavailable label; never Live or Just now |

Default to hiding heart-rate detail at wrist down. Retain duration as useful expected workout context; do not automatically expose additional health metrics. This is a product privacy choice, not a prohibition on all workout metrics. Redaction changes presentation only, not stored records or authorization. Add no collection, transfer or permission request for this adaptation.

## Transitions and update rules

1. **Active → dimmed:** On the system dimmed-state signal, redact immediately, before any visual settling. Preserve layout and viewport. Remove the repeating second-by-second pulse. Ease any in-flight appearance animation toward rest using supported system behavior; never delay redaction to complete a pulse. The resting summary has no recurring animation in either state.
2. **While dimmed:** Retain the last successful snapshot and its absolute timestamp. No app-owned repeating refresh, ticking counter or per-second animation. Completed metrics stay fixed. A system-delivered meaningful correction or confirmed save result may update once in place without animation, retaining redaction. No background refresh cadence is promised.
3. **Dimmed → active:** On wrist raise or system-recognized wake interaction, restore normal system-managed appearance and permitted private details in the original bounds. The visible restoration distinguishes active from dimmed. Retain workout and viewport; do not replay missed updates. Read the latest available snapshot. While refresh is pending retain the timestamped snapshot; on failure show Couldn’t update · last updated 10:42. Never fabricate freshness.
4. **Rapid transitions/interruption:** Latest system state wins; cancel obsolete transitions without queuing playback. No delayed private frame may appear after lowering. Restore the same summary when the system returns to it. If access was revoked, show unavailable content rather than cached private history.

## Acceptance checks

- Compare active/dimmed views: row bounds, viewport and any action positions match; heart-rate detail is fully replaced while primary context remains readable.
- Lower during motion or data delivery: redaction takes precedence, movement rests, and no second-by-second work continues.
- Withhold updates while dimmed: snapshot and timestamp stay truthful; pending/failed refresh on raise never appears live. Valid corrections update without replay.
- Rapidly raise/lower, wake by tap, interrupt and resume: preserve workout/context, trigger no action on wake, and reveal no obsolete private frame.
- Exercise missing duration/history, unknown save status, revoked access, and Always On disabled/unavailable: no invented metric, false Saved state, permission bypass or forced display behavior.

## Basis

Derived from the supplied local HIG snapshot: [Always On — Best practices](https://developer.apple.com/design/human-interface-guidelines/always-on#Best-practices) supports contextual workout information, private-detail redaction, stable layout, dimmed secondary detail, legibility and infrequent subtle updates. [Designing for watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices) supports brief glances; [Workouts](https://developer.apple.com/design/human-interface-guidelines/workouts#Best-practices) supports truthful recorded summaries. [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices) supports protecting granted data; [Motion](https://developer.apple.com/design/human-interface-guidelines/motion#Best-practices) supports purposeful movement. Exact fields, default redaction and absence of recurring refresh are application requirements, not universal Apple mandates. This is a specification, not verified API or device behavior.
