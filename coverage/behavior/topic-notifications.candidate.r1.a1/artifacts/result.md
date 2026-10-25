# Appointment reminder repair

Patched `interface.md` in place, replacing the original one-paragraph problem statement with a concrete iPhone notification specification. It now defines exact copy, privacy boundaries, delivery policy, deduplication, action transitions, appointment deep linking, denied-permission recovery, and acceptance criteria.

## Decisions and support

- Remove diagnosis and other appointment details from every notification presentation and payload. A generic hidden-preview category provides another layer. This applies [Notifications — Best practices and Content](https://developer.apple.com/design/human-interface-guidelines/notifications#Content); private details remain behind authorized app access, following [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy).
- Send one reminder per appointment schedule version; dismissal and nonresponse never trigger repeats. This applies [Notifications — Best practices](https://developer.apple.com/design/human-interface-guidelines/notifications#Best-practices). The 24-hour trigger and no catch-up policy are explicit product choices, not HIG mandates.
- Ordinary activation resolves the exact appointment. `Acknowledge` updates only reminder state, with authentication, ownership/version validation, and idempotency. No notification cancellation action or redundant Open App action is offered. This applies [Notifications — Notification actions](https://developer.apple.com/design/human-interface-guidelines/notifications#Notification-actions) and [Writing — Best practices](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices).
- Use Active urgency and honor system delivery controls. A routine reminder does not establish a critical health event. Preserve the in-app appointment route when authorization is denied or revoked; ask only when reminders are invoked. See [Managing notifications — Integrating with Focus](https://developer.apple.com/design/human-interface-guidelines/managing-notifications#Integrating-with-Focus) and [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission).
- Specify foreground updates without duplicate interruption and choose no badge. The latter is a product choice avoiding an unnecessary count; HIG permits meaningful unread-notification badges.

## Worked before/after

Illustrative fixture, not a real patient record: appointment A42, version 1, tomorrow at 10:00, booked.

| Step | Before, as described in the supplied brief | Revised contract |
| --- | --- | --- |
| Lock Screen | Full diagnosis exposed; exact original wording was not supplied | Title: `Appointment Reminder`. Body: `You have an upcoming appointment. View the details in the app.` Hidden-preview description: `Appointment reminder`. No diagnosis in payload |
| Person dismisses | Repeats every minute | No repeat for A42/version 1; booking stays booked |
| Person opens | Generic home screen | Authenticate if necessary, validate ownership, open A42 details |
| Person acknowledges | Appointment canceled | Reminder becomes acknowledged, presentation clears, A42 stays booked |
| Permission denied | Denial is possible; fallback unspecified | Appointments remain available; settings explain notifications are off and offer system settings recovery |

## Acceptance checks and results

Passed — static review of the revised specification:

- Exact generic title, body, preview-hidden description, and action label are present; disclosure is prohibited even when previews are enabled.
- Deduplication key, no-repeat rule, reschedule/cancellation cleanup, and foreground behavior are explicit.
- Deep-link success, sign-in continuation, wrong-account/missing record, cancellation, stale version, and load-failure outcomes are defined.
- All reminder interactions explicitly preserve booking state; acknowledgment is idempotent and failure cannot report success.
- Denied/revoked permission, preference withdrawal, return from Settings, and an in-app fallback are specified.

Failed — supplied starting specification: diagnosis disclosure, repeat interruption, generic-home activation, and acknowledgment canceling a booking. These are reported by the brief, not independently observed runtime defects.

Not executed — native acceptance checks required after implementation:

- On iPhone, inspect locked/unlocked and expanded notifications with previews enabled/hidden; inspect payloads and logs for private content.
- Deliver duplicate events, dismiss, ignore, acknowledge twice, reschedule, cancel, and simulate offline failures; verify one event does not repeat and booking records remain unchanged by reminder actions.
- Test activation and actions while signed out, on the wrong account, with stale/missing records, and after failed network loads.
- Deny and revoke authorization, disable reminders, and return from Settings; verify continued appointment access and pending-reminder cleanup.
- Exercise Focus, scheduled summaries, silent mode, foreground delivery, authentication, text enlargement, and VoiceOver on the actual implementation. Check copy fits and essential meaning survives without sound.

## Evidence and limits

Read the installed root `.agents/skills/apple-hig/SKILL.md` explicitly, then searched `references/topic-index.md`. Read the System experiences family and Notifications procedure; Patterns family and Managing notifications procedure; Foundations family and Privacy and Writing procedures. Each procedure was read before its corresponding local reference article. Each file read used its own command. All paths were resolved inside the installed apple-hig package.

Only `interface.md` and installed local guidance supplied the evidence. Official links above identify the sources named by the local snapshot; no web browsing occurred. The package describes itself as independent, dated guidance rather than an SDK reference. No source code, payload sample, screenshot, existing schedule, framework, or booking API was supplied. Timing and lifecycle rules are proposed product decisions. Device, SDK, GUI, notification delivery, security enforcement, localization, and accessibility execution were not performed or established. This work completes the requested specification repair, not a running application implementation or privacy certification.
