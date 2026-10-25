# Notification preferences: revised interaction specification

## Scope and decisions

For the iOS/macOS shared project app described in `interface.md`. This is a framework-agnostic design contract, not an SDK implementation. Preferences belong to the signed-in person; changing them never changes teammates’ preferences or project activity history.

The supplied interface bundles urgent assigned-task alerts with marketing, requests permission before a project exists, claims an app toggle overrides system settings, and ignores quiet hours. Replace that global toggle with independent content choices, contextual authorization, and an explicit delivery policy.

HIG-backed decisions:

- Separate informational preferences from marketing. Marketing requires explicit, content-specific acceptance and an equally clear decline; system authorization is not marketing consent. Never use Time Sensitive for marketing. [Managing notifications — Sending marketing notifications](https://developer.apple.com/design/human-interface-guidelines/managing-notifications#Sending-marketing-notifications)
- Respect system authorization, Focus, scheduled summaries, and later silencing. App preferences control what the app submits; they cannot grant authorization or guarantee presentation. [Managing notifications — Integrating with Focus](https://developer.apple.com/design/human-interface-guidelines/managing-notifications#Integrating-with-Focus)
- Ask for permission when the person invokes notification functionality, after its purpose is clear. Project creation and ordinary work remain available after refusal. [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission)
- Keep personal app-wide preferences in app Settings; expose a route from project context to the same preferences. On macOS support App menu → Settings and Command-Comma, and restore the last settings pane. [Settings](https://developer.apple.com/design/human-interface-guidelines/settings)
- Use labeled switch rows on iOS and independent labeled checkboxes in the macOS settings body. Show state through position/checkmarks as well as color. Permission requests are commands, not switches. [Toggles](https://developer.apple.com/design/human-interface-guidelines/toggles)

Product decisions, rather than Apple requirements: quiet hours apply even to urgent tasks; no breakthrough option is provided; new-user task preferences default on, marketing defaults off; all task alerts initially use Active. No Critical entitlement or validated Time Sensitive use case is supplied.

## Screen and control contract

Entry: iOS app Settings → Notifications; macOS app Settings → Notifications. Project settings include “My notification preferences,” linking here with “Applies to all your projects” visible. No project-admin control changes personal consent.

Render in this order:

1. **Notifications**. Explanation: “Choose alerts for your projects. These preferences affect only you.”
2. **System delivery on this device**: read-only authorization status and a contextual action, as defined below. Helper: “Your device settings, Focus, and notification summary can silence or delay alerts.”
3. **Project alerts**: independent “Assigned tasks” and “Urgent assigned tasks” controls. Helpers: “Assignments and ordinary updates to tasks assigned to you” and “Updates marked urgent on tasks assigned to you.” Urgent events use only the urgent preference, avoiding duplicate ordinary alerts. Neither setting authorizes marketing.
4. **Marketing**: “Product news and offers,” initially off. Helper: “Occasional announcements, feature news, and promotional offers from this app.” Off → on expands an inline consent section with this description and “Accept marketing notifications” / “No thanks.” Keep off until acceptance is saved. Decline collapses the section without changing task preferences. On → off withdraws consent immediately on successful save; no confirmation or retention offer.
5. **Quiet hours**: on/off control, initially off for new users. Helper: “Pause all app notification submissions, including urgent task alerts and marketing. Project activity remains available in the app.” When on, show saved schedule and “Edit schedule.” When off, retain but deactivate the saved schedule.

There is no master switch or aggregate/mixed state. Independent controls remain editable when system authorization is denied; checked means “requested by your app preferences,” never “will appear on this device.” The status explains the unavailable delivery dependency.

Task and marketing preferences are account-wide; system authorization is per device. Quiet hours are account-wide and use a saved named time zone, shown beside the schedule. Changes synchronize across signed-in clients. Do not silently follow a traveling device’s time zone. Sign-out removes the previous account’s preference display and pending device registrations before another account can receive its notifications.

### Quiet-hours editor

Fields: Start, End, and Time zone, with Save and Cancel. Daily recurrence, no weekday selection. Default draft is 22:00–08:00 in the device’s current zone, visibly labeled; this draft does not activate until saved and enabled. Display localized 12/24-hour values; store wall-clock minutes and a named time zone, not formatted strings. Allow every minute from 00:00 through 23:59. Provide adjacent time-only selection on iOS and precise textual time entry on macOS without requiring a particular framework. Use a zone selector that displays the stored zone unambiguously. [Pickers](https://developer.apple.com/design/human-interface-guidelines/pickers)

Start is inclusive, End exclusive. Start > End crosses midnight. Reject equal times with “Choose different start and end times”; leave the editor open and the previous schedule active. Reject invalid input or unknown zones in context, without rounding or changing meaning. Save commits the whole valid schedule atomically; Cancel discards the draft. Enabling quiet hours without a saved schedule opens this editor; cancellation leaves quiet hours off.

Evaluate quiet membership by converting each current instant into the saved zone’s local wall time. Both occurrences of a repeated daylight-saving hour follow the same membership rule; skipped local minutes never occur. Release held work at the first subsequent instant outside the quiet interval. A zone edit takes effect after saving and recalculates pending releases.

### Persistence and recovery

Persist toggles immediately, without a page-level Save. Show “Saving…” for the affected row and prevent overlapping writes to it. Do not show an unqualified committed on/off state until acknowledged. On failure restore the last confirmed value and show “Couldn’t save. Try again.” with a retry action. Offline edits are not silently queued; existing confirmed preferences continue. Consent acceptance is effective only after persistence succeeds.

Version preference writes; reject stale concurrent updates, refresh the confirmed values, and explain “Preferences changed on another device. Review and try again.” Preserve an open schedule draft for review. Reopening reads confirmed preferences and restores the last pane; returning from system settings refreshes authorization independently.

## Authorization flow

No permission prompt at launch, account creation, or before joining/creating a project. After the first project is available, offer a persistent, nonmodal notification setup row in project context: “Get alerts for tasks assigned to you.” The person can ignore it and continue working. “Set up task alerts” opens these preferences; it does not itself invoke permission.

| Detected state | Status and action | Transition |
| --- | --- | --- |
| Not requested | “Device notifications haven’t been enabled.” “Enable device notifications” | Explicit activation invokes the real platform permission flow once, in this task context. |
| Allowed | “Device notifications allowed. Delivery follows your system settings.” | No repeat permission request. |
| Denied/revoked | “Device notifications are off in system settings.” “Open notification settings” | Open the supported system destination; if unavailable, show platform-specific manual instructions. Never silently request again. |
| Unknown/unavailable | “Device notification status unavailable.” “Check again” | Refresh capability; retain preferences and do not assume permission. |

Supporting copy beside the enable action: “Receive alerts about tasks assigned to you. You can change alert categories here.” No custom imitation of the system alert or extra pre-permission modal. Platform-owned prompt text is not prescribed. Denial leaves app preferences and project access intact. If a platform reports limited authorization or presentation settings, show those accurately rather than flattening them into a promise of banners or sound. Authorization changes refresh on foregrounding and return from system settings.

## Event, consent, and urgency policy

| Event | Eligibility and consent | Level | Quiet hours |
| --- | --- | --- | --- |
| Ordinary assigned-task event | Person is current assignee and member; Assigned tasks enabled | Active: ordinary timely work update | Hold |
| Urgent assigned-task event | Same recipient checks; Urgent assigned tasks enabled | Active: an “urgent” label alone does not prove immediate personal impact | Hold |
| Product news/offers | Explicit saved marketing acceptance plus current preference on | Passive: leisurely promotional information | Hold or expire campaign |
| Unassigned task or teammate who never responded to setup | No assignment eligibility; no inferred consent or repeated permission nag | No send under this policy | Not applicable |

These are noncommunication task events. Direct person-to-person messages are outside the brief and need a separate sender/communication integration design. No response to an alert does not authorize escalation, additional devices, or a higher interruption level. Time Sensitive could be considered later only for a validated immediate personal impact now/within an hour, with user control and verified platform capability. Critical is excluded: neither urgent health/safety need nor entitlement is evidenced. [Managing notifications — Best practices](https://developer.apple.com/design/human-interface-guidelines/managing-notifications#Best-practices)

Framework-agnostic dispatch contract:

```text
on event or held-event release:
  deduplicate event + recipient + delivery destination
  reload confirmed preferences, membership, assignment, event validity
  if recipient no longer eligible or event resolved/expired: discard
  if category disabled or marketing consent absent: discard
  if inQuietHours(now, savedSchedule): hold; schedule reevaluation; stop
  for each currently registered destination:
    if authorization known denied/unavailable: do not submit there
    otherwise submit once through its supported authorized delivery adapter
    record submission, not guaranteed presentation
```

Never bypass system policy using email, sound, repeated sends, or a second channel. Recheck eligibility and consent at release. Retain only the latest held state per task; release at most one current task-update summary per recipient/destination after quiet hours, rather than a burst. Do not release resolved tasks or expired marketing. Withdrawal cancels unsent matching work. Already submitted notifications cannot be promised recalled; copy and support behavior must distinguish that limit. System authorization and Focus may change after submission, and the system can defer presentation beyond the app’s schedule. Quiet hours promise control over app submission, not recall or control over system-delayed alerts.

### Data and purpose boundary

| Data/access | Purpose and boundary |
| --- | --- |
| Device notification authorization and destination identifier | Deliver selected categories to that signed-in person; request in context, never treat as marketing acceptance. |
| Preferences, saved zone, and marketing consent decision/version | Synchronize personal choices and enforce withdrawal; no collection of Focus schedules or private notification history is required. |
| Existing task membership/assignment and event identifiers | Determine eligible recipients and deduplicate; do not add contacts, location, or tracking access. |

This is a minimum design contract; storage security, retention durations, privacy disclosures, and delivery infrastructure require implementation review. The spec adds no unrelated permission request. [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy)

## Worked before/after

Before, from the brief: Alex is asked for permission before any project exists. Later, the single global control forces Alex to disable urgent-task alerts to stop marketing. Its copy claims system settings are overridden, and quiet hours have no effect.

After, illustrative trace: Alex joins Launch Plan and opens notification setup. Assigned tasks and Urgent assigned tasks are on; Product news and offers is off. Alex activates Enable device notifications and allows the system request. Alex saves quiet hours 22:00–08:00, Europe/London. At 23:15 an urgent assigned task update is held. A promotion is discarded because Alex never accepted marketing. At 08:00 the task is still assigned and unresolved, so one current update is eligible for Active submission; Focus can still silence or delay it. If Alex resolves the task at 07:50, no release occurs. Turning off Assigned tasks leaves Urgent assigned tasks unchanged. If Alex later disables notifications in system settings, the app shows that status while preserving category choices; no in-app toggle claims to reverse it.

## Acceptance checks and audit status

**Passed — document/static review:** supplied `interface.md` and installed root skill were read; relevant topic-index rows, owning families, topic procedures, then their local guides were read. This specification addresses each of the four supplied problems and defines independent categories, consent, authorization states, scheduling, persistence, and recovery. Official links above identify the local guides’ sources; they were not opened online.

**Failed — supplied design against this contract:** bundled categories/consent; misleading system-override claim; permission before project context; quiet hours ignored. These findings are based only on the brief, not executed behavior.

**Not executed — implementation acceptance scenarios:**

| Check | Required result |
| --- | --- |
| Fresh account, no project; create/join without setup | No permission prompt; work remains usable. |
| Enable explicitly; allow, deny, revoke, or return without changes | Correct refreshed status; no repeat nag or claim of guaranteed delivery. |
| Toggle each category both ways; cancel/accept/withdraw marketing | Independent confirmed state; no marketing before saved acceptance or after withdrawal. |
| Backend failure, offline save, concurrent device write, reopen | Truthful pending/error state, last confirmed value, explicit conflict recovery and persistence. |
| 21:59, 22:00, 07:59, 08:00 for overnight schedule | Submit, hold, hold, reevaluate respectively; urgent and marketing obey the same schedule. |
| Same-day schedule, midnight boundary, equal/invalid values | Correct half-open interval; invalid edits cannot replace saved schedule. |
| Locale, time-zone changes, daylight-saving repeated/skipped hours; editor cancellation | Stored semantics preserved, localized display, documented membership and release rules, no accidental commit. |
| Category disabled, consent withdrawn, assignment removed, task resolved while held | No stale release; other recipients’ choices remain unchanged. |
| Focus, scheduled summary, silent mode, Time Sensitive disabled, no Critical entitlement | No attempted breakthrough or escalation; no guaranteed-delivery claim. Actual OS behavior needs device execution. |
| Many held updates, retry, duplicate dispatch, nonresponding recipient | One current summary, deduplication, no unauthorized escalation. |
| macOS settings access/restoration; iOS switch rows; keyboard and assistive-technology inspection | Expected access, correct labels/state, independent choices, usable schedule editor; state perceivable without color. |

Evidence limits: no application code, backend, screenshots, SDK, entitlement records, device sessions, GUI interaction, or accessibility execution were supplied or performed. Runtime dispatch, native rendering, system permission UI, Focus behavior, keyboard operation, and assistive-technology announcements remain unverified. Local HIG references are an installed dated snapshot, not an SDK availability guarantee or independent source-validation result. New-user defaults and legacy migration are separate: preserve an existing global off as both task categories off; map global on to task categories on; enable marketing only with evidence of prior specific opt-in; otherwise leave it off. Preserve any valid existing quiet-hours schedule and flag invalid legacy schedules for explicit repair rather than silently ignoring them.
