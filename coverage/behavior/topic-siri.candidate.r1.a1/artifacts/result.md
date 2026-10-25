# Revised cooking timer interaction specification

Scope: iOS and watchOS where supported; framework-agnostic design, not an implementation. Input evidence is the single paragraph in `interface.md`. The example durations below are invented fixtures, not observed saved values.

## Decisions and rationale

1. **Resolve ambiguity before starting.** “Start pasta timer” must not select randomly, rank two equally plausible presets, or silently reuse a previous choice. Ask “Which pasta timer: 8 minutes or 12 minutes?” Speak and display the same choices. The reply must work without seeing a card. This applies the [Siri dialogue guidance](https://developer.apple.com/design/human-interface-guidelines/siri#Customizing-your-apps-experience-with-Siri): specific follow-ups, brief independent spoken results, and essential information outside optional snippets.
2. **Speak only the task result.** Success is “Pasta timer started for 8 minutes.” Never append account name, email, subscription, account identifiers, or authentication details. Do not interpolate arbitrary account or saved-record text into speech. Use the generic “Pasta timer” for this flow; keep potentially sensitive custom labels out of spoken output. Bystander-aware dialogue is supported by [Siri guidance](https://developer.apple.com/design/human-interface-guidelines/siri#Customizing-your-apps-experience-with-Siri); this strict output allowlist is a product decision.
3. **Speech is optional throughout.** Saved presets, custom duration entry, Start, Pause/Resume, Cancel timer, and Dismiss completion remain available without microphone or speech recognition. Recognition, output speech, permission denial, offline service failure, and unsupported voice integration each degrade independently. This addresses the brief's blocked control path and follows [Accessibility: Speech and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Speech).
4. **Use brief platform-appropriate views.** On iPhone, put active timer remaining time and Pause/Resume together, with frequent touch actions within comfortable reach and preset/custom creation readily available. On Watch, show remaining time and Pause/Resume on the timer detail; keep the two preset choices in a shallow selection flow, with custom duration entry available without the phone. Preserve running state across app interruption and wrist lowering. These follow [iOS best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices) and [watchOS best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices). No complication, Action button, custom Crown behavior, or Always On presentation is specified here.
5. **Do not promise Siri integration from a design.** Define actions/entities below for any voice adapter. A later Siri adapter must explicitly expose appropriate actions and entities and verify device, OS, language, and API support. HIG describes this integration requirement, not guaranteed availability: [Getting your app to work with Siri](https://developer.apple.com/design/human-interface-guidelines/siri#Getting-your-app-to-work-with-Siri). Unsupported adapters leave in-app controls usable; they must not advertise working hands-free invocation.

## Action and data contract

- `Preset`: stable ID, duration in seconds, safe spoken category, display label, version. Two different durations matching pasta are ambiguous. Duplicate records with identical effective duration can collapse to one choice.
- `StartTimer(category?, presetID?, durationSeconds?, requestID)`: requires one positive, supported duration. A preset ID supplies its duration. Conflicting explicit duration and preset require clarification. An explicit “Start pasta timer for 10 minutes” supplies a duration and bypasses saved-duration ambiguity.
- `PauseTimer`, `ResumeTimer`, `CancelTimer`, `GetRemaining`, `DismissCompletion`: require a timer ID or unambiguous timer reference. With several matches, ask which timer, using safe label plus remaining time; never stop all timers by guessing. “Cancel” during clarification cancels only the pending request.
- `Timer`: ID, safe label, duration, deadline or paused remainder, status (`running`, `paused`, `completed`, `cancelled`). Persist timer state before reporting success. Countdown uses a clock strategy resilient to app suspension; merely rendering ticks must not drive elapsed time.
- `PendingRequest`: request ID, resolved fields, candidate IDs/versions, state, last prompt. It is not a running timer. Retries with the same request ID return the original committed outcome rather than creating another timer. A new explicit request may create another timer.

## Dialogue and transition contract

| State/event | Required behavior and next state |
|---|---|
| Idle / start request | Resolve required parameters. One valid duration → commit. Multiple plausible durations → AwaitChoice. No match → ask “How long should the pasta timer run?” and show duration entry. |
| AwaitChoice | No timer starts. Speak “Which pasta timer: 8 minutes or 12 minutes?” Display separate “8 minutes” and “12 minutes” choices plus Cancel. Stable ascending duration order; the question and visual order agree. |
| Reply “8 minutes,” or select its control | Resolve against current pending choices; revalidate preset version, then commit exactly one timer. “The first one” resolves only against this session's unchanged ordered choices. |
| Reply “yes,” unrecognized speech, or unresolved tie | No state mutation. Ask “Please choose 8 minutes or 12 minutes.” Never treat confidence alone as permission to pick a candidate. |
| Reply specifies a new valid duration | Treat it as the requested custom duration; commit that value. If interpretation remains uncertain, repeat the interpreted duration as a question before committing. |
| Invalid duration | No timer starts. Explain the actual constraint and ask again; supported range is a product/configuration prerequisite, not an invented HIG limit. |
| Silence, session ending, or Cancel | No timer starts. End listening when the adapter ends its session. Keep a visible “Timer not started” result with choices available until dismissal or a new request. Later voice invocation re-resolves; it must not accept stale ordinal choices. No timeout selects a default. |
| Candidate changes during clarification | Re-resolve and ask with current durations; do not commit a changed saved value silently. |
| Commit succeeds | Persist timer and request outcome atomically; show running time and Pause/Resume. Say “Pasta timer started for 8 minutes.” Start time is commit time, not the beginning of clarification. |
| Commit fails | No success wording. Say/display “The timer couldn't start. Try again.” Preserve chosen duration and offer Retry. If result is uncertain, reconcile by request ID before retrying. |
| Output speech fails after commit | Timer keeps running; visual success remains. Do not replay the start operation. |
| Recognition unavailable or denied | Stop capture, show “Voice input unavailable. Choose a duration to start a timer.” Keep all non-speech actions enabled. Do not claim a timer started from an unresolved utterance. |
| Pause / Resume | Apply to selected timer; persist, then report “Pasta timer paused” or “Pasta timer resumed.” Failure leaves previous state visible. |
| Cancel timer | Stop the selected timer and report “Pasta timer cancelled.” Pending clarification cancellation does not affect existing timers. |
| Deadline reached | Mark completed once; display “Pasta timer finished” persistently with Dismiss. Offer sound and, where supported, haptic feedback according to user/system settings. Do not rely on sound alone. Dismiss stops completion feedback, not another timer. |

For more than a short pair of candidate durations, ask for a duration rather than reading a long list. Do not require “look at the screen” in any spoken recovery. Prefer system-provided responses where they satisfy this contract; avoid redundant app attribution.

## Non-speech presentation and access

The initial screen exposes saved duration choices and “Custom duration.” Selecting a saved duration shows its value and a Start control; entering a custom value provides labeled minutes/seconds fields and Start. A voice clarification instead shows direct choice controls that commit the requested start, labeled with that purpose in their accessible descriptions. Cancel is always available before commit.

A running timer shows label, remaining time, textual state, Pause/Resume, and Cancel timer. Completion shows “Finished” and Dismiss. All voice prompts/results have equivalent visible text. Screen state, not a disappearing toast, carries success/failure. No account data belongs on these task surfaces.

Use labeled controls with names, roles, values, and enabled/paused states; navigation order follows prompt, choices or entry, primary action, then Cancel. Do not announce every countdown tick. Necessary actions must support applicable assistive navigation/activation without speech. Start from 44 × 44 pt activation areas on both iOS and watchOS, with adequate separation. Reflow at at least 200% text enlargement on iOS and 140% on watchOS; keep duration choices and actions reachable rather than truncating them. Pair state colors with text. These values and alternatives come from [Accessibility: Vision, Hearing, and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision); physical geometry and assistive behavior remain untested.

On iPhone preserve pending duration, selected timer, and running state through orientation changes and interruption. On Watch preserve them through wrist lowering and interruption; running timers remain independently controllable without a connected phone if the supported implementation provides local timers. Background scheduling and completion delivery are implementation gates to verify, not promises established here.

## Privacy and capability contract

| Data/access | Purpose and handling decision |
|---|---|
| Saved preset ID and duration | Resolve the request; prefer local lookup. Do not send account records to a speech renderer. |
| Audio / transcript | Only for explicitly invoked voice input. No app-controlled continuous listening. Prefer on-device processing where feasible. Do not retain raw audio or transcripts in app logs; discard transient request text after resolution/session end. Actual system-provider retention is unknown and must be disclosed accurately before release. |
| Account details | Unnecessary for timer execution or dialogue; exclude from voice payloads, timer feedback, and diagnostic events. No account access request for this task. |
| Microphone / recognition authorization | Only if the chosen adapter needs app access. Request at invocation, not launch. Proposed microphone purpose: “Use your microphone to hear spoken timer commands.” Provide any separate recognition explanation required by the verified adapter; do not invent permission requirements for system-owned Siri capture. |

If permission is denied, show the alternative controls immediately and an optional route to applicable settings; do not repeatedly prompt or gate timers on access. Actual provider transfers, authorization categories, and App Store disclosures must be verified against the eventual implementation. These decisions apply [Privacy: Best practices and Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission), especially minimum collection and contextual requests.

## Worked before → after

Fixture: two saved pasta durations, 8 and 12 minutes; no timer running.

**Before, as supplied:** User says “Start pasta timer.” The app randomly chooses one duration and speaks private account details. If speech is unavailable, there is no timer control. The supplied brief does not provide exact original dialogue.

**After:**

1. User: “Start pasta timer.” App: “Which pasta timer: 8 minutes or 12 minutes?” Matching choices appear. Running timer count remains zero.
2. User: “8 minutes.” App commits one 480-second timer, then says “Pasta timer started for 8 minutes.” The screen shows Pasta, remaining time, Pause, and Cancel timer. No account data is read.
3. User: “How much time is left on the pasta timer?” At a fixture clock value 90 seconds after commit, app says/displays “Pasta timer has 6 minutes 30 seconds left.” The spoken result needs no card.
4. Equivalent degraded path: recognition is unavailable. User selects the 8-minute saved preset and Start using touch or supported assistive activation. The same timer state and visible result are produced without speech. If only speech output fails after step 2, the original timer continues; no replacement timer is created.

## Acceptance checks and evidence status

**Passed — document/static inspection only:** Read `interface.md`; explicitly read installed apple-hig root; searched the topic index; read Getting started, Technologies, and Foundations families, then iOS/watchOS, Siri, Privacy, and Accessibility topic procedures before their source guides. This specification supplies ambiguity, privacy, non-speech, recovery, and platform contracts. No web requests were used. These passes concern the written artifact only.

**Failed — supplied design:** The paragraph explicitly describes arbitrary ambiguity resolution, spoken account disclosure, and loss of timer control without speech. These are failures against this revised contract, not reproduced runtime failures.

**Not executed — implementation acceptance:** All checks below require a future implementation or prototype. None is claimed to pass.

| Check | Observable pass criterion |
|---|---|
| Equal candidates | Repeated starts with the two fixture presets always ask; zero timers exist until a resolved choice. No random branch. |
| Resolution and correction | “8 minutes” starts exactly 480 seconds at commit; “yes” starts none; cancellation/silence starts none; changed presets re-prompt; explicit 10 minutes starts 600 seconds. |
| Standalone dialogue | Hide/omit the visual snippet: user can choose and hear duration/result and remaining time without screen references. Test noisy kitchen recognition separately. |
| Privacy | Populate account fields and custom labels with distinctive secrets; capture every prompt, response payload, diagnostic event, and visible task result. None contains those secrets. Verify actual audio/transcript transfers and retention independently. |
| Speech independence | Disable recognition, deny permission, disconnect any required voice service, and separately disable speech output. Create, inspect, pause, resume, cancel, and dismiss via non-speech controls; no optional access gate appears. |
| Atomic outcome | Inject commit failure, duplicate request delivery, and output failure. No false success, duplicate timer, or stopped timer after output failure. Retry reconciles uncertain outcomes. |
| Multiple timers | An ambiguous Pause/Cancel asks for the target; only the resolved timer changes. “Cancel” in a start clarification leaves existing timers intact. |
| Lifecycle | Background/resume, rotate iPhone, lower/raise Watch wrist, and test the supported disconnected-Watch case. Timer deadline and state survive; pending choices never silently start. Verify completion delivery under supported system conditions. |
| Accessible alternatives | On supported Apple environments, test assistive focus/activation, labels/states, no per-second announcement flooding, and complete non-speech task paths. Measure activation areas and separation, text reflow at stated scales, and contrast in light/dark appearances. |
| Completion | At deadline, finished state appears once and persists until dismissal; disabling sound does not hide completion. Verify actual audible/haptic delivery only on supported hardware. |

## Evidence limits

Only a short interaction brief and installed local instructions/guides were inspected. The guides identify themselves as original application guidance based on a dated English HIG snapshot, retrieved 2026-10-25; they are not SDK documentation. Official links above are attribution from those local files, not browsed or independently verified sources. No source conflict was found in the selected passages.

Durations, wording, state model, allowlist, transaction rules, and retention policy are proposed product decisions. No source code, executable prototype, device, SDK, GUI, recognition engine, permission prompt, accessibility tool, security audit, or background timer delivery was exercised. iOS/watchOS voice availability, provider privacy behavior, lock-state behavior, natural-language quality, physical reach/readability, haptics, and reliable suspended execution remain implementation and device validation work. This specification does not establish accessibility conformance or runtime support.
