---
name: apple-hig-segmented-controls
description: Use when creating, reviewing, or adapting grouped related choices, view switches, or momentary actions in segmented controls.
---

# Give every segment the same interaction model

Read [the segmented-control guide](../../references/segmented-controls.md). This procedure is application advice; multiple selection and focus behavior are platform-qualified.

Inspect each segment's purpose, retained selection, count, labels/icons, platform/input, and create/review/adapt request. Classify the whole control as single choice, supported multiple choice, or momentary actions. Do not mix these contracts under one visual group.

Use segments for related attributes or closely related views, with similar content footprints and consistently text or imagery. Keep counts within usable platform space rather than squeezing unlimited options. Use tabs for top-level destinations. On Mac main-body pane switching may fit tab views better; supply context/captions/tooltips for unclear glyphs. On TV selection follows focus, so avoid accidental transitions from nearby controls and consider split filtering. In visionOS give icon segments descriptive text for look tooltips. Watch lacks this component; adapt to supported choice UI.

Implement the model/selection behavior, specify segment meanings and affected content, or review exact mixed-model and scope defects. Keep accessibility names and selected state aligned with the visible content.

**Worked transformation:** Before: a photo inspector groups `Grid`, `List`, and `Export`, retaining selection on the first two while the last opens a task. Decision: view choice and action contracts conflict. After: keep a single-choice Grid/List control and move Export to a distinct action; preserve the selected view through unrelated work.

Deliver the artifact and common interaction model, choices, and state contract. Verify each segment, repeat activation, localization, external state changes, and TV focus where relevant. Fail for mixed action/selection semantics, indistinguishable selected state, or top-level navigation disguised as local view choice. Native focus/spring-loading/gaze checks require execution evidence.

Load [tab-bars](../../../apple-hig-navigation-and-search/.topics/apple-hig-tab-bars/SKILL.md) for app sections, [tab-views](../../../apple-hig-layout-and-organization/.topics/apple-hig-tab-views/SKILL.md) for Mac panes, or [buttons](../../../apple-hig-menus-and-actions/.topics/apple-hig-buttons/SKILL.md) for separate commands.
