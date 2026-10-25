---
name: apple-hig-status-bars
description: Use when creating, reviewing, or adapting device-status visibility, contrast, content overlap, and fullscreen restoration on iOS or iPadOS.
---

# Preserve access to device context

Read [the status-bar guide](../../references/status-bars.md). This procedure is application advice for the source's iOS/iPadOS component, not desktop window status text.

Inspect underlying content/appearance, safe layout, immersion state, platform, and create/review/adapt mode. Identify whether time/connectivity remain readable and whether apparent controls under status are actually operable. Obtain normal and media/fullscreen states; a single frame cannot establish restoration.

Keep status legible over changing content using suitable system style and preferred scroll-edge separation rather than an arbitrary decorative overlay. Move/arrange controls so obscuration does not imply false affordances. Fullscreen media may temporarily hide status, but specify a discoverable simple gesture to restore it and avoid permanently removing access. Use platform-supported layout/status behavior rather than drawing a fake device bar. The guide marks this component unsupported on Mac/TV/visionOS/watchOS.

Implement status appearance/overlap/restoration or provide an annotated state specification; reviews identify the exact background/control collision and access defect. Do not claim native safe-area behavior from an HTML approximation.

**Worked transformation:** Before: a document scanner permanently hides status and places a small flash control beneath where it reappears. Decision: device information needs temporary restoration and controls need reliable selectable space. After: expose a familiar tap-to-reveal path, preserve readable system status, and keep flash outside the obscured region in both states.

Deliver the artifact and visible/hidden/restored state contract. Verify bright/dark content, scroll transitions, media exit, and tap restoration. Fail for unreadable status, permanently lost time/connectivity access, or controls visually offered where blocked. Native safe-area/device-status behavior needs runtime execution; report static checks honestly.

Load [going-full-screen](../../../apple-hig-patterns/.topics/apple-hig-going-full-screen/SKILL.md) for immersion or [scroll-views](../../../apple-hig-presentation/.topics/apple-hig-scroll-views/SKILL.md) for edge separation.
