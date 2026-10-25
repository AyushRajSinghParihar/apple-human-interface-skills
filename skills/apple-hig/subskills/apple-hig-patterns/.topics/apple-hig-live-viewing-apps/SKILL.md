---
name: apple-hig-live-viewing-apps
description: Use when creating, reviewing, or adapting live-channel playback, electronic guides, channel browsing, and cloud-DVR tasks.
---

# Keep live playback primary while people browse

Read [the live-viewing guide](../../references/live-viewing-apps.md). This workflow is application advice; source recommendations do not establish streaming or recording capability in an unseen app.

Inspect launch-to-play route, live/on-demand labels, channels/program schedule, browsing audio, DVR support, platform, and create/review/adapt request. Obtain actual stream/recording states; do not infer live status from a red dot or claim measured startup delay without timing.

Prioritize relevant live content with zero/one prominent Watch activation where appropriate, removing that affordance during playback. Distinguish live channels consistently from recordings/on-demand. Keep secondary actions ordered consistently and only offer supported restart/record/download operations. A browsing footer should preserve playback, identify current program, share guide categories, and have predictable opposite reveal/dismiss gestures. Give immediate channel-change feedback while the stream resolves. In-context audio follows playing content, but leaving the live tab stops it. The guide should expose current time/channel/program and efficient return to playback, with favorites and suitable PiP/background continuity.

Implement the viewing/guide state model, specify playback/browse/record routes, or review exact loss-of-live-context defects. DVR workflows need clear current/future scope, recorded-item actions, and storage policy before capacity is exhausted.

**Worked transformation:** Before: a TV app keeps Watch over playing video, plays old channel audio after leaving Live, and labels recorded episodes Live. Decision: controls and status misrepresent current playback. After: replace Watch with appropriate playback actions, stop live audio on tab exit, and distinguish recordings while preserving guide-to-current-channel return.

Deliver the artifact, launch/play/browse/audio/record contract. Verify channel transitions, guide navigation, live-tab exit, recording scope, and storage limits. Fail for wrong-stream feedback, false live identity, or recordings silently lost by an undisclosed policy. The source adds no separate platform rules; native remote, PiP, streaming, and DVR execution need evidence.

Load [playing-video](../apple-hig-playing-video/SKILL.md), [tab-bars](../../../apple-hig-navigation-and-search/.topics/apple-hig-tab-bars/SKILL.md), or [top-shelf](../../../apple-hig-system-experiences/.topics/apple-hig-top-shelf/SKILL.md) for related entry/playback work.
