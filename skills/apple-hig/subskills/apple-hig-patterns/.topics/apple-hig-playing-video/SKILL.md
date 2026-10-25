---
name: apple-hig-playing-video
description: Use when creating, reviewing, or adapting video playback controls, aspect behavior, TV-app handoff, exit context, and spatial or watch presentation.
---

# Preserve playback intent across entry and exit

Read [the video guide](../../references/playing-video.md). This workflow is application advice; the source's overlapping 2:1 aspect endpoint must not become an invented exclusive rule.

Inspect content aspect/duration, controls, resume state, entry/exit destinations, platform, and create/review/adapt request. Identify system-player use versus a justified custom need. Record real transport/keyboard/remote behavior; a poster or mock control does not prove playback support.

Prefer system players and preserve original aspect without baked-in bars. Use system aspect behavior at the source's ambiguous boundary. Keep useful metadata unobtrusive and extra actions close to playback. Honor Space/remote conventions and secondary-audio hints. For TV-app entry begin/resume the requested content directly with its supplied profile, preparing an in-app exit destination immediately so even a quick exit is coherent. Avoid unnecessary splash/detail barriers and show honest loading only when needed. On TV keep overlays restrained and use the documented delay before an interactive overlay pauses playback. On visionOS start by choice in a modest resizable window, never force immersion, and preserve system control space; inline video remains 2D. Watch clips should be short with suitable unscaled assets rather than a phone player compressed onto the wrist.

Implement playback/entry/exit states or supply transport/aspect/resume specifications; reviews identify exact control, crop, or context failures. Keep encoding/dimension tables in the reference.

**Worked transformation:** Before: a TV-app launch opens a branded detail screen, restarts a long film, and exits to nowhere when Back is pressed quickly. Decision: the playback request already carries intent. After: resume directly at the retained position/profile and prepare the corresponding in-app detail/menu before playback begins.

Deliver the artifact and entry, resume, controls, aspect, loading, and exit contract. Verify quick exit, PiP, different aspect ratios, interruption, overlays, and supported input. Fail for lost resume position, baked-in cropping/bars, forced immersion, or a missing exit context. Native media, audio routing, captions, and comfort need runtime/device evidence.

Load [playing-audio](../apple-hig-playing-audio/SKILL.md), [going-full-screen](../apple-hig-going-full-screen/SKILL.md), or [live-viewing-apps](../apple-hig-live-viewing-apps/SKILL.md) as required.
