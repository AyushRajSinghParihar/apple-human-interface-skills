# Revised Action button interaction specification

## Scope and decisions

Input: `interface.md` describes supported iPhone hardware, a new recording on every press, status available only inside the app, and possible locked-pocket use. The task is quick audio capture. No implementation, existing shortcuts, OS version, or capability configuration was supplied.

1. Expose **Record Audio** as the assignable action: a present-tense, title-case, two-word label. It performs capture rather than opening settings or merely launching the app. Let the system explain Action button assignment. This follows [Action button — Best practices](https://developer.apple.com/design/human-interface-guidelines/action-button#Best-practices).
2. Treat the intent as **ensure one recording is running**. When idle, start; when already recording, preserve that session and report “Already recording.” Never toggle stop, replace, delete, or start a second file on a later press. This is a product decision for predictable pocket use. The source’s advice about a memorable secondary press and normally ending through UI is specifically under **watchOS**, not an iPhone prohibition. We borrow its caution without claiming a universal iPhone rule. See [platform considerations](https://developer.apple.com/design/human-interface-guidelines/action-button#Platform-considerations).
3. Keep the current app/context on ordinary success. Offer a Live Activity for ongoing status, with an explicit **Stop and Save** action where supported. Opening the recorder is justified for authorization, recovery, or reviewing a note, not routine capture. See [Action button — iOS](https://developer.apple.com/design/human-interface-guidelines/action-button#iOS) and [Live Activities — Offering interactivity](https://developer.apple.com/design/human-interface-guidelines/live-activities#Offering-interactivity).
4. Siri, Spotlight, Shortcuts, and the app’s Record control invoke the same state contract. No required parameters; use the current recording input configuration, with no naming or folder question before capture. The existing product configuration is unknown; implementation must establish a usable input before reporting success. A proposed Siri phrase is “Record audio with <App Name>”; substitute the actual product name. See [App Shortcuts](https://developer.apple.com/design/human-interface-guidelines/app-shortcuts#Best-practices) and [Siri](https://developer.apple.com/design/human-interface-guidelines/siri#Best-practices). These are integration requirements, not claims that discovery already works.

## Action/state contract

“Invocation” below means one system-delivered activation, not a raw button-down event. Preserve the system’s activation gesture and reserved button combinations; do not invent double-press or press-duration modes.

| State | Record Audio invocation | Result and feedback |
| --- | --- | --- |
| Idle, authorized and capable | Atomically reserve one session; enter Starting | “Starting recording…”; no success cue yet |
| Starting | Join the pending start; no second recorder | Return the same operation’s outcome |
| Recording | Keep session ID, file, start time, and capture unchanged | “Already recording · [elapsed]”; refresh status, no new activity |
| Saving | Do not queue a new recording | “Saving recording. Try again when saving finishes.” |
| Needs authorization / authentication | Capture nothing; request supported authorization in context, or offer the relevant recorder screen if necessary | “Recording has not started. Unlock to allow microphone access.” when unlock is actually required |
| Permission denied/restricted | Capture nothing | “Recording has not started. Microphone access is unavailable.” Offer relevant permission recovery when change is possible; do not repeatedly prompt |
| Unavailable input / insufficient storage / start failure | Release reservation; retain prior notes | Explain the actual reason, e.g. “Recording has not started. Storage is full.” Retry requires a fresh invocation |
| Interrupted / recovery needed | Do not silently resume or create another note | Report “Recording stopped” plus retained-audio status; open recovery on deliberate user request |

Starting becomes Recording only after the capture service confirms that audio is being written. If authorization completes during the original active request, recheck all preconditions before starting. If the request was canceled, expired, or handed off for unlock, return to Idle and require a fresh Record action; never start unexpectedly later.

Framework-agnostic pseudocode:

```text
recordAudio(request):
  serialize all recorder commands across every entrypoint:
    if request.id already handled: return stored result
    reconcile session state with capture service
    if Recording: return alreadyRecording(session)
    if Starting: join pendingStart
    if Saving: return busySaving
    if RecoveryNeeded: return recoveryRequired
    if authorization or capability missing: return preciseRecovery
    reserve session and transition to Starting
  asynchronously start capture for reserved session
  serialize completion:
    accept only matching session/generation
    if capture confirmed: transition to Recording; publish actual start time
    else: release reservation; transition to Idle; publish failure

stopAndSave(sessionID):
  serialize:
    require matching Recording session; transition to Saving
    stop capture exactly once; finalize retained audio
    if durable save confirmed: transition to Idle; return Saved
    else: transition to RecoveryNeeded; retain recoverable audio
```

The command serializer must also order Stop and Save against simultaneous Record requests. Repeated stop requests join the same save. Ignore stale start/save callbacks from older generations. Reconcile after process restart; an old UI flag cannot establish that recording is active. A failed or interrupted session must not display a running timer.

Explicit Stop and Save is available in the recorder and, conditionally, the expanded/Lock Screen activity. Stop finishes the current note without a deletion step. Saving feedback remains distinct from “Saved.” On save failure, state what was retained and offer retry in the recorder; never promise a saved note before durable completion. No automatic deletion, restart, or upload is part of this action. On interruption or process failure, preserve recoverable captured audio, terminate misleading active status, and require deliberate recovery. Exact capture/interruption capabilities remain an implementation dependency.

## Feedback, locked use, and alternatives

The Live Activity starts only when capture is confirmed, updates from real capture state, and ends when capture ends. Saving can be communicated as a terminal “Saving…” result, followed by “Saved” only on confirmation. Retain the final safe summary for **15 minutes**, a product choice within the source’s commonly suggested 15–30 minute range. Failure summaries distinguish “Audio retained; save incomplete” from “No audio captured.” See [Live Activities — lifecycle](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity).

| Presentation | Required information and action |
| --- | --- |
| Compact | Recording/microphone symbol and elapsed capture time; both halves link to current session |
| Minimal, including multiple activities | Recognizable recording-state symbol, changing for stopped/error state; no decorative-logo-only presentation |
| Expanded / Lock Screen | “Recording,” elapsed time, one explicit Stop and Save control when supported; body links to current session |
| StandBy / reduced luminance | Same essential state; legible at system scaling, night tint, and reduced luminance; no animation dependency |
| Mirrored/paired surfaces | Status remains meaningful without controls. CarPlay must not depend on its disabled buttons; paired Mac activation remains system-owned |

Do not expose waveform, transcript, note title, location, or audio content on shared/locked surfaces. Show only generic state and elapsed time. Actual lock-screen privacy settings govern visibility. Provide an opt-out for the activity in the recorder. Activity dismissal is not a Stop command. These choices follow [Live Activities — Best practices and Presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Best-practices).

For a physical invocation, propose one brief generic tactile acknowledgment synchronized with confirmed capture, and a brief Error cue on failure, only where supported and enabled. Repeated presses during capture receive visual status without repeated vibration. No periodic vibration, audible beep, or automatic spoken hardware response during recording: these can contaminate field audio. The acknowledgment is not “note saved.” Validate microphone interference before enabling the start cue; omit it if it pollutes capture. Haptics are supplementary, never the sole status route. See [Playing haptics — Best practices](https://developer.apple.com/design/human-interface-guidelines/playing-haptics#Best-practices).

For Siri invocation, provide complete spoken and visual outcomes: “Recording started,” “Already recording,” or the precise failure and recovery. Do not read private note content. Siri speech may enter the microphone; timing and routing need real-device verification. Essential results cannot depend on an optional visual surface. See [Siri — Customizing your app’s experience](https://developer.apple.com/design/human-interface-guidelines/siri#Customizing-your-apps-experience-with-Siri).

When locked, attempt capture only if authorization, system policy, and runtime capabilities allow it. Do not claim these are established by HIG. If blocked, say capture has not started and identify the necessary unlock/recovery step; do not loop launch attempts or report success. If Live Activities are disabled/unavailable, capture may still proceed when allowed: return the invocation outcome and provide current-session status in the app. Do not force-launch on every successful press. With both screen unseen and haptics unavailable, pocket confirmation is unavailable; the user must inspect status or request it through an available entrypoint. No silent-feedback guarantee is possible.

The app’s labeled Record and Stop and Save controls provide an alternative to hardware. Essential state is text plus a symbol, not color or vibration alone. Detailed assistive-technology semantics and execution are outside the supplied evidence and must be validated during implementation.

Microphone access is the only new protected input specified. Request it when Record is invoked, before collection, using the real system authorization flow. Proposed purpose text: “Record audio to save your field notes.” No location, contacts, or tracking request is needed. Store capture locally for this contract; cloud transfer and transcription are separate, unspecified features. Do not play back private content while locked. These are proposed data decisions, not findings about existing storage. See [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission).

## Worked before/after

**Before, from the supplied brief:** With the phone locked in a pocket, the user activates Record at time 0, then again at 12 seconds because they cannot see whether capture started. Both activations start a recording. The brief does not establish whether the first is replaced, overlapped, or otherwise retained; any of those details would be invented. The person must open the app to see state.

**After, specified:** Assume prior microphone consent and verified locked capture capability. At time 0, the first activation reserves session A. On confirmed capture, the activity shows “Recording · 0:00,” with a brief tactile acknowledgment if usable. At 12 seconds, another activation returns “Already recording · 0:12”; A continues with no second file, reset, stop, or vibration. The user later expands the activity and chooses Stop and Save. A finalizes once, then shows “Saved” only after durable confirmation. The activity ends and retains the safe summary for 15 minutes. If locked capture is disallowed, the first activation instead reports “Recording has not started” with recovery; it never displays the successful timeline.

## Acceptance checks and current audit

**Passed — specification inspection only:** the label meets the naming rule; one shared intent/state mapping covers first and subsequent activations; routine success preserves context; explicit completion and failure paths exist; state is available beyond the full app; Watch-specific guidance is identified as such. Root → Inputs → Action button procedure → source was read from the installed package, along with the topic-index search and the routed Siri, App Shortcuts, Live Activities, Privacy, and Playing haptics family/procedure/source files. Each read used a separate command for one file.

**Failed — supplied design against this revised contract:** every activation starts a recording even during capture; status requires opening the app. These are brief-level findings, not observed runtime failures.

**Not executed — implementation/device acceptance:**

| Scenario | Required observable result |
| --- | --- |
| Idle start from hardware, Siri, Spotlight, Shortcuts, and app | Each produces the same confirmed single-session result, without routine full-app launch |
| Rapid/concurrent activations during start and capture | One file/session and original timer; all callers receive truthful outcomes |
| Stop races with Record; repeated Stop; stale callbacks | Serialized outcome, one finalization, no queued surprise recording or stale success |
| Permission unknown, denied, restricted, canceled; unlock handoff | No pre-consent audio; no false success; precise recovery; no delayed surprise start |
| Locked pocket and current-app contexts | Verify actual capture eligibility, system activation, context preservation, feedback, and accidental activation risk on supported iPhone |
| Storage/input failure; interruption; process restart; save failure | Accurate nonrecording state, retained audio where recoverable, deliberate retry, no false “Saved” |
| Activity unavailable, disabled, dismissed, stale, or multiple activities | Core recording remains coherent; app status works; no dismissal-as-stop; no stale running state |
| All activity presentations and forwarded destinations | Check compact/minimal/expanded/Lock Screen, large text, dark/light, Always On, StandBy night tint, and status without controls |
| Haptics absent/disabled and repeated activations | Functional visual/spoken alternatives; no vibration flood; measure microphone interference and physical detectability |
| Siri eyes-away and privacy; app assistive technologies | Spoken result stands alone, no private content disclosure; labeled controls and state usable with actual assistive technology |
| Capture ends and save completes/fails | Activity ends promptly; accurate summary expires at 15 minutes; no duplicate push alert |

## Evidence limits

This deliverable is a framework-agnostic design specification. Only supplied local files and installed instruction/source snapshots were used; official URLs above are attribution links, not browsed evidence. Snapshot files identify 2026-10-25 retrieval/snapshot dates and are derived guidance, not SDK references or proof of independent source review. No source conflict was found in the consulted material; platform scope remains important.

No device, SDK, GUI, microphone, lock-state, Siri, Live Activity, accessibility, compilation, or runtime test was performed. Hardware availability was supplied by the brief; it does not prove background/locked recording permission, delivery, feedback, or integration feasibility. An implementation must verify those capabilities and adapt the fallback honestly. Existing shortcut definitions, persistence guarantees, authorization configuration, and audio-session behavior remain unknown. The acceptance rows above are pending requirements, not passed tests.
