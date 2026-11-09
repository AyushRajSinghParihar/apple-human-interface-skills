# Revised lesson playback routing specification

## Scope and decisions

Target: iOS/iPadOS, optional AirPlay receivers, lesson video plus a separate private narration asset. This is a framework-agnostic interaction contract, not SDK code. `interface.md` supplies the observed design; it supplies no implementation, asset timings, minimum OS, or receiver inventory.

Treat video and narration as one lesson with one clock, play/pause state, seek position, and rate. A separate audio file is not evidence of independently selectable hardware outputs. Product decision: narration must never reach a shared receiver merely because it was used previously. Do not start output on launch or claim system media ownership until the user starts this lesson.

HIG supports respecting selected output, pausing on headphone removal, appropriate media/learning playback behavior, and preserving context. The stricter narration authorization rule, atomic routing transaction, and fallback policy below are product decisions addressing this brief, not claims that Apple prescribes these exact mechanisms. See [Playing audio — Best practices and interruptions](https://developer.apple.com/design/human-interface-guidelines/playing-audio#Best-practices).

## Outputs and controls

Show the video with familiar play/pause, timeline, elapsed/duration, and available captions. Keep the original aspect ratio; prefer standard player behavior if the eventual stack supports it. A custom player must provide equivalent familiar transport behavior. Space toggles playback when player context owns the command, not while typing. Exit returns to the containing lesson with its resume position. PiP is offered only if the implementation can preserve both tracks and the privacy contract. See [Playing video](https://developer.apple.com/design/human-interface-guidelines/playing-video).

Expose output selection beside transport controls. Prefer the standard output chooser; where available, use the system AirPlay control and its starting/playing/unavailable states. On iOS/iPadOS 16+, its player placement is lower right. Never use the noninteractive AirPlay compatibility artwork as a button. If the stack cannot provide a supported chooser or establish output safely, show local playback and an unavailable explanation rather than a decorative, nonfunctional AirPlay control. See [AirPlay — Best practices](https://developer.apple.com/design/human-interface-guidelines/airplay#Best-practices).

Always show confirmed route status, independently for each track when split:

- `Video: This iPad` / `Narration: Headphones — Bluetooth`.
- `Video: Living Room TV — AirPlay` / `Narration: This iPad speaker`.
- Pending: `Connecting to Living Room TV…`; do not label it connected yet.
- Unknown transport: use the confirmed destination name plus `Transport unknown`; never infer Bluetooth from “wireless,” destination history, or a user-supplied device name.

Use “This iPhone” on iPhone. Distinguish headphones, built-in speaker, AirPlay, Bluetooth, and wired output only when reported by the media adapter. No color-only route state is required to understand these text labels.

Opening the chooser does not itself transfer media. Cancel preserves the committed route, clock, and play state. Revalidate any selection before committing it.

## Routing policy

| Situation or selection | Required behavior |
| --- | --- |
| New lesson; last route was Living Room | Hold narration before rendering. Show actual current output and require a current choice. History never authorizes narration. |
| Local speaker selected | Explicit Play with `Narration: This iPad speaker` visible authorizes that speaker for this lesson session. The app does not call a speaker acoustically private. |
| Headphones selected | Use the confirmed headphones. Connecting them may smoothly reroute from a previously authorized local output. Loss of headphones pauses both tracks before any speaker fallback. |
| No receiver, discovery denied, or remote capability unavailable | Local playback remains available; show `No AirPlay destinations available` or the actual capability error. Never require a receiver to take the lesson. |
| User requests video on TV, narration here | Offer only when the adapter can guarantee independent video and narration destinations, synchronization, and isolation of all narration-bearing audio. Show both destinations before starting. |
| Independent routing unsupported or unknown | Explain `Separate video and narration outputs aren’t available. Keep both on this device, or send both to the selected destination.` Retain the existing route until a supported option is chosen. Never silently send narration with video. |
| User requests both tracks on a shared receiver | Require explicit action `Send video and narration to Living Room TV`, with `People near this receiver can hear the narration.` Selecting a generic video destination alone is insufficient authorization. This is an in-app media choice, not an OS permission prompt. |
| Receiver disappears, changes identity, or route changes without authorization | Pause both tracks, preserve time, invalidate affected authorization, show `Output changed. Choose where to continue.` No automatic speaker or remembered-receiver playback. |
| Same receiver selected again after disconnection or new session | Revalidate capability and obtain a fresh narration choice. Persisted receiver history is display convenience only. |

Do not promise split routing solely because AirPlay or separate audio assets exist. The adapter must account for embedded video audio, duplicate narration, receiver audio, and system-wide route coupling. If narration is embedded in video, use a verified narration-free rendition for video-only output; otherwise disable split routing. Never automatically mirror app screens containing private activity. Send only the selected lesson, keep unrelated previews local, and expose all available suitable stream renditions rather than artificially restricting receiver quality. See [AirPlay](https://developer.apple.com/design/human-interface-guidelines/airplay).

## Playback, lifecycle, and recovery

Maintain `lessonID`, asset revision, canonical lesson time, narration-to-video timing map, rate, selected captions, desired play state, committed route identities, route generation, and narration authorization scope. Separate *desired* state from actual `paused / preparing / playing / interrupted / blocked / ended`. Persist lesson progress locally during playback and on pause, seek, route change, and background transition; do not persist authorization to play private narration remotely across sessions.

For this lesson, use playback semantics: narration is essential, deliberate media; silent mode may permit user-started playback, mixing with sustained competing primary audio is disabled, and global system volume is never changed by the app. Support system volume/output controls. No recording, microphone capture, or call feature is required. See the [Playing audio category table](https://developer.apple.com/design/human-interface-guidelines/playing-audio#Best-practices).

| Event | Transition and retained context |
| --- | --- |
| Play | Validate outputs, authorization, timing map, and both tracks' readiness; start from the retained common time. Unknown output blocks narration and playback. |
| Pause / seek / rate change | Apply to both tracks as one operation. Seek while paused remains paused. Do not let one track continue while the other seeks or buffers. |
| Buffering or synchronization loss | Pause the pair at a common recoverable time; show waiting. Resume only if desired state is still playing, output remains authorized, and synchronization is restored. |
| App switch, local foreground-only lesson | Save state and pause at the same position. Return shows Resume; it never resets or automatically plays just because focus returns. |
| App switch or lock during explicitly selected AirPlay lesson | Continue the selected stream and its synchronized narration only if the adapter supports that background configuration and output remains authorized. Do not replace it with browsing clips or mirror private UI. If unsupported, explain before starting remote playback rather than promising uninterrupted streaming. |
| Supported active PiP | Keep the same lesson, clock, controls, and authorized outputs. Closing PiP preserves progress; return does not create another player. |
| Temporary system interruption | Pause both; remember whether playback was active. Resume only on an appropriate system resume signal, unchanged authorized outputs, no subsequent user pause, and continuing media ownership. Otherwise show Resume. |
| New music/podcast or other sustained primary audio | Pause indefinitely. Do not automatically resume over the user's new choice. |
| Remote play/pause/seek | Affect the same active lesson and canonical clock. Ignore stale commands or commands when another app owns media control; remote Play cannot bypass a blocked route. |
| Process recreation | Restore lesson/time/captions/rate and paused UI; discover actual routes again. Require fresh output validation and authorization before sound. |
| Lesson exit or completion | Save progress; release playback ownership when appropriate. Do not start another lesson or send incidental audio remotely. |

AirPlay continuation qualifies the general attention-dependent pause policy; a focus change is not an audio interruption. This distinction follows [Multitasking](https://developer.apple.com/design/human-interface-guidelines/multitasking) and [AirPlay](https://developer.apple.com/design/human-interface-guidelines/airplay). On iPad, resizing or another visible app must preserve lesson state; rotation or larger text must keep transport and route information usable. See [iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios) and [iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados).

## Adapter contract and pseudocode

The following names describe responsibilities, not Apple API availability. Route introspection alone is insufficient: an adapter must establish safe output before unmuting, including blocking automatic receiver reconnection. If it cannot enforce this, that routing mode is unavailable.

```text
onRouteRequest(plan):
    remember current intent and canonical time
    pause both tracks; hold narration before any output
    generation += 1
    token = generation
    validate plan capabilities and explicit narration authorization
    prepare tracks at canonical time without audible output
    establish outputs under the narration hold
    actual = confirm track destinations and transport identities
    if token != generation: discard stale completion; return
    if actual differs from authorized plan or isolation is unproven:
        stay blocked; show actual destinations and recovery choices; return
    commit actual route identities and token
    if intent == playing and media ownership still valid:
        start synchronized pair; release narration hold on authorized route only

onUnexpectedRouteChangeOrLoss():
    invalidate generation and affected narration authorization
    hold narration; pause pair; save canonical time
    show output-change recovery; require a supported current choice

onReturn():
    restore UI from retained lesson state
    reconcile actual playback and routes; never initialize time to zero
    never resume solely because foreground became active
```

Use the asset timing map for narration offsets; do not assume both files start at zero. The implementation must set measurable synchronization and seek tolerances after inspecting assets and backend capabilities; none are supplied here. Reject a mode that cannot meet those chosen tolerances rather than allowing narration to drift. Late connection callbacks must not override a newer destination selection or a Pause command.

Permission/data scope: lesson assets are playback inputs; progress is local restoration state; current route identity is used for routing and labels. No new route-history upload or microphone collection is authorized by this design. If the chosen implementation requires protected discovery access, request only the required permission when output selection is invoked, with an accurate purpose string; denial preserves local playback. Do not assume AirPlay universally requires an app-managed Bluetooth or local-network permission. See [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission).

## Worked before / after

**Before (from the brief):** The last used destination is a living-room receiver. Starting a lesson silently sends private narration there, the interface calls it “Bluetooth” regardless of actual transport, and returning from another app resets playback.

**After (illustrative trace, not an executed test):** At lesson entry the adapter reports `Living Room TV — AirPlay`, inherited from earlier use. Both tracks remain paused; narration is held. The learner chooses `This iPad` and presses Play while `Narration: This iPad speaker` is visible. At 03:12 they request TV video with narration in connected headphones. If independent routing is verified, the app pauses at 03:12, establishes `Video: Living Room TV — AirPlay` and `Narration: Headphones — Bluetooth`, then resumes both at that time. If unsupported, nothing transfers: the learner can keep both local or explicitly choose to send both to the TV after the narration disclosure.

While verified AirPlay playback continues, the learner switches to notes. Returning shows the same lesson at its actual advanced time, not 00:00. If headphones disconnect during that interval, both tracks pause at the last common position; neither TV nor speaker receives fallback narration. Returning shows the output-change explanation and retained time. Choosing a new authorized output and Resume continues there. With no receiver available, the same lesson works locally and app switching pauses without resetting.

## Acceptance checks and evidence limits

**Passed — specification inspection only:** the delivered contract covers all three reported defects, no-receiver operation, per-track output policy, unsupported split fallback, common-clock control, lifecycle preservation, route races, and explicit narration authorization. The installed root skill, relevant family routers, topic procedures, and supporting local guides were read in that order per route. The topic index was searched for audio, video, AirPlay, routing, and multitasking. No web access was used; official links above are attribution copied from local guidance.

**Failed — supplied design contract:** `interface.md` explicitly reports unauthorized remembered-receiver narration, incorrect transport labeling, and app-return reset. These are brief-level findings, not reproduced runtime failures.

**Not executed — implementation acceptance checks:**

1. With a previously used shared receiver, launching and opening a lesson emits no narration there. Selecting video-only does not authorize remote narration; cancel leaves committed state intact.
2. With no receiver, discovery failure, or permission denial, choose local output and complete play/pause/seek. No remote dependency blocks the lesson.
3. Exercise built-in speaker, wired headphones, Bluetooth, and AirPlay. Labels match confirmed transport and destination; unknown values are reported honestly. Disconnect headphones or a receiver and verify no audible fallback, including during background playback.
4. On supported split routing, verify both destination outputs physically, embedded-audio isolation, no duplicate narration, timing offsets, buffering, seek, rate change, and agreed sync tolerance. Unsupported split remains unavailable and never silently becomes combined remote audio.
5. Switch apps locally at 03:12: return paused at 03:12. Repeat with authorized AirPlay and lock: playback continues and returns at actual time. Browse other app areas: previews and private screens never replace the intended stream.
6. Pause during a pending connection; select another destination; deliver callbacks out of order. No stale callback resumes playback or commits an old route. Repeat with unexpected automatic reconnection before first audible sample.
7. Test silent mode, system volume, brief interruption with/without resume signal, sustained competing audio, and external commands. No global volume mutation, stolen playback ownership, or unauthorized resume occurs. Confirm no microphone access is requested.
8. Recreate the process and reopen the lesson: progress is restored paused, routes revalidated, and remote narration authorization renewed. Exit immediately after starting: return destination is coherent.
9. On iPhone portrait/landscape and iPad wide/narrow windows with larger text, verify usable transport and route information without state loss. Exercise touch, keyboard Space, captions when supplied, and supported PiP; unsupported capabilities are presented honestly. Check multiple video aspect ratios against the chosen player behavior.

Only local text was inspected and a specification was written. No device, receiver, SDK, GUI, media engine, accessibility technology, or runtime execution occurred. No claim of native rendering, accessibility conformance, successful transport isolation, real background execution, receiver quality, or compilation follows from this document. The installed references are derived HIG snapshots dated 2026-10-25, not an SDK contract or independently verified current Apple documentation. Asset inventory, precise timing tolerances, minimum OS, platform-adapter feasibility, permission requirements, and hardware behavior remain implementation evidence gaps; unsupported routes must remain disabled until validated.
