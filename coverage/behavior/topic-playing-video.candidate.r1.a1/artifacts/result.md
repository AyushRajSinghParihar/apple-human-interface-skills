# iPad lecture reader: revised playback interaction specification

This replaces the behavior described in `interface.md`. It specifies interactions, not an SDK implementation. The only product evidence is that short brief; duration, media format, implementation, caption availability, and PiP capability are unknown. Assume an on-demand lecture with a seekable timeline when its duration is known.

## Decisions and source basis

1. Open the lecture silently in Ready, at its saved playback time, with Play visible. Do not autoplay on entry, return, resize, or lecture completion. This is a product decision to fix unexpected loud playback, informed by [Accessibility — Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive). Deliberately played lecture audio is essential media: use playback-like audio behavior, respect the selected output and system volume, and never raise global volume. Silent mode need not suppress deliberately initiated lecture audio. See [Playing audio — Best practices](https://developer.apple.com/design/human-interface-guidelines/playing-audio#Best-practices).
2. Prefer a system player when the chosen environment supplies one; otherwise reproduce familiar transport behavior through a capability adapter. No Apple SDK is assumed. Keep captions, controls, and useful metadata from obscuring one another; preserve original aspect ratio without baked-in bars. For lecture slides, choose aspect-fit to preserve all slide text (a product choice). The local video source describes overlapping defaults at exactly 2:1; do not invent an exclusive rule there. See [Playing video — Best practices](https://developer.apple.com/design/human-interface-guidelines/playing-video#Best-practices).
3. Separate media time from transcript reading position. Seeking never silently scrolls the transcript. Preserve both across exits, interruptions, and resizing. This applies [Multitasking — Best practices and iPadOS](https://developer.apple.com/design/human-interface-guidelines/multitasking#iPadOS) to the reader's task.
4. Represent loading, buffering, pause, interruption, and failure distinctly. Keep available transcript content usable while media waits. Use text plus an indeterminate activity indication when the wait duration is unknown; never invent a percentage or ETA. See [Loading — Showing progress](https://developer.apple.com/design/human-interface-guidelines/loading#Showing-progress).
5. Captions convey synchronized audible information; a transcript remains a separate reading resource, not a substitute for captions. Preserve caption preferences, expose unavailable tracks honestly, and support text enlargement. See [Accessibility — Hearing and Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Hearing).

## State and persistence contract

Use orthogonal state so a single “paused” flag cannot hide a stall:

```text
intent = stopped | play
transport = ready | loading | playing | paused | buffering |
            seeking | interrupted | ended | error
presentation = inline | pipStarting | pip | pipReturning
confirmedTime, duration?, pendingSeek?, requestGeneration
reader = {segmentId, offsetWithinSegment, selection, follow: off|on}
preferences = {captionTrack, captionStyle, playbackRate}
interruption = {reason, wasPlaying, resumePermitted}
```

Save lecture ID, confirmed media time, reader anchor/selection, and preferences on pause, committed seek, exit, and lifecycle loss; checkpoint confirmed time during playback. Never persist an unconfirmed seek as the resume time. On reopening, restore the reader anchor independently and enter Ready, even if the last session was playing. If an anchor's segment is missing, restore the nearest preceding available segment and explain the fallback. If duration changed, clamp resume time to the new duration and show the adjusted time. A completed lecture opens Ended with Replay, without starting another lecture.

Only actual media-clock advancement establishes Playing. `intent=play` alone does not. Status labels are persistent while applicable and do not depend on color or animation. Last frame/poster stays visible during waits; never present frozen media as successful playback.

| Event / current condition | Result and visible interaction |
|---|---|
| Open lecture | Ready, “Play” (or “Resume” with saved time); transcript immediately usable if available. Fetch metadata/initial media independently; do not download the entire lecture before enabling playback. |
| Play / Ready or Paused | Set intent=play. If data is ready, request playback; otherwise Loading with “Loading video…” and a Pause action that cancels play intent. |
| Clock advances / intent=play | Playing; Pause is the main transport action. |
| Data starvation / intent=play | Buffering; show “Buffering…” and activity feedback in the media status area, with Pause available. Preserve confirmed time and reader anchor. |
| Pause / Playing, Loading, Buffering | Set intent=stopped; halt output and enter Paused. Show “Paused” and Play. Later readiness cannot restart it. |
| Data ready / Buffering or Loading | Resume only if intent is still play and no interruption/error blocks it; otherwise remain Paused. |
| Begin scrub | Capture confirmed time, intent, and reader anchor; suspend output; enter Seeking. Preview candidate time without committing reader movement. |
| Commit scrub | Clamp target to [0,duration]; issue one seek with a new generation. Show “Seeking to mm:ss…” until confirmed. On confirmation update confirmedTime; restore captured intent unless the person paused or an interruption intervened. Wait for data if needed. |
| Cancel scrub / Escape or visible Cancel Seek | Restore prior confirmed time and captured intent, subject to later pause/interruption; reader stays at its original anchor. |
| Seek failure | Error with “Couldn’t seek. Retry” and last confirmed time retained. Intent becomes stopped. Retry repeats the target, then returns paused; Play remains a separate choice. |
| Media/network failure | Error, “Video unavailable” with contextual reason when known, Retry, and preserved transcript. Clear play intent. Retry enters Loading, suppresses duplicate requests, and returns Ready/Paused on success. Never leave a permanent spinner after a reported failure. |
| No readiness or progress for 15 seconds | Offer “Still waiting for video” with Retry and Stop Waiting. This is a proposed product timeout, not an Apple requirement. Stop Waiting preserves context and pauses; no false offline claim. |
| Media reaches end | Ended, intent=stopped; Replay seeks to zero and plays only on activation. Keep transcript anchor. |
| Leave reader / Back | Pause unless confirmed PiP owns playback. Save state and return to the containing lecture/course context; rapid exit during loading must work. |

On any new lecture, retry, or seek, invalidate obsolete asynchronous completions. Apply callbacks only to their lecture ID and generation. A late callback must never undo Pause, select an old lecture, move the reader, or restart sound. When a temporary interruption arrives during seeking, its pause policy overrides the captured scrub intent.

## Reader, captions, and controls

The default transcript mode is independent reading (`follow=off`). Playback may mark the current spoken segment without scrolling or moving focus. “Follow Playback” explicitly scrolls to the current segment and enables following; manual transcript scrolling switches it off. “Return to Reading Position” restores the anchor saved when following began and turns following off. A timestamp action seeks media to that segment; it does not change the transcript viewport. PiP time updates obey the same rule.

In a wide window, show video and transcript together. In a narrow window, stack them in one reader flow, keeping a persistent compact transport area. Resizing or orientation changes retain time, pending state, reader anchor, selection, and caption preferences. Choose arrangement from available space rather than inferring the user's multitasking configuration. See [Designing for iPadOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados#Best-practices).

Reserve a caption region clear of the control and status regions. Controls and buffering/error messages must never cover caption glyphs, including at 200% text size and narrow widths. Reflow the player/controls or move controls below the video when space is insufficient; do not shrink captions to fit. Fit the video without cropping slide edges. Captions track confirmed presentation time; do not advance them with a scrub preview. If a requested track is absent, show “Captions unavailable” and retain the saved preference for future lectures. Preserve system caption preferences where the environment exposes them; an adapter must report its actual capabilities.

| Control | Contract |
|---|---|
| Play / Pause / Replay | One prominent transport button; its name states the action, while a separate status states reality. During delayed initial Play, retain its context and show activity with “Loading”; Pause remains operable. |
| Timeline | Labeled “Playback position”, linear 0–duration, increasing from leading to trailing edge; expose current and preview mm:ss (hh:mm:ss when needed). Disable seeking with “Seeking unavailable” until bounds/capability are known. |
| Back 10 Seconds / Forward 10 Seconds | Visible alternatives to precision dragging; clamp to bounds. Keyboard/assistive timeline increments are 1 second. These intervals are product choices. |
| Follow Playback / Return to Reading Position | Explicit reading actions as specified above; no hidden gesture required. |
| Retry / Stop Waiting | Retry only the failed media operation; activity feedback while pending. Stop Waiting clears intent and pending work without resetting reading context. |
| Picture in Picture | Offer only when capability is reported. Starting is pending until confirmed; failure returns inline with an explanation and the same time/intent. |

Use at least 44 × 44 pt nonoverlapping activation regions for these iPad controls, with clear separation, press feedback, and visible keyboard focus. Icon controls require action names. This adopts the default iPad control size rather than the smaller accessibility minimum; see [Buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices) and [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility). Timeline quantity and endpoint behavior follow [Sliders — Best practices](https://developer.apple.com/design/human-interface-guidelines/sliders#Best-practices).

Touch and pointer activate the same visible actions; hover is never required. With playback context active and focus outside editable text, Space toggles playback; do not intercept Space for transcript text editing or system accessibility commands. All actions must be reachable by keyboard and assistive input. Expose status text, action names, enabled/pending states, and timeline role/range/value; announce state changes without announcing every clock tick. Keep controls available while focused rather than timing them out. Use static text feedback instead of relying on spinner motion, honor Reduce Motion and exposed flashing-light preferences, and evaluate actual light/dark contrast at implementation time.

## PiP, audio, and lifecycle matrix

PiP is a presentation of the same playback session, not a second player. There must be one clock, one intent, and one audio output. In inline mode while PiP is active, show “Playing in Picture in Picture” (or the actual paused/buffering status), retain the transcript, and offer Return to Reader.

| Event | Policy |
|---|---|
| PiP confirmed | Preserve time, intent, rate, captions and reader anchor. Transfer rendering/control ownership without restarting audio. |
| PiP rejected/unsupported | Remain inline. Do not advertise an active PiP session or pause solely because a request failed. |
| Restore from PiP | Restore the same lecture and transcript anchor, preserving current time and play/pause state; confirm inline attachment before relinquishing PiP. |
| PiP closed without restore | Pause and save; do not start a hidden inline player. Return later in Paused. |
| App loses focus / reader still visible | No blanket pause for focus change alone; preserve context. |
| App backgrounds without active PiP | Product policy: pause this attention-dependent lecture and save; foregrounding stays paused. |
| App backgrounds with confirmed PiP | Continue the existing session where supported; suspension or capability failure must save state and pause honestly. |
| Temporary audio interruption | Record whether actually playing, pause, show “Playback interrupted”. Resume only if the environment explicitly permits it, it was playing, and no later user pause/exit/route loss occurred. Otherwise offer Play. |
| Sustained competing media | Pause indefinitely; require explicit Play. Do not reclaim another app's external controls. |
| Headphones disconnect | Pause immediately, clear resume eligibility, preserve time. Do not automatically continue through speakers. Connecting a new output does not itself start playback. |
| Output selection/volume | Respect chosen route and volume; use an available system output/volume surface rather than rebuilding or raising global volume. External commands affect only the relevant active lecture session. |

These policies apply [Playing audio — Handling interruptions](https://developer.apple.com/design/human-interface-guidelines/playing-audio#Handling-interruptions) and [Multitasking — iPadOS](https://developer.apple.com/design/human-interface-guidelines/multitasking#iPadOS). PiP availability, captions in PiP, lifecycle signals, and background permissions require implementation verification. Do not claim them from the platform name alone.

## Worked before/after

Illustrative trace, not an executed session: the lecture's saved video time is 12:30 and the reader is at transcript segment 88, scrolled independently to 18:10.

**Before (brief's behaviors):** Opening starts loud playback. Revealed controls cover captions. Scrubbing to 25:00 discards the reader's place. A network stall appears paused, leaving the reader unsure whether Play is required. PiP is mentioned, but its state transfer is unspecified.

**After:** Opening restores 12:30 silently with Play and keeps segment 88 at its saved offset. Play uses the chosen output and existing volume. Controls occupy a region clear of captions. Dragging previews 25:00 while the transcript stays at segment 88; committing seeks once. Data starvation displays “Buffering…” with Pause available. Pressing Pause before recovery clears play intent, so restored data leaves the lecture paused at 25:00. A later explicit Play resumes. Entering supported PiP transfers that session; restoring the reader returns the same transcript anchor and the current media time, with no second audio stream. Follow Playback remains an explicit choice.

## Acceptance checks and current evidence

**Passed — static specification inspection:** Every defect stated in `interface.md` has a correction and observable check below. The specification separates intent/readiness, retains independent reading state, defines pending/error recovery, and covers PiP entry/return/failure. Installed root, selected family procedures, routed topic procedures, and corresponding local guides were read. No web sources were fetched.

**Failed — supplied behavior against the revised contract:** The brief reports loud autoplay, caption obstruction, lost transcript position after scrubbing, and stalls that resemble pause. These are reported baseline failures, not reproduced runtime findings. No implementation was supplied to verify a fix.

**Not executed — acceptance scenarios for a future implementation:**

| Check | Pass condition |
|---|---|
| Entry/resume/quick exit | Open new, partially watched and completed lectures; all remain silent with correct time and reader anchor. Exit immediately during loading returns to the course context and late callbacks cannot play. |
| Loading/partial success | Slow or offline video leaves cached transcript usable; unknown progress has no invented percentage. Timeout exposes recovery, failure resolves pending UI, and Retry neither duplicates work nor autoplays. |
| Buffering vs pause | Starve data while playing: Buffering appears. Pause then restore data: remains paused. Restore without Pause: resumes only with retained intent. |
| Seeking | Test 0, midpoint, end, unknown duration, rapid repeated seeks, cancellation, and failed seek. Applied/displayed times agree after confirmation; obsolete callbacks are ignored; transcript anchor and selection remain unchanged. |
| Reading | Follow Playback scrolls only by explicit choice; manual scroll stops following; Return to Reading Position restores the saved anchor. Timestamp activation seeks without stealing reading focus. |
| Captions/aspect | Reveal all controls and all statuses over varied lecture aspect ratios. No caption overlap, cropped slide text, or baked-in bars; caption timing follows confirmed media, not preview. Test absent tracks and retained preferences. |
| Resize/text/access | Wide/narrow, rotation, and 200% text retain content and usable controls. Measure 44 pt targets and actual contrast in light/dark and Increase Contrast. Verify touch, pointer, keyboard, VoiceOver, Switch Control, Full Keyboard Access and AssistiveTouch through the complete task. |
| PiP | Test supported, unavailable, start failure, pause/stall in PiP, restore and close. One session/audio stream; time, caption settings and reader anchor retained; closing pauses without hidden playback. |
| Audio/lifecycle | Test silent mode with deliberate Play, system volume preservation, output change, headphone disconnect, temporary interruption with/without resume permission, competing audio, app switch, background and return. No unintended speaker playback or unauthorized resume. |
| Preferences | Reduce Motion keeps status intelligible; caption styling and exposed flashing-light preferences are honored without losing content or controls. |

## Evidence limits

This is a concrete proposed contract based only on `interface.md` and the installed independent HIG package's dated local guidance (2026-10-25). Official links identify the guide sections underlying decisions; they were not browsed or checked for updates. Local files do not establish independent source review. Product choices such as no autoplay, a 15-second recovery threshold, independent transcript anchoring, and skip intervals are explicitly design decisions, not universal Apple rules.

No code, media assets, screenshot, playback engine, SDK, GUI, device, accessibility execution, timing measurement, contrast calculation, or target measurement was available or performed. No claim of native rendering, compilation, audio routing, caption accuracy, physical comfort, PiP support, or accessibility conformance follows from this document. Runtime and device checks above remain open; the work completed here is specification and static trace review.
