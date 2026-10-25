---
name: apple-hig-sheets
description: Use when creating, reviewing, or adapting a short parent-related task, sheet sizing, step navigation, and dismissal protection.
---

# Keep the sheet scoped to its parent task

Read [the sheet guide](../../references/sheets.md). This procedure is application advice; sheet modality and placement differ by platform.

Inspect the parent/task, steps, unfinished edits, window widths, platform, and create/review/adapt mode. Determine whether the task is short and related, ongoing supplementary work, or a complex editor. Record Done/Cancel/Back/gesture outcomes separately; one screenshot cannot establish data protection.

Choose another workspace for substantial editing or repeated input-and-observe work. Keep one main-interface sheet at a time. Define Cancel/Close as exit without saving, Done as finish/save, and Back as step navigation; avoid all three together. For iOS/iPadOS choose useful detents with a grabber for resizing, protect edits on vertical dismissal, and use standard centered iPad sizing. A composition flow may need large-only rather than medium-only confinement. Nonmodal sheets can support supplementary iOS/iPadOS work. Mac sheets block their parent while allowing other windows; repeated adjustments fit panels. VisionOS sheets center in the field of view with parent context visible. Watch sheets are brief occasional custom tasks, never content navigation, with unmistakable leading dismissal.

Implement the task/exit/size behavior, create a step-and-exit contract, or review specific loss/navigation defects. Preserve the user's stack and verify capability before naming an API implementation.

**Worked transformation:** Before: a phone message composer is medium-only, stacks an attachment sheet, and labels its first-step exit Back. Decision: composition needs room and one understandable task route. After: use a suitable large composer, internal attachment navigation, Cancel/Done on the first step, and Back only for returning within the task; dismissal resolves unsaved work.

Deliver the artifact, step actions, detents, parent availability, and data outcomes. Verify clean/edited gesture dismissal, Back, completion, resize, and replacement. Fail for lost drafts, modal stacking, inaccessible completion, or Back that exits. State native gesture/grabber/assistive checks separately.

Load [modality](../../../apple-hig-patterns/.topics/apple-hig-modality/SKILL.md), [action-sheets](../apple-hig-action-sheets/SKILL.md), [panels](../apple-hig-panels/SKILL.md), or [windows](../apple-hig-windows/SKILL.md) according to task length and exit needs.
