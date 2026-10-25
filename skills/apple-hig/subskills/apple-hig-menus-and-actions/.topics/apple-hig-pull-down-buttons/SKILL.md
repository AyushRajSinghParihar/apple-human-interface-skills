---
name: apple-hig-pull-down-buttons
description: Use when designing, reviewing, or adapting buttons that reveal related commands or secondary actions.
---

# Reveal related commands without hiding the main task

Read [the pull-down guide](../../references/pull-down-buttons.md). This workflow is application advice, preserving the source's component-specific confirmation guidance.

Inspect button purpose, command set, current task, platform, and create/review/adapt intent. Determine whether choices execute related commands or represent one flat selected state. Identify the primary action's visible route and the evidence for destructive consequences.

Choose a pop-up for a flat mutually exclusive noncommand value. Use a pull-down for a useful set of related commands, generally enough to justify the reveal step; one or two may be clearer as direct controls. Keep the main task discoverable and use More only for genuinely secondary work. Use a title only if button and commands fail to explain scope. Destructive choices need marked consequences and intent confirmation using the guide's iOS action-sheet/iPad popover treatment; load the destination presentation topic before detailing it. Avoid unsupported tvOS/watchOS component claims.

Implement the menu and handlers, specify button-to-command scope/confirmation, or review exact discovery and consequence defects. Touch-and-hold alternatives on mobile supplement recognizable activation; they must not silently become the only practical route.

**Worked transformation:** Before: a drawing screen's ellipsis hides both Save and one rarely used Duplicate command. Decision: the main task has lost a visible route, and two commands do not justify hiding everything. After: expose Save directly and place appropriate secondary operations under a predictive related menu or separate control.

Deliver the artifact, visible-primary route, command list, and destructive resolution. Verify open/select/dismiss, cancellation, long labels, and the named affected object. Fail for a hidden-only primary action, wrong-target command, or destructive selection without the specified intent resolution. Separate inspected logic from native menu/gesture execution.

Use [pop-up-buttons](../apple-hig-pop-up-buttons/SKILL.md), [action-sheets](../../../apple-hig-presentation/.topics/apple-hig-action-sheets/SKILL.md), [popovers](../../../apple-hig-presentation/.topics/apple-hig-popovers/SKILL.md), or [buttons](../apple-hig-buttons/SKILL.md) as the selected branch requires.
