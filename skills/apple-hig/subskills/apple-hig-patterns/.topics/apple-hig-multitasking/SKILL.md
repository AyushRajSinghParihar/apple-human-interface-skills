---
name: apple-hig-multitasking
description: Use when creating, reviewing, or adapting task continuity, background work, window focus, media interruptions, and simultaneous app use.
---

# Treat focus changes as continuity decisions

Read [the multitasking guide](../../references/multitasking.md). This workflow is application advice; do not collapse its visionOS media exception into a universal pause rule.

Inspect attention-dependent work, input-free background tasks, audio/video, saved state, target platform, and create/review/adapt request. Distinguish losing app activity, window focus, closing a window, and receiving an audio interruption. Record actual lifecycle handlers and completion sources.

Preserve context and finish eligible user-initiated input-free tasks before suspension. Notify only for important completion requiring another timely step; routine results can appear on return. Pause attention-dependent gameplay/media when appropriate, distinguishing sustained competing audio from brief directions and restoring only as justified. On iPad adapt to size without assuming access to the user's multitasking configuration. On Mac retain system key/main/layering cues. In visionOS looking at another window should not stop video merely because attention shifts; closing a Now Playing window pauses it, while closing a window backgrounds rather than quits the app. Shared Space and Full Space differ. The source does not define this mode on watchOS.

Implement lifecycle/resumption behavior or provide event-to-preservation/media/background-task contracts; reviews identify the exact event that loses work or wrongly stops/continues activity.

**Worked transformation:** Before: a spatial lecture pauses whenever someone looks at notes, while an unsent annotation disappears after closing its window. Decision: attention shift is not departure from video, and window closure is not app termination. After: let video continue on the documented focus change, preserve annotation state, and treat explicit Now Playing closure separately.

Deliver the artifact and lifecycle/event matrix with retained state and completion routes. Verify app switch, resize, competing audio, window close/reopen, and return. Fail for lost work, indiscriminate media pause/resume, or routine background completion spam. Native PiP/audio/lifecycle behavior and real background execution need runtime evidence.

Load [windows](../../../apple-hig-presentation/.topics/apple-hig-windows/SKILL.md), [playing-audio](../apple-hig-playing-audio/SKILL.md), or [playing-video](../apple-hig-playing-video/SKILL.md) for detailed handling.
