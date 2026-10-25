---
name: apple-hig-panels
description: Use when creating, reviewing, or adapting macOS floating inspectors, contextual tools, or HUD-style information.
---

# Match the panel to the active context

Read [the panel guide](../../references/panels.md). The procedure is application advice for Mac; other platforms need their own supported supplementary presentation.

Inspect selection/window ownership, tool frequency, active/inactive behavior, platform, and create/review/adapt request. Determine whether the view follows current selection or preserves one object's information. The latter is an Info window, not an inspector panel. Record actual key/main behavior when available rather than inferring it from a floating border.

Use panels for quickly accessible contextual adjustments, favoring direct sliders/steppers over multistep selection. Give a movable title bar and short purpose title. Define selection updates, activation bringing panels forward, and deactivation hiding them. Expose show/hide commands without listing panels among document windows; generally disable minimization. Prefer standard styling. Reserve a small restrained HUD for appropriate media/immersive information when ordinary controls are unnecessary, preserving its style in fullscreen rather than forcing standard controls into it.

Implement the inspector behavior or provide a context/visibility/window-contract specification; review concrete stale-context and window-management defects. Consider an in-window split inspector when parallel contextual tools do not need floating placement.

**Worked transformation:** Before: a Mac design inspector continues showing the previous shape after selection changes, minimizes like a document, and appears in the document list. Decision: it is a contextual tool with incorrect ownership. After: update it with active selection, provide Show Inspector, and apply panel activation/hiding behavior without document-list membership.

Deliver the artifact and selection/visibility/command contract. Verify selection changes, app activation/deactivation, no selection, hide/restore, and fullscreen if relevant. Fail for editing the wrong object, no restoration route, or stale floating tools over another app. Native key-window/activation behavior needs runtime verification.

Load [windows](../apple-hig-windows/SKILL.md) for stable-object Info windows, [split-views](../../../apple-hig-layout-and-organization/.topics/apple-hig-split-views/SKILL.md) for embedded inspectors, or [sliders](../../../apple-hig-selection-and-input/.topics/apple-hig-sliders/SKILL.md) for direct adjustment.
