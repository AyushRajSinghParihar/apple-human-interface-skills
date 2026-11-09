# Revised Action button interaction specification

## Scope and decisions

The supplied `interface.md` describes an iPhone recorder that starts a recording on every press, hides recording state until the app opens, and may be used locked in a pocket. This specification replaces that contract. It assumes supported Action button hardware as supplied; it does not establish OS/API availability or locked-background recording feasibility.

1. Expose **Record Audio** as the assignable action: a present-tense verb, title case, two words. It performs capture, with no settings detour or mandatory app launch. Let the system teach Action button assignment; do not duplicate its setup tutorial. This follows [Action button — Best practices and iOS](https://developer.apple.com/design/human-interface-guidelines/action-button).
2. Give every invocation one stable intent: **ensure one audio note is recording**. Idle starts one note; starting/recording returns the current status without creating, splitting, stopping, deleting, or restarting it. This is our iPhone product decision to protect a pocket recording from accidental repeats. The source's recommendation about subsequent presses and not normally ending an activity is specifically watchOS guidance; it is not an iPhone prohibition on toggles. Do not import Watch Action-plus-side-button pause behavior.
3. Keep the current app or locked context for a ready-to-record invocation. Opening the recorder is justified only for permission/authentication recovery or detailed management. Provide explicit **Stop and Save** in the recorder and, where supported, the expanded/Lock Screen activity. No hidden press sequence, double-press command, or custom press-duration interpretation; handle the activation delivered by the system. Context preservation is supported by [Action button — iOS](https://developer.apple.com/design/human-interface-guidelines/action-button#iOS); the exact state mapping and completion control are product decisions.
4. Use the same contract from the Action button and the Record Audio shortcut in Shortcuts, Spotlight, or Siri. No required parameters: use the user's current recording configuration, an automatic local note name, and no overwrite. Suggested phrase templates: “Record audio with <App Name>” and “Start an audio note with <App Name>”; replace the placeholder with the actual product name. No existing intents or product name were supplied. Share the intent rather than implementing separate behaviors. See [App Shortcuts — Best practices and responses](https://developer.apple.com/design/human-interface-guidelines/app-shortcuts) and [Siri — Customizing your app’s experience](https://developer.apple.com/design/human-interface-guidelines/siri).

## State and action contract

All entrypoints use a serialized recorder coordinator and one authoritative session ID. A delivered activation is an intent invocation, not a raw hardware-down event. Recording truth comes from the audio engine, not the screen or Live Activity.

| State on invocation | Result of Record Audio | Visible/result text |
|---|---|---|
| Idle, prerequisites satisfied | Reserve one session; start capture; enter Starting | “Starting recording…” |
| Starting | Join the pending operation; never reserve another session | “Starting recording…”; then its actual result |
| Recording | Keep session and original start time unchanged | “Already recording · <elapsed>” |
| Stopping/Saving | Do not queue a new recording | “Saving recording. Try again when saving finishes.” |
| Permission unknown | Request microphone access in permitted interactive context; start only after grant and successful capture | “Microphone access is needed to record an audio note.” |
| Permission denied/restricted | No capture; explain recovery, without repeatedly prompting | “Recording didn’t start. Microphone access is unavailable.” Offer applicable Settings/help route |
| Locked and authentication/interactive setup required | No capture and no deferred automatic start | “Unlock to finish setting up recording.” After unlock, require a fresh Record Audio invocation |
| Interrupted or failed | Never claim to be recording; retain recoverable audio and identify the problem | “Recording stopped. <specific reason>.” Provide review/retry in recorder |

Permission purpose copy: “Use the microphone to record your audio notes.” Ask on first recording intent, using the system permission mechanism where available, rather than an unrelated launch prompt. If permission can complete immediately in an unlocked flow, that same invocation may proceed; cancellation ends it. Do not silently start after a later unlock, Settings visit, or interruption. Permission and minimal-access decisions follow [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission).

Data-purpose contract: microphone samples create the audio note; local storage retains it. This action requires no location, contacts, camera, transcription, account, or server transfer. Those exclusions are proposed product scope, not findings about an existing implementation. Do not expose a note title, transcript, location, or waveform content on a locked/shared surface.

Framework-agnostic pseudocode (adapter operations require later platform validation):

```text
recordAudio(invocation):
  serialize through recorderCoordinator:
    reconcile persisted session with actual capture state
    if state == Recording: return AlreadyRecording(sessionID, elapsed)
    if state == Starting: return resultOfExistingStart
    if state in [Stopping, Saving]: return BusySaving
    if unresolvedInterruptionOrFailure: return NeedsReview(reason)
    if authorizationOrUnlockRequired: return obtainConsentOrNeedsUnlock
    sessionID = reserveUniqueSession()
    state = Starting
    asynchronously startCapture(sessionID)

captureDidStart(sessionID):
  accept only if sessionID is still current
  state = Recording
  publish actual start time and Recording result

captureDidFailOrInterrupt(sessionID, reason):
  accept only if sessionID is current
  preserve recoverable samples; clear active-capture status
  enter InterruptedOrFailed; end recording activity with truthful summary

stopAndSave(sessionID):
  serialize; accept only for the current recording
  state = Stopping; stop capture
  state = Saving; finalize note without overwriting prior notes
  on durable success: state = Idle; publish Saved result
  on failure: preserve recoverable data; state = Failed; publish recovery route
```

Duplicate callbacks and repeated stop commands must be harmless. Capture-start callbacks arriving after cancellation/failure must not resurrect a session. Retry after failure is explicit in the recorder, after acknowledging any recoverable note. Stopping capture ends the “Recording” status immediately; saving is a separate status. Never say “Saved” until storage confirms success.

## Feedback and completion

Start feedback only confirms recording after capture has actually begun. On hardware invocation, request distinct nonverbal feedback for “started,” “already recording,” and “could not start,” using available system facilities. Do not automatically speak into a field recording. These feedback distinctions are product requirements subject to hardware validation; no exact haptic pattern, delivery guarantee, or Apple rule is asserted. For Siri invocation, provide complete spoken and visual results: “Recording started,” “Already recording,” or a specific failure/recovery sentence. Optional visual content must not carry the only essential result. Consider that bystanders can hear Siri. See [Siri — Best practices and customization](https://developer.apple.com/design/human-interface-guidelines/siri).

A recording is a bounded user task. Where available and allowed, begin one Live Activity after actual capture starts; reuse it for repeated invocations. Its lifecycle follows actual capture, saving, completion, and interruption events. Do not depend on network pushes for local recording truth. Update state on change; derive elapsed time from the capture clock rather than incrementing a guessed counter. Do not issue duplicate notifications for the same status. See [Live Activities — Best practices, interactivity, and lifecycle](https://developer.apple.com/design/human-interface-guidelines/live-activities).

| Presentation | Required content and destination |
|---|---|
| Lock Screen / expanded | “Recording,” elapsed time, recording symbol; one explicit Stop and Save action where supported. Body opens the current recorder session, respecting authentication. Saving replaces recording status; Saved appears only after durable success. |
| Compact | Recording symbol/state and elapsed time, arranged consistently with expanded layout; both halves open the same session. |
| Minimal / multiple activities | State-bearing recording symbol, with changed appearance for saving/error; never only a static app logo. Opens current session. |
| StandBy / Always On | Same truthful, minimal status; verify scaled margins, reduced luminance, and red Night Mode. No meaning depends only on color or animation. |
| System-forwarded paired surfaces | Generic recording state only; no private note content. Remain useful when controls are absent/disabled, including CarPlay. Do not imply a Watch Action button integration. |

End the active recording presentation on actual termination. Retain a generic “Audio note saved” summary for 15 minutes where the system permits, then remove it; failures retain a recovery summary for the same proposed interval and remain available in the app. Never leave a frozen elapsed time labeled “Recording.” Activity dismissal/opt-out does not stop capture. Repeated presses do not override opt-out. If Live Activities are disabled or unavailable, return a truthful invocation result and retain in-app status; do not launch the app solely to show success. Persistent off-app visibility is then unavailable, which must be disclosed during recording setup and tested as a degraded path. No guarantee is made that a pocketed/locked device will deliver perceptible feedback.

The Live Activity status, single direct action, privacy reduction, and bounded lifecycle follow the linked local Live Activities guidance. The 15-minute retention, no automatic spoken hardware response, and idempotent start are product choices, not universal HIG requirements.

## Worked before → after

Before (supplied behavior): a person presses the Action button with the locked phone in a pocket, then presses again because recording status is hidden. Each press starts a recording. The brief does not establish whether the old recording is stopped, overlaps, or is lost; none of those outcomes is assumed.

After (proposed trace): with microphone permission and locked capture available, the first delivered invocation reserves session A. While capture starts, a second invocation joins A's pending result. Capture confirmation publishes “Recording,” elapsed 00:00, and start feedback. At 00:12 another invocation returns “Already recording · 00:12”; A continues with its original start time and no second file. The person checks Lock Screen status, then selects Stop and Save. Capture stops, status becomes Saving, and only durable completion produces “Audio note saved.” A press during saving returns BusySaving. A later press after successful save starts session B. If the first attempt instead needs unlocking, no session starts, and the person receives a recovery result rather than false success.

## Acceptance checks and current evidence

**Passed — static specification inspection:** the supplied brief was read; the revised label is a two-word present-tense action; the table covers first/repeated/starting/saving/blocked invocations; shared entrypoints and explicit completion are specified; iPhone decisions are separated from Watch-specific source advice; no SDK dependency appears in the pseudocode.

**Failed — supplied contract review:** starts on every press and app-only state visibility fail this revised specification's single-session and off-app-status requirements. This is a comparison of documented behavior, not a runtime test or proof of a specific data-loss bug.

**Not executed — required implementation/device checks:**

1. Invoke once idle, repeatedly while starting, and concurrently through hardware/shortcut: exactly one capture session and one note; all results agree with the engine. Deliver stale callbacks after failure: no resurrection.
2. Invoke during recording: unchanged session ID/start time, uninterrupted samples, no stop/restart/file split. Invoke during saving: no queued start. Invoke after save: exactly one new note.
3. On supported iPhone, test unlocked/current-other-app and locked/pocket conditions, including authentication required, microphone unknown/denied/restricted, and canceled setup. No samples before authorization; no deferred start after unlock; no unjustified context switch.
4. Test Siri, Spotlight, and Shortcuts against the same coordinator. Without any snippet, spoken Siri results still communicate the real outcome and recovery. Verify actual discovery and invocation separately.
5. Stop explicitly; simulate storage failure, audio interruption, capture failure, and process termination/relaunch. Preserve recoverable data, reconcile real capture state, and never report Recording or Saved falsely. Audio continuity and recovery require recorded-file inspection.
6. Verify Lock Screen, compact, minimal alongside another activity, expanded, StandBy, dark/Always On and red mode. Status remains legible and truthful, deep links reach the correct session, and locked surfaces expose no note content. Verify forwarded status with disabled controls where available.
7. Disable/dismiss Live Activities: recording continues, opt-out is respected, results stay accurate, and degraded visibility is disclosed. End capture: activity ends promptly, summary expires per policy, no duplicate alerts.
8. Validate nonverbal feedback on actual hardware in pocket conditions and available system settings; confirm it is distinguishable and does not audibly contaminate recorded audio. Check labeled controls and status with assistive technology and larger text. None of this is established by this document.

## Evidence limits and source audit

Inputs were only `interface.md` and the installed local skill package. No code, build, SDK, device, GUI, audio file, or accessibility execution was available or performed. The official links above identify the articles cited by the local snapshots; they were not opened or independently verified. The package is derived guidance, not SDK documentation. Locked/background capture, system invocation delivery, authentication, haptic support, Live Activity delivery/interactivity, and OS availability remain implementation validation gates. The supplied hardware support is an assumption from the brief, not a feasibility finding. No newer-release claims are made.

Auditable local route, rooted at `.agents/skills/apple-hig/`: root `SKILL.md`; Inputs family → Action button topic procedure → `references/action-button.md`; Technologies family → Siri topic procedure → `references/siri.md`; System experiences family → Live Activities topic procedure → `references/live-activities.md`, and App Shortcuts topic procedure → `references/app-shortcuts.md`; Foundations family → Privacy topic procedure → `references/privacy.md`. Each was read explicitly from the installed package, one file per shell command, with procedures preceding their source guides. No web browsing was used.
