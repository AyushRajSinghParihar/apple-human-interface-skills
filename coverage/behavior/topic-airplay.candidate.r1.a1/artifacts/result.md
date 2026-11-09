# Revised lesson playback interaction specification

Scope: iOS/iPadOS lesson video plus a separate, private narration track, with optional AirPlay receivers. This is a framework-agnostic design contract; it does not require an Apple SDK. `interface.md` is the only supplied product evidence. No receiver, stream inventory, implementation, or split-routing capability is established.

## Decisions and source support

1. **One lesson, one transport timeline, two explicit media roles.** Video is the lesson visual stream; narration is essential lesson audio, not incidental feedback. Play, pause, seek, rate, completion, and interruption affect both together. A standard player is preferred where it can meet this contract; a custom adapter must retain familiar controls. Use playback-style audio semantics: deliberately started learning audio may play in silent mode, supports background playback when available, and does not change global volume. Avoid mixing competing primary media into the lesson. These choices follow [Playing audio — Best practices](https://developer.apple.com/design/human-interface-guidelines/playing-audio#Best-practices) and [Playing video — Best practices](https://developer.apple.com/design/human-interface-guidelines/playing-video#Best-practices). Exact category/API configuration is implementation work.

2. **A remembered receiver is a suggestion, never authorization to send narration.** Opening the lesson stays paused and does not acquire audio control or activate the last receiver. Show actual current outputs before Play. Narration defaults to a currently verified personal headphone output when available; otherwise require an explicit local-speaker choice before its first audible playback. An already active shared receiver is not a safe default. If a safe output cannot be established, stay paused. This conservative product policy extends HIG's respect for chosen output and headphone-disconnection privacy; HIG does not prescribe this exact consent flow. See [Playing audio](https://developer.apple.com/design/human-interface-guidelines/playing-audio).

3. **Selecting video output never implicitly selects narration output.** Offer video-only external playback with local narration only if the adapter verifies independent routing, no narration leakage through the video stream, and synchronized playback. Otherwise show “Separate video and narration outputs aren’t available. Keep the lesson on this device, or send both to a receiver.” Sending both requires an explicit choice naming the destination: “Play video and narration on Living Room TV.” Cancel preserves the previous route and position. Never silently mute, omit, or move narration to make external playback appear successful. Split routing is a product requirement subject to feasibility verification, not an AirPlay capability claimed by HIG.

4. **Show confirmed destinations and transports honestly.** Near playback controls show, for example, “Video: Living Room TV · AirPlay” and “Narration: Headphones · Bluetooth,” but only when reported by the adapter. If transport is unknown, show the destination without guessing. Pending changes say “Connecting to Living Room TV…”; confirmation alone changes the active label. A failed request keeps the last verified route if still valid; otherwise pauses. Prefer a standard routing chooser; use a familiar AirPlay control for AirPlay, not the compatibility marketing mark. For a custom iOS/iPadOS 16+ player, place that control at lower right. See [AirPlay — Best practices and Using AirPlay icons](https://developer.apple.com/design/human-interface-guidelines/airplay#Best-practices).

5. **External playback is optional.** With no receiver, discovery failure, denial, or unsupported routing, local playback remains usable. An unavailable AirPlay action explains “No available receivers”; it never blocks local Play. Send only the selected lesson stream; previews, other screens, notifications, and unrelated private activity must not replace it. Supply available destination-appropriate renditions; the brief supplies none, so do not claim 4K or invent encodes. See [AirPlay](https://developer.apple.com/design/human-interface-guidelines/airplay#Best-practices).

6. **Preserve context across app changes.** Save lesson ID, timeline position, rate, narration selection, captions selection, navigation context, playback intent, interruption reason, and confirmed route identities. Saved routes are descriptive, not permission for reconnection. App return reconciles actual playback instead of rebuilding at zero. An active external stream continues across background/lock when supported, as AirPlay guidance recommends. Local inline playback pauses when leaving the viewing experience unless supported PiP was explicitly entered. PiP continues the same lesson and narration where supported. Return after an attention pause restores a paused frame with Resume; it does not autoplay. This resolves the general attention-dependent pause advice in [Multitasking](https://developer.apple.com/design/human-interface-guidelines/multitasking#Best-practices) with the more specific external-stream continuity advice in [AirPlay](https://developer.apple.com/design/human-interface-guidelines/airplay#Best-practices). Background incapability pauses safely at the retained position rather than promising continuation.

## Interaction and state contract

The main player exposes Play/Pause, seek, rate, available captions/chapters, and current route status. Route changes are at most two actions away. Preserve original video aspect without baked-in bars. Space toggles playback when the player owns keyboard focus, without intercepting text entry. iPhone portrait/landscape and iPad wide/narrow windows retain the same lesson and controls; compact layouts reflow status text instead of hiding the narration destination. These adaptations follow [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices), [Designing for iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados#Best-practices), and [Playing video](https://developer.apple.com/design/human-interface-guidelines/playing-video#Best-practices).

States: `ready-paused`, `preparing`, `playing`, `buffering`, `route-pending`, `interrupted`, `ended`, `recoverable-error`. Keep desired intent separate from observed state. A single coordinator owns both tracks and remote-command handling.

| Event | Required transition and visible result |
| --- | --- |
| Open/reopen | Restore context and query actual outputs. Resume an existing live session in place; a recreated session starts paused at its checkpoint. Never activate a saved receiver. |
| Play | Validate both output assignments and explicit narration authorization; prepare both tracks at the retained lesson time. Start together only once both are ready. Missing narration produces a recoverable error with Retry, not silent partial playback. |
| Pause / remote Pause | Pause both and checkpoint. Clear automatic-resume eligibility. |
| Seek / rate / remote command | Apply once to the lesson coordinator and both tracks. Reject unsupported commands honestly; never operate another lesson or steal another app's controls. |
| Route request | Capture time and prior intent, pause both, describe exactly which tracks will move. Obtain explicit narration approval for a shared destination. Validate capability before committing. |
| Route succeeds | Verify actual destinations for each track, align both at captured time, update labels, then resume only if prior intent was playing and authorization remains valid. |
| Cancel / route failure | Restore the prior assignment only if still verified and authorized; retain time. Otherwise stay paused with “Output unavailable. Choose an output to continue.” |
| Headphones disconnect / unexpected narration route change | Pause both before fallback audio is emitted. Revoke affected authorization. Show “Narration output changed. Choose where to continue.” Never automatically play on device speakers or a receiver. |
| Receiver lost | Pause both, retain position, show “Living Room TV disconnected.” Offer local playback and another output; require a new choice before audible playback. Receiver reappearance alone does not resume. |
| Temporary system interruption | Remember whether playing, pause both, checkpoint. Resume only on an appropriate system resume signal, unchanged authorized outputs, and no subsequent user pause. Otherwise show Resume. |
| Competing playlist / uncertain interruption end | Stay paused indefinitely until explicit Play. Release audio ownership when appropriate so other media can resume. |
| Background / lock / return | Apply decision 6. Reconcile live timeline on return; do not overwrite an advancing session with an old checkpoint. Resize/orientation alone changes no transport state. |
| End / exit | Stop both at the lesson boundary. Exit returns to lesson details with retained progress and Resume/Replay as appropriate. No automatic next receiver activation. |

Framework-agnostic coordinator sketch:

```text
onPlay(request):
    routes = adapter.observeActualRoutes()
    if !routes.verified or !authorized(narration, routes.narration):
        remainPaused(); presentOutputChoice(); return
    if routes.split and !adapter.verifiedSplitCapability:
        remainPaused(); offerLocalOrExplicitCombinedRoute(); return
    prepareBoth(savedLessonTime, selectedRate)
    when bothReady and authorizationStillValid:
        startBothUsingSharedLessonClock()

onRouteChangeUnexpected or onHeadphoneDisconnect:
    adapter.suppressNarrationBeforeAnyFallback()
    pauseBoth(); checkpoint(); invalidateAffectedAuthorization()
    presentOutputChoice()

onReturn:
    if adapter.hasLiveLessonSession:
        adoptObservedTimelineAndState()
    else:
        restoreCheckpointPaused()
    reconcileActualRoutesWithoutAutoConnecting()
```

The adapter must prevent fallback leakage, not merely update the UI after a route notification. If it cannot provide that guarantee, do not offer the affected routing mode. Use one lesson clock, map track offsets to it, and buffer/pause both when either track stalls. For this product, require video/narration position difference no greater than 100 ms during steady playback; beyond that, pause and realign before resuming. This is a proposed engineering acceptance target, not an Apple HIG threshold. Receiver latency and synchronization require measurement.

## Privacy and capability boundaries

No recording or microphone access is needed for prerecorded narration. Store only the lesson checkpoint/preferences needed for continuity; receiver identity and shared-output approval need only live-session storage. Do not treat route approval as a system privacy permission. If the actual implementation requires protected discovery/network access, request it when the person invokes external routing, explain its specific use, and preserve local playback after denial. Do not invent required Bluetooth/local-network permissions from the route label alone. This applies [Privacy — Best practices and Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission).

## Worked before/after

**Before, documented in the brief:** The last output was a living-room receiver. Starting a lesson silently sends private narration there, labels it “Bluetooth” regardless of transport, and returning from another app resets playback.

**After, illustrative scenario:** Open Lesson A with an illustrative retained position of 08:42. It stays paused and does not connect to the remembered TV. The player shows verified device outputs. The person selects headphones for narration and presses Play. They then select Living Room TV for video. If verified split routing is available, the chooser explicitly says video goes to the TV and narration stays in headphones; both restart at the captured lesson time. The labels report AirPlay for the TV only if confirmed. If split routing is unavailable, the person can cancel and keep local playback, or explicitly send both tracks to the named TV. While the authorized external session plays, switching to notes and returning shows its current advancing time instead of 00:00. If headphones disconnect, both tracks pause; narration does not fall through to speakers or the TV. Resume requires an output choice.

## Acceptance checks and evidence status

**Passed — document inspection:** The supplied platform and three reported defects are captured; this contract defines independent track intent, explicit shared narration authorization, honest transport labels, local fallback, and retained state. Installed root, selected families, topic procedures, and their supporting guides were read locally in that order. No web browsing was used.

**Failed — supplied existing design, as reported in `interface.md`:** narration consent/output privacy, transport labeling accuracy, and return-state preservation. These are brief-based findings, not reproduced runtime failures.

**Not executed — implementation acceptance suite:**

| Check | Pass condition |
| --- | --- |
| Remembered/shared receiver | Opening and first Play emit no narration on a shared receiver without the explicit named-output choice. Launch does not interrupt other media. |
| Split and combined paths | Verified split sends only video externally; unsupported split explains alternatives; combined playback requires explicit narration approval. No duplicate audio. |
| No receiver / denied access / cancel / timeout | Local lesson remains playable; time is retained; labels show confirmed state, with no fabricated Bluetooth transport. |
| Privacy on loss | Headphone removal and unexpected route changes emit no fallback narration. Receiver loss/reappearance does not trigger automatic local/shared audio. |
| Timeline | Play, pause, seek, rate, buffering, route change, and end keep both tracks aligned within the proposed target or pause to recover. |
| Continuity | App switch, lock, return, process recreation, and iPad resize preserve progress/context; eligible external playback continues; recreated sessions do not autoplay. |
| Interruptions | A signaled temporary interruption resumes only eligible playback; competing music and explicit Pause never auto-resume. Silent-mode deliberate playback works without changing system volume. |
| Controls | Relevant remote play/pause/seek affects the current lesson once; Space works in player context; unavailable capabilities are honest. |
| Media/viewing | Available captions, chapters, PiP, aspect handling, quick exit, portrait/landscape, enlarged text, and iPad narrow/wide layouts retain usable controls and route information. |

## Evidence limits

Only the brief and installed local HIG snapshot were inspected. Official links above identify the guides represented by that snapshot; they were not fetched or independently verified. The package describes its references as derived application guidance, not SDK documentation. No code, actual media, rendition inventory, screenshots, receiver, device, SDK, GUI, audio output, accessibility tooling, or background session was exercised. There is no evidence of split-route support, synchronization quality, permission requirements, remote control integration, native rendering, or assistive-technology behavior. The proposed checks remain pending; a written specification does not establish runtime compliance or platform availability.
