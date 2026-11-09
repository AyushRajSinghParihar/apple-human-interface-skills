# Revision result

Patched `interface.md` in place from the supplied one-paragraph brief into an implementable interaction and state specification for iPadOS and visionOS.

## Decisions and patch summary

The observed defects are stated in the brief: all feeds start with loud audio, camera location is hidden, and disconnected footage freezes while retaining Live. The revision replaces these with deliberate Watch entry, one primary camera, optional two-camera comparison, visible camera/location metadata, explicit audio ownership, and per-camera connection states. It defines switching, cancellation, late-response rejection, retries, pause/resume, leaving playback, and independent comparison failures.

visionOS uses a modest Shared Space window with deliberate playback and resting indirect interaction. iPadOS adapts camera choices and comparison to window size while retaining state. Standard controls, platform target sizes, accessible names, text reflow, and non-color status are requirements for the later implementation.

HIG supports playback priority, truthful identity, user control of sound, system players, adaptable layout, and comfortable spatial interaction. Muted Watch, a two-stream ceiling, five-second watchdog, retry schedule, and stopping playback on exit are explicit product choices. They are not claimed as universal Apple rules. No DVR, synchronized capture, PiP, immersive media, or background-streaming capability is inferred. Official source links and their decision mappings are in interface.md; they refer to local snapshot attribution, not browsing.

## Worked before/after

Example fixture names and times below are illustrative, not observed service data.

Before: opening the experience starts Riverbank, Nest, and Clearing together, with competing sound. The viewer cannot locate the selected camera. Riverbank disconnects at 14:03:10; its still image continues to say Live.

After: opening displays static Preview cards and selects Riverbank without playing. Watch Riverbank opens one muted stream and displays “Riverbank — North hide.” Enable Audio makes only Riverbank audible. Compare Cameras → Compare with Nest opens a second muted stream with its own identity and status; Clearing never starts. Riverbank disconnects at 14:03:10: a reported error immediately removes Live, silences Riverbank, and labels its dimmed image “Connection interrupted — last frame received 14:03:10.” If there is no error signal, the proposed arrival watchdog detects the stall after five seconds. Nest continues. Reconnection attempts show their state and eventually offer Retry if unsuccessful. Fresh Riverbank playback remains muted and regains Live only after freshness validation. If that validation is unavailable, it says “Playing — live status unverified.” End Comparison releases Nest without changing the primary camera.

## Acceptance checks

Static specification review passed: all three reported failures have explicit replacement behavior, and both target platforms have a presentation/input contract. This establishes document coverage only.

| Implementation acceptance scenario | Required result | Execution status |
| --- | --- | --- |
| Cold launch, then Watch | Zero streams before Watch, one muted stream afterward; visible matching location/status | Not executed |
| Compare, swap primary, end comparison | At most two streams; at most one audible source; swap mutes; ending comparison releases secondary | Not executed |
| Rapid camera changes with late network responses | Selection, media and metadata always share camera ID; obsolete responses discarded | Not executed |
| Inject disconnect; separately stop decoded-frame delivery | Immediate error handling or proposed 5-second watchdog; no stale Live cue; timestamp explicitly means frame receipt | Not executed |
| Exhaust reconnect attempts, then Retry | Bounded recovery ends in Unavailable; Retry affects only failed camera and stays muted | Not executed |
| Stationary scene; missing freshness metadata | Unchanged pixels alone do not trigger stall; unverified freshness never gets Live | Not executed |
| Pause/resume and leave/return | Paused is never Live; resume connects to current edge; exit stops streams/audio and retains selection | Not executed |
| Missing location/audio/captions | Explicit unavailable labels; no invented location, track, or animal description | Not executed |
| Headphone loss, interruption, competing media | No speaker spill, global-volume change, stolen media commands, or unintended resume | Not executed |
| iPad resize and 200% text, narrow/wide comparison | Selection and state persist; essential labels/actions remain reachable without overlap | Not executed |
| Keyboard, assistive input, light/dark and Increase Contrast | Named actions reachable; no unexpected focus movement; measured readable contrast | Not executed |
| Vision Pro worn, seated/standing, indirect input and Pointer Control | User-started windowed playback; resting activation; distinct targets; comfortable comparison without repeated turns | Not executed |

Failed checks: none observed in specification review. This is not evidence that implementation checks pass.

## Evidence and limits

Read the installed apple-hig root SKILL.md explicitly, then routed through Getting started → iPadOS/visionOS; Patterns → Live-viewing apps, Playing video, Playing audio, Loading; Foundations → Accessibility, Layout, Spatial layout; Menus and actions → Buttons. Each selected topic procedure was read before its supporting source guide. The complete topic index was searched for platform, audio/video, camera, live-viewing, loading, accessibility and button concepts. All reads used one local file per command. Installed paths resolve under `.agents/skills/apple-hig/`; no web browsing was used.

Evidence consists of the original interface.md and installed guidance. There was no source implementation, player configuration, stream telemetry, screenshot, runtime, or device measurement. The before/after is a worked design walkthrough. No build, SDK verification, native rendering, GUI, actual audio routing, accessibility execution, contrast measurement, latency timing, or worn-device comfort testing was performed. Freshness metadata availability and service cadence remain integration questions; if the provider cannot establish freshness, the specified conservative label must remain. Acceptance scenarios above are pending implementation tests, not test results.
