# Revised iPhone weather notification settings

## Basis and decisions

The supplied `interface.md` says the toggle is labeled “Enable not off?”, switching immediately deletes history, a pending network failure leaves it falsely On, and storm alerts and daily summaries are separate settings. No implementation, screen, stored values, or backend contract was supplied.

Use an in-app **Settings → Notifications** screen with two labeled list rows, each containing an iOS-style switch:

| Label | Supporting text | Meaning when On |
| --- | --- | --- |
| Storm alerts | Notifications about storms. | Storm notifications are requested. |
| Daily summaries | A daily weather summary. | Daily summary notifications are requested. |

These are independent Boolean preferences. All four combinations are valid. There is no master switch, radio group, or implicit dependency between them. Keep each label unchanged when its value changes; remove “Enable not off?”. Show On/Off through switch position and shape as well as color; retain the usual green On appearance unless a concrete need justifies an alternative. This follows the iOS list-row guidance in [Toggles — platform considerations](https://developer.apple.com/design/human-interface-guidelines/toggles#Platform-considerations). Positive, concrete labels and nearby recovery text follow [Writing — best practices](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices).

Changing either preference must never delete weather history, notification history, or the other preference. Deletion is outside this interaction. A switch represents persistent state, rather than a destructive command ([Toggles — best practices](https://developer.apple.com/design/human-interface-guidelines/toggles#Best-practices)). This removal of the side effect is a product decision applying that distinction.

These are app-wide notification-category preferences. Keep their access in the app's settings; reopening restores persisted values rather than screen defaults ([Settings — general settings](https://developer.apple.com/design/human-interface-guidelines/settings#General-settings)). Product default for a new installation: both Off until deliberately enabled. Preserve existing confirmed values during migration; the brief does not establish how the old ambiguous value maps to either category, so never infer that mapping or enable both from it.

## State and persistence contract

Maintain separate state per category:

```
confirmed: Boolean or unknown
phase: loading | ready | saving | reconciling | error
requested: Boolean or none
operationId: unique identifier or none
```

The switch position always represents the last confirmed persisted value. It must not move to the requested position just because a request started. A nearby status identifies an outstanding change, for example “Turning on…” or “Turning off…”. Disable repeat activation of that row while saving or reconciling; the other row remains independently usable. No Apply or Save step is required.

| Event | State and visible result |
| --- | --- |
| Open screen | Load confirmed values; show “Loading…” with unavailable switches until values are known. Do not flash Off as a placeholder. A load error shows “Couldn’t load notification settings. Try again.” and permits another load. |
| Activate a ready switch | Submit an absolute assignment for this category only, with a unique operation ID. Retain its confirmed position and show the pending target in text. |
| Persistence acknowledged | Update confirmed to the acknowledged value, clear pending status, and enable the row. Store the confirmed value durably. |
| Definitive rejection with no write | Keep confirmed unchanged. Show, for example, “Couldn’t turn on storm alerts. Storm alerts are still off. Try again.” Repeat activation retries the intended change. |
| Timeout, lost response, or interrupted request | Do not assume failure means no write. Enter reconciling and show “Checking storm alert setting…”. Resolve the operation and read authoritative state before enabling another mutation of that row. |
| Reconciliation unavailable | Retain last confirmed position, mark it “Last confirmed: Off. Current setting couldn’t be verified. Try again.” The row remains unavailable for mutation; retry reconciliation through the nearby recovery action. Never present the stale position as verified current state. |
| Leave screen or app interruption | Persist the pending operation metadata. Do not treat navigation as cancellation or report success. On return, reconcile unresolved operations before accepting another change to that category. |

Recovery text substitutes the correct category and target in both directions. Ordinary errors appear inline beside the affected row and remain until retried or resolved; they do not erase the other row's status.

Framework-agnostic mutation contract:

```
change(category):
    require phase[category] == ready or definitiveFailure
    target = not confirmed[category]
    persistPending(category, target, uniqueOperationId)
    showSaving(category, target)   // switch retains confirmed position
    assignPreference(category, target, operationId)

onAcknowledgement(category, operationId, authoritativeValue):
    ignore responses belonging to an older operation
    persistConfirmed(category, authoritativeValue)
    clearPending(category)
    renderReady(category)

onUnknownOutcome(category, operationId):
    reconcile operationId and authoritative category value
    // retry must reuse the idempotency key, never invert server state
```

The persistence service must support category-specific absolute writes and idempotent retry, or an equivalent serialization/version mechanism. A read cannot settle an unknown outcome while the original write could still commit afterward. Reconciliation must establish that the operation completed or cannot later apply. If the available service cannot provide this guarantee, keep the outcome visibly uncertain and record this as an implementation blocker. Never overwrite both preferences with a stale full-settings object.

## System permission and delivery

Category preference and system authorization are separate facts. Detect authorization on entry and on return from system Settings. Saving a preference is not evidence that permission was granted or that a notification will arrive.

If authorization has not been requested, an explicit first enable intent may initiate the system permission flow in context. Resolve that flow before applying the requested enable; on denial or dismissal, leave that category's prior confirmed value unchanged and explain that notifications need system permission. A new enable intent is required to retry. Existing preferences survive later permission revocation.

When permission is denied or revoked, show “Notifications are turned off in system Settings.” Provide a route labeled “Open Settings” where the host supports it; otherwise provide clear manual guidance. Keep category choices editable and label the screen “Preferences are saved, but notifications need system permission.” Regranting permission does not silently enable an Off category. Unknown authorization shows “Notification permission couldn’t be checked.” Do not request permission repeatedly on screen entry.

| Category | Consent and interruption policy |
| --- | --- |
| Storm alerts | Explicit category enable plus system authorization. Ordinary Active delivery by default; only an event with verified immediate personal impact now or within an hour is a candidate for Time Sensitive. The brief supplies no such event evidence. |
| Daily summaries | Explicit category enable plus system authorization. Passive delivery is the proposed product policy because summaries are leisurely information. |

Respect Focus, scheduled summaries, silencing, and withdrawal. Do not promise immediate delivery or Critical alerts; no Critical entitlement is evidenced. These boundaries follow [Managing notifications — Integrating with Focus and best practices](https://developer.apple.com/design/human-interface-guidelines/managing-notifications#Integrating-with-Focus). Exact event eligibility and permission integration remain implementation dependencies.

## Worked before / after

**Before, as reported:** A person activates “Enable not off?”. History is immediately deleted. The network operation fails or remains unresolved, but the switch looks On. The label does not explain the enabled behavior.

**After, illustrative initial values:** Storm alerts Off, Daily summaries On, history contains 12 records, system authorization granted.

1. Activate Storm alerts. Its switch remains Off with “Turning on…”. Daily summaries stays On and usable; history remains at 12 records.
2. The service rejects the write definitively. Storm alerts remains Off with “Couldn’t turn on storm alerts. Storm alerts are still off. Try again.”
3. Activate Storm alerts again. On acknowledgment it becomes On. Daily summaries remains On; history remains at 12 records.
4. Turn Daily summaries Off. Only after acknowledgment does that switch become Off; Storm alerts remains On.
5. If step 3 instead times out after a server commit, show “Checking storm alert setting…”. Reconciliation can confirm On without a duplicate mutation. If reconciliation cannot finish, show the last-confirmed value explicitly as uncertain rather than claiming Off or On is current.

The initial values and record count are worked-example fixtures, not observations of an app.

## Acceptance checks and evidence status

**Passed — specification inspection:** Two separately named Boolean settings are defined; all four combinations are valid. The specification removes destructive side effects, defines both mutation directions, separates confirmed/pending/unknown state, and distinguishes preferences from system permission. Root, owning families, topic procedures, and supporting guides were read from the installed package, with each read command consuming one file.

**Failed — supplied interface, based on its textual report:** Label meaning is ambiguous; preference changes delete history; displayed On state can contradict the applied result. These are reported defects, not reproduced runtime failures.

**Not executed — implementation acceptance:**

- Exercise Off/Off, Off/On, On/Off, and On/On. Changing either category must preserve the other's value and history contents, including under simultaneous requests and out-of-order responses.
- Test On→Off and Off→On with slow success, definitive rejection, offline failure, timeout before commit, timeout after commit, and stale responses. Pending targets must be explicit; a switch must never imply an unconfirmed successful write.
- Retry an uncertain write using the same operation ID. Verify no inversion, duplicate effects, late overwrite, or stale full-object write occurs.
- Navigate away, terminate, and reopen during saving and reconciliation. Confirm persisted values and unresolved operation metadata are restored; failed loading must not masquerade as Off.
- Test fresh installation, known existing preferences, and ambiguous legacy data. Verify no unrequested enablement or history deletion.
- Test unrequested, granted, denied, revoked, and unknown authorization, including returning from system Settings. Verify independent preferences persist, denial has a remedy, and no repeated unsolicited prompt appears.
- Verify Focus and scheduled-summary behavior, absent Critical entitlement, and category opt-out gating future notification generation. No delivery guarantee may appear in copy.
- In an actual rendered implementation, verify both states are distinguishable without color; labels, pending state, errors, and recovery remain understandable at larger text sizes and through assistive technology. Verify control value announcements and input behavior separately.

## Evidence limits and source route

Work used only `interface.md` and installed local instructions. No web browsing, Apple SDK, device, simulator, GUI, network service, notification delivery, or accessibility execution occurred. Acceptance checks above are requirements, not passed tests. The local guides are dated 2026-10-25 and describe themselves as original guidance derived from Apple sources; their presence does not establish independent review or current API availability. Official links identify source guidance and were not opened.

Installed package root: `.agents/skills/apple-hig/`. Read `SKILL.md`, searched `references/topic-index.md`, then read each owning family before its topic procedures and the corresponding references:

- `subskills/apple-hig-selection-and-input/SKILL.md` → `.topics/apple-hig-toggles/SKILL.md` → `references/toggles.md`.
- `subskills/apple-hig-patterns/SKILL.md` → `.topics/apple-hig-settings/SKILL.md` and `.topics/apple-hig-managing-notifications/SKILL.md` → `references/settings.md` and `references/managing-notifications.md`.
- `subskills/apple-hig-foundations/SKILL.md` → `.topics/apple-hig-writing/SKILL.md` → `references/writing.md`.

Default values, migration conservatism, history preservation, pessimistic commit presentation, and retry/reconciliation mechanics are concrete product decisions applying the guidance, not claims of Apple-mandated API behavior. Backend guarantees, existing consent, event classification, and host permission/settings capabilities remain unverified.
