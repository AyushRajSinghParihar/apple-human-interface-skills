# Revised notification preferences

This is a framework-agnostic design contract for the iOS/macOS shared project app. The only product evidence is `interface.md`: one global toggle combines urgent assigned-task alerts and marketing, claims to override system settings, requests permission before a project exists, and ignores quiet hours. No implementation or screen was supplied. The choices below replace that behavior; they are not claims about an existing implementation.

## Decisions and screen contract

Preferences belong to the signed-in recipient, across their projects, and never alter teammates’ preferences. Product decision: category preferences and quiet hours sync across that recipient’s devices; operating-system authorization remains device-specific. Project-specific overrides are outside this revision.

Entry: iOS app Settings → Notifications, with normal Back navigation. macOS app menu → Settings (Command-Comma) → Notifications; restore the last visited pane, titled Notifications. Keep project context intact when returning. Use a stable settings surface rather than a modal onboarding requirement. These placements follow [Settings](https://developer.apple.com/design/human-interface-guidelines/settings#Best-practices) and its [macOS guidance](https://developer.apple.com/design/human-interface-guidelines/settings#macOS).

Display, in order:

1. **Notifications on this device** — read-only current authorization summary: “Not requested,” “Allowed by system,” “Blocked in system settings,” or “Status unavailable.” Never infer delivery from authorization. Below it: “Your device controls notification delivery, Focus, sounds, and scheduled summaries. These app preferences cannot override those choices.” For not-requested status show **Set up device notifications**. For denied/revoked status show **Open system notification settings**, with manual navigation instructions if a supported link is unavailable. Unknown status exposes Retry; preferences remain editable.
2. **Project notifications** — independent **Assigned-task alerts**, initially on for new users. Helper: “Updates about tasks assigned to you. Device alerts also depend on system settings.” This does not imply marketing consent or guaranteed delivery.
3. **Marketing** — independent **Product news and offers**, initially off. Helper: “Optional notifications about new features, plans, and offers.” Enabling opens an ordinary content-consent editor: “Receive product news and offers as device notifications?” with **Receive news and offers** and **No thanks**. Only affirmative confirmation stores consent. Cancellation leaves off. This is a marketing decision, not a custom pre-permission screen. Turning off withdraws immediately without confirmation.
4. **Quiet hours** — **Use quiet hours**, initially off for new users; preserve any known existing schedule. When enabled, show **From**, **Until**, and “Every day · [device time zone]. During quiet hours, device alerts pause, including assigned-task alerts. Project activity remains available when you open the app.” New schedule editor starts with a proposed 22:00–08:00; it takes effect only on Save. No bypass setting is offered.

Use labeled row switches on iOS and independent checkboxes in the macOS window body. No aggregate master switch is needed. On/off must be perceptible through control state and text/shape, not color alone. A control expresses app preference even if system authorization is blocked; show the block separately rather than falsifying or disabling the preference. This follows [Toggles](https://developer.apple.com/design/human-interface-guidelines/toggles#Best-practices), including its iOS/macOS distinctions.

## Consent, scope, and delivery policy

System permission is not marketing consent. Do not request authorization on launch, project creation, or receiving an assignment alone. After joining/creating a first project, the ordinary project screen may offer “Get device alerts for tasks assigned to you” linking to these settings. Work remains available if ignored. **Set up device notifications** invokes the system request only following deliberate activation and only when status is not requested. Use the existing context; add no custom pre-alert. Decline leaves project access and in-app activity available. Never automatically repeat a denied request; explain the system-settings route. Returning from system settings refreshes status without changing saved preferences. See [Privacy: Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission).

| Event | App consent gate | Requested interruption level | Rationale |
| --- | --- | --- | --- |
| Assigned-task update, even if labeled urgent | Assigned-task preference | Active | An urgent label alone does not establish immediate personal impact |
| Product news or offer | Separate recorded explicit marketing consent and preference on | Passive | Optional leisurely information; never Time Sensitive |

Both categories also require system authorization, eligibility for the current recipient, and being outside quiet hours. No Critical entitlement is evidenced; do not request Critical delivery. Time Sensitive is also excluded from this revision. A future proposal would need evidence of direct personal impact now or within an hour, separate user control, and continued respect for system choices. Focus and summaries may delay or silence permitted alerts; do not claim guaranteed arrival, silent-mode override, or escalate because someone has not responded. The policy follows [Managing notifications](https://developer.apple.com/design/human-interface-guidelines/managing-notifications#Integrating-with-Focus) and [Sending marketing notifications](https://developer.apple.com/design/human-interface-guidelines/managing-notifications#Sending-marketing-notifications).

Store only the needed preference values and marketing consent category, version, timestamp, and affirmative source. System permission stays device-local. Assignment routing uses existing project membership/assignment data; this flow requests no contacts, tracking, or additional project data. Server-side delivery needs recipient preferences and event eligibility, not Focus contents. This is a proposed minimum data contract, not a security or legal certification; see [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices).

## State, persistence, and quiet-hour semantics

Binary changes save immediately, except marketing opt-in and schedule editing. While saving, expose “Saving…” and prevent repeated writes to that same control. Only acknowledged persistence shows “Saved.” On failure restore the last confirmed value and show persistent inline “Couldn’t save. Try again.” with Retry. Independent categories retain their values. Do not silently treat an unconfirmed marketing opt-in as consent.

Quiet hours use daily wall-clock minutes, 00:00–23:59, start inclusive and end exclusive. Store start/end and the enabled flag; evaluate in the receiving device’s current time zone. Device zone changes update the visible zone and evaluation. Across midnight, 22:00–08:00 means minute >= 1320 OR minute < 480. Equal endpoints are invalid: “Choose different start and end times.” Never interpret equal endpoints silently as zero or 24 hours. All minutes are reachable. Localize 12/24-hour display; store minutes independently of formatting. On macOS permit precise textual time entry; on iOS use an adjacent time editor with equivalent accessible input. These choices follow [Pickers](https://developer.apple.com/design/human-interface-guidelines/pickers#Best-practices); no SDK style or API is assumed.

Schedule edits are a draft with Save and Cancel. Save validates the pair atomically; invalid entry retains the draft and identifies its field. Cancel restores the saved pair. Switching apps preserves the draft; Back/closing the editor cancels uncommitted edits. Enabling quiet hours for the first time opens this editor; cancellation leaves it off. Disabling retains the saved schedule for later reuse.

During a spring clock gap, evaluate the actual local time after the jump; during a repeated autumn hour, the same wall-clock rule applies on both occurrences. Quiet hours suppress new app-controlled external alerts rather than building a burst for the end time. Task activity remains in the app; marketing suppressed during the interval expires. Do not replay suppressed task alerts automatically. These scheduling rules are product decisions, not HIG mandates.

Framework-agnostic policy:

```text
on event for recipient/device:
    if recipient no longer eligible: suppress
    if category preference is off: suppress
    if marketing and explicit category consent absent: suppress
    if system authorization is not allowed: suppress external alert
    if quietHours.enabled and withinQuietHours(device.localTime): suppress external alert
    otherwise: request ordinary category delivery; system decides presentation

withinQuietHours(time):
    m = time.hour * 60 + time.minute
    require start != end
    return start <= m < end if start < end else m >= start or m < end
```

Check the latest confirmed policy before enqueueing and again before controllable delivery; cancel pending app-controlled alerts when a preference turns off or quiet hours begin. Already presented notifications cannot be promised retractable. If the stack cannot enforce scheduling or revalidation at its delivery boundary, that is an implementation blocker: do not ship copy promising quiet hours until it can. Permission changes, offline writes, and stale synchronization must not cause marketing delivery without confirmed opt-in. Migration preserves known informational intent; marketing defaults off unless explicit content-specific consent is evidenced. A legacy mixed toggle is insufficient evidence of marketing consent.

## Platform and access contract

On iOS preserve swipe-back, selected project, and scroll context across orientation and app switching. On Mac provide a complete keyboard path through settings, category controls, schedule fields, Save/Cancel, and recovery; switching apps retains the active draft. Resizing must keep all actions reachable through scrolling. This applies [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices) and [Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Best-practices), without assuming native integration exists.

Expose names, roles, values, disabled/busy states, and grouped helper/error text for every control. Logical traversal follows the screen order, then local editor field order. Preserve focus on save failure; associate the error with the affected setting and make it perceivable without sound. Support at least 200% text enlargement without truncating labels, values, or actions. Start with platform default activation areas: iOS 44 × 44 pt, macOS 28 × 28 pt, with sufficient separation. Measure actual contrast in light/dark and Increase Contrast configurations. These are implementation acceptance targets from [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision) and [Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility), not measurements of supplied UI.

## Worked before/after

**Before (supplied behavior):** Alex disables the global toggle to stop promotions. Assigned-task alerts stop too; the UI claims this setting overrides system choices. Permission had already been requested before Alex had a project. A 23:00 urgent assignment ignores quiet hours.

**After (specified scenario):** Alex joins Project Atlas with device permission not requested. No system prompt appears. In Notifications, Alex leaves Assigned-task alerts on, declines Product news and offers, and deliberately selects Set up device notifications. After system approval, status reads Allowed by system. Alex saves quiet hours 22:00–08:00. At 23:00 an assignment is recorded in project activity but produces no device alert. At 08:00 there is no alert backlog. A fresh eligible assignment at 09:00 requests Active delivery; Focus may still delay it. Promotions remain suppressed. If Alex later revokes system permission, the app shows Blocked in system settings while retaining the independent app preferences.

## Acceptance checks and evidence limits

**Passed — document inspection only:** Read the installed root skill, relevant family routes, topic procedures, then their local source guides, one file per command. The revised contract separates consent, defines device authority, postpones permission, specifies quiet hours, and includes recovery and platform paths. No web access was used; official links identify sources from the local snapshots, not independently checked live pages.

**Failed — supplied behavior against this contract:** the combined category control, override claim, pre-project permission request, and ignored quiet hours each fail. These are failures reported by `interface.md`, not reproduced runtime defects.

**Not executed — required implementation acceptance:**

| Check | Expected observable result |
| --- | --- |
| New account / no project / ignored setup | No authorization prompt; project work remains usable |
| Allow, deny, revoke, return from system settings, status lookup failure | Truthful status; no repeated denied prompt; preferences retained; Retry available |
| Turn each category on/off; cancel/accept marketing consent | Independent settings; no promotion without affirmative consent; withdrawal stops controllable future sends |
| Legacy toggle migration | Informational intent retained when known; no inferred marketing consent |
| Focus, summary, Time Sensitive disabled, silent mode, entitlement absent | Ordinary system-controlled delivery; no unsupported bypass or escalation for nonresponse |
| 22:00, 07:59, 08:00; daytime interval; equal times; malformed time | Inclusive start/exclusive end; correct cross-midnight result; invalid drafts cannot save |
| Time-zone travel, DST gap/repeat, 12/24-hour locale | Visible zone updates; stored minute meaning retained; documented local-time rule applies |
| Quiet-hour start with pending sends; opt-out race; end of interval | Pending controllable sends canceled; no backlog burst; already delivered limits remain truthful |
| Failed/offline save, restart, cross-device sync, user/account switch | Confirmed values restored; errors recoverable; no cross-account leakage or phantom marketing consent |
| Cancel schedule, Back, interruption, reopen settings | Defined draft cancellation; app-switch draft retained; last pane and project context restored |
| Keyboard and assistive input; 200% text; rotation/resizing | Entire task reachable; correct announced names/values; no lost content/actions |
| Geometry, light/dark contrast, Increase Contrast, actual device use | Measured readable controls and comfortable activation; no color-only state |

No device, GUI, SDK compilation, notification delivery, Focus, entitlement, accessibility-tool, or assistive-technology execution occurred. No screenshots, source code, persistence implementation, consent records, or backend delivery capabilities were provided. Local guides are dated application guidance derived from Apple HIG, not SDK documentation; their existence does not establish independent review or current API availability. Platform adapters, delivery scheduling capability, synchronization behavior, and the acceptance scenarios above require implementation evidence before release.
