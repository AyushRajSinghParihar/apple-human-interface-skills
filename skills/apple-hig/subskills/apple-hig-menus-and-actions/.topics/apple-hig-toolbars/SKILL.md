---
name: apple-hig-toolbars
description: Use when creating, reviewing, or adapting toolbar actions, navigation, titles, grouping, overflow, and restoration.
---

# Keep essential actions reachable as width changes

Read [the toolbar guide](../../references/toolbars.md). This is application advice; preserve the requested stack and the platform's system behavior.

Inspect the current-view task, command frequency, navigation/completion controls, window widths, platform, and create/review/adapt mode. Separate top-level destinations from actions and distinguish Back from modal Close. Obtain wide/narrow/customized/hidden states or mark them unverified.

Prioritize navigation and essential completion before secondary tools. Group related controls in familiar leading/center/trailing regions; use symbols when recognizable and text when needed. Name the content/location rather than the app. Define what collapses as width shrinks, retaining critical routes. Mac/iPad system overflow should not gain a redundant manual overflow, and customization must not remove navigation essentials. Contextual hiding needs reliable restoration.

Implement the toolbar or deliver placement/priority/overflow/state specifications; review concrete missing routes and misplaced actions. On Mac every toolbar action also needs a menu command. On iPad preserve the distinction when tabs share the top region. On visionOS prefer the standard bottom presentation, avoid undiscoverable pull-downs and vertical bars, protect essential minimum width, and restore normal tools after modal editing. On watch choose persistent corners/bottom versus a scrolling primaryAction according to the task; do not assume identical visibility.

**Worked transformation:** Before: a Mac diagram editor places Close among drawing tools and hides Save behind its own More plus system overflow. Decision: dismissal and critical work need predictable distinct routes. After: keep window/task completion separate, prioritize useful drawing groups, let system overflow handle secondary tools, and retain Save in the menu bar.

Deliver the artifact and wide/narrow/hidden/customized access map. Verify title localization, overflow, restoration, and editing-mode exit. Fail for unreachable critical actions, Back that dismisses unexpectedly, duplicate overflow, or toolbar-only Mac commands. Report native overflow, gaze, and assistive execution separately.

Use [tab-bars](../../../apple-hig-navigation-and-search/.topics/apple-hig-tab-bars/SKILL.md) for destinations, [the-menu-bar](../apple-hig-the-menu-bar/SKILL.md) for Mac parity, or [ornaments](../apple-hig-ornaments/SKILL.md) for genuinely custom spatial tools.
