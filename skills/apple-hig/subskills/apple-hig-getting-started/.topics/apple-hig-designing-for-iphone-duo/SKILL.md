---
name: apple-hig-designing-for-iphone-duo
description: Use when an iPhone Duo interface must preserve tasks while folding, opening, changing pose, encountering reserved regions, or using vertical controls.
---

# Preserve the iPhone task through a fold

Read [Designing for iPhone Duo](../../references/designing-for-iphone-duo.md). Inspect existing compact/regular layouts, navigation state, safe-area assumptions, toolbar groups, and custom containers. Identify design, review, or adaptation mode. Work within the existing stack; the guide's APIs describe implementation options, not a requirement to replace another supported architecture.

Trace the same selected content from the closed outer display through open and partially folded configurations. Use available size classes, margins, safe areas, and reserved regions rather than panel dimensions or pose names as breakpoints. Expand an existing hierarchy, such as list plus detail, without dropping features or resetting selection on closure.

Choose containers by relationship. A split view navigates a hierarchy and collapses appropriately. An arrangement repositions existing primary/secondary content across axes or around a fold; it does not replace navigation. Keep navigation split/tab structures outside an arrangement. For games, adapt aspect ratio before padding and preserve control/text size in supported poses.

Audit controls where side bars appear. Preserve system vertical placement, hardware-side alignment, group distinctions, and local controls near the pane they affect. Supply titles with meaningful symbols for expansion and overflow. Express action priorities so common commands and important badges survive compression; keep tabs available for navigation-led views and task tools prominent for task-led views. Check asymmetrical safe areas, including multitasking on either side and RTL, rather than mirroring hardware alignment.

**Worked transformation:** Before, a reading app treats the open device as a new tablet screen, resets to its library, and positions annotations across the fold. Decision: opening should reveal more of the same book. After, the selected chapter remains active, a regular-width contents pane appears beside the page, reserved regions keep notes and actions usable, and closing collapses back to that chapter with the same reading position.

Deliver a state-preserving pose sequence and toolbar priority specification or implementation. Fail if folding loses context, a camera/fold region covers a necessary control, or overflow removes the only route to an action. Use Device Hub/platform previews when available; Linux layout inspection cannot verify device pose behavior.

Use [Layout](../../../apple-hig-foundations/.topics/apple-hig-layout/SKILL.md) for environmental sizing and [Right to left](../../../apple-hig-foundations/.topics/apple-hig-right-to-left/SKILL.md) when adapting reading direction without reversing hardware alignment.
