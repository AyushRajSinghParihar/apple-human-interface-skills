---
name: apple-hig-shazamkit
description: Use when designing or reviewing audio recognition with Shazam or custom catalogs, microphone sampling, recognition-driven content, or opt-in library addition.
---

# Recognize the needed sample without unnecessary recording

Read [ShazamKit](../../references/shazamkit.md). Inspect the recognition task, Shazam versus custom catalog, microphone lifecycle, result use, and requested design/review/adaptation. Preserve the existing audio stack and verify current API availability for the target platform; this overview adds no platform-specific rules.

Choose the recognition result that actually serves the task: identifying a song, aligning accessible captions/sign language, or revealing contextual learning content are different outcomes. Define what the app does with a match and what it shows when no useful match exists. Those result/retry states are application engineering choices, not a claim that every catalog guarantees a match.

Explain and request microphone access before recording. Bound the recording session to the needed recognition sample and stop as soon as it has been captured; continuous recording after a result needs a separate justified task, not inertia. Keep recording status and its result understandable. If recognized songs can be added to the person's iCloud library, obtain opt-in first even when Music Recognition/Shazam identifies the originating app. Recognition is not consent to modify the library.

**Before → decision → after:** A music-history app starts listening silently on launch, keeps recording after identifying a track, and automatically adds every match to the library. Decision: recognition and saving are separate intents. After, an explicit recognition action explains microphone use, sampling stops when sufficient, the result shows the identified track, and a separate opt-in controls library addition.

Deliver the permission/sample/result/library-action contract or implementation. Fail if recording starts before required access, continues after the needed sample without purpose, or recognition changes the library without opt-in. Test actual microphone start/stop and catalog matching where supported; static flow review cannot establish recognition accuracy, synchronized accessibility content, or iCloud library behavior.

Use [Privacy](../../../apple-hig-foundations/.topics/apple-hig-privacy/SKILL.md) for recording explanations and [Accessibility](../../../apple-hig-foundations/.topics/apple-hig-accessibility/SKILL.md) when recognition drives captions/sign-language alternatives.
