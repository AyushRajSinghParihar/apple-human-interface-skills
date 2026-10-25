---
name: apple-hig-the-menu-bar
description: Use when creating, reviewing, or adapting Mac or iPad menu-bar command structure, standard menus, keyboard routes, and extras.
---

# Expose the app's command structure

Read [the menu-bar guide](../../references/the-menu-bar.md), including the relevant standard-menu sections. This workflow is application advice; preserve platform differences and the source's explicitly unresolved ordering wording.

Inspect the command inventory, document/window model, supported platform, keyboard shortcuts, and create/review/adapt request. Map each command to app, document, selection, appearance, or window scope. Inventory visible/toolbar/context-only commands so the menu structure exposes real capabilities rather than an invented generic template.

Preserve standard ordering and shortcuts for supported commands. Place app-wide preferences in the app menu, document settings in File, editing in Edit, rich-text formatting in Format only when present, appearance in View, and window management in Window. Include meaningful standard subsets rather than renaming familiar actions for branding. Keep unavailable commands visible/dimmed and use ellipses for required input. Consult the guide for detailed command order and distinctions such as Duplicate versus Export and Zoom versus Full Screen; do not reproduce its entire tables.

Implement the menu structure or deliver a scoped command tree/shortcut map; reviews must identify missing or misplaced commands and concrete replacements. Give advanced modifier alternates discoverable routes and retain one-modifier simplicity. Place custom menus using concrete app hierarchy/frequency criteria because the source's general/specialized wording conflicts.

On iPad, every function needs in-app access because the bar is often hidden. Omit unsupported Mac-only commands such as About, Services, and app-visibility items; supported commands that are temporarily unavailable may remain disabled. Distinguish system App Settings from in-app configuration. On Mac keep the system Apple menu untouched. For an extra, allow opt-in, adaptive template imagery, and another access route: its visibility/position is not guaranteed. Do not promise this bar on iOS/tvOS/visionOS/watchOS.

**Worked transformation:** Before: a Mac editor offers Export only in a customizable toolbar, puts document paper size in app Settings, and treats Zoom as fullscreen. Decision: commands have wrong scope and fragile access. After: expose `Export As…`/document setup in File, retain toolbar acceleration, and keep Zoom distinct from fullscreen under familiar menus.

Deliver the artifact with command scope, standard/custom placement, shortcuts, and alternate routes. Verify no document, active selection, hidden toolbar, multiple windows, and iPad UI-only access. Fail for toolbar-only Mac actions, changed standard semantics, hidden-only modifier commands, or reliance on an extra staying visible. State keyboard/native-menu execution separately from code inspection.

Load [menus](../apple-hig-menus/SKILL.md) for item semantics, [toolbars](../apple-hig-toolbars/SKILL.md) for command parity, or [windows](../../../apple-hig-presentation/.topics/apple-hig-windows/SKILL.md) for document/window identity.
