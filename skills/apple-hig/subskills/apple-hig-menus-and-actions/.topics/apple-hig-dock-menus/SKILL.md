---
name: apple-hig-dock-menus
description: Use when creating, reviewing, or adapting macOS Dock icon commands for background, windowless, or recent-item workflows.
---

# Offer useful actions before the app is frontmost

Read [the Dock-menu guide](../../references/dock-menus.md). The decision process is application advice; Dock menus are a Mac component.

Inspect the app's running/window states, common tasks, current/recent items, platform, and create/review/adapt goal. Identify tasks useful without a frontmost window and their existing visible/main-menu routes. Do not infer launch-state command availability from a menu shown only while running.

Select a few valuable actions such as composing or choosing a current/recent window. Use brief labels and logical order. Preserve system commands and ensure custom commands remain accessible through the main menu or visible UI. Define command resolution for no window, existing window, and stale recent target so it opens the intended context rather than a duplicate empty task. For iOS/iPadOS evaluate Home Screen quick actions instead; other destinations do not gain Dock menus by copying their appearance.

Implement the requested Dock commands, provide a state-to-command/window map, or review exact duplication, stale-target, and discoverability defects. Keep state-dependent operations within the user's authorized app behavior.

**Worked transformation:** Before: a notes app's Dock menu has twenty editing commands that do nothing when all windows close. Decision: background entry should accelerate a useful task, not mirror every editor action. After: offer `New Note` and a short current/recent window list, each resolving to the correct existing or new window; editing stays in its main-menu context.

Deliver the menu artifact and state/target contract. Verify no-window, background, existing-window, and missing-recent-item cases. Fail for commands with no effect, lost existing context, or custom commands available only in the Dock. Native Dock execution must be reported separately from static inspection.

Load [the-menu-bar](../apple-hig-the-menu-bar/SKILL.md) for alternate access, [windows](../../../apple-hig-presentation/.topics/apple-hig-windows/SKILL.md) for identity, or [home-screen-quick-actions](../apple-hig-home-screen-quick-actions/SKILL.md) for mobile adaptation.
