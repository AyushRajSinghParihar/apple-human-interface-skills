# Revised rowing companion interaction specification

This replaces the behavior described in `interface.md`. Target: watchOS, brief glances while rowing, with local session continuity. This is a framework-agnostic design contract, not an SDK implementation. No sensor, storage backend, or Apple Health integration is established by the supplied brief.

## Decisions and source basis

| Supplied behavior | Revised decision | Basis |
| --- | --- | --- |
| Start appears active before data permission resolves | Resolve access before offering a recording Start; retain a useful timer-only path | [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission), [HealthKit — Privacy protection](https://developer.apple.com/design/human-interface-guidelines/healthkit#Privacy-protection) |
| Pause is below a long chart | Initial active viewport contains status, elapsed active time, current supported metric, and full-width Pause. Chart is secondary detail | [watchOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices), [Workouts — Best practices](https://developer.apple.com/design/human-interface-guidelines/workouts#Best-practices) |
| End immediately erases the session | End opens a retained review draft; saving and discarding are separate explicit outcomes | [Workouts](https://developer.apple.com/design/human-interface-guidelines/workouts#Best-practices), [Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices) |
| Dropout means zero effort | Unavailable is a distinct metric state; retain useful unaffected information | [Workouts — sensor limitations](https://developer.apple.com/design/human-interface-guidelines/workouts#Best-practices) |
| Person may leave mid-session | Preserve recording intent and progress across view departure; distinguish view absence from recorder failure | [watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices), [Always On](https://developer.apple.com/design/human-interface-guidelines/always-on#Best-practices) |

Exact fallback modes, freshness deadlines, recovery rules, persistence strategy, and the five-second brief-session threshold below are product decisions, not numerical HIG requirements. Apple guidance recommends glanceability and truthful session control; it does not establish this product's hardware capabilities.

## Access and preparation

| Data | Purpose | Access contract |
| --- | --- | --- |
| Local session ID, timing intervals and state | Timer, pause/resume and recovery | Local durable storage; no health-data permission required for timer-only mode |
| Supported rowing sensor samples | Show the selected metric with its unit | Request only access actually needed by the installed provider, when Enable Metrics is chosen; no sensor-specific capability is assumed |
| Heart rate, if supported and selected | Optional live heart rate | Request only that health category; absence does not block the timer |
| Apple Health workout write access, if integration exists | Optional export of a completed workout | Separate from local Save; request at export time and label export success separately |

Do not request location, contacts, unrelated health categories, or network transfer without an implemented feature needing them. Session data remains local in this contract; remote sync is outside scope. Protect stored health data using the eventual platform's established protections. An implementation adding health sharing must provide its actual privacy policy and accurate disclosures.

Preparation displays “Rowing” and “Choose recording mode,” with Enable Metrics and Use Timer Only. Neither is represented as starting a workout. Enable Metrics invokes the standard authorization mechanism available to the eventual implementation. Purpose copy, where accurate: “Use your heart rate to show it during your rowing workout.” Do not imitate the authorization dialog. While it is pending show “Checking access”; Start is disabled and explained, with no timer, sensor collection, or active-session claim. Leaving this screen starts nothing.

After resolution, show the supported available categories and omissions. A missing read result is not proof of denial: use “Heart rate unavailable,” unless the provider explicitly supplies a reason. If access is unavailable, offer Use Timer Only or a contextual route to system access settings where supported, without repeated prompts. Timer-only mode explicitly says “Timer only · No sensor metrics.” Start becomes enabled only after a mode is selected and required preparation has resolved. Recheck usable access when needed, including on resume; never treat past data as evidence of present permission.

## Session model and transitions

Keep three independent dimensions:

- `session`: READY, STARTING, RECORDING, PAUSED, INTERRUPTED, REVIEW, SAVING, SAVED, DISCARDED.
- `metric[channel]`: LIVE(value, unit, timestamp, source), UNAVAILABLE(reason, lastTimestamp), or UNSUPPORTED.
- `view`: ACTIVE, DIMMED, or AWAY. View changes never imply Pause or End.

Only one unfinished session may exist. Re-entry opens it rather than offering another Start.

| State / event | Result and visible contract |
| --- | --- |
| READY / Start | STARTING; disable duplicate Start; persist a new ID and selected mode, then request recorder start. “Starting” is not “Recording.” |
| STARTING / start acknowledgment | Persist the acknowledged start boundary; RECORDING, with “Recording” or “Timer running,” elapsed active time and Pause. |
| STARTING / failure or departure before acknowledgment | Cancel pending start if possible; otherwise reconcile its result by session ID. Show failure/recovery, never silently create a second session. |
| RECORDING / Pause | Commit a pause boundary and checkpoint; PAUSED. Freeze active elapsed time and metric accumulation. Show “Paused,” Resume, and End. If persistence fails, show that pause took effect but recovery storage failed. |
| PAUSED / Resume | Recheck capabilities; start a new active interval only on acknowledgment. Until then remain paused with “Resuming.” On failure retain PAUSED and offer retry or End. Optional sensor loss permits explicit timer-only continuation. |
| RECORDING / sensor loss | Remain RECORDING; only affected metric becomes UNAVAILABLE. Timer and independent channels continue. No automatic zero or auto-pause. |
| RECORDING or PAUSED / End | Close an active interval if needed; retain data in REVIEW. Display “Workout ended · Not saved.” End never deletes. |
| REVIEW / Continue Workout | Return to PAUSED with retained samples; Resume explicitly begins another interval. Review time is excluded. |
| REVIEW / Save | SAVING; disable repeated activation; save under the same session ID. Show “Saved on this watch” only after durable acknowledgment; SAVED summary. Failure returns to REVIEW with Retry Save and retained draft. |
| REVIEW / Discard | Show the confirmation defined below. Cancel retains REVIEW. Confirmed deletion becomes DISCARDED only after storage acknowledges deletion; failure retains the draft and offers retry. |
| Any unfinished state / view leaves or wrist lowers | Persist current state; view becomes AWAY or DIMMED. No automatic deletion, restart, or resume. |
| Recorder explicitly suspends, or continuity cannot be established after process loss | INTERRUPTED; close confirmed recording at the last trustworthy recorder boundary and mark the uncertain interval as a gap. “Recording interrupted · Check session.” Offer Resume and End. Never backfill unobserved exercise or silently resume. |
| Return to app | Reconcile durable state with recorder by session ID. If continuity is verified, restore RECORDING with actual current elapsed time; restore PAUSED, INTERRUPTED or REVIEW otherwise. Until reconciled, show “Checking session” and prevent conflicting commands. |

Checkpoint every transition before acknowledging its durable result and periodically during recording (product target: every five seconds). Persist sample timestamps, interval boundaries, gaps, selected mode and pending save operation. Recovery loss is bounded by the last successful checkpoint unless a trusted recorder can reconstruct it. Storage failures must be visible and must not be labeled Saved. Use monotonic timing during a process lifetime; across restart require trusted recorder timing rather than inventing elapsed duration from an unreliable wall-clock change.

## Active, paused and wrist-down presentation

The first active viewport has: Rowing / recording status; large elapsed active time; one prioritized available metric with unit; full-width Pause. If no provider exists, show time and “Timer only.” Do not invent an “effort” score. Separate session controls from chart/detail content; Pause is always available without scrolling the chart. PAUSED replaces Pause with Resume and exposes a separated End button. End is also available on a dedicated controls view one navigation step from recording. No unrelated navigation is embedded in the session. No Now Playing page is added without an audio feature.

Buttons use short visible labels, perceivable pressed/disabled states, nonoverlapping selectable areas of at least 44 × 44 pt, and common heights for peers. These dimensions follow the supplied [Buttons guide](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices); actual moving-user comfort remains untested. Prefer full-width capsule actions consistent with its [watchOS guidance](https://developer.apple.com/design/human-interface-guidelines/buttons#watchOS). Start, Pause, Resume, End, Save and Discard are immediate commands with the state effects above. End has normal role because it retains data; Discard communicates destruction. No hardware shortcut or Apple API is assumed.

Where Always On is supported, retain positions, status and rounded elapsed minutes; dim secondary content and present controls as unavailable until active interaction returns. Leave the detailed chart static and omit rapidly changing sensor values in dimmed mode. Retain workout timing as contextually expected information; redact heart rate and other detailed health readings. At wrist raise restore the same session and control positions, with reconciled values. Unsupported Always On means no dimmed rendering requirement; ordinary screen-off still preserves session state. No display transition changes the recorder.

## Sensor and summary truth

A provider must declare each channel's unit, provenance, expected cadence and freshness deadline before it can be displayed as live. If it cannot do so, omit that channel from live mode. For example only, a provider supplying one sample per second may declare a three-second deadline. At deadline expiry display “—” and “Signal lost,” optionally “Last reading 12 s ago”; never label the last value as current. Show zero only when a fresh valid sample actually reports zero. Unsupported metrics say “Not available,” rather than implying a temporary reconnection.

Charts leave gaps for missing samples and paused/uncertain intervals; no line or zero-value fill bridges them. Summaries distinguish measured totals, provider-labeled estimates, and unavailable quantities. Do not infer distance, calories or effort from elapsed time or missing heart rate. Recovery uses the next valid timestamped sample, with no interpolation over the gap. Reject duplicate/out-of-order samples from live presentation; a provider may reconcile historical samples without fabricating continuity. Sensor status is inline, not a repeated modal alert.

REVIEW and SAVED summaries show active duration, paused duration, interruption gaps, actual available metrics with units and sources, and coverage limitations such as “Heart rate missing for 20 s.” Unknown coverage says unknown. Local saving and Apple Health export have separate status; optional export failure never loses a locally saved session. Timer-only summaries contain timing and mode, with no implied health recording.

For active duration ≤5 seconds, REVIEW prominently says “Short workout · 4 seconds recorded.” Require explicit Save or confirmed Discard; never auto-save or auto-delete. This implements the HIG's brief-session save/discard guidance using a product-defined threshold.

Discard alert: title “Discard Workout?”; message “This deletes this workout's recorded data from this watch.” Use that wording only while no external export exists. Top action Discard, destructive role; bottom action Cancel. No default activation: a deliberate choice is required. Cancel or supported dismissal preserves REVIEW and its data. Leaving during confirmation retains the draft and returns to REVIEW, never commits deletion. Duplicate alerts are suppressed. This conservative role/default choice is a product decision; the Alerts guide permits a normal default for explicitly requested destruction, rather than universally prohibiting it.

## Worked before / after

Before, per the brief: Start appears usable while access is unresolved; the person begins rowing, cannot promptly reach Pause beneath the chart, sees zero effort during a dropout, then taps End and loses the session. Returning behavior is unspecified.

After, illustrative trace (not an executed test): the person selects Enable Metrics. While access resolves, Start is disabled and the timer remains at zero. Only a configured rowing channel becomes available; no heart-rate availability is assumed. Start is acknowledged at t=0. At t=120 s the provider stops sending; at its declared freshness deadline the metric becomes “— · Signal lost,” while elapsed time continues. The person taps visible Pause at t=140 s. At t=160 s they leave the app; at t=200 s they return to PAUSED with 2:20 active time and the retained gap. Resume is acknowledged at t=210 s; valid samples resume independently. End at t=270 s opens REVIEW: 3:20 active time, 1:10 paused time, and the actual measured coverage/gaps. Accidental End is recoverable through Continue Workout → Resume. Save yields a retained local summary only after acknowledgment. Discard would require a separate explicit confirmation.

## Acceptance checks and evidence limits

Static specification review passed: every supplied issue has a replacement; Start has a gate; Pause is in the first viewport; missing data is distinct from zero; End retains a draft; view departure and recorder interruption have different outcomes; Save and Discard have failure paths. The worked timing calculation is internally consistent: 140 + 60 = 200 active seconds, with 70 paused seconds.

The original brief fails these design checks: truthful Start availability, direct Pause access, non-destructive End, and truthful dropout display. Its unspecified return behavior is an evidence gap, not proof of data loss on departure.

The following are implementation acceptance scenarios, all **not executed**:

| Check | Required observable outcome |
| --- | --- |
| Unresolved / rejected / unavailable access | No recording before acknowledgment; no collection before required consent; timer-only remains available; no inference of denial from missing health data |
| Repeated Start or delayed acknowledgment | One session ID and one acknowledged start; failure is visible |
| Pause / Resume | Pause reachable without chart scroll; paused time excluded; resume failure remains paused |
| Zero versus dropout | Fresh zero stays zero; expired sample becomes unavailable; unaffected timer/channel continues; chart has a gap |
| End after four seconds | Retained short-session review; no automatic deletion or saving; Continue Workout preserves data |
| Cancel Discard / confirm Discard | Cancel preserves all data; explicit confirmation alone requests deletion; storage failure retains recovery |
| Save failure and retry | No false Saved label; same ID prevents duplicate saves; draft survives app restart |
| Wrist down/up and app departure | No state loss; paused stays paused; verified recording continues; no chart/control layout jump in supported dimmed mode |
| Recorder/process interruption | Reconcile before showing recording; uncertain interval is marked; explicit Resume required when continuity is unverified |
| Permission changes mid-session | Unavailable channels stop claiming live data; permitted useful work continues; no repeated coercive prompts |
| Presentation on supported watch sizes | Controls do not overlap; labels remain readable and unclipped; first viewport contains Pause; selectable areas meet the contract |

Evidence is limited to `interface.md` and the installed HIG package. Root, owning families and routed topic procedures were read before their supporting guides: watchOS; Workouts; Privacy; Buttons; Alerts; HealthKit (authorization semantics only); Always On. Official links above identify the guides, but were not opened. Local snapshots are dated 2026-10-25, with older article revision dates where supplied; no current-web verification or independent source review is claimed.

No device, SDK, GUI, sensor, storage implementation, background-session capability, physical rowing, accessibility, native rendering, authorization dialog, or health export was executed. Readability, selectable geometry, wrist transitions, assistive-technology behavior, energy usage and recording accuracy need implementation/device evidence. No haptics are specified or claimed. The data providers, supported devices, actual persistence mechanisms and platform background capability must be established during implementation; this specification does not certify them.
