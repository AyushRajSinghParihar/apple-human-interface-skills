---
name: apple-hig-controls
description: Use when creating, reviewing, or adapting system controls in Control Center, Lock Screen, or Action button contexts.
---

# Make a compact action truthful in every state

Read [the controls guide](../../references/controls.md). This workflow is application advice; preserve platform/locked-device qualifications and verify actual API support in the supplied stack.

Inspect the action or binary state, configuration, security sensitivity, locked/unlocked surfaces, platform, and create/review/adapt request. Identify direct action versus app-opening behavior and the authoritative state source. A tinted symbol alone does not prove the controlled device changed.

Choose useful focused work, preferably avoiding an app launch. Supply a symbol understandable without text because some surfaces omit labels, plus title/value for larger presentations. Keep state accurate after interaction, completion, and remote changes; distinguish ongoing duration from confirmed completion. Configure required parameters when added and allow later changes. Redact private titles/values while locked and require authentication for security-sensitive actions. A locked camera experience is capture-only until unlocking for further work; preserve UI continuity. Do not promise Controls on watchOS/tvOS/visionOS.

Implement the control/configuration/state binding or provide an action-state/authentication contract; reviews identify exact wrong-state or locked-disclosure defects. Keep a proposed UI change separate from unverified access-control enforcement.

**Worked transformation:** Before: a garage control displays “Open” immediately on press, leaks the home name while locked, and never reflects a remote close. Decision: request acceptance differs from device state and locked text is private. After: expose an understandable symbol, authenticated action, pending/confirmed behavior, redacted text, and updates from authoritative remote changes.

Deliver the artifact, surface variants, configuration, authoritative state, and locked/auth rules. Verify remote change, failed action, reconfiguration, locked state, and symbol-only comprehension. Fail for falsely confirmed state, unauthenticated sensitive action, or private locked text. Report native Control Center/Action-button/security execution separately from logic inspection.

Load [widgets](../apple-hig-widgets/SKILL.md) for information, [live-activities](../apple-hig-live-activities/SKILL.md) for bounded progress, or [privacy](../../../apple-hig-foundations/.topics/apple-hig-privacy/SKILL.md) for sensitive handling.
