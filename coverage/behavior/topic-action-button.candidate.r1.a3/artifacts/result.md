# Revised Action button interaction specification

Scope: iPhone models with an Action button; quick field-audio notes, including a locked phone in a pocket. This is a framework-agnostic design contract, based on `interface.md`, not an SDK implementation.

## Decisions and rationale

Expose **Record Audio** in Settings: a present-tense verb, title case, two words. It performs capture directly and retains the current foreground context. Use the system’s Action button assignment education. This follows [Action button — Best practices and iOS](https://developer.apple.com/design/human-interface-guidelines/action-button).

The intent means **ensure one recording is active**. First invocation starts one note; subsequent invocations report its current status without creating another file, stopping, pausing, deleting, or restarting it. This is a product decision to make pocket use predictable. The source’s recommendation against ending an activity through repeated presses is explicitly watchOS guidance; it is not an iPhone prohibition. Do not import Watch Action-plus-side-button behavior onto iPhone.

Provide the same intent through the app’s Record action and, when integrated, Shortcuts, Spotlight, and Siri. No required parameters; use the current recording configuration and generate a local note identifier. Naming, folder selection, and editing happen later. Suggested Siri phrase: “Record audio with [actual app name]”; substitute the shipped name before release. Each entry point uses the same state machine. [App Shortcuts — Best practices and responses](https://developer.apple.com/design/human-interface-guidelines/app-shortcuts), [Siri — Customizing your app’s experience](https://developer.apple.com/design/human-interface-guidelines/siri).

Completion belongs in an explicit **Stop and Save** action on the ongoing status UI and recorder screen. It stops capture and commits the note; it never deletes the recording. Opening the app is justified for permission recovery, unsaved-data recovery, naming, playback, and editing, rather than routine successful capture.

## State and transition contract

“Press” means one system-delivered invocation of the assigned shortcut. Do not reinterpret raw button duration, double presses, or reserved hardware combinations. Only one recorder may own capture at a time.

| State | Record Audio invocation | Truthful feedback / next state |
|---|---|---|
| Idle, authorized and capable | Allocate one note and begin capture | “Starting recording…”; Starting |
| Starting | Join the pending start; allocate nothing | “Starting recording…”; unchanged |
| Recording | Return the existing note/status | “Already recording · [elapsed]”; unchanged |
| Saving | Do not queue another start | “Saving recording. Try again when it finishes.”; unchanged |
| Permission needed, denied, or restricted | Capture nothing | “Recording didn’t start. Microphone access is required.” Offer relevant permission/recovery route |
| Locked execution unavailable | Capture nothing; do not defer an automatic start | “Recording didn’t start. Unlock to record.” |
| Resource/start failure | Release failed start resources; retain any recoverable data | “Recording didn’t start: [specific reason]. [specific recovery].”; Idle or Recovery |
| Recovery, unsaved note present | Do not overwrite or hide the note | “Recording stopped. Open the recorder to recover your audio.” |

Transitions from recorder events:

- Capture engine confirms capture and storage readiness: Starting → Recording. Only then say “Recording started” and publish active status.
- Stop and Save: Recording → Saving. Ignore duplicate stop requests. A stale stop carrying a different note ID must not stop a newer note.
- Durable commit confirms: Saving → Idle; report “Recording saved · [duration].” A later invocation can start a new note.
- Save fails: Saving → Recovery; retain recoverable audio, show “Couldn’t save recording” and Retry Save. Never report “Saved” early.
- Interruption, microphone loss, or revoked access: stop claiming Recording, preserve captured audio, attempt finalization, and report “Recording stopped · [reason].” Do not silently resume. A new recording requires a new explicit invocation after finalization/recovery.
- Process restart: reconcile persisted note/engine truth before accepting another start. A persisted flag alone cannot establish live capture. Recover incomplete audio rather than inventing elapsed recording time.

Serialize commands across all entry points. A delivered request ID is deduplicated; simultaneous requests join a single pending start. State changes and publication are ordered by note ID and revision so delayed updates cannot revive a completed recording. Stop remains available while recording even if status publication fails.

```text
recordAudio(requestId):
  under recorderCommandLock:
    if requestId already handled: return its current truthful outcome
    reconcileRecorderAndRecoverableData()
    if state in {Starting, Recording, Saving, Recovery}:
      return statusAndRecoveryFor(state)
    if permission or execution prerequisites missing:
      return notStartedWithRecovery()
    reserveOneNoteAndEnterStarting()
    beginCaptureAsynchronously()
  # engine/storage callbacks, serialized with commands, decide success or failure
```

No automatic retry starts capture after a permission dialog, unlock, resource failure, or app restart. When foreground permission is granted, show Record again so the person chooses when capture begins.

## Feedback and in-context completion

Use a Live Activity for the bounded recording session where supported and allowed; do not require the app to be opened for status. Publish from recorder truth, not from button activation. [Live Activities — Anatomy, interactivity, and lifecycle](https://developer.apple.com/design/human-interface-guidelines/live-activities).

| Presentation | Content and destination |
|---|---|
| Compact | Microphone/active-state mark plus elapsed duration; both halves open the current recorder |
| Minimal / multiple activities | Distinguishable active vs stopped mark, not just an app logo; expand for text and duration |
| Expanded and Lock Screen | “Recording”, elapsed duration, one essential action: Stop and Save; Saving and recovery replace active status truthfully |
| StandBy / reduced luminance | Same essential status with system scaling; no dependence on animation, color alone, or bright backgrounds |
| Mirrored Mac / Watch / CarPlay if surfaced by the system | Preserve meaningful status; never depend on a control for comprehension. CarPlay controls are disabled; Mac activation follows system iPhone Mirroring behavior |

Deep links identify the current note/recorder, not the home screen. No title, transcript, location, waveform, or audio playback appears on the Lock Screen. A user can opt out of the Live Activity in the recorder. On completion, end the activity immediately; retain a non-sensitive “Recording saved” summary for 15 minutes where the system allows. On failure, end live-recording status with an accurate recovery summary. Never imply recording continues because status is stale or dismissed.

If Live Activities are disabled/unavailable, return concise system invocation feedback where supported and retain full status and Stop and Save in the app. Do not force app launch merely to compensate for an absent optional surface. Actual locked/background execution and feedback capabilities are release feasibility gates, not proven here.

For pocket feedback, request a brief standard success haptic only after capture actually starts, and an error cue when starting fails, subject to system capability/settings. An already-active invocation gets textual status without another start-success cue. Saving success follows durable commit. Do not emit continuous pulses or routine speaker sounds that could contaminate field audio. Suppress app-generated haptics during capture until microphone-interference testing supports them. Visual/text status remains available with haptics disabled; Siri responses independently say “Recording started,” “Already recording,” or the precise failure and recovery without requiring a visible card. No spoken note content. These are product channel choices informed by [Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback) and [Playing haptics — Best practices and iOS](https://developer.apple.com/design/human-interface-guidelines/playing-haptics); pocket perceptibility is unverified.

## Permission and data boundary

| Data/access | Purpose | Boundary |
|---|---|---|
| Microphone | Capture the requested audio note | Required permission before capture |
| Local audio and note ID/duration | Preserve and identify this recording | Persist recoverable data; no new upload/transcription behavior specified |
| Lock Screen status | Let the person verify capture | Generic state and duration only |

Request microphone access when Record is invoked in a context where the system can present authorization. Suggested purpose string: “Record audio to save your field notes.” Use the system prompt without a redundant imitation. If unavailable while locked, explain unlock/retry; denial leads to the relevant settings recovery, restriction explains that access is unavailable. Never repeatedly prompt or bypass consent. This contract does not require contacts, location, or tracking access. [Privacy — Requesting permission and Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy).

## Worked before → after

**Before, from interface.md:** A user presses the Action button while the locked phone is pocketed. The app starts a recording. The user presses again to check whether it worked; another recording starts. Recording state is only visible after opening the app. The brief does not establish whether the first file survives or whether capture overlaps.

**After, specified trace:** With permission already granted and locked capture supported, invocation A enters Starting for note N. Invocation B arrives before confirmation and joins N. Engine confirmation changes N to Recording and produces start feedback. At 12 seconds, invocation C returns “Already recording · 00:12”; the same N continues. Lock Screen/expanded status shows Recording and Stop and Save. The user activates Stop and Save; status becomes Saving. After durable commit, it becomes Recording saved and the Live Activity ends. An additional Record Audio invocation can now create note N+1. No duplicate file or silent stop occurs.

## Acceptance checks and evidence

**Passed — static specification checks:** Inspected interface.md; explicitly read the installed root skill, searched its topic index, and followed family → topic procedure → source-guide routing for Action button, Siri, App Shortcuts, Live Activities, feedback, haptics, and privacy. The written contract includes the label, first/later invocation mapping, shared intent, alternative entry point, completion, failure/recovery, and feedback. These are document checks only.

**Failed — supplied behavior against this revised contract:** The brief explicitly says every press starts a recording even when already recording, and status is only visible after opening the app. Both conflict with the revised contract; these are brief-based findings, not observed runtime failures.

**Not executed — release acceptance scenarios:**

1. On a supported iPhone, invoke while idle, starting, recording, and saving; verify exactly one capture session/file, correct feedback, and no unexpected ending or deletion. Race hardware, app, Siri, and shortcut invocations; replay request IDs.
2. Verify recording actually captures recoverable audio while locked/in a pocket and from another app without forced navigation. Verify system assignment and invocation semantics on target OS versions.
3. Deny/restrict/revoke microphone access; test first-use authorization while locked, unlock cancellation, unavailable microphone, storage exhaustion, engine delay/failure, and save failure. Confirm no false success and no later automatic start.
4. Interrupt capture and terminate/relaunch the process; verify honest stopped status, recoverable audio, failed-save retry, and no silent resume. Deliver stale callbacks/stop requests after a new note starts.
5. Verify Live Activity compact/minimal/multiple/expanded/Lock Screen states, disabled activities, dismissal, stopped updates, opt-out, ending and retained-summary expiry. Check dark/light, reduced luminance, large text, StandBy red tint, and any mirrored/control-disabled destinations enabled by the system.
6. With sound muted and haptics off, confirm text/status and completion remain usable. With screen unseen, verify Siri dialogue is sufficient. Test pocket haptic detectability and recorded-audio contamination before allowing capture-time haptics. Verify accessible labels, reading order, and Stop and Save operation using assistive technology.

Evidence limits: Only supplied local text and installed guidance were used; no web access. Official links above identify the local guides’ source articles, not fresh verification. Those guides describe themselves as derived guidance from a dated snapshot, not SDK availability proof or independently reviewed source evidence. No implementation, device, SDK compilation, GUI rendering, hardware press, background/locked capture, Siri recognition, haptic, privacy prompt, or accessibility execution occurred. Framework bindings, deployment availability, system permissions, and reliable locked-state feedback must be established during implementation. Do not promise pocket capture until those gates pass.
