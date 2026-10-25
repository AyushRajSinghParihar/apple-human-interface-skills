---
name: apple-hig-activity-views
description: Use when designing, reviewing, or adapting system sharing, custom activities, and share or action extensions.
---

# Share the current content through its context

Read [the activity-view guide](../../references/activity-views.md). The procedure is application advice; distinguish activity views from Mac share/action extensions.

Inspect the content types, selection, Share entry point, target platform, and create/review/adapt request. Determine whether a proposed extension transfers information elsewhere or acts on it in context. Record available content and current task eligibility; do not assume every system destination supports every payload.

Use the standard Share button and system presentation where supported. Offer only relevant custom activities, avoid duplicate system actions, and name specialized variants distinctly with concise verbs. Do not prescribe system task order, which the app cannot control. Choose a familiar composition view; if custom UI is necessary keep it short and related to the host app. An extension is already modal, so avoid another modal except a necessary alert.

Implement the share payload/activities, deliver a payload-to-destination/action specification, or review exact relevance and handoff failures. If work continues after dismissal, specify background continuation and status in the main app; notify for problems rather than routine completion. On Mac use supported share/action extension entry points without claiming a Mac activity-view component; tvOS/watchOS lack activity views.

**Worked transformation:** Before: a document share sheet adds branded `Acme Print`, duplicates Print, and closes only after a large upload finishes. Decision: the custom action is redundant and long work should not trap the extension. After: retain system Print, name the distinct transfer `Send for Approval`, dismiss after accepting the task, and surface its status/problem in the app.

Deliver the artifact plus payload, custom eligibility, dismissal, and continuation contract. Verify with the actual selected content, unavailable destinations, cancellation, and post-dismissal work. Fail for missing payload, duplicate misleading actions, nested modal traps, or claimed ordering control. Separate extension execution from inspected specification.

Load [collaboration-and-sharing](../../../apple-hig-patterns/.topics/apple-hig-collaboration-and-sharing/SKILL.md) for permissions or [modality](../../../apple-hig-patterns/.topics/apple-hig-modality/SKILL.md) for extension exits.
