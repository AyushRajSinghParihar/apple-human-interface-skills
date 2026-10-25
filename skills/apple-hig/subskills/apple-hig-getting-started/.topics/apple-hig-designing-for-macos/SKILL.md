---
name: apple-hig-designing-for-macos
description: Use when creating, reviewing, or adapting a Mac experience for multiple windows, menu commands, keyboard workflows, precise selection, or desktop file work.
---

# Give desktop work desktop control

Read [Designing for macOS](../../references/designing-for-macos.md). Inspect the current task, document/content model, windows, commands, and interruption behavior. Determine whether the request is a design, review, or port. Preserve the existing stack and distinguish observed behavior from proposals or missing runtime evidence.

Choose window boundaries around useful units of work. If documents or parallel comparisons benefit from independent windows, retain their own selections and edits. If one workspace suffices, make it resizable and avoid unnecessary modal navigation. Plan full screen for focused work without making it the only usable arrangement. Keep essential commands reachable even when a window is partly offscreen.

Build a command inventory from the task. Put app commands in the menu bar, give common operations appropriate shortcuts, and ensure a keyboard-only completion path. Align toolbar/contextual controls with those same actions and availability states. Use pointer precision for selection and editing rather than inflating a phone-style interface across the display. Preserve conventional file opening/saving and relevant Dock-menu behavior.

Specify app activation changes: switching away and back must preserve work and clearly distinguish the active target for commands. Offer customization where different work styles justify it, such as tools or window arrangement; do not require customization before basic use.

**Before → decision → after:** A photo catalog port displays every album as a full-screen drill-down and exposes Export only through a floating touch menu. Desktop comparison needs persistent context and a discoverable command. After, an album sidebar and resizable detail area support selection; File > Export and a keyboard command act on that selection, and optional second windows compare collections without losing the original state.

Deliver the revised window/command model or implementation, with a keyboard path and activation scenario. Fail if menu and toolbar act on different selections, switching apps loses edits, or resizing hides the only completion action. Linux inspection does not establish actual menu-bar integration, multi-display behavior, or native keyboard accessibility.

Use [Keyboards](../../../apple-hig-inputs/.topics/apple-hig-keyboards/SKILL.md) for command details, [Layout](../../../apple-hig-foundations/.topics/apple-hig-layout/SKILL.md) for window constraints, and [Mac Catalyst](../../../apple-hig-technologies/.topics/apple-hig-mac-catalyst/SKILL.md) when adapting an iPad app through that technology.
