---
name: apple-hig-carplay
description: Use when designing or reviewing an iPhone app's CarPlay templates, driving interaction, locked-phone independence, audio interruptions, or in-car error handling.
---

# Complete driving interactions without reaching for the phone

Read [CarPlay](../../references/carplay.md). Inspect the supported app category, chosen templates, setup requirements, audio states, and requested design/review/adaptation. Preserve the existing integration; this is connected-iPhone/iOS guidance, not permission to invent arbitrary car UI. Use category-appropriate system templates to handle display/input variation.

Separate pre-drive setup from driving tasks. Finish phone-dependent account/configuration before driving, then ensure CarPlay works while the iPhone is locked and inaccessible. A necessary failure must be explained in CarPlay; defer phone-only resolution until stopped rather than asking a driver to pick up the phone. Keep content scannable with prominent primary actions, generally toward the upper half of template layouts.

For audio, distinguish deliberate selection, resumable interruption, and replacement by another source. Do not start a session early and silence other audio. Begin playback when buffered enough, show Now Playing, and load descriptive metadata afterward; signal readiness so the system does not retain a selection spinner indefinitely. Resume after a call only if previously playing and resumable, not after a new Siri-selected playlist replaces it. Adjust mixing without overriding user volume.

Use restrained brand-related color, adaptive light/dark behavior, and appropriate icon/density assets. In-car sunlight/night conditions matter more than a single desktop preview.

**Before → decision → after:** A radio app initializes its audio session at launch, interrupts navigation audio, and asks for phone login after a token expires. Decision: deliberate playback and phone-independent recovery are essential driving conditions. After, launch leaves other audio alone, a selected station starts when ready, and CarPlay explains unavailable account content with a safe retry/deferred setup path.

Deliver a template/task/audio-state specification or implementation. Fail if the locked phone blocks ordinary use, playback resumes over a replacement source, or an error requires phone interaction while driving. Real car controls, lighting, audio interruptions, and template rendering need supported testing; Linux review cannot establish driving usability.

Use [AirPlay](../apple-hig-airplay/SKILL.md) for separate media-routing concerns and [Writing](../../../apple-hig-foundations/.topics/apple-hig-writing/SKILL.md) for concise in-car messages.
