---
name: apple-hig-designing-for-tvos
description: Use when creating, reviewing, or adapting an Apple TV experience for across-room viewing, remote focus navigation, shared viewers, or television discovery.
---

# Make television choices visible from across the room

Read [Designing for tvOS](../../references/designing-for-tvos.md). Inspect the primary activity, content hierarchy, viewer/profile model, authentication, and input assumptions. Establish design, review, or adaptation mode and use supplied evidence to separate confirmed defects from untested remote behavior.

Rebuild the hierarchy around distant viewing and focus navigation. Prioritize legible titles and recognizable imagery rather than filling the TV with desktop density. Map directional movement and selection from each major region. The focused item must visibly identify both location and the available action through the platform's focus treatment; do not leave essential navigation dependent on pointer hover or tiny touch targets.

Choose the appropriate input contract. Siri Remote must support ordinary browsing; games may add controllers and relevant companion/voice input. Avoid making controller possession necessary for non-controller tasks. For long sessions or picture-in-picture, preserve the person's place when attention changes.

Reduce repetitive authentication using appropriate system integration. If the current system viewer changes, switch to the matching app profile deliberately and preserve privacy boundaries. Add Top Shelf, TV-app discovery, provider support, or SharePlay only when the content/activity warrants it, with a destination that matches the selected item.

**Before → decision → after:** A cooking-video app uses small tab labels, pointer hover menus, and one permanently signed-in household profile. Decision: across-room remote browsing and changing viewers require explicit focus routes and profile ownership. After, clear focusable categories lead into large recipe artwork, Select starts the highlighted recipe, and a viewer change updates saved recipes instead of exposing another person's history.

Deliver a focus-route map and corrected screen/profile flow or implementation. Fail if focus is invisible, a region has no remote exit, or a viewer change retains another profile's personal content. Check actual remote traversal, television legibility, and focus enlargement on supported hardware; a desktop screenshot only supports visual hypotheses.

For detailed movement use [Focus and selection](../../../apple-hig-inputs/.topics/apple-hig-focus-and-selection/SKILL.md) and [Remotes](../../../apple-hig-inputs/.topics/apple-hig-remotes/SKILL.md); for shared viewing use [SharePlay](../../../apple-hig-technologies/.topics/apple-hig-shareplay/SKILL.md).
