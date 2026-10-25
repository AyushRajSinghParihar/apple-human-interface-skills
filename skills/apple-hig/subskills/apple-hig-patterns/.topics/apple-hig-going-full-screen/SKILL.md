---
name: apple-hig-going-full-screen
description: Use when creating, reviewing, or adapting fullscreen entry, hidden controls, system access, and continuity after leaving.
---

# Let immersion remain under the person's control

Read [the fullscreen guide](../../references/going-full-screen.md). This workflow is application advice; fullscreen is not the same as modality or visionOS immersion.

Inspect the task, essential controls, playback/time sensitivity, entry/exit, platform, and create/review/adapt request. Record hidden/restored states and position retention; a fullscreen screenshot cannot prove access to system gestures.

Offer fullscreen only when it serves concentration/media/play. Adapt subtly without replacing the interface or programmatically resizing the window. Keep necessary actions visible/easily revealed, preserve normal system access, and let the person choose when to exit rather than automatically leaving after playback/app switch. Pause time-sensitive content on departure and restore position. On iOS/iPadOS retain ordinary Home behavior unless a game justifies first-gesture deferral. On Mac use standard controls/commands/shortcut and camera-housing support; do not change display modes automatically. TV/watch already fill displays and visionOS has different immersion/window mechanisms, so do not claim this distinct mode there.

Implement entry/reveal/leave/return behavior, provide an immersion-state specification, or review concrete trapped-access and continuity defects. Decide modal blocking separately using the modality topic.

**Worked transformation:** Before: a lecture player exits fullscreen at every pause, hides its exit permanently, and restarts playback after app switching. Decision: the system is overriding viewing intent and losing position. After: preserve fullscreen until explicitly changed, reveal controls through a familiar gesture, pause on departure, and restore the same playback location.

Deliver the artifact and entry, hidden/revealed chrome, system access, and return contract. Verify media end, app switch, pause, control reveal, and explicit exit. Fail for trapped navigation, forced exit, lost position, or unsupported display-mode claims. Native gestures/window controls and actual media continuity need runtime/device evidence.

Load [status-bars](../../../apple-hig-system-experiences/.topics/apple-hig-status-bars/SKILL.md), [playing-video](../apple-hig-playing-video/SKILL.md), or [modality](../apple-hig-modality/SKILL.md) as required.
