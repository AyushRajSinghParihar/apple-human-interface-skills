# Rowing companion: revised interaction specification

## Scope and decisions

Input: `interface.md`, a watchOS behavior brief, with no implementation, screenshots, metric definitions, permission categories, or hardware inventory. This is a framework-agnostic design contract. The following lifecycle, thresholds, and persistence policies are product decisions; they are not claimed Apple API behavior.

1. **Start means a request to start, not proof of recording.** Resolve required access and confirm recorder readiness before displaying Active or advancing workout time. Request only access needed by the selected feature, at its point of use. Optional metrics must not gate a timer-only session. This applies [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission).
2. **Make Pause immediately reachable.** The first active screen contains state, elapsed active time, one supported live rowing metric, and a full-width Pause button. Move the long chart to secondary detail; no scrolling is required to pause. A separate Controls destination, one explicit tap away, contains End Workout. This combines the glance priority of [Designing for watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices) with [Workouts](https://developer.apple.com/design/human-interface-guidelines/workouts#Best-practices), which describes separate controls and metrics surfaces. No Now Playing page is added without an audio feature.
3. **End preserves work.** End Workout stops recording into a retained draft and opens a summary; it never deletes samples. Saving and discarding are separate explicit decisions. Brief accidental sessions get an explicit save/discard resolution, as advised in [Workouts](https://developer.apple.com/design/human-interface-guidelines/workouts#Best-practices).
4. **Missing data is unavailable, not zero effort.** Keep valid remaining metrics useful and explain the affected source. Do not import swimming limitations or promise rowing-specific sensor accuracy from general workout guidance. See [Workouts — Best practices](https://developer.apple.com/design/human-interface-guidelines/workouts#Best-practices).
5. **Leaving is distinct from pausing.** Wrist lowering or app departure preserves the session. Continue only while a recorder can confirm continuity; an actual recording interruption produces Interrupted and requires an explicit Resume. The watchOS platform guide supports progress preservation. The local [Multitasking — Platform considerations](https://developer.apple.com/design/human-interface-guidelines/multitasking#Platform-considerations) explicitly excludes that multitasking mode on watchOS; its media pause rules are not used to justify pausing this workout.

## Data and access contract

| Data/capability | Purpose and minimum scope | Unavailable behavior |
| --- | --- | --- |
| Monotonic clock and local draft storage | Active duration and recoverable session | Cannot start if timing or durable recording cannot be established |
| Selected rowing metric source | Display and record only supported values, with units and source | Optional; offer timer-only recording, label metric unavailable |
| Protected source access, if actually required | Only the selected metric's needed categories; no unrelated permissions | Unknown/requesting/declined never masquerades as granted; use the same unavailable path |
| External health-store write, location, phone/cloud transfer | Not established by the brief | Outside this design's recording promise; no inferred collection or export |

The implementation must supply a capability manifest listing each real metric, source, unit, access requirement, update interval, and validity rules before exposing it. No default claim of heart rate, distance, GPS, calories, power, or stroke-rate availability. “Saved” below means durable local storage only.

Permission flow: Start → Preparing, “Preparing workout — Not recording yet” → request actual required access through the platform's authorization mechanism → establish recorder → Active. No custom imitation permission prompt. Example purpose copy, only if true for the eventual source: “We use rowing sensor readings to show and record your effort during this workout.” Replace with a precise category-specific sentence when the source is known.

Declined or unavailable optional access: show “Rowing data unavailable” with Start Timer Only and Back. Required recording capability failure: “Workout couldn't start. Nothing was recorded.” with Retry and Back. Never loop prompts after denial; explain that access can be changed through the platform's supported settings route, without inventing a settings deep link. Returning to a pending request rechecks its result; it does not start automatically after cancellation.

## State model and transitions

Store orthogonal fields: `phase`, `visibility`, `metricAvailability[metric]`, `sessionId`, `operationId`, acknowledged active intervals, samples with provenance, gaps, and durable draft revision. Visibility is foreground, dimmed, or away; it is not recording state. Metric availability is valid, stale, or unavailable, not a workout phase.

| Phase | Presentation and actions | Transition and data consequence |
| --- | --- | --- |
| Ready | Start | Start → Preparing; no active interval yet |
| Preparing | Not recording yet; Cancel | Read access and readiness; success → Active only after durable start acknowledgment. Cancel → Ready. Failure → inline recovery above |
| Active | “Recording”, active duration, valid metric or unavailable explanation; Pause; Controls | Pause → pending stop acknowledgment → Paused. End Workout → pending stop → Review. Dropout changes only that metric |
| Paused | “Paused”, frozen active duration; Resume and End Workout | Resume → readiness check → Active acknowledgment, new interval. Failure leaves Paused with explanation |
| Interrupted | “Recording interrupted”, last confirmed duration, reason if known; Resume and End Workout | Resume revalidates capability and opens a new interval after acknowledgment. End → Review. Unknown gap remains missing |
| Review | “Workout ended”; retained-data summary; Save Workout, Discard Workout | Save → Saving. Discard opens confirmation; Cancel retains Review |
| Saving | “Saving workout”; prevent duplicate save | Durable success → Saved. Failure → Review with “Couldn't save. Draft retained.” and Retry |
| Saved | “Saved on this watch”, summary; Done | Done → Ready; repeated completion cannot create another session |
| Discarded | “Workout discarded”; Done | Enter only after confirmed deletion succeeds; Done → Ready |

Every pending start/pause/resume/end carries a unique operation ID. Repeated taps do not duplicate operations. While pausing or ending, show “Pausing…” or “Ending…” and the last confirmed state; do not prematurely show a frozen final duration or successful outcome. If acknowledgment cannot establish continuity, enter Interrupted, explaining uncertainty. If finalization fails, retain the draft and offer Retry; never present Saved.

End stops new collection at the acknowledged end boundary. Review is a completed draft, so Back or app departure preserves it and reopening returns to Review. There is no automatic resume from Review. Discard confirmation: title “Discard Workout?”, message “This removes this workout's recorded data.” Buttons Discard (destructive) and Cancel (cancellation), with no implicit default. In a vertical stack, put Discard above Cancel; dismissal cancels and returns to Review. A deletion failure retains Review with a retry explanation. Never stack alerts. These are conservative product choices within [Alerts — Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons); that guide permits a normal default for explicitly requested destruction, rather than universally prohibiting it. [Modality](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices) supports matching all exits to the same preservation policy.

For active duration under 10 seconds, Review adds “Short workout — Save or discard this recording.” Ten seconds is a provisional product threshold interpreting “a few seconds,” not an Apple requirement. Never auto-delete it. Review can remain pending indefinitely without choosing either outcome.

## Active, dimmed, and interrupted presentation

Use short text labels, large high-contrast primary values, explicit units, and state words rather than color alone. Active layout, in order: state; elapsed active time; selected valid rowing metric or availability text; full-width Pause; Controls link. Controls places Resume (when paused) and End Workout in clearly separate targets; Back returns to the same session. The chart is optional detail below the primary task, with gaps rather than zero-filled dropout segments.

Use contrasting capsule buttons, full-width for primary actions, equal heights for peers, and separated selectable regions of at least 44 × 44 pt per the installed general button guidance. Custom controls require visible press feedback. Labels and unavailable reasons must remain readable without overlapping targets; this is a layout requirement, not a measured result. See [Buttons — Best practices and watchOS](https://developer.apple.com/design/human-interface-guidelines/buttons#watchOS). Primary emphasis goes to Pause while Active, Resume while Paused/Interrupted, and Save Workout in Review; End and Discard never share the primary moving-user target.

On supported Always On hardware, retain layout and control positions while dimming secondary content and rendering controls unavailable until active interaction resumes. Keep state and elapsed time legible; retain the selected rowing metric as expected workout context if privacy settings permit. Redact optional sensitive health details and any fields the person has hidden; never override platform privacy behavior. No animated chart in the dimmed view. Use coarse elapsed minutes and latest valid source value at permitted refresh opportunities, never imply a continuous update guarantee. Wrist raise/tap restores interaction in the same phase and destination, reconciled with recorder state. Unsupported or disabled Always On may show no app content; recording continuity is independent. This applies [Always On — Best practices](https://developer.apple.com/design/human-interface-guidelines/always-on#Best-practices).

A metric becomes stale when the source reports failure or sample age exceeds `max(3 × declared sample interval, 5 seconds)`; this provisional timeout must be tuned to the actual source. Replace the live value with “—” and “Sensor unavailable”; details may show “Last reading: [value/unit], [age] ago” explicitly as historical. Resume the live display only on a valid new sample. Valid zero is allowed only when actually measured. Do not interpolate missing effort, treat missing samples as zero in averages, or extend cumulative distance through gaps. Label partial totals and coverage; omit an aggregate when its validity cannot be established.

## Departure and recovery contract

- Wrist down: retain phase and draft. Dimmed appearance never pauses or ends a workout.
- App switch/ordinary departure: checkpoint state and acknowledged samples. Continue if the recorder demonstrably remains active. Return directly to the current session, not Ready or the chart.
- Recorder suspension, permission revocation, or process loss without verified continuity: close the confirmed interval at the last trusted boundary, preserve samples, mark an unknown gap, and show Interrupted on return. Do not infer recorded time from wall-clock absence.
- Reopen after termination: recover session ID, phase, data, and pending operation; reconcile against durable recorder truth. Verified ongoing recording → Active; verified pause → Paused; uncertain continuity → Interrupted; ended draft → Review. Never silently create a second workout.
- If the person leaves while Preparing, a canceled or obsolete operation cannot activate recording later. Late callbacks must be reconciled and any started recorder stopped safely, with resulting draft retained.

Pseudocode contract:

```text
on(event):
  serialize per sessionId
  reject duplicate or obsolete operationId
  if metricEvent: validate source/timestamp; append valid sample or gap
  if visibilityEvent: checkpoint; change visibility only
  if recorderAcknowledgment:
    atomically persist boundary + phase + operation completion
  if continuityLost:
    persist last trusted boundary + unknown gap + Interrupted
  if confirmedDiscard:
    delete draft atomically; enter Discarded only on success
  render from durable phase and reconciled capability state

activeDuration = sum(acknowledged active interval lengths)
# Exclude paused time and unverified gaps; expose partial duration if uncertain.
```

## Worked before/after

**Before, as supplied:** Start appears active while permission remains unresolved. During rowing, the person must traverse a long chart to Pause. A sensor dropout appears as zero effort. End immediately erases the session. Departure recovery is unspecified, so no existing recovery failure is asserted.

**After, illustrative trace:** At 00:00 the person taps Start; Preparing says Not recording yet. Optional sensor access is declined; Start Timer Only records a timer workout after recorder acknowledgment, showing “Rowing data unavailable.” Later access is granted through a supported route and valid readings become available; their provenance and coverage start there. At active time 04:00 the source stops reporting. At the declared freshness timeout the display changes to “— / Sensor unavailable”; time continues and the chart records a gap. At 04:20 Pause is one tap away and freezes acknowledged active time. The person leaves; return still shows Paused at 04:20. Resume acknowledges a new interval. At 04:50 an actual recorder interruption occurs; return shows Interrupted at the last confirmed boundary, excluding the unknown gap. End Workout opens a partial-data Review. Canceling Discard keeps the draft. Save Workout yields Saved on this watch only after durable success. No missing metric becomes zero and no departure deletes the session.

## Acceptance checks and evidence limits

**Passed — static specification review only:** The revised contract explicitly covers start authorization, pause/resume/end, brief sessions, dropout, wrist return, departure, interruption, recovery, and save/discard exits. Controls have named outcomes and pending states. Missing data is distinguished from valid zero. The worked trace is consistent with the defined transitions; this is a manual specification trace, not executed software.

**Failed — supplied brief against this revised contract:** Active appearance precedes readiness; Pause requires chart traversal; End irreversibly deletes immediately; missing sensor data is represented as zero. These are supplied behavior statements, not device observations. Existing departure behavior cannot be classified from the brief.

**Not executed — implementation acceptance scenarios:**

| Check | Required observable result |
| --- | --- |
| Start with access unknown, declined, canceled, or delayed | No recording label/time before acknowledgment; optional-data refusal permits explicit timer-only choice; no stale callback starts a canceled session |
| Repeat Start/Pause/Resume/End rapidly | One operation and one interval boundary per acknowledged transition; failures leave truthful state |
| Pause from initial active screen | No chart traversal; clear Paused state; resumed time excludes pause |
| End after 3 seconds; dismiss Review; reopen | Explicit short-session choice remains, data retained, no false Saved status |
| Discard, then Cancel or supported dismissal | Same draft and summary retained; confirmed discard alone deletes; deletion failure remains recoverable |
| Save twice; simulate write failure and restart | One saved session; retained draft on failure; pending save reconciles without duplication |
| Drop sensor and restore it; inject valid zero | Missing shown as unavailable with chart gap; valid zero remains valid; aggregates show partial coverage |
| Lower wrist, switch away, terminate, and return | Stable context; verified recording may continue; uncertain intervals excluded and labeled Interrupted; explicit Resume required |
| Render shortest watch viewport and enlarged text | Pause and primary status usable, labels readable, targets separated and measured; detailed content may scroll |
| Test supported Always On and privacy settings | Layout preserved, no hidden-field exposure, same session on return; no unsupported background or refresh promise |

No device, Apple SDK, simulator, GUI, sensor, physical exercise, assistive-technology, contrast measurement, target measurement, haptic, native authorization, energy, or background-execution test was run. Those checks remain unverified. No source proves a particular rowing sensor exists or is accurate. No SDK integration or external health-store save is specified or claimed.

Evidence was limited to `interface.md` and installed apple-hig instructions and references. Root SKILL.md was explicitly read; topic-index rows were searched; selected family instructions and topic procedures were read before their references: watchOS, Workouts, Buttons, Alerts, Modality, Privacy, Multitasking, and Always On. Official links above are attribution from the local snapshot, not live-web verification. The installed references identify a 2026-10-25 snapshot/retrieval date and describe themselves as derived application guidance; independent source/media review and current API availability were not established. No browsing was performed.
