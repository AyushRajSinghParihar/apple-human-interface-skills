---
name: apple-hig-tab-bars
description: Use when creating, reviewing, or adapting top-level destination tabs, retained section state, labels, badges, and sidebar conversion.
---

# Give destinations stable identities

Read [the tab-bar guide](../../references/tab-bars.md). This workflow is application advice; top-level tab bars differ from pane-style or watch page tab views.

Inspect app destinations, per-section navigation, target platform, window states, and create/review/adapt request. Separate actions from destinations and identify current empty/unavailable sections. Record what each tab retains when leaving and returning; do not assume persistence from visual selection.

Keep tabs available through section navigation except temporary modal coverage. Do not hide/disable an empty destination: explain its state inside. Avoid More/overflow destinations when restructuring or sidebar conversion can preserve discovery. Use short labels and scalable recognizable icons; badges indicate information requiring attention rather than decoration. Preserve section state independently from the selected tab.

Implement destination/state behavior, create an annotated navigation contract, or review concrete lost-state and misclassified-action defects. On iPad begin with five or fewer default tabs when customizing and evaluate convertible sidebars. On TV preserve focus return via Menu and appropriate pinning for split-view tabs. In visionOS provide both symbol and short label, allowing leading-bar expansion, with secondary sidebar navigation confined to its tab. Watch uses a different page presentation; do not shrink this bar onto it.

**Worked transformation:** Before: a finance app hides Transactions when empty and uses a tab titled Add to create a payment; switching tabs resets an account detail. Decision: tabs are stable destinations, while Add is a command. After: retain Transactions with an empty-state explanation, move Add to an action control, and restore each section's navigation state.

Deliver the artifact, destination/empty-state map, retained state, and attention policy. Verify back-and-forth navigation, empty content, modal return, localization, and destination adaptation. Fail for a tab that unexpectedly executes an action, vanishes with content, or loses routine section context. Native focus/gaze behavior requires runtime verification.

Load [toolbars](../../../apple-hig-menus-and-actions/.topics/apple-hig-toolbars/SKILL.md) for actions, [sidebars](../apple-hig-sidebars/SKILL.md) for hierarchy, or [tab-views](../../../apple-hig-layout-and-organization/.topics/apple-hig-tab-views/SKILL.md) for pane/page switching.
