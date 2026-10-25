---
name: apple-hig-live-activities
description: Use when creating, reviewing, or adapting bounded live-event progress, compact and expanded presentations, updates, actions, and ending behavior.
---

# Give the live event a start and an end

Read [the Live Activities guide](../../references/live-activities.md). This workflow is application advice; destination layouts and interaction support differ.

Inspect event duration/start/end, update source, sensitivity, destinations, platform, and create/review/adapt intent. Decide whether the information is a bounded task with frequent changes or ordinary periodic widget data. Record real update/termination signals; a timer mockup is not a delivery guarantee.

Design essential iPhone compact/minimal/expanded/Lock Screen content first, retaining identity/relative positions as it expands, then tailor other destinations. Keep minimal content informative rather than a static logo. Use supported background customization only in Lock Screen, with appropriate dark/tint/Always On contrast. Favor one essential direct action and precise deep links. Protect sensitive content, omit promotion, update only changed content, and alert only for crucial updates without duplicate pushes. End immediately when the task ends and choose a useful short retained summary, not indefinite activity.

Implement the lifecycle/layouts or provide event-state/destination specifications; review exact lifecycle, privacy, or missing-presentation defects. StandBy needs scaling/red-mode checks. Watch custom layout can share CarPlay use, where controls are disabled. Mac activation uses iPhone Mirroring; tvOS/visionOS are unsupported. Do not reuse a control-dependent watch layout as a driving workflow.

**Worked transformation:** Before: a courier activity runs after delivery, exposes a full address, and requires Pause on CarPlay. Decision: the task is over, private information is excessive, and driving controls are disabled. After: end at delivery, retain a brief safe summary where allowed, show only necessary destination context, and make CarPlay status useful without interaction.

Deliver the artifact, state lifecycle, update/alert policy, all relevant presentations, and destinations. Verify multiple activities/minimal state, completion, stale updates, red/Always On, and control-disabled destinations. Fail for unbounded lifecycle, misleading status, duplicate alerts, or unsupported interaction. Actual push delivery/native rendering/device behavior requires execution evidence.

Load [widgets](../apple-hig-widgets/SKILL.md) for periodic data, [notifications](../apple-hig-notifications/SKILL.md) for separate events, or [app-shortcuts](../apple-hig-app-shortcuts/SKILL.md) for relevant initiation.
