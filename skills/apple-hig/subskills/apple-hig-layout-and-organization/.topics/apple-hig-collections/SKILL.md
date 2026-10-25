---
name: apple-hig-collections
description: Use when designing, reviewing, or adapting visual grids or rows of selectable and editable items.
---

# Preserve item identity through layout changes

Read [the collection guide](../../references/collections.md). The workflow is application advice, with documented support qualified by platform.

Inspect actual items, screen/code, target input/platform, and create/review/adapt intent. Determine whether visual recognition or text comparison drives selection; record selection, reorder, insertion, and scrolling behavior only when evidenced. Text-heavy comparison may belong in a list/table rather than a collection.

Choose a familiar row/grid before a custom arrangement. Size cells around meaningful imagery and labels, allowing focus/hover expansion without collision. Retain standard selection/editing interactions and use custom gestures only for a demonstrated task need. For iOS/iPadOS layout changes during manipulation, favor explicit triggers and preserve the person's location and selected item; do not reshuffle a live grid merely because a data property changed. The guide marks collections unsupported on watchOS, so adapt to a suitable list rather than assert parity.

Implement a requested collection or produce a cell/layout/interaction specification; review findings must name affected items or transitions. Specify stable identity and understandable insertion/deletion/reorder feedback as application decisions consistent with the guide.

**Worked transformation:** Before: a wallpaper grid reorders by popularity while someone drags an image, causing the target to move. Decision: dynamic ranking conflicts with manipulation. After: preserve the displayed order during the drag and expose an explicit refresh/sort action; animate a deliberate reorder while retaining selection.

Deliver the artifact and layout-change policy. Verify long labels, odd item counts, focused edge cells, reorder, and deletion of the selected item. Fail for overlapping focused cells, accidental activation during scrolling, or identity/location lost after a layout change. Report native focus/gesture execution separately from inspected logic.

Use [lists-and-tables](../apple-hig-lists-and-tables/SKILL.md) for text comparison, [image-views](../../../apple-hig-content/.topics/apple-hig-image-views/SKILL.md) for fitting, or [drag-and-drop](../../../apple-hig-patterns/.topics/apple-hig-drag-and-drop/SKILL.md) for transfer behavior.
