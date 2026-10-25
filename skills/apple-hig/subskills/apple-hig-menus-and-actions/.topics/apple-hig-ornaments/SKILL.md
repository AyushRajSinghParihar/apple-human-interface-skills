---
name: apple-hig-ornaments
description: Use when designing, reviewing, or adapting persistent visionOS tools attached to a window edge.
---

# Attach persistent tools to their window

Read [the ornament guide](../../references/ornaments.md). This workflow is application advice for visionOS; do not infer ornament support elsewhere.

Inspect the parent window/content, frequent tools, existing standard toolbars/tabs, target platform, and create/review/adapt mode. Identify controls that need stable access while content scrolls and those only occasionally needed. Record window widths and management-control locations from evidence; screenshots do not prove spatial attachment.

Prefer system toolbars/tabs for those standard components instead of rebuilding them as custom ornaments. Use a custom ornament for persistent contextual tools/information that otherwise cover content. Keep it parallel, slightly forward, attached to its window, and stable during content scrolling. Balance several ornaments; move lower-priority tools inside the window if visual weight grows. Keep width within window width and preserve access to side/window controls. Temporary hiding may suit focused media, but specify a reliable restoration path.

Implement the authorized attachment or produce a window/ornament layout and visibility specification; in review identify actual overlap, redundancy, or relationship failures. Standard borderless controls on ornament glass can inherit system feedback; do not invent custom gaze effects from a static design.

**Worked transformation:** Before: a spatial score editor has a custom “toolbar” ornament wider than its window and another floating panel for two rare commands. Decision: standard tools should use their system presentation, and rare tools do not justify persistent weight. After: use the standard toolbar, move rare commands into the window, and reserve a bounded ornament only for frequently inspected playback information.

Deliver the artifact, attachment/width contract, and visibility/restore behavior. Verify narrow window, content scroll, move, and hide/restore states. Fail for covering essential content/window controls or tools that drift independently of their context. Spatial comfort, gaze, and attachment execution require Apple-device/runtime checks.

Load [toolbars](../apple-hig-toolbars/SKILL.md) or [designing-for-visionos](../../../apple-hig-getting-started/.topics/apple-hig-designing-for-visionos/SKILL.md) when standard placement or spatial context determines the design.
