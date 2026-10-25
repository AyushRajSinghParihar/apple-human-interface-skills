---
name: apple-hig-alerts
description: Use when creating, reviewing, or adapting critical alerts, consequential confirmations, button roles, defaults, and cancellation.
---

# Interrupt only for a decision that warrants it

Read [the alert guide](../../references/alerts.md). Apply the following as application advice and preserve the documented deliberate-destruction exception.

Inspect the triggering condition, urgency, reversibility, prior user intent, platform, and create/review/adapt request. Establish whether immediate attention is necessary. Do not turn every status update or startup network failure into an alert; ordinary undoable deletion can use recovery instead. Record evidence of the actual outcome and default-key behavior, not just button color.

Write a contextual neutral title and only useful supporting text; name outcomes instead of Yes/No. Use at most three buttons with meaningful roles and a safe Cancel beside destruction. Distinguish unexpected destructive consequences from confirmation of explicitly requested destruction: the latter may retain a normal default so Return confirms intent. Cancel is not the default; consider no default when deliberate reading is necessary. A single default completion acknowledgment should be Done, while OK can acknowledge purely informational content. Do not impose one platform's button geometry everywhere.

Implement the alert/handlers or deliver exact copy, role/default/order, trigger, and result specification; reviews must identify the specific misleading consequence or unnecessary interruption. Use fields only when resolution requires input and secure entry for passwords. Apply relevant platform accessory/cancellation rules: Mac suppression/Help only when useful, visionOS accessory limits and parent/space relationship, keyboard/remote alternate cancellation where supported. Post-action alternatives may belong in an action sheet.

**Worked transformation:** Before: an editor displays `Error 47` with OK/Cancel after an unrequested operation would overwrite unsaved work; Return commits overwrite. Decision: the consequence is unexpected and concealed. After: explain the conflicting draft, offer explicit safe recovery/cancellation and appropriately destructive replacement, and define a default that cannot accidentally accept unexplained loss.

Deliver the artifact and trigger/outcome/default contract. Verify Return, Cancel, supported escape, enlarged text, and repeated errors without stacked alerts. Fail for concealed loss, misleading action text, no safe cancellation, or routine status forcing interruption. Separate handler checks from native alert/assistive execution.

Use [action-sheets](../apple-hig-action-sheets/SKILL.md) for alternatives, [undo-and-redo](../../../apple-hig-patterns/.topics/apple-hig-undo-and-redo/SKILL.md) for reversible work, or [modality](../../../apple-hig-patterns/.topics/apple-hig-modality/SKILL.md) for surrounding exits.
