---
name: apple-hig-managing-notifications
description: Use when creating, reviewing, or adapting notification permission, urgency, Focus behavior, and informational or marketing preferences.
---

# Preserve the person's control over interruption

Read [the notification-management guide](../../references/managing-notifications.md). The workflow is application advice; delivery levels and entitlements are source constraints, not guaranteed delivery.

Inspect event categories, personal impact/timing, consent history, preference UI, platform, and create/review/adapt mode. Distinguish communication from noncommunication and marketing from requested information. Record permission/entitlement evidence; do not infer it from an urgent-looking mockup.

Request consent and respect later silencing/Focus/summary choices. Assign Passive/Active/Time Sensitive/Critical from real urgency rather than business attention goals. Time Sensitive concerns immediate personal impact now/within an hour and remains user-controllable; Critical needs the entitlement and an actual urgent health/safety case. Marketing requires separate explicit content-specific opt-in with accept/decline and must never be Time Sensitive. Provide in-app settings for informational/marketing preferences without pretending they override system settings. Use sender-based supported communication integration when relevant. Watch generally follows companion settings with its documented controls.

Implement authorized category/permission/settings behavior, specify an event/urgency/consent matrix, or review exact overclassification and consent defects. Do not send actual notifications merely to demonstrate a proposed policy without authorization.

**Worked transformation:** Before: a shopping app labels every discount Time Sensitive after a generic permission prompt and offers no marketing opt-out. Decision: sales urgency is not immediate personal impact and permission is not specific marketing consent. After: use appropriate ordinary delivery only after explicit promotional opt-in, with independent preference changes and respect for Focus.

Deliver the artifact, event rationale, interruption level, consent source, and preference routes. Verify denied/revoked permission, Focus, opt-out, nonresponding recipients, and entitlement absence. Fail for marketing breakthrough, implied guaranteed delivery, or inaccessible preference withdrawal. Native Focus/delivery/entitlement execution requires separate evidence.

Load [notifications](../../../apple-hig-system-experiences/.topics/apple-hig-notifications/SKILL.md) for content/actions or [privacy](../../../apple-hig-foundations/.topics/apple-hig-privacy/SKILL.md) for consent and exposure.
