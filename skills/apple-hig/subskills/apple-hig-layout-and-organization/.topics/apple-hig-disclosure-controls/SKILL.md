---
name: apple-hig-disclosure-controls
description: Use when designing, reviewing, or adapting progressive disclosure, expansion labels, and collapsed or expanded state.
---

# Reveal the optional without hiding the essential

Read [the disclosure guide](../../references/disclosure-controls.md). This workflow applies the source; it does not invent support for custom controls.

Inspect the content hierarchy, platform, evidence artifact, and create/review/adapt goal. Separate common actions from advanced/occasional detail. Record which view/control owns each expansion and whether hidden contents include validation errors or essential next steps.

Keep common information visible. Use a labelled triangle for revealing details or hierarchy children, with inward-leading collapsed and downward expanded direction. Use the distinct disclosure button for functionality associated with a particular control; its down/up directions and one-per-view constraint must not be generalized to every disclosure triangle. Place the trigger beside its controlled content and expose state/name in the accessibility structure. The guide identifies platform disclosure behavior on iOS/iPadOS/visionOS and marks tvOS/watchOS unsupported; adapt the information architecture there rather than copying unsupported chrome.

Implement the expansion, specify the trigger/content/state relationship, or review exact hidden-task failures. Preserve entered values and task continuity when a section collapses; that is an application decision to verify, not an asserted system guarantee.

**Worked transformation:** Before: a video export view hides Format and Destination under an unlabeled triangle alongside three separate down/up expansion buttons. Decision: necessary choices are hidden and trigger meanings conflict. After: keep Format/Destination visible, put rare encoder parameters under `Advanced Encoding`, and use a single nearby control-specific expansion only if needed.

Deliver the modified hierarchy and initial/expanded states. Verify the label predicts revealed content, keyboard activation changes exposed state, resizing does not clip content, and collapse preserves intended values. Fail for hidden essential actions, ambiguous ownership, or a state announced opposite to its visual direction. Native accessibility execution requires a suitable runtime.

Use [outline-views](../apple-hig-outline-views/SKILL.md) for tree traversal or [buttons](../../../apple-hig-menus-and-actions/.topics/apple-hig-buttons/SKILL.md) for action semantics.
