# Revised interaction specification: watch breathing timer

## Scope and decisions

The supplied `interface.md` describes watchOS behavior: Crown rotation changes duration and volume together, gives no visible value feedback, and traps scrolling during a session. It also requires accidental wrist motion not to destroy an active session. No implementation or device evidence was supplied.

Use one Crown owner per visible context. On main screens, rotation navigates vertically; adjustment requires explicitly opening a dedicated, non-scrolling editor. Keep Crown presses system-owned. These decisions apply the local [Digital Crown guidance, Apple Watch section](https://developer.apple.com/design/human-interface-guidelines/digital-crown#Apple-Watch): navigation takes priority where needed, touch equivalents are provided, and rotation has visible feedback.

Freeze duration when a session starts. Crown rotation, wrist movement, navigation, and leaving the foreground cannot pause, reset, restart, or discard that session. This is a product safety decision implementing the brief, consistent with the routed watchOS procedure's instruction to preserve progress through wrist lowering and interruptions. Keep remaining time and the current breathing cue on the initial session view; keep navigation shallow, following [Designing for watchOS, Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices).

The numeric ranges and rates below are proposed product defaults, not Apple requirements: duration 1–10 minutes in 1-minute steps, initial value 3 minutes; app breathing-audio volume 0–100% in 5-percentage-point steps, initial value 50%. Volume affects only this app's breathing audio, not system volume. Confirm suitable ranges during product validation.

## Context and action contract

| Context | Crown rotation | Equivalent touch action | Visible response / exit |
| --- | --- | --- | --- |
| Setup | Scroll setup content; never edit values | Vertical swipe | Content follows movement; rows show `Duration · 3 min`, `Audio Volume · 50%`; tapping either opens its editor |
| Duration editor (setup only) | Adjust duration draft only | `Decrease` / `Increase` buttons | Persistent `Session Duration`, value with `min`, and `Turn Crown to adjust`; `Save` commits, `Cancel` discards |
| Running or paused session | Scroll session content; no value adjustment | Vertical swipe | Remaining time and breathing cue first, session controls and Audio Volume reachable below; no scroll interception by breathing animation |
| Audio Volume editor (setup or active session) | Adjust audio draft only | `Decrease` / `Increase` buttons | Persistent `Audio Volume`, percentage, and `Turn Crown to adjust`; `Save` applies, `Cancel` discards; active timer continues independently |
| Completed session | Scroll completion content | Vertical swipe | Show completion and `Set Up Another Session`; rotation never starts another session |

Editors must fit value, adjustment controls, Save and Cancel without vertical scrolling on supported layouts. If a layout cannot satisfy this, use a scrollable touch-only editor with Crown navigation, rather than mixing scrolling and adjustment. Do not assign adjustment until that layout condition is met. Save/Cancel return to the previous screen and its scroll position. Back, interruption, or loss of editor visibility discards the draft and releases adjustment ownership; it never ends a session. Do not auto-open an editor on focus, wrist raise, or rotation.

`Start` is the prominent full-width setup action; it snapshots duration and creates exactly one session. Running shows `Pause`; paused shows `Resume`. These explicit taps alone change pause state. Pause preserves remaining time, and Resume continues it. Duration editing is unavailable during either state; show the original total duration as read-only. Completion occurs only when remaining time reaches zero. This revision adds no discard/reset gesture or early-end action.

Use inline capsule buttons with visible press feedback and distinct enabled/disabled states. Save is the editor's prominent action; Cancel has cancellation semantics. Decrease/Increase have equal heights and readable action names. At bounds, disable the corresponding button; keep the limit value visible. Provide separate, nonoverlapping hit regions of at least 44 × 44 pt as the local guide's general target guidance, subject to layout validation. See [Buttons, Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices) and [watchOS](https://developer.apple.com/design/human-interface-guidelines/buttons#watchOS). These are specified controls, not claims about measured geometry or accessible execution.

## Rotation, feedback, and state rules

- The input adapter supplies signed normalized rotation units: positive means increase in an editor or forward navigation outside it. Resolve hardware orientation in that adapter; do not assume physical clockwise means increase for every wearing configuration.
- Proposed tuning: one normalized unit yields one step at slow speed (up to 2 units/second), two steps above 2 through 5 units/second, and three above 5. Accumulate fractional steps, emit whole steps, and retain the remainder. On reversal, clear the old fractional remainder. Reset rate history and remainder on entering/exiting an editor; require fresh rotation after entry.
- Clamp at the stated bounds; never wrap. Clear accumulated excess at a bound so reversal responds promptly. Slow rotation must reach every permitted value. Fast rotation traverses the range more quickly without changing any other field.
- Render each new draft value immediately alongside its unit; rotation never changes an invisible field. At a bound, show `Minimum` or `Maximum` beside the value. Navigation at a content boundary remains navigation and cannot fall through into adjustment.
- Use default haptic detents at value steps where available and compatible. Do not overlay custom Crown taps with the breathing rhythm. If detents conflict with breathing cues, disable adjustment detents and retain visual feedback. Selection of the final haptic behavior requires device evaluation. This preserves the qualifications in [Digital Crown, Apple Watch](https://developer.apple.com/design/human-interface-guidelines/digital-crown#Apple-Watch).
- Route each event exactly once. System-owned input is never converted into app commands. No motion-sensor event changes timer state. Navigating away releases app adjustment ownership while session time continues.

Framework-agnostic pseudocode:

```text
onRotation(event):
    if systemOwns(event): return TO_SYSTEM
    if visibleEditor exists AND editorFitsWithoutScrolling:
        draft = clamp(draft + quantizedSteps(event) * fieldStep, min, max)
        render(fieldLabel, draft, unit, boundaryStatus)
        return HANDLED              // no propagation to scroll or another field
    return NAVIGATE_VISIBLE_CONTENT // never changes timer or settings

onStartTap():
    if session is absent or completed:
        session = newSession(total = savedDuration, remaining = savedDuration)
        persist(session)
        showSession()

onSaveTap():
    if editor == duration AND session is active: discardDraftAndReturn()
    else: commitOnlyEditedSetting(); closeEditorAndRestoreScroll()

onPauseTap(): freezeRemaining(); persist(session)
onResumeTap(): resumeFromRemaining(); persist(session)
onWristLowerOrInterruption(): discardDraft(); releaseEditor(); persist(session)
onWristRaiseOrReturn(): showSessionIfActive(); reconcileElapsedTime()
```

Use an elapsed-time source independent of animation frames and foreground rendering. Persist session identity, total, running/paused state, and enough timing data to recover remaining time. A running session continues across wrist lowering and app interruption; a paused session remains paused. Reconcile elapsed time on return and show completion if its deadline passed. Breathing phase derives from elapsed session time, excluding pauses. Persistence failures and process recovery need implementation validation; they must not silently create a fresh session. Input events and timer completion are serialized: if completion occurs during volume editing, discard the draft, release the editor, and show completion.

## Worked before/after

Before (illustrative values): a 3-minute session is running with 2:20 remaining and volume at 50%. The user turns the Crown to reach lower content. The brief says duration and volume both change, without values showing, and scrolling is trapped. Their exact resulting values are unknown because the brief specifies no rate or bounds.

After: the same turn scrolls to lower session content. Total remains 3 minutes; remaining time advances only with elapsed time; volume stays 50%. The user taps Audio Volume. One slow positive normalized unit changes the visible draft from 50% to 55%; total and remaining-time calculation are unaffected. Cancel restores 50%; alternatively Save applies 55% and returns to the prior scroll position. Lowering the wrist with 2:10 remaining and returning 20 seconds later shows about 1:50 remaining, assuming uninterrupted elapsed time. Any unsaved volume draft is discarded. Accidental rotation can scroll, or adjust a draft if already editing; it cannot destroy or restart the session.

## Acceptance checks and current results

**Passed — specification inspection only:** one Crown owner per context; separate duration/volume edits; visible values and units; explicit touch alternatives; system presses reserved; duration frozen after Start; wrist/interruption preservation specified. The table, rules, and pseudocode agree on these contracts.

**Failed — supplied design, based solely on the brief:** independent adjustment, visible value feedback, and navigation priority. This is a review of described behavior, not a reproduced runtime failure.

**Not executed — required implementation checks:**

| Scenario | Required result |
| --- | --- |
| Rotate on setup/running/paused screens, including at scroll boundaries | Content navigates where possible; no setting or session-state mutation |
| Edit each field independently via Crown and via touch | Same legal values; only the named draft changes; Save and Cancel behave as specified |
| Slow, fast, fractional, reversing, and out-of-range input | Precise slow selection, faster traversal, clamping without wrap or reversal delay |
| Enter/exit an editor mid-rotation | No stale delta, double handling, scroll leakage, or hidden adjustment |
| Accidental rotation, wrist motion, wrist lowering, foreground loss, process restoration | Session identity and total preserved; elapsed/paused state reconciled; no reset/restart |
| Pause/resume and repeated Start activation | Remaining time preserved; no duplicate session; no Crown activation |
| Timer completes while volume editor is open | Completion shown once; draft discarded; adjustment capture released |
| Smallest supported layout and enlarged labels | Editor fits or uses specified navigation fallback; values, units, and actions remain reachable; hit regions do not overlap |
| Supported Watch hardware, system navigation, and assistive technology | Correct Crown direction/rate, reserved presses, touch access, meaningful control names/order, readable feedback, and compatible haptics |

## Evidence limits and audit trail

Only supplied local files and installed instructions were used; no web requests were made. Official links above identify the sources recorded in the local snapshot, not live verification. Local guides identify retrieval/snapshot date 2026-10-25; they are derived guidance, not SDK documentation or proof of independent review.

Read the installed root `apple-hig/SKILL.md`, inspected `interface.md`, and searched `references/topic-index.md` for Crown/watchOS and buttons. Read each selected family, then its topic procedure, before its supporting guide:

- `subskills/apple-hig-inputs/SKILL.md` → `.topics/apple-hig-digital-crown/SKILL.md` → `references/digital-crown.md`.
- `subskills/apple-hig-getting-started/SKILL.md` → `.topics/apple-hig-designing-for-watchos/SKILL.md` → `references/designing-for-watchos.md` (routed by Digital Crown).
- `subskills/apple-hig-menus-and-actions/SKILL.md` → `.topics/apple-hig-buttons/SKILL.md` → `references/buttons.md` (for explicit touch actions).

All these paths resolve under the installed `.agents/skills/apple-hig/` package; each file was consumed by a separate cat or rg command. No implementation, Apple SDK, device, GUI, accessibility session, or physical haptic test was executed. No runtime pass is claimed. Rate thresholds, supported-layout fit, timing recovery, and haptic compatibility remain validation work. Always On rendering, notifications, complications, and health/sensor integrations are outside this Crown revision; no behavior for those surfaces is inferred.
