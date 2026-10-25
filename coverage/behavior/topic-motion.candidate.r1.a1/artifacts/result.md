# Revised iPhone habit-completion interaction

This specification replaces the behavior described in `interface.md`. It is framework agnostic and requires no Apple SDK. The task is to mark a habit complete, understand its current state, and continue immediately.

## Decisions and rationale

| Supplied behavior | Revised decision | Basis |
|---|---|---|
| Every checkbox triggers eight seconds of confetti. | Remove confetti. On a newly committed completion, reveal a permanent checkmark and “Completed” label immediately; optionally accent the checkmark with one 180 ms opacity fade of a surrounding highlight. No movement, scale, bounce, flashing, or delayed checkmark. | HIG recommends brief, precise, interruptible feedback for repeated operations. The highlight and its 180 ms duration are product choices. [Motion: Providing feedback](https://developer.apple.com/design/human-interface-guidelines/motion#Providing-feedback) |
| Background continuously parallax-scrolls. | Keep the background stationary in every mode. Ordinary user-driven content scrolling remains available; no background drift, tilt response, or depth effect. | Movement adds no task information here. HIG recommends motion that supports the task and reduced or optional experiences. [Motion: Best practices](https://developer.apple.com/design/human-interface-guidelines/motion#Best-practices) |
| Reduce Motion removes animation and checkmark. | Reduce Motion removes the decorative highlight only. State, checkmark, label, actions, and semantic value remain identical. | Important information must survive removal of motion; reduce automatic movement and depth effects. [Accessibility: Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive) |
| Status changes must remain understandable. | Use shape plus persistent text, with equivalent programmatic state. Completion never depends on color, sound, motion, or a disappearing message. Routine feedback stays beside the habit. | [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision), [Feedback: Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices) |

No sound or haptic is required or introduced by this specification. Celebration is the brief local highlight and affirmative persistent state. There is no full-screen overlay, modal confirmation, automatic row reordering, or focus jump.

## State and control contract

Assumption: completion is reversible and keyed by habit and day. The brief supplies no storage or synchronization model. Use the application's authoritative commit boundary; local durable storage may be that boundary. A remote acknowledgement is necessary only if the product defines remote storage as authoritative. Never equate animation completion with persistence.

| State | Visible representation | Available behavior |
|---|---|---|
| Incomplete | Empty completion indicator; “Not completed” | Activate to request completion. |
| Saving target state | Preserve last committed indicator; show “Saving completion…” or “Saving change…” | Other habits, scrolling, and navigation remain usable. Further activation of this same control does not enqueue a second write. Expose pending/unavailable state. |
| Complete | Checkmark; “Completed” | Activate to mark incomplete; no timed undo deadline. |
| Save rejected | Keep last committed indicator and status; persistent adjacent “Couldn’t save change. Try again.” | Retry the same target through the completion control. Clear error on retry or a later successful change. No success highlight. |

Completion indicators must identify the habit, expose their binary committed value, and expose pending/error descriptions through the host's accessibility facilities. Support ordinary accessible activation without a custom gesture. Keep focus on the activated control and decorations out of the accessibility tree. A state notification must convey the result without moving focus; avoid duplicating a state change already announced by the host control. Actual spoken behavior needs platform testing.

Use a comfortable iPhone activation area of at least 44 × 44 pt as this design's target; this follows the guide's iOS default rather than treating its smaller minimum as a target. [Accessibility: Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility)

The brief calls the controls checkboxes but does not establish their layout. They represent independent binary habit states, with no aggregate or mixed state. Preserve that meaning. If implemented as labelled iOS list-row toggles, follow the guide's switch-style convention; outside lists use a stateful button. This specification does not establish that a native checkbox exists on iOS or that the unseen layout is defective. Every treatment must distinguish off/on beyond color. [Toggles: Best practices and iOS](https://developer.apple.com/design/human-interface-guidelines/toggles#iOS-iPadOS)

## Motion lifecycle and pseudocode

All timing below is a proposed design value, not measured performance or an Apple duration requirement. Commit and render are independent of decorative playback.

```text
motionAllowed = systemReduceMotion is explicitly false
                // unknown or unavailable preference: choose static fallback
highlight = none

activate(habit, day):
    if writePending(habit, day): return   // no queued writes or celebrations
    target = not committedValue(habit, day)
    cancelHighlight(habit, day)
    clearError(habit, day)
    token = beginWrite(habit, day, target)
    renderCommittedStateWithPendingText()

onWriteResult(token, result):
    if token is not currentWriteForItsHabitAndDay: return
    clearPending(token)
    if result.failed:
        retainCommittedState()
        showPersistentInlineError()
        return
    setCommittedValue(result.value)
    renderPermanentIndicatorAndStatusImmediately()
    exposeStateChangeToAccessibilityHost()
    if result was incomplete -> complete AND rowIsVisible AND appIsActive
       AND motionAllowed:
        cancelAllDecorativeHighlights()   // at most one active; no queue
        showHighlightAroundThisIndicator(opacity = 1)
        fadeHighlightToZero(duration = 180 ms, linear)
        removeHighlight()

onReduceMotionChanged(enabledOrUnknown):
    recompute motionAllowed
    if not motionAllowed: cancelAllDecorativeHighlights()
    // never hide or regenerate committed indicators; never replay on disabling

onNavigationAwayOrBackgroundOrRowRemoved:
    cancelAllDecorativeHighlights()
    // persistence proceeds independently; no delayed celebration on return
```

The highlight uses a fixed footprint around the indicator, never obscures its glyph or label, accepts no input, and changes no layout or hit region. The permanent glyph stays fully visible throughout. Completing another habit cancels the prior highlight and may show its own; a new interaction never waits for an old effect. Reversing completion cancels the effect, commits the opposite state, and shows “Not completed” without a celebration. Restoring saved data, rebuilding a view, sync updates, and opening the app do not replay celebrations. If writes can outlive a view, route their results to the data model; visibility governs decoration only.

## Worked before/after

**Before, as supplied:** A person marks “Read” complete and gets eight seconds of confetti over a continuously moving background. With Reduce Motion enabled, the animation and checkmark disappear. The resulting visual status cannot rely on that missing checkmark. The brief does not establish whether input is blocked or animations queue.

**After, proposed:** A person activates “Read,” initially “Not completed.” While saving, its label says “Saving completion…” and other habits remain usable. On successful commit at time T, its checkmark and “Completed” label appear. With Reduce Motion off, the local highlight fades from T to T + 180 ms. If “Walk” completes at T + 80 ms, Read's highlight is canceled; its checkmark remains, and Walk can receive its own highlight. With Reduce Motion on, both commits show exactly the same permanent states with no decorative animation. Marking Read incomplete later returns it to “Not completed.” A rejected write preserves the prior state and provides an inline retry explanation.

## Acceptance checks and current results

**Passed — document inspection only:** The revised contract preserves state in both motion modes, removes continuous parallax and confetti, defines cancellation without queued effects, separates persistence from decoration, covers both state directions and errors, and specifies a static fallback when preference access is unavailable. The installed root, selected families, and topic procedures were read before their supporting guides.

**Failed — supplied design against the revised contract:** Eight-second confetti fails the proposed brief local feedback rule; continuous parallax fails the stationary-background rule; removing the checkmark with Reduce Motion fails state preservation. These are findings from the supplied description, not observed application execution.

**Not executed — implementation acceptance:**

1. Complete and uncomplete a habit with Reduce Motion off, on, and unavailable. Check identical durable state, text, semantics, and available actions in every mode; only the optional highlight differs.
2. Instrument the highlight: it ends within 180 ms of its start, with no wait before the permanent state. Rapidly complete multiple habits and reverse a completed one; confirm at most one highlight, no playback queue, no blocked next task, and correct final data.
3. Enable Reduce Motion halfway through the effect. Decoration stops on preference handling; the checkmark and text remain. Disable it again; no replay occurs.
4. Navigate away, scroll the row out of view, or background during saving or highlighting. On return, show the current committed state without replay or stale callbacks changing another habit/day.
5. Delay and reject writes. Pending state remains truthful; repeated activation of the pending control creates no extra writes. Failure leaves the old state and persistent recovery explanation. Retry succeeds without false completion feedback.
6. With animations disabled and sound muted, identify each habit's state through text and shape. Verify no color-only distinction, flashing, layout shift, or timed access to an essential action.
7. On a supported iPhone environment, verify accessible names, state updates, pending/error exposure, focus retention, and activation using VoiceOver and supported alternative inputs. Measure activation geometry and check status readability with enlarged text and light/dark appearances. These require actual implementation evidence.

## Evidence and limits

Evidence consists of the one-paragraph `interface.md` brief and the installed apple-hig package. Route: root `SKILL.md` → topic-index search → Foundations (Motion and Accessibility), Patterns (Feedback), and Selection and input (Toggles) family/topic procedures → their local source guides. The guides identify a 2026-10-25 snapshot and are derived guidance, not SDK documentation. Official links above identify the cited source sections; they were not browsed.

No implementation, screen geometry, colors, storage system, executable prototype, device recording, or runtime measurement was supplied. No device, SDK, GUI, accessibility, haptic, performance, contrast, or comfort execution was performed. The 180 ms duration and single-highlight policy remain design hypotheses for validation; reading guidance does not establish comfort or accessibility conformance. No source conflict affecting these decisions was found in the consulted local passages. No newer Apple guidance or unconsulted media is claimed.
