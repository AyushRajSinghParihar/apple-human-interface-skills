---
name: apple-hig-action-sheets
description: Use when creating, reviewing, or adapting short modal alternatives after an intentional action, including save or discard choices.
---

# Resolve the decision the person started

Read [the action-sheet guide](../../references/action-sheets.md). This procedure is application advice; use its component-specific platform limits.

Inspect the initiating action, related alternatives, data at risk, target platform, and create/review/adapt mode. Establish whether the person deliberately began a choice, requested a menu, or encountered an urgent problem. Record the actual Cancel and destruction outcomes; screenshots cannot prove them.

Choose an action sheet for short related post-action alternatives, a menu for an explicit menu request, and an alert for critical situations without a set of alternatives. Keep the decision brief enough to avoid scrolling. Explain context with a concise title and only necessary additional text. Mark destructive options and place them as the guide specifies; provide safe cancellation rather than allowing dismissal to imply destruction. On watch preserve mandatory Cancel and the four-total-button limit. The source marks this component unsupported in visionOS; choose a supported presentation rather than infer support from a shared API name.

Implement the choices/handlers, specify an action-to-outcome transition table, or review exact ambiguity and loss risks. Bind every option to the same original object/draft so a delayed decision cannot affect a changed selection.

**Worked transformation:** Before: canceling a recorded voice note immediately deletes it, while a generic “Are you sure?” has Yes/No buttons. Decision: the person needs clear related outcomes. After: offer `Save Recording`, destructive `Discard Recording`, and safe `Cancel`/keep-editing resolution appropriate to the platform, naming the recording's consequence.

Deliver the artifact, trigger, choices, cancellation, and retained-work contract. Verify each option, outside/system dismissal where applicable, enlarged text, and repeated invocation. Fail for accidental data loss, a destructive option with neutral semantics, or cancellation that commits an action. State native presentation/input checks separately from source inspection.

Load [alerts](../apple-hig-alerts/SKILL.md) for urgent confirmation, [menus](../../../apple-hig-menus-and-actions/.topics/apple-hig-menus/SKILL.md) for command reveal, or [modality](../../../apple-hig-patterns/.topics/apple-hig-modality/SKILL.md) for exit consistency.
