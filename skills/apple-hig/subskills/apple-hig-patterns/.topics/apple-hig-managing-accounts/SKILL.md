---
name: apple-hig-managing-accounts
description: Use when creating, reviewing, or adapting account necessity, authentication, deletion, subscription explanation, or TV-provider account flows.
---

# Match account friction to the committed task

Read [the account guide](../../references/managing-accounts.md). This workflow is application advice; verify current legal obligations separately rather than treating the guide as legal advice.

Inspect core versus optional account needs, authentication methods/capabilities, creation/deletion routes, subscriptions, platform, and create/review/adapt request. Record actual supported methods and retention behavior; do not advertise Face ID or passkeys from a design alone.

Allow useful unregistered access when accounts are not essential and defer sign-in until needed. Explain benefits/requirements briefly. Evaluate Sign in with Apple or platform-supported passkeys and preserve appropriate stronger password authentication where retained. Avoid redundant biometric opt-in and misuse of device-passcode terminology. If creation exists, expose real deletion rather than deactivation or a buried policy link. Explain timing, required retention, immediate versus scheduled choice, token revocation for Sign in with Apple, and completion notification. Deletion does not cancel Apple auto-renewable billing: provide separate management guidance and allow deletion even for externally purchased subscriptions.

Implement authorized account UI/state, specify create/auth/delete/subscription outcomes, or review exact dead-end and misleading-capability defects. Do not delete real accounts or subscriptions without authorization. On TV reduce remote entry, preserve current profiles, and route system TV-provider sign-out through Settings rather than independent sign-out. Watch can use credential/settings synchronization.

**Worked transformation:** Before: a recipe app requires signup before browsing and its “Delete” button only deactivates, promising billing stops. Decision: optional access is gated and deletion/subscription semantics mislead. After: allow browsing, defer authentication to account work, and provide explicit deletion plus separate subscription management with honest completion timing.

Deliver the artifact and access/auth/deletion/billing contract. Verify guest, missing capability, linked account, active subscription, and deletion completion states. Fail for deletion absent despite creation, falsely canceled billing, or unsupported biometric claims. Backend enforcement/legal requirements/native authentication need separate evidence.

Load [sign-in-with-apple](../../../apple-hig-technologies/.topics/apple-hig-sign-in-with-apple/SKILL.md), [privacy](../../../apple-hig-foundations/.topics/apple-hig-privacy/SKILL.md), or [onboarding](../apple-hig-onboarding/SKILL.md) as appropriate.
