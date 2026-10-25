---
name: apple-hig-drag-and-drop
description: Use when creating, reviewing, or adapting content transfer, copy or move semantics, drop eligibility, representations, and drag feedback.
---

# Define the transfer before animating it

Read [the drag-and-drop guide](../../references/drag-and-drop.md). This workflow is application advice; default operations and input support are platform-qualified.

Inspect source/destination containers, content representations, identity, reversibility, platform/input, and create/review/adapt mode. Establish move versus copy: generally move within a container, copy between containers, and always copy interapp. Record exceptions explicitly with expected behavior/data-loss rationale. Do not infer an accepted drop from a highlight alone.

Offer another transfer route and accessible source/destination descriptions. Supply richest-to-simplest representations; choose the richest accepted and extract only relevant fields. Show eligible target feedback, remove it on exit, autoscroll inside edges, and keep useful drag representation continuity. Slow transfers need placement/progress; failed drops must not imply success. Preserve final selection rules and undo/meaningful reversal; confirm irreversible drops where needed. On Mac check Option at drop time and allow useful background-window dragging. On iPad support gathering when relevant. On visionOS consider user activity for empty-space window creation. tvOS/watchOS lack this component.

Implement transfer/feedback/selection or provide a source-operation-target contract; reviews identify exact duplication/loss and eligibility defects. Do not perform real external transfers without authorized scope.

**Worked transformation:** Before: dragging a contact into Recipients moves the contact out of its source and imports the entire record. Decision: interapp transfer copies, and the field needs only an email identity. After: copy the relevant email representation, highlight compatible targets, preserve the source, and keep the resulting recipient selected.

Deliver the artifact, operations, accepted representations, feedback, and reversal. Verify rejection, cancel, modifier release before drop, slow/failing transfer, and multi-item selection. Fail for unintended source deletion, false success feedback, or gesture-only essential transfer. Native drag, Universal Control, and assistive gestures need actual runtime/device evidence.

Load [undo-and-redo](../apple-hig-undo-and-redo/SKILL.md), [file-management](../apple-hig-file-management/SKILL.md), or [accessibility](../../../apple-hig-foundations/.topics/apple-hig-accessibility/SKILL.md) for the affected transfer.
