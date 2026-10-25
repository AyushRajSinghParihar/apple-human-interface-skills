---
name: apple-hig-notifications
description: Use when creating, reviewing, or adapting notification content, previews, actions, badges, foreground treatment, and watch looks.
---

# Make the notification useful before opening the app

Read [the notification guide](../../references/notifications.md). This workflow is application advice; delivery remains subject to consent and system/user settings.

Inspect event value/timeliness, consent/category, sensitive content, foreground context, actions, platform, and create/review/adapt request. Distinguish communication from generic updates and one event from duplicate reminders. Record real badge/account/action state; do not assume delivery or permission from mock notification text.

Write concise contextual titles/bodies with a generic private-preview description. Avoid repeating app identity or exposing confidential details. Provide useful simple actions with outcome labels and no redundant Open App; mark consequential destruction. Keep essential meaning independent of sound. In foreground integrate updates into the current UI instead of duplicating interruption. Badge unread notifications only, update/clear addressed counts promptly, and preserve an in-app route when badges are disabled.

Implement content/category/action/badge handling or supply an event-to-presentation contract; reviews identify exact disclosure, duplication, or action defects. On watch short looks must be discreet, long looks preserve system structure and static fallback, and the likely nondestructive first action should fit supported double tap. Do not promise custom vibration through this guidance.

**Worked transformation:** Before: a banking notification exposes an account balance on Lock Screen, badges show the balance, and `Open App` repeats ordinary activation. Decision: private data and badge semantics are misused. After: provide a generic transaction category when previews hide, use unread count only, and offer a truly useful safe action or rely on precise ordinary activation.

Deliver the artifact, preview-hidden text, actions/deep links, foreground behavior, and badge lifecycle. Verify locked previews, duplicate events, action resolution, addressed counts, and watch fallback where relevant. Fail for confidential exposure, unrelated badge values, duplicate interruption, or wrong-object action. Separate native delivery/permission/sound checks from inspected logic.

Load [managing-notifications](../../../apple-hig-patterns/.topics/apple-hig-managing-notifications/SKILL.md) for permission/urgency strategy or [alerts](../../../apple-hig-presentation/.topics/apple-hig-alerts/SKILL.md) for immediate error resolution.
