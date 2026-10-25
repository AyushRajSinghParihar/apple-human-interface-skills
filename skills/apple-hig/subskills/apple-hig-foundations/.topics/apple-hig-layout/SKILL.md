---
name: apple-hig-layout
description: Use when designing, reviewing, or adapting layout hierarchy, safe areas, size classes, resizable windows, enlarged text, or platform-specific spacing.
---

# Preserve relationships while available space changes

Read [Layout](../../references/layout.md). Inspect content priority, navigation, controls, supported environments, constraints, and current implementation. Identify design/review/adaptation mode and keep the existing layout system. Record actual available space and text/localization conditions; device names alone are insufficient evidence for a breakpoint.

Start with relationships: align peers, group related items, indent subordinates, and reveal secondary choices progressively. Place important content toward the leading/top region in the locale's reading order. Separate backgrounds that can extend beneath bars from important content/actions that must respect safe regions.

Choose adaptations from available width/height and environmental values, not a phone/tablet or portrait/landscape guess. Preserve selection, content, functionality, and idiom when columns collapse, actions overflow, or horizontal rows stack for larger text. Test the smallest and largest useful layouts first, then intermediate resizing, longer localization, direction changes, and display accommodations. Crop decorative backgrounds without distorting aspect ratio or hiding essential imagery.

Apply platform conditions deliberately: Mac essential controls cannot depend on a bottom edge that may be offscreen; TV content needs the guide's overscan insets and focus-expansion room; Watch normally needs very few side-by-side actions. visionOS windows/volumes should resize, use meaningful bounds, and avoid inline 3D crowding controls; use separate volumes for model-centric work. Read numeric platform specifications from the guide rather than generalizing one platform's spacing.

**Before → decision → after:** A reading list positions Delete at a fixed bottom coordinate and fixes each row to one line. Decision: resized windows and enlarged titles need flow-based layout. After, row height/wrapping adapt, secondary actions remain reachable through contextual overflow, and the selected article persists when the sidebar collapses.

Deliver corrected layouts/constraints or implementation plus an environment matrix. Fail if a required action disappears, related items detach, content overlaps hardware/bars, or resizing changes the task's meaning. Report tested dimensions/settings; static or Linux checks cannot establish native safe-area/focus behavior absent supported execution.

Use [Typography](../apple-hig-typography/SKILL.md) for text behavior, [Right to left](../apple-hig-right-to-left/SKILL.md) for direction, and [Spatial layout](../apple-hig-spatial-layout/SKILL.md) for 3D position/scale.
