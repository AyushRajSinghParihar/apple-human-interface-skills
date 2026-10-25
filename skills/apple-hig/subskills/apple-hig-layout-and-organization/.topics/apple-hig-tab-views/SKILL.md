---
name: apple-hig-tab-views
description: Use when choosing, reviewing, or adapting mutually exclusive related content panes within a shared view.
---

# Keep pane switching distinct from app navigation

Read [the tab-view guide](../../references/tab-views.md). This procedure is application advice; distinguish the conventional Mac pane control from top-level tab bars and framework names.

Inspect the pane contents, affected controls, platform, and create/review/adapt request. Determine whether the choices are self-contained related views or unrelated app destinations. Count meaningful choices, record their labels, and identify any action that affects another pane.

Use tabs for a small set of related panes, with short predictive labels and controls scoped to their pane. Keep the tab control visible unless switching is programmatic; otherwise people lose the route among choices. Evaluate another presentation already at six or more choices rather than squeezing a growing category list. Normally inset the content within window margins. Conventional pane-style tabs belong to macOS; evaluate segmented controls on iOS/iPadOS, appropriate navigation elsewhere, and page behavior for watch SwiftUI tab views. Do not equate every `TabView` API with the Mac component.

Implement the pane switch, produce a pane/control ownership specification, or review specific category/scope defects. Preserve the intended state of each pane when changing views, documenting that application choice rather than assuming automatic persistence.

**Worked transformation:** Before: a Mac audio inspector has nine tabs and a gain control in “Metadata” that unexpectedly changes “Mix.” Decision: choice count and cross-pane scope obscure the model. After: group related inspector content into fewer coherent panes or a view-choice pop-up, and place gain with the mix controls it affects.

Deliver the artifact, labels, ownership, and switching/state policy. Verify every choice is reachable, labels fit localization, and controls affect only their documented scope. Fail for hidden user-driven navigation, misclassified app destinations, or effects in an unrelated pane. Report native page/Crown behavior only when exercised.

Use [tab-bars](../../../apple-hig-navigation-and-search/.topics/apple-hig-tab-bars/SKILL.md) for top-level navigation or [segmented-controls](../../../apple-hig-selection-and-input/.topics/apple-hig-segmented-controls/SKILL.md) for a supported related-view switch.
