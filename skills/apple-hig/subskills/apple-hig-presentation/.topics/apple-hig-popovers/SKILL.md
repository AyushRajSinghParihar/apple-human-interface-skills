---
name: apple-hig-popovers
description: Use when creating, reviewing, or adapting temporary anchored information, choices, and their dismissal or save behavior.
---

# Anchor temporary work without losing it

Read [the popover guide](../../references/popovers.md). This workflow is application advice; do not assume dismissal semantics from visual style.

Inspect trigger/source, related task, selection count, edits, platform/width, and create/review/adapt request. Identify essential reference content that must stay visible and every available dismissal route. Distinguish transient help/choices from persistent tools and warnings.

Anchor the arrow closely to its source while preserving context. Keep dimensions fitted to content and one popover at a time; replace the old one rather than cascade. Multi-selection stays open until explicitly dismissed. For automatic nonmodal dismissal save work; discard only through explicit Cancel. Add Done/Close/Cancel only when they clarify completion/saving. Use an alert for warnings that cannot be accidentally missed. On compact iOS/iPadOS layouts adapt to a sheet/fullscreen presentation; tvOS/watchOS do not support the component. On Mac detachability may suit persistent reference work, with continuity into panel form.

Implement the anchor/selection/dismissal behavior or supply a transition/size specification; reviews must identify the exact accidental-loss or context defect. If only screenshots exist, label outside-tap saving and replacement behavior as checks rather than observed failures.

**Worked transformation:** Before: a tag popover closes after the first choice and discards edits when a second toolbar button opens another popover. Decision: multi-selection and automatic dismissal need retention. After: keep it open for multiple tags, retain committed work on automatic dismissal, and close/replace it in one activation with explicit Cancel for discard.

Deliver the artifact and anchor, size, selection, save/cancel, and adaptation contract. Verify outside dismissal, explicit Cancel, multiple selection, replacement, and narrow width. Fail for lost work, warning-only popovers, cascades, or obscured essential source context. Report native positioning/animation/accessibility execution separately.

Load [sheets](../apple-hig-sheets/SKILL.md) for compact adaptation, [panels](../apple-hig-panels/SKILL.md) for persistent Mac tools, or [alerts](../apple-hig-alerts/SKILL.md) for critical warnings.
