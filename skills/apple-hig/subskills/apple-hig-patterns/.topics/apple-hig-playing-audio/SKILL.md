---
name: apple-hig-playing-audio
description: Use when creating, reviewing, or adapting audio sessions, output routes, silence, interruptions, media controls, and spatial sound behavior.
---

# Respect the output and interruption the person chose

Read [the audio guide](../../references/playing-audio.md), including the audio-category table. This workflow is application advice; do not infer playback or microphone behavior from UI alone.

Inspect essential/incidental audio purpose, playback/recording state, route/category configuration, interruptions, platform, and create/review/adapt request. Distinguish deliberate media from incidental feedback and sustained competing playback from resumable interruption.

Choose the category matching silence/mixing/background needs rather than globally raising volume. Respect output selection; reroute smoothly on connection and pause on headphone disconnection for privacy. Expose supported output/volume controls and respond to external playback commands only in a relevant context without stealing another app's controls. Specify interruption resume based on actual system signals/user intent; a new playlist is not a brief ducking event. Recording/call policy needs explicit handling, including not automatically unmuting a VoIP session after a closed-folio microphone interruption. On TV do not add automatic notification sounds. In visionOS complement essential spatial cues visually, preserve native control sounds, and distinguish Now Playing window closure from attention ducking. Watch short/long playback and system Now Playing have their own supported behavior.

Implement the session/route/interruption contract, produce it as a state specification, or review exact privacy/coexistence defects. Keep category facts in the reference, not duplicated tables.

**Worked transformation:** Before: a meditation app sets global volume, resumes over a newly chosen music playlist, and plays through speakers after headphones disconnect. Decision: it overrides three user choices. After: adjust only relative mix, pause for route loss, and resume only for appropriate signaled interruptions rather than unrelated playback.

Deliver the artifact and category, route, external-control, interruption/resume contract. Verify silent mode, competing audio, headphone disconnect, temporary interruption, and recording/privacy states. Fail for unintended speaker playback, global volume changes, or unauthorized automatic resume. Actual audio routing, microphones, sound comfort, and hardware behavior need device tests.

Load [multitasking](../apple-hig-multitasking/SKILL.md), [playing-video](../apple-hig-playing-video/SKILL.md), or [feedback](../apple-hig-feedback/SKILL.md) for related lifecycle and cue decisions.
