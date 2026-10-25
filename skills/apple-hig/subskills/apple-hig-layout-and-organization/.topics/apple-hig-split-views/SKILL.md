---
name: apple-hig-split-views
description: Use when creating, reviewing, or adapting coordinated navigation, detail, or supporting panes across window sizes.
---

# Preserve the route as panes change

Read [the split-view guide](../../references/split-views.md). This workflow applies its platform rules without promising identical layouts everywhere.

Inspect content relationships, selection, window ranges, target platform, and create/review/adapt mode. Identify primary/secondary/tertiary panes versus tools supporting a canvas. Record current selection and return routes; screenshots alone do not prove resize transitions.

Keep navigation selections persistent so detail has an identifiable parent. Define a logical collapsed route before arranging simultaneous panes. On iOS prefer multiple panes at regular widths; on iPad design narrow/intermediate transitions explicitly. On Mac choose operable min/max sizes, visible resizable dividers, and restoration controls for hidden supporting panes. On TV balance filter/results proportions under one overall title. On visionOS prefer a split view for contextual supplement rather than imposing extra-window management; use a sheet for a small required blocking task. On watch list and detail are full-screen; choose relevant initial detail and appropriate vertical page movement rather than shrinking adjacent panes.

Implement the requested transitions or produce pane/selection/size-state specifications; review exact resize or selection defects. Consider cross-pane drag/drop only when moving content is part of the task.

**Worked transformation:** Before: a mail client hides the mailbox pane at narrow width and loses the selected message when widened. Decision: layout state should not replace navigation identity. After: preserve mailbox/message selection, provide a clear back route while collapsed, and restore the same coordinated panes on expansion.

Deliver the artifact with wide/intermediate/compact states and restoration paths. Resize through thresholds, hide/restore tools, and change parent selection. Fail for clipped controls, inaccessible hidden panes, wrong parent/detail relationships, or selection lost solely through resizing. Distinguish inspected transitions from native window/input execution.

Load [sidebars](../../../apple-hig-navigation-and-search/.topics/apple-hig-sidebars/SKILL.md), [windows](../../../apple-hig-presentation/.topics/apple-hig-windows/SKILL.md), or [sheets](../../../apple-hig-presentation/.topics/apple-hig-sheets/SKILL.md) when those choices determine the pane contract.
