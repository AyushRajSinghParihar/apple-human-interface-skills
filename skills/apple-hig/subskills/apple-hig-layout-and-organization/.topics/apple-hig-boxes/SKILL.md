---
name: apple-hig-boxes
description: Use when creating, reviewing, or adapting bordered groups of related controls or information.
---

# Give each boundary a reason

Read [the box guide](../../references/boxes.md). This procedure is application advice; platform conventions come from the guide.

Inspect the screen/code, target platform, requested create/review/adapt mode, and relationships among enclosed items. Identify whether a boundary communicates a real group, or merely decorates the whole screen. Record available width, titles, and nested boundaries; do not infer accessibility grouping from a screenshot.

First express subgroups with alignment and spacing. Retain a box when its boundary makes a meaningful group easier to understand; keep it smaller than its container so surrounding context remains visible. Add a brief sentence-case title when the relationship needs explanation or an accessible introduction. Apply the settings-pane colon exception only in that context. On iOS/iPadOS use appropriate semantic background treatment; on Mac account for the title above the box. Do not propose the component on tvOS/watchOS, where the guide marks it unsupported; adapt the relationship through suitable layout.

Implement the requested grouping, supply a concrete annotated layout, or report specific redundant/misleading boundaries in review. Preserve control relationships and reading order when removing a border.

**Worked transformation:** Before: printer settings have one screen-sized border and three nested borders around paper options. Decision: the outer edge adds no relationship; paper size and orientation already group through alignment. After: remove the outer border, use spacing for subgroups, and retain a titled `Paper options:` group only where it helps explain the controls.

Deliver the changed layout and group/title rationale. Verify narrow layouts, larger text, and that the title introduces the intended controls in the accessibility structure. Fail for cramped nested boundaries, a title attached to the wrong group, or a box that obscures context. Separate source inspection from native assistive execution.

Load [labels](../apple-hig-labels/SKILL.md) for title semantics or [layout](../../../apple-hig-foundations/.topics/apple-hig-layout/SKILL.md) when spacing is the underlying issue.
