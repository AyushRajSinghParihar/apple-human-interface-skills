---
name: apple-hig-windows
description: Use when creating, reviewing, or adapting primary or auxiliary windows, size transitions, context ownership, and spatial window or volume choices.
---

# Preserve context without multiplying clutter

Read [the window guide](../../references/windows.md). This workflow is application advice for the supported multiwindow platforms, not a claim that every OS has identical windows.

Inspect document/task identity, current windows, parallel-work needs, size ranges, platform, and create/review/adapt request. Distinguish a primary workspace from a short auxiliary task and a context-following panel. Record open/reuse/close behavior and main/key ownership from evidence; a screenshot does not establish window identity.

Open another window when preserving context or parallel work helps, with explicit Open in New Window where useful; avoid clutter by default. Retain system frames/movement/resize/close controls and call them windows in product copy. Set useful size constraints and adapt between them. On iPad protect leading tools from window controls and support the chosen fullscreen/windowed context. On Mac preserve key/main/inactive cues and normal movement/minimization; avoid critical bottom controls potentially offscreen.

For visionOS choose familiar glass windows for familiar tasks, shallow depth near their surface, and volumes for deeper multi-angle objects. Preserve glass legibility/grouping unless the requested content justifies another supported style. For volumes choose true-scale versus dynamic scaling intentionally, appropriate alignment, viewer-relative attachments, and bounded ornament placement. Do not prescribe the multiwindow component on iOS/tvOS/watchOS.

Implement window identity/adaptation, specify open/reuse/size/ownership behavior, or review concrete clutter/context defects. Do not infer physical size comfort or clipping from Linux rendering.

**Worked transformation:** Before: a spatial model viewer removes window glass, places a deep model outside its clipped surface, and opens a fresh window for every property click. Decision: depth and UI context require different containers. After: keep property tools in the existing window/split context and put the deep model in a suitable volume with bounded attachments and deliberate scaling.

Deliver the artifact and window/container lifecycle, sizing, and context contract. Verify repeated opens, multiple documents, resize extremes, close/reopen, and activation state. Fail for wrong-object reuse, unreachable controls, lost task context, or deeper content clipped by the selected container. Separate static/runtime checks from native window management and spatial-device validation.

Load [panels](../apple-hig-panels/SKILL.md) for selection-following tools, [split-views](../../../apple-hig-layout-and-organization/.topics/apple-hig-split-views/SKILL.md) for contextual supplements, or [multitasking](../../../apple-hig-patterns/.topics/apple-hig-multitasking/SKILL.md) for continuity across apps/windows.
