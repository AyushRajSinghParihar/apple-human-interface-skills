# Revised lesson playback routing specification

## Scope and decisions

Target: iOS/iPadOS, with optional AirPlay receivers. This is a framework-agnostic interaction contract, not an SDK implementation. `interface.md` supplies the existing behavior; no code, media inventory, screenshots, or receiver capabilities were supplied.

Treat a lesson as one synchronized timeline with two media roles: **lesson video** (including its intended program soundtrack, if present) and **private narration** (a separate audio asset). Neither role is an incidental preview. Playback, pause, seek, rate, and completion act on the lesson as a unit. Narration can be explicitly turned off; failure to play enabled narration must not silently disable it.

The following privacy and synchronization policies are product decisions derived from the brief, not claims that HIG mandates this exact routing architecture:

- Never select the last-used living-room receiver automatically. Remembering its name does not authorize transmission of either role in a new lesson session.
- Private narration defaults to a verified local route. Prefer the person's connected headphones; otherwise show “Narration: This iPhone speaker” or “This iPad speaker” before Play. If the runtime cannot verify or select a local route, keep playback paused and ask the person to choose one. Do not assume that requesting “local” overrides a system-wide route.
- Selecting an external video destination does not grant permission to send narration there. Offer external narration only through a separate explicit selection labeled with the actual receiver, for example “Play narration on Living Room TV (AirPlay).” A fresh external narration selection is required after ending/reopening the lesson or losing that receiver.
- Split video/narration routing is conditional on runtime capability and synchronized playback. If unavailable, offer “Play everything on this device” or “Play video on Living Room TV without narration.” The latter requires an explicit narration-off choice. Never silently combine the streams remotely or promise independent routing merely because two assets exist.

