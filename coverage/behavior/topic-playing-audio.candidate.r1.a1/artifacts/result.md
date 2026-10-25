# Revised iPhone lesson audio interaction specification

## Scope and evidence

Input: `interface.md` describes silent flashcards stopping music, narration continuing after explicit Pause, calls restarting the lesson at full volume, and available caption/transcript data. These are reported behaviors; no implementation, audio configuration, screens, or runtime traces were supplied. This is a framework-agnostic design contract, not SDK code.

Installed guidance was read in this order: apple-hig root; topic-index audio/interruption search; Patterns family → Playing audio procedure → audio source guide; Multitasking procedure → source guide; topic-index accessibility search; Foundations family → Accessibility procedure → source guide. All paths were resolved under `.agents/skills/apple-hig/`. No web access was used.

## Decisions

1. **Silent flashcards acquire no audio session.** Entering, flipping, answering, and advancing a silent card produce no app audio and do not stop, duck, or claim controls from music. If optional incidental feedback is added later, it must respect Silent mode and mix with other audio (ambient behavior); solo ambient would interrupt music and is unsuitable here. Narration is separate deliberate learning media, using playback-category behavior only after Play. Playback may sound in Silent mode because the person requested it. These category descriptions are requirements for an eventual platform adapter, not assumed APIs. [Playing audio: best practices](https://developer.apple.com/design/human-interface-guidelines/playing-audio#Best-practices).

2. **Explicit Play owns a bounded narration session.** Use nonmixing playback for intelligible speech during that session; this is a product choice permitted by configurable playback mixing, not a universal HIG requirement. Activate only for requested playback; release on Pause, completion, navigation to a silent card, interruption, failure, or departure from the lesson. Release with notification to let eligible other audio resume; do not directly start another app. Never change global volume, force speaker output, or set gain to maximum. Use a stable app-relative narration gain and system volume/output controls where supported. [Playing audio](https://developer.apple.com/design/human-interface-guidelines/playing-audio#Best-practices).

3. **Pause is authoritative.** It stops audible narration and its clock, cancels queued speech and pending starts, and preserves position. Completion callbacks and delayed interruption-end events cannot undo it. Resume requires a new Play unless a strictly eligible temporary interruption ends. Replay from the beginning is an explicit separate action; it never happens as recovery.

4. **Recover only with valid intent and system permission.** Save lesson/card identity, answers, narration asset/version, confirmed playback position, caption location, and relative gain. A call pauses at the last confirmed position. Auto-resume is allowed only if narration was playing immediately before the interruption, the system explicitly permits resumption, no later Pause/route-loss/competing-playback/navigation event revoked intent, the same lesson is active in the foreground, and the selected output is available. Otherwise show “Paused — tap Play to continue.” Missing or ambiguous signals mean stay paused. A newly chosen playlist revokes automatic resume indefinitely; a brief direction may temporarily pause and resume under the same guard. [Playing audio: interruptions](https://developer.apple.com/design/human-interface-guidelines/playing-audio#Handling-interruptions), [Multitasking](https://developer.apple.com/design/human-interface-guidelines/multitasking#Best-practices).

5. **Preserve output choice and context.** Headphone disconnection stops playback before any subsequent speaker playback and requires explicit Play. Headphone connection reroutes active narration smoothly without resetting its position or starting paused narration. If the route cannot be confirmed, remain paused. App switching or screen locking pauses this attention-dependent lesson and saves state; returning never starts audio automatically. Background listening is outside this design. [Playing audio](https://developer.apple.com/design/human-interface-guidelines/playing-audio), [Multitasking](https://developer.apple.com/design/human-interface-guidelines/multitasking).

6. **Audio is optional for lesson access.** Show the available transcript on silent cards and offer synchronized captions during narration, including meaningful non-speech information if present. Preserve caption preference across cards. Pause freezes caption progress; manual transcript reading remains available without starting audio. Label states and actions “Play narration,” “Pause narration,” “Replay narration,” and “Paused”; do not convey them by sound or color alone. Use comfortable iPhone activation areas starting at 44 × 44 pt and support text enlargement to at least 200% without losing content or controls. These are design targets pending measurement. A pronunciation-listening exercise may require an explicitly labeled text alternative rather than claiming text provides an identical listening assessment. [Accessibility: hearing, mobility, vision](https://developer.apple.com/design/human-interface-guidelines/accessibility).

## State and event contract

State: `SILENT`, `READY`, `STARTING`, `PLAYING`, `PAUSED(reason)`, or `COMPLETE`. Keep user intent separate from transport state. Every async start carries a generation token; every stop invalidates that token. Serialize events, with Pause/route loss taking precedence over pending starts. The transport must support stopping buffered/queued output, reporting confirmed position, and releasing audio ownership; absent capability is a paused error, not permission to keep playing.

| Event | Required transition and visible result |
| --- | --- |
| Enter silent card | Stop prior narration; release session; `SILENT`; show transcript and optional Play. Preserve external music. |
| Play | Save explicit intent; `STARTING`; request playback ownership on current output. On success and valid token, start at saved position → `PLAYING`. On failure, release → `PAUSED(error)` with Retry and transcript. |
| Pause, including while starting | Revoke resume intent; invalidate starts; stop output/clock; save confirmed position; release → `PAUSED(user)`. |
| Temporary interruption begins | Snapshot whether playing and current intent token; stop/save/release → `PAUSED(interruption)`. No reset or volume change. |
| Temporary interruption ends | Apply guard below. Resume at saved position only if eligible; otherwise remain paused with Play. |
| Sustained competing audio begins | Stop/save/release; revoke resume intent → `PAUSED(otherAudio)`. Its ending does not restart narration. |
| Headphones disconnect / output unavailable | Stop/save/release; revoke resume intent → `PAUSED(route)`. Show “Audio paused — check output, then tap Play.” |
| App leaves active lesson | Stop/save/release; revoke resume intent → `PAUSED(departure)`. Return restores card, answer, transcript and position. |
| Narration ends | Release ownership → `COMPLETE`; keep transcript; offer Replay. Do not autoplay the next card. |
| Next card / leave lesson | Stop and invalidate pending work before changing identity; save progress; never carry a resume token into the next card. |
| External Pause / Play | Honor only while this lesson owns a relevant active or resumable media context. Pause has identical authority to onscreen Pause. Do not register ownership on silent entry or reclaim controls after another app takes over. Expose only supported commands. |

```text
onTemporaryInterruptionEnd(signal, interruption):
    eligible = interruption.wasPlaying
        and signal.explicitlyAllowsResume
        and interruption.intentToken == currentIntentToken
        and noOtherInterruptionIsActive
        and sameLessonAndAsset
        and lessonIsActiveInForeground
        and selectedOutputIsAvailable
    if eligible: requestPlaybackAt(savedPosition, newGenerationToken)
    else: remainPaused()

onAnyPlaybackStartCompletion(token):
    if token != currentGeneration or resumeIsBlocked:
        stopAndReleaseThatStart()
    else:
        playAt(savedPosition)  // never set system volume
```

A new explicit Play may reestablish intent after a block, but cannot play through an ongoing system interruption. After process termination, restore saved context paused. Persist checkpoints during playback and at transitions; use the latest confirmed position if shutdown prevented a final save, never silently reset the whole lesson.

No microphone use is required by this brief. Do not record, request microphone access, or activate record/play-and-record behavior. Recording exercises would require a separate consent and interruption design; recording/call-specific policies are not established by this artifact.

## Worked before/after

**Before (reported):** Music is playing. Opening a silent flashcard stops it. Narration continues despite Pause. A call interrupts the lesson; afterward it restarts from the beginning at full volume.

**After (specified):** Music continues while the learner reads and answers card 4 silently. They tap Play; narration obtains playback ownership and other audio may pause. At 00:18 they tap Pause: speech and captions stop at 00:18 and the audio session releases. A subsequent call cannot restart this paused lesson. They later tap Play, reach 00:27, and accept a call. Position 00:27 is saved. When the call ends, a positive resume signal and all guards permit continuation at 00:27 using unchanged system volume and relative gain. Without that signal, Play remains available at 00:27. If headphones were disconnected during the call, automatic resume is blocked even with a positive signal.

## Acceptance checks and results

**Passed — specification inspection only:** The contract separates silent and deliberate audio, defines category/mixing choices, gives explicit Pause priority, guards resumption, preserves progress, forbids global volume changes, specifies routes/external controls, and uses existing text alternatives. The worked example covers both user-paused and interrupted playback. The artifact includes the topic procedure's required contracts.

**Failed — reported current behavior only:** The brief's silent-card coexistence, explicit Pause, and call recovery behaviors fail the revised contract. These failures were not independently reproduced.

**Not executed — implementation/device acceptance:**

| Check | Pass condition |
| --- | --- |
| Silent mode and coexistence | With music playing, open/flip/answer silent cards: music and volume unchanged. Incidental feedback, if added, is suppressed in Silent mode. Explicit narration Play can sound in Silent mode. |
| Pause races | Pause during playback, pending activation, and just before interruption-end: no further queued narration starts; position remains stable until Play. |
| Call recovery | Call at 00:27: preserve card/answers/position. Positive system signal resumes only under every guard; negative/missing signal stays paused. Never restart from zero or raise volume. |
| Competing audio | Start a new playlist during narration: lesson pauses indefinitely. Playlist ending does not resume lesson. Temporary directions use guarded recovery. |
| Routes | Disconnect headphones while playing, starting, and interrupted: no unintended speaker output. Reconnect does not start paused audio. Manual output changes retain progress. |
| Lifecycle and persistence | Switch apps, lock, return, and relaunch: restore context paused; no hidden narration or lost answers. |
| External controls | Lesson commands work in relevant context; silent cards and another app's playback retain that other app's control ownership. |
| Errors and completion | Activation/asset/output failures release ownership and retain transcript/progress; Retry works. Completion releases without next-card autoplay. |
| Silent access and accessibility | Complete the text alternative with sound off; captions follow media and pause correctly. Verify enlarged text, control geometry, and assistive navigation/activation on an actual implementation. |
| Recording/privacy | No microphone capture, permission request, or recording session occurs in this flow. |

## Evidence limits

Only local prose and installed guidance were inspected. Official links above identify the source articles; they were not opened. The installed references are dated 2026-10-25 and are guidance snapshots, not verified SDK documentation. No newer-release claim is made. Auto-resume guards, nonmixing narration, no autoplay, foreground-only behavior, and checkpoint policy are concrete product decisions within that guidance, not quotations of universal Apple requirements.

There is no evidence of actual session categories, caption timing quality, accessible semantics, route ordering, latency, background execution, or persistence implementation. No device, Apple SDK, GUI, audio comfort, microphone, Accessibility Inspector, or assistive-technology execution occurred. An eventual adapter must verify platform capabilities and timing; these acceptance checks remain pending until exercised. Other-platform exceptions (including visionOS and recording/call examples) are not imported into this iPhone lesson.
