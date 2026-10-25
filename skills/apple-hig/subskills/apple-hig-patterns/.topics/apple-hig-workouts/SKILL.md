---
name: apple-hig-workouts
description: Use when creating, reviewing, or adapting activity-data workout sessions, moving-user metrics, session controls, sensor limitations, and summaries.
---

# Keep the active session about the activity

Read [the workout guide](../../references/workouts.md). This workflow is application advice; activity-session guidance targets iOS/iPadOS/watchOS, distinct from fitness media on larger stationary devices.

Inspect workout type, real sensor/metric sources, session lifecycle, moving-user controls, platform, and create/review/adapt request. Identify supported metrics and limitations for this activity rather than copying a swimming caveat onto every workout. Do not invent heart-rate/GPS availability or recorded accuracy.

Keep useful changing progress prominent with large high-contrast metrics and easy pause/resume/end targets. On watch retain relevant session visibility and separate controls, metrics, and Now Playing appropriately; keep unrelated navigation out. Explain concrete sensor limits and any estimate semantics without hiding useful remaining data. Communicate start/stop, summarize what was actually recorded, and resolve sessions ended after only a few seconds through discard/save confirmation. Optional Activity rings preserve defined measures/rendering rather than branding session goals as system rings.

Implement session/control/metric states, provide a lifecycle and sensor-availability specification, or review exact accidental-end, false-metric, and summary defects. Do not claim this session pattern exists on Mac/TV/visionOS merely because classes can play there.

**Worked transformation:** Before: a pool-swim app displays fabricated GPS distance and a frozen heart-rate value as live, with tiny adjacent Pause/End targets. Decision: sensor limits and moving input make both metrics and control safety misleading. After: explain pool/GPS and water/heart-rate limitations, show supported lap/distance estimates truthfully, and separate easily targeted session controls.

Deliver the artifact, session transitions, metric provenance/availability, and saved/discarded summary. Verify start/pause/resume/end, brief accidental session, missing sensor, and wrist-return state. Fail for fabricated live values, ambiguous recording state, accidental irreversible end, or false saved summary. Physical exercise, sensors, health recording, and wrist readability need actual device evidence.

Load [activity-rings](../../../apple-hig-status/.topics/apple-hig-activity-rings/SKILL.md), [healthkit](../../../apple-hig-technologies/.topics/apple-hig-healthkit/SKILL.md), or [playing-audio](../apple-hig-playing-audio/SKILL.md) for daily context, health data, or session audio.
