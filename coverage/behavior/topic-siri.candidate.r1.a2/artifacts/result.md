# Revised cooking timer interaction specification

## Scope and decisions

The supplied `interface.md` targets iOS/watchOS where supported and reports three defects: an ambiguous saved duration is selected randomly, private account details are spoken, and timer control disappears when speech is unavailable. This revision defines a framework-independent contract, not an SDK implementation. Assume two saved pasta durations; the example values below are illustrative, not supplied facts.

1. **Resolve ambiguity before changing timer state.** “Start pasta timer” with two distinct matching durations asks “Which pasta timer: 8 minutes or 12 minutes?” Neither choice is preselected or inferred from recency. An explicit duration bypasses this question. A single unambiguous saved duration starts directly. This applies Siri guidance on specific follow-up questions; the deterministic resolver is a product decision. [Siri — Customizing](https://developer.apple.com/design/human-interface-guidelines/siri#Customizing-your-apps-experience-with-Siri)
2. **Make the spoken result sufficient and discreet.** After successful creation say “Pasta timer started for 8 minutes.” Mirror this as text. Never include account name, email, subscription, account identifiers, or unrelated saved content in timer dialogue. Use the minimum timer label and duration; arbitrary private preset titles are not read aloud by default. “Timer” substitutes for a sensitive title. This applies the guidance that spoken responses stand alone and may be heard by bystanders. [Siri — Customizing](https://developer.apple.com/design/human-interface-guidelines/siri#Customizing-your-apps-experience-with-Siri)
3. **Keep speech optional.** The same action handler serves voice and labeled onscreen buttons. Presets, ambiguity choices, active timers, Pause/Resume, and Stop remain available with microphone access denied, recognition offline, speech output muted, or Siri unavailable. Speech input and output availability are separate capabilities. Nonvoice control does not fully replace hands-free operation when hands are busy; say so rather than silently implying it does. [Accessibility — Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Speech)
4. **Keep the wrist task short.** iPhone shows active timers first and presets below; frequent actions sit in comfortable reach. Watch opens to the active timer and its next action, or saved starts when none is active. Two ambiguity choices occupy one shallow screen. Watch operation must not require a reachable phone for already-local presets and timers. Preserve timer state across app interruption and wrist lowering. These are product applications of platform guidance. [iOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices), [watchOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices)

## Action and state contract

Entities:

- `Preset {id, safeSpokenLabel, displayLabel, durationSeconds}`; match only locally available, authorized presets.
- `Timer {id, safeSpokenLabel, durationSeconds, remainingSeconds, status}`; status is running, paused, completed, or stopped.
- `Request {requestId, action, targetId?, label?, durationSeconds?, candidateIds?, version}`. Actions: start, remaining, pause, resume, stop, dismiss completion.

Duration must be positive and supported by the timer engine. Display the engine's documented limits before accepting input; no platform limit is invented here. Invalid or missing duration produces a specific question and no timer. Example: “How long should the pasta timer run?”

| Current state/event | Required transition and response |
|---|---|
| Idle; explicit valid duration or one resolved preset | Commit one timer; enter Running only after persistence/engine acknowledgement; speak and display label + duration. |
| Idle; two equally plausible distinct durations | Enter AwaitingChoice; create no timer; ask the full question and show `Start 8-Minute Pasta Timer`, `Start 12-Minute Pasta Timer`, and `Cancel`. Both duration choices have equal emphasis. |
| AwaitingChoice; “8 minutes” or matching button | Revalidate pending candidates, commit exactly one selected timer, clear pending request. |
| AwaitingChoice; “yes,” unrelated answer, or recognition failure | Do not guess. “Choose 8 minutes or 12 minutes for pasta, or say cancel.” Keep choices available. |
| AwaitingChoice; cancel or system voice-session end | No new timer; preserve existing timers. Clear voice context. Retain a visible unresolved draft until explicit cancel or replacement; reopening it revalidates candidates. Never auto-start on timeout. |
| Preset removed/changed while choosing | Invalidate stale choice and ask again using current values; do not use an obsolete duration. |
| No matching preset | “No saved pasta timer. How long should it run?” Provide saved alternatives and editable duration entry onscreen. |
| Running; remaining query | “Pasta timer has 6 minutes remaining,” using current engine state. No mutation. |
| Running; pause / Paused; resume | Resolve timer, commit state, then report “Pasta timer paused” / “Pasta timer resumed.” |
| Any ambiguous timer target | Ask which timer, naming safe label and remaining time/state. No mutation until resolved; “stop it” cannot select randomly. |
| Running/Paused; stop | Stop only the resolved timer; report “Pasta timer stopped.” Preserve a stopped record with a `Restart` action that starts the full original duration; this does not restore elapsed time. |
| Running reaches zero | Enter Completed; persistent text “Pasta timer finished” plus audible alert when available. `Dismiss` acknowledges completion; `Restart` starts the original duration. Audio delivery is capability-dependent. |
| Commit fails | Keep previous state; “The pasta timer couldn’t start. Try again.” Offer `Try Again` and `Cancel`. Never say “started” before success. |

When more than two candidates exist, ask a narrowing question about duration or timer label rather than reciting an unbounded list. Never choose by random score or an equal-confidence tie. A new deliberate start while another pasta timer runs asks “A pasta timer is already running. Start another?” with `Start Another` and `Cancel`; a transport retry is not a new deliberate start.

```text
handle(request, input):
    if request.requestId has committed result:
        return that result without repeating the mutation
    resolved = resolve(input, pendingContext, currentAuthorizedData)
    if resolved missing or ambiguous:
        return specificQuestionAndEquivalentVisibleChoices(resolved)
    if resolved is stale or invalid:
        return correctedQuestionWithoutMutation()
    result = atomicallyCommit(resolved, request.requestId)
    return result.success
        ? minimalSpokenAndVisibleOutcome(result)
        : preciseFailureAndRecovery(result)
```

Serialize conflicting commands per timer and reject stale pending versions. Completion, pause, and stop races resolve against current engine state; report the resulting state rather than an outdated success. Use an elapsed-time source for running countdowns and persist enough state for interruption recovery; actual background execution and alert delivery remain implementation feasibility checks.

## Nonvoice controls and accessibility contract

The start screen always exposes preset start buttons plus `Set Duration`, which opens a labeled duration entry with `Start Timer` and `Cancel`. The active timer presents its label, remaining time, explicit state, and Pause/Resume and Stop. Completed timers expose Dismiss and Restart. Stopping affects only that timer, not the saved preset. Cancel abandons only the uncommitted request. No hidden gesture or voice command is required.

Use semantic buttons, short outcome-specific labels, visible pressed/focus/disabled states, and nonoverlapping activation regions of at least 44 × 44 pt on both iOS and watchOS as the design target. The supplied accessibility guide lists 44 × 44 pt defaults and smaller minima; this design deliberately retains the defaults. On Watch, use full-width inline primary controls and consistent peer heights. Do not assign Return/default activation to either ambiguous duration. During a pending commit, show `Starting…`, prevent duplicate submission, and leave existing timer controls usable. [Buttons — Best practices and Platform considerations](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices)

Text status duplicates every essential spoken question, result, and error; status is never conveyed only by color or sound. Accessible control names identify action and timer, for example “Pause pasta timer”; timer value and running/paused state remain queryable without announcing every countdown tick. Logical task order is question/status, choices or primary action, secondary action. These semantics are specified, not verified with VoiceOver.

Allow text reflow without clipped labels or lost actions at at least 200% text enlargement on iOS and 140% on watchOS, retaining logical order in portrait/landscape where supported. Keep drafts and active timers on interruption; resumed voice requests must revalidate their target. Test keyboard and supported assistive navigation through the full nonvoice task. No automatic screen dismissal requires a fast response. [Accessibility — Vision, Mobility, Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility)

## Data and capability boundary

| Data/access | Purpose and rule |
|---|---|
| Local preset label, duration, timer ID/state | Resolve commands and operate timers. Send only necessary resolved parameters to the timer engine. No account details in response payloads. |
| Account/profile fields | Not needed for the cooking task. Exclude from dialogue generation, timer snippets, and timer diagnostic events. Local timer use is not gated on account sign-in. |
| Microphone / recognition | Optional voice entry only. If an app-owned voice adapter requires authorization, request it only on invocation through the appropriate system permission flow. Proposed purpose: “Use the microphone to hear your timer commands.” Adapt this copy truthfully to the eventual processing architecture. |
| Raw audio/transcript | No app-owned retention or analytics collection in this design. Prefer local processing where feasible. An external/system voice provider's processing and retention must be assessed separately; do not promise it is local. |

Do not assume Siri activation grants app microphone access or requires a duplicate app prompt. A Siri adapter, if feasible, maps system-resolved actions/entities to the same contract; HIG is not proof of an available timer schema or watchOS API. Prefer built-in Siri dialogue if it meets this contract. Do not impersonate system listening UI, create a custom wake phrase, or assume continuous background listening. In-app voice failure shows “Voice input is unavailable. Use the timer controls below.” A successful start with failed speech playback still shows Running; retrying output must not create a second timer. [Privacy — Best practices and Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy), [Siri — Getting your app to work with Siri](https://developer.apple.com/design/human-interface-guidelines/siri#Getting-your-app-to-work-with-Siri)

## Worked before/after

Fixture: saved pasta presets are 8 and 12 minutes; no active timer.

**Before (supplied behavior):** User says “Start pasta timer.” The app chooses a saved duration randomly, announces private account details, and offers no timer control when speech fails. Exact original dialogue and preset values were not supplied.

**After (proposed):**

1. User: “Start pasta timer.”
2. App speaks and displays: “Which pasta timer: 8 minutes or 12 minutes?” No timer exists yet. Both start buttons and Cancel are visible.
3. User: “8 minutes.” The engine successfully creates one timer.
4. App: “Pasta timer started for 8 minutes.” The screen shows “Pasta · 8:00 · Running” and Pause / Stop. No account fields enter the response.
5. Speech input becomes unavailable. User activates Pause onscreen; state becomes Paused. Resume and Stop remain operable. If the user cannot touch the screen while cooking, the app cannot promise continued hands-free control; the running timer continues without requiring another voice session.

Alternate branch: “Cancel” at step 3 creates nothing. Silence/session expiry also creates nothing. If speech output alone fails at step 4, the timer remains running and text conveys success.

## Acceptance checks and current evidence

**Passed — static specification inspection only:** `interface.md` read; all three supplied defects mapped to revised behavior; deterministic ambiguity handling, minimal responses, nonvoice controls, cancel/failure paths, platform distinctions, and explicit commit semantics appear in this document. Root skill, topic index search, selected families, routed procedures, and corresponding source guides were read locally. No web access used.

**Failed — supplied baseline behavior:** random selection fails the ambiguity criterion; private account speech fails the response-data criterion; no speech-free control fails the alternative-input criterion. These findings rely on the written brief, not a reproduced runtime.

**Not executed — required implementation acceptance scenarios:**

| Check | Pass condition |
|---|---|
| Ambiguous start repeated 100 times | Every request asks; no timer is created before a valid choice. Neither recency nor tie ordering selects a duration. |
| Choice, invalid reply, cancel, silence, stale preset | Correct duration starts once; invalid/cancel/silence create nothing; stale data triggers renewed resolution. Existing timers survive. |
| Retry and race handling | Same request ID creates one timer; distinct deliberate repeat asks about another timer; conflicting commands report actual final state. |
| Response privacy | Inspect audible, visual, error, and diagnostic payloads with synthetic account secrets: no account fields or secrets appear. Safe label substitution works. |
| No optional visual snippet | With all snippets omitted, spoken question and success still identify the timer and duration. |
| Speech unavailable / permission denied | Start, pause, resume, stop, completion dismissal, and restart succeed entirely through visible controls; no optional permission gate blocks them. |
| Output failure after commit | Visible Running remains accurate; retry of speech output creates no timer. |
| Engine unavailable | No false success; Try Again can recover, Cancel preserves prior state. |
| Timer expiry, app interruption, wrist lowering | Correct remaining time/state survives; completion is persistent; no duplicate completion or false alert-delivery claim. |
| iPhone orientation and enlarged text; Watch enlarged text | Required labels and controls remain readable, reachable, and nonoverlapping at specified scales. |
| Supported assistive inputs and focus | Full task works without speech; names, state, focus order, and activation match the contract; countdown does not overwhelm announcements. |
| Geometry, appearance, and device use | Measure hit areas and separation; evaluate contrast in light/dark and Increase Contrast; assess actual reach/readability on supported devices. |

## Evidence limits and remaining feasibility work

Only the short written interface brief and installed guidance were available. There is no implementation, screenshot, timer engine contract, device/version matrix, permission configuration, or runtime evidence. Example durations, state rules, idempotency, and privacy filtering are proposed product decisions, not universal HIG mandates. Numerical accessibility targets retain the local guide's platform scope; geometry and contrast were not measured.

Local source guides describe themselves as derived guidance, with snapshot/retrieval dates of 2026-10-25; their existence does not establish independent source review or current API availability. Official links above identify their source sections and were not opened. No conflict material to the selected decisions was found in the read guides.

Before implementation commitment, verify supported iOS/watchOS versions, system voice action/entity availability, permission and processing requirements, background timer persistence, and completion delivery against actual platform documentation and devices. Watch support remains conditional; do not advertise it until these checks pass. No SDK compilation, GUI interaction, device testing, Siri recognition/entity-resolution testing, accessibility execution, security certification, or reliable background alert delivery is claimed.
