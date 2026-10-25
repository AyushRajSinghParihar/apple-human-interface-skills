---
name: apple-hig-progress-indicators
description: Use when creating, reviewing, or adapting determinate or indeterminate work status, refresh feedback, pause, cancellation, and stalls.
---

# Report the work that is actually measurable

Read [the progress-indicator guide](../../references/progress-indicators.md). This workflow is application advice; progress estimates need implementation evidence.

Inspect operation stages, known total, actual progress signals, cancellation cost, target platform, and create/review/adapt request. Separate elapsed time or completed requests from measured whole-task completion. Do not fabricate percentages to make an indeterminate task feel faster.

Use determinate progress when its denominator covers the whole operation; otherwise communicate ongoing activity. Keep shape/placement stable: a compatible indeterminate bar can become determinate, but switching spinner to bar midtask disrupts context. Explain meaningful stalls and recovery. Allow safe cancellation and consider pause where cancelling discards useful work; consequential cancellation must permit resuming rather than silently losing progress. On Mac small background spinners often need no redundant label. Pull-to-refresh supplements automatic updates and may show useful freshness context, not gesture instructions. Remove temporary progress when the task resolves.

Implement the status/estimate/cancel state machine, supply it as a concrete specification, or review exact dishonest progress and trapped-wait defects. Keep success, failure, and “request accepted” distinct according to the operation.

**Worked transformation:** Before: a backup bar reaches 90% after scanning but spends most time uploading, then Cancel silently deletes partial work. Decision: the estimate omits the main stage and cancellation conceals cost. After: use measured whole-work progress or honest indeterminate status, explain upload state, and offer safe pause/resume or deliberate cancellation.

Deliver the artifact, measurement basis, state transitions, and recovery contract. Verify unknown-to-known duration, stage boundaries, stall, completion, failure, and cancel/resume. Fail for invented percentage, resolved work still spinning, or unrecoverable consequential cancellation. Mark runtime timing and actual backend completion separately from source review.

Load [loading](../../../apple-hig-patterns/.topics/apple-hig-loading/SKILL.md) for content strategy or [buttons](../../../apple-hig-menus-and-actions/.topics/apple-hig-buttons/SKILL.md) for initiating-control feedback.
