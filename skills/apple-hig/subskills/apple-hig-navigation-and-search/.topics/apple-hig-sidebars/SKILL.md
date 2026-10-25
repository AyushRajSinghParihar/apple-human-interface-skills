---
name: apple-hig-sidebars
description: Use when creating, reviewing, or adapting leading app navigation, sidebar hierarchy, tab conversion, and hide or restore behavior.
---

# Keep navigation shallow and recoverable

Read [the sidebar guide](../../references/sidebars.md). Treat the process as application advice and retain the documented platform differences.

Inspect top-level destinations, hierarchy depth, important actions, window sizes, platform, and create/review/adapt intent. Identify selection identity and hidden/sidebar-converted states. Do not infer restoration or width adaptation from one screen.

Evaluate tabs for frequent destinations/content space before retaining a permanent sidebar. Keep sidebar hierarchy generally to two levels; use a middle list pane for deeper structure. Use short group labels and familiar scalable symbols, respecting system accent expectations rather than branding every row. Allow meaningful customization where feasible. Rich content can extend beneath floating glass using appropriate system treatment, without sacrificing legibility.

Implement navigation/adaptation or provide destination/hierarchy/selection/restore specifications; reviews should name unreachable branches and exact repairs. On Mac support useful auto-collapse and familiar button/View-menu restoration, keeping critical content away from potentially offscreen bottom space. On iPad preserve edge-swipe restoration and tab conversion where selected. In visionOS, selections inside a tab's sidebar must stay within that tab; do not use them to switch top-level tabs. The guide marks watch sidebars unsupported.

**Worked transformation:** Before: a library sidebar nests five levels and its final row is the only Add action; a visionOS child row switches to Settings. Decision: depth, offscreen critical action, and cross-tab navigation break the model. After: move deep content to a middle list, expose Add in a stable command location, and confine each sidebar branch to its tab.

Deliver the artifact and navigation/resize/restore map. Verify deep branches, compact conversion, hidden state, selection persistence, and larger sidebar sizing. Fail for a sidebar with no restoration route, cross-tab child selection, or critical actions lost below the visible window. Report native swipe/gaze execution separately.

Use [split-views](../../../apple-hig-layout-and-organization/.topics/apple-hig-split-views/SKILL.md), [tab-bars](../apple-hig-tab-bars/SKILL.md), or [toolbars](../../../apple-hig-menus-and-actions/.topics/apple-hig-toolbars/SKILL.md) for the selected structure.
