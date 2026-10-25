---
name: apple-hig-menus
description: Use when creating, reviewing, or adapting menu command labels, availability, grouping, submenus, and toggled options.
---

# Organize commands around their consequences

Read [the menu guide](../../references/menus.md) and the specialized component topic when applicable. This workflow is application advice; context-menu exceptions differ from ordinary menus.

Inspect the current selection, command inventory, state model, platform/input, and create/review/adapt request. Map each item to immediate action, further input, state selection, or submenu. Record actual enablement and effects rather than inferring them from an icon.

Use short predictive verbs and ellipses for required further input. In ordinary menus keep unavailable commands dimmed and their parent openable, preserving discovery. Keep related commands together, prioritize useful groups, and use shallow real submenus rather than indentation. Dynamic user-created sets may remain complete/scrollable rather than being cut off to obey a simplistic length limit. Apply icons consistently within logical groups only when meaningful. Use checkmarks for applied attributes and action wording for toggles so state and next action cannot be confused.

Implement/restructure the menu, provide a command tree with availability/state rules, or review exact label/scope/organization defects. On mobile choose small icon-only layouts only for familiar tightly related commands. On visionOS keep the menu near its target and choose breakthrough behavior deliberately; do not claim occlusion behavior without scene evidence. For games verify menu targets/type independently of scaled gameplay and respect platform input.

**Worked transformation:** Before: `HDR On` ambiguously describes a state or action, unavailable exports disappear from an ordinary menu, and Sort uses fake indentation. Decision: predictability needs explicit actions and true structure. After: use `Turn HDR On`/`Turn HDR Off`, dim ineligible exports, and create a real `Sort By` submenu with a selected attribute.

Deliver the menu tree and state/command contract. Verify empty selection, all-disabled children, toggling twice, localization, and platform input. Fail for an action label opposite to its result, undiscoverable ordinary capabilities, or submenu structure inaccessible to keyboard/assistive navigation. Separate native menu execution from static inspection.

Load [context-menus](../apple-hig-context-menus/SKILL.md), [pop-up-buttons](../apple-hig-pop-up-buttons/SKILL.md), [pull-down-buttons](../apple-hig-pull-down-buttons/SKILL.md), or [the-menu-bar](../apple-hig-the-menu-bar/SKILL.md) according to the actual menu type.