These decisions apply [Playing audio: Best practices](https://developer.apple.com/design/human-interface-guidelines/playing-audio#Best-practices) on respecting output choices and [AirPlay: Best practices](https://developer.apple.com/design/human-interface-guidelines/airplay#Best-practices) on sending only intended media.

## Controls and route presentation

Keep ordinary Play/Pause, position/seek, elapsed/duration, volume, captions and available chapters. Prefer a standard player when the implementation environment supplies one; otherwise preserve familiar behavior. Narration has an On/Off setting and an output row separate from video output. Space toggles playback when the player owns keyboard input, without intercepting typing elsewhere. Preserve original video aspect ratio and use standard aspect behavior where available; do not bake in bars. See [Playing video: Best practices](https://developer.apple.com/design/human-interface-guidelines/playing-video#Best-practices).

Show verified current destinations, not just requested destinations:

| Role | Example confirmed label | Transitional/failure label |
|---|---|---|
| Video | “Video: Living Room TV · AirPlay” | “Connecting to Living Room TV…” |
| Narration | “Narration: Headphones · Bluetooth” | “Narration paused — choose an output” |
| Local playback | “Video: This iPad”; “Narration: This iPad speaker” | “Output unavailable” |

Use Bluetooth only when the runtime reports Bluetooth. Use AirPlay only when reported as AirPlay. If transport is unknown, show the destination name with “Connection type unavailable”; do not guess. Distinguish an audio-only receiver from a video-capable destination. Do not list an audio-only speaker as a video destination.

Use the platform route chooser when available, constrained or explained according to the media role it actually affects. If it changes all media, describe that effect before committing; do not present it as video-only. For a custom AirPlay player, use the provided control symbol when available, at lower right on iOS/iPadOS 16+, with starting, active, and unavailable states. A compatibility logo is not a route button. Without a suitable runtime control/capability, show the honest unavailable state and keep local playback usable. See [AirPlay](https://developer.apple.com/design/human-interface-guidelines/airplay#Best-practices).

Canceling a chooser keeps the prior verified route and playback intent. If no receiver is discovered, display “No external destinations available” with local playback still available. A route error offers Retry and Choose output; it must not strand the person in setup. Only show connection progress while genuinely pending.

## State and transition contract

Persist lesson ID, timeline position, playback rate, narration setting, caption choice, and lesson navigation/exit context. Persist destination names only as preferences, never as authorization. Keep current route identities, capability checks, external-narration approval, user play intent, and interruption reason in session state. Use one active lesson controller so remote commands cannot address an old lesson or start duplicate narration.

| Event | Required behavior |
|---|---|
| Open/reopen lesson | Restore position and settings, paused. Verify routes before enabling playback; no receiver transmission on launch. Prepare exit to this lesson's detail/context immediately. |
| Play | Verify both enabled roles and required approvals. Buffer/align both at the saved position, then start together. Essential learning audio follows deliberately initiated playback semantics, including playback in silent mode; do not change global volume. |
| Pause/seek/rate | Apply to both roles. During seek or rebuffering hold both, align to the target timeline, then resume only if prior user intent and route approval still allow it. |
| Change destination | Save position and intent, pause both, validate capabilities/approvals, prepare both routes, then resume if previously playing. Do not emit narration during negotiation. On failure remain paused at the saved position. |
| Headphones disconnect or approved route disappears | Immediately pause both before fallback audio is emitted. Clear approval for the lost destination. Show “Output disconnected. Choose where to continue.” No automatic speaker fallback or automatic reconnection playback. |
| Unrequested route change | Pause and verify the new route before emitting narration. A system-selected remote route does not count as app-level approval for private narration. |
| Ordinary app switch, local inline lesson | Save state and pause both because the visual lesson needs attention. Return to the same frame, paused with Resume; never reset to zero or automatically restart. |
| Explicit AirPlay playback, supported active PiP, or explicitly chosen background listening | Continue the intended lesson while backgrounded/locked if supported. Returning attaches the UI to the ongoing timeline rather than reconstructing playback. Unrelated app previews cannot replace the stream or narration. |
| Unsupported background continuation | Communicate unavailability before offering that mode. Pause and preserve position if continuation fails; do not claim that media is still playing. |
| Temporary interruption | Preserve state and pause both (chosen policy for intelligible narration). Resume only if the runtime signals resumption is appropriate, playback was active, user has not paused since, and routes/approvals remain valid. Otherwise remain paused. |
| New competing music/podcast | Pause indefinitely; do not automatically resume over the person's new selection. App return is not a resume signal. |
| Explicit exit/end | Pause both, save progress, release remote-control ownership appropriately, clear external narration approval. Reopening uses saved position. |

The distinction between attention-dependent local playback and intentional remote/background playback reconciles [Multitasking](https://developer.apple.com/design/human-interface-guidelines/multitasking#Best-practices) with [AirPlay background continuity](https://developer.apple.com/design/human-interface-guidelines/airplay#Best-practices). App inactivity is not itself an audio interruption. Handle relevant Lock Screen/receiver play, pause, and seek through the same lesson controller, only while the lesson owns the appropriate media context; never steal another app's controls. See [Playing audio: Handling interruptions](https://developer.apple.com/design/human-interface-guidelines/playing-audio#Handling-interruptions).

Framework-agnostic guard:

```text
requestPlay(origin):
    require currentLessonOwnsPlaybackContext(origin)
    require allEnabledRolesHaveVerifiedSupportedRoutes()
    require narrationIsLocalOrExplicitlyApprovedForCurrentReceiver()
    require noUnresolvedInterruptionOrRouteLoss()
    prepareBothRolesAt(savedTimelinePosition)
    if eitherRoleNotReady: holdBothAndShowActualReason()
    else: startBothUsingSharedTimeline()

onRouteOrCapabilityChange():
    holdBothAndSaveTimeline()
    invalidateStaleApprovals()
    verifyActualDestinationsBeforeAnyFurtherOutput()
```

Use a shared clock and compensate for destination latency. Proposed product acceptance target: narration/video offset stays within 100 ms after initial alignment and seeks. This is a test target, not an Apple requirement or a demonstrated capability. If the runtime cannot meet it for split routing, disable that configuration and offer the fallbacks above.

## Privacy and platform boundaries

Send only the selected lesson media to an approved receiver; never automatically mirror unrelated screens or app activity. No microphone or recording is needed for playback. Keep progress/settings on device by default; receiver identity is needed for route display and session validation, not analytics. If the eventual runtime needs protected discovery/network access, request only the necessary access when the person invokes external routing, with an accurate purpose explanation. Denial must preserve local playback. Do not invent a universal Bluetooth, local-network, or AirPlay permission prompt: exact requirements remain implementation-dependent. See [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission).

On iPhone preserve context across portrait/landscape. On iPad preserve the same state across window resizing and simultaneous app use; never infer multitasking configuration from window size. Keep transport controls and both route summaries reachable at narrow widths and enlarged text sizes. Touch must work without accessories. These are design requirements pending layout/input validation, consistent with [iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices) and [iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados#Best-practices).

## Worked before/after

**Before, supplied:** A person opens a lesson after previously using Living Room TV. Private narration silently goes there, the interface calls the connection Bluetooth, and switching to notes then returning resets playback.

**After, illustrative:** At 06:20, video and narration are playing locally through the person's verified headphones. They select Living Room TV for video. Playback pauses at 06:20; the app checks split-routing and synchronization support. If supported, it shows “Video: Living Room TV · AirPlay” and “Narration: Headphones · Bluetooth” and resumes the synchronized lesson. Narration never reaches the TV without its separate explicit selection. If unsupported, playback remains paused and offers local playback or external video with narration explicitly off. While the approved AirPlay lesson continues, the person opens notes and returns at 07:05: the player shows the actual ongoing position. If instead they had stayed with local inline playback, switching apps would pause at 06:20 and return there with Resume. Disconnecting headphones pauses both without exposing narration through speakers.

## Acceptance checks and evidence limits

**Passed — static specification review:** Read the installed root skill, selected family routes, topic procedures, then their local guides. Read `interface.md`. This document addresses all three supplied failures, distinguishes the two media roles, and defines cancel, unavailable, failure, interruption, and restoration paths. Official links above are attribution from local sources; no web pages were fetched.

**Failed — supplied baseline description:** It contradicts the proposed contract on unsolicited external narration, transport labeling, and resume preservation. This is a comparison against the brief, not a reproduced runtime defect.

**Not executed — implementation/device acceptance:**

1. Cold open with a remembered receiver: no media is transmitted before Play and explicit route selection; private narration remains local or playback stays paused.
2. Select/cancel AirPlay and Bluetooth destinations: labels match actual transport, cancel preserves state, audio-only receivers cannot receive video, and unavailable/denied discovery leaves local playback usable.
3. Exercise supported and unsupported split routes, receiver loss/reconnection, and headphones disconnect: no unintended narration output; both roles pause together, retain position, and obey fresh approval requirements.
4. Measure synchronization across local/split playback, seeks, rate changes, buffering, and remote commands against the proposed 100 ms target. Verify no duplicate narration or stale lesson ownership.
5. Switch apps, lock/unlock, return, terminate/reopen, and exit quickly: restore correct position/settings/context. Test local pause separately from supported AirPlay/PiP/background continuation. Browse other media without replacing the selected stream or exposing private activity.
6. Test silent mode, system volume, calls, brief directions, new competing playlists, and user pause during interruption. Deliberate media may play in silent mode; global volume never changes; no unauthorized automatic resume. Recording/call features are outside this lesson's scope.
7. Verify familiar transport/Space behavior, captions where assets exist, aspect ratios, orientation, narrow iPad windows, enlarged text, touch access, assistive-technology labels/order, and remote-control ownership.
8. On actual available receivers, verify destination-quality renditions are offered when supplied, background/Lock Screen control behavior, and receiver latency. No receiver is assumed to exist.

Only a design artifact was produced. No SDK availability, compilation, GUI rendering, device, receiver, audio, accessibility, or background execution was tested. The local guidance is a dated English HIG-derived snapshot (2026-10-25), not an API reference or independently verified current Apple documentation. Independent routing, synchronization, permissions, media renditions, and supported OS versions remain implementation feasibility questions; inability to verify them must result in the specified honest fallback, not a claimed capability.
