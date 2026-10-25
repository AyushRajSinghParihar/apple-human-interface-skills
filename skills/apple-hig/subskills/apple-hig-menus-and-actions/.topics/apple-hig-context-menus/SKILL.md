---
name: apple-hig-context-menus
description: Use when creating, reviewing, or adapting item-specific context menus, previews, grouping, and alternate command access.
---

# Keep hidden shortcuts supplemental

Read [the context-menu guide](../../references/context-menus.md). This workflow is application advice; apply its exceptions rather than ordinary-menu rules indiscriminately.

Inspect selected objects, current task, platform/input, menu evidence, and create/review/adapt intent. Map every command to its affected selection and visible/main-menu alternative. A long-press screenshot does not prove another discoverable route exists.

Choose a short set of likely item actions, consistent across comparable objects. Hide unavailable contextual commands, preserving the Mac Cut/Copy/Paste dimmed exception where appropriate. Keep grouping shallow and predictive; put destructive commands last with their role on iOS/iPadOS/visionOS. Reconcile ordering with where scanning starts when the menu opens above/below. Put keyboard equivalents in main menus, not here.

Implement/specify command availability and preview scope, or review concrete missing routes and target mismatches. On iOS/iPadOS choose context or edit menu for an object rather than ambiguous competing gestures; preview clipping must match the object. On Mac retain menu-bar access. On visionOS keep controls around the parent accessible and consider context tools before extra windows. Do not propose the component on watchOS.

**Worked transformation:** Before: a file menu exposes Rename only by long press and includes unavailable sharing plus three nested levels of export commands. Decision: essential capability is hidden and scan cost exceeds the item task. After: add visible/main-menu Rename, hide ineligible sharing, and retain one predictive Export submenu with the relevant formats.

Deliver the menu tree, availability rules, selection scope, and alternate routes. Verify one/multiple selection, ineligible items, above/below placement, and comparable objects. Fail for hidden-only functionality, wrong affected object, gesture ambiguity, or unusable menu height. Mark native preview/focus/input execution separately.

Use [edit-menus](../apple-hig-edit-menus/SKILL.md) for selected-content editing or [menus](../apple-hig-menus/SKILL.md) for shared command organization.
