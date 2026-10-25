# Pickup summary and delivery tracking design

Design specification based on `interface.md` and the installed Apple HIG snapshot. No web browsing, implementation, SDK compilation, device, GUI, or accessibility execution occurred.

## Concrete result

The widget answers **“Does the household have a pickup to check?”** The private Live Activity answers **“What is happening with my active delivery?”** Keep these as separate data scopes: a delivery in progress does not establish that a parcel is ready for pickup.

The brief supplies a parcel, recipient, address, gate code, an 80-minute delivery duration and a server update age of 35 minutes. It supplies no confirmed pickup readiness, delivery stage, start time or ETA. Therefore the actual input renders an uncertain status, never “Ready” or “Arriving now.” All future-state examples below are illustrative copy, not observed shipment facts.

### Surface contract

| Surface / family | Concrete hierarchy with supplied stale data | Activation |
| --- | --- | --- |
| iPhone Home Screen, system small | Package symbol; “Household pickups”; prominent “Status unavailable”; “Last update 35 min ago” | Entire card opens household pickup summary |
| Shared Apple HomeView Modular face, system small | Package symbol; “Pickups”; prominent “Check status”; “Updated 35 min ago” | Opens only the safe household summary on the activating device; personal details require the authorized app session |
| iPhone Lock Screen, accessory inline | “Pickups · update 35 min ago” | One target opens pickup summary |
| iPhone Lock Screen, accessory rectangular | “Pickups”; “Check status”; “Updated 35 min ago” | One target opens pickup summary |
| Optional watch glance, accessory rectangular in Smart Stack / supported face slot | “Pickups”; “Check status”; “Updated 35 min ago” | Relevant watch summary if a watch app exists; do not promise an unimplemented watch destination |

Use small as the primary widget; do not add medium/large variants without additional useful content. HomeView Modular is a shared system-small widget context, distinct from a watch Modular complication. Ship the watch variant only if watch app/support is established; no legacy ClockKit art is specified.

Household configuration is explicitly selected in the app: “Share pickup summary” defaults off, with explanation “Show pickup status to everyone who can see the household display. Names, addresses and access codes stay private.” Select the household and eligible shared parcels; exclude personal parcels by default. Without selection: “Choose a household” → configuration. Without shared parcels: “No shared pickups”; this does not mean the person has no private parcels. A fresh, confirmed eligible ready parcel can show “1 pickup ready”; plural counts are localized. Ready counts must not include merely scheduled deliveries.

### Privacy and access contract

“Private Live Activity” means personal scope and minimized content, not a confidential display: Lock Screen, StandBy and paired surfaces can be visible to other people.

| Data | Household/widget payload | Personal Live Activity payload | Authorized app |
| --- | --- | --- | --- |
| Eligible pickup count/status and update time | Allowed after sharing choice | Not needed for delivery activity | Allowed |
| Recipient name, full address | Omitted | Omitted | Delivery details after authorization |
| Gate/access code | Omitted, including labels, previews and accessibility strings | Omitted, including push content and URLs | Reveal on demand after authentication; protect secret storage with system key management |
| Delivery phase, validated ETA, freshness | No private delivery details | Allowed as generic status | Allowed |
| Identity | Household scope token only | Opaque activity/delivery identifier | Resolve only after access check |

No name, address or code appears on any external variant, even when unlocked. Never encode secrets into deep links. Recheck authorization at destination; a valid link is not authorization. Account change, sign-out or revoked household access clears cached summaries and ends personal tracking. Shared-display copies require invalidation too; propagation guarantees remain unverified.

In the delivery screen offer “Track delivery on Lock Screen” with “Show delivery progress on your personal devices. Anyone nearby may see it.” Provide “Stop tracking” in that screen; this ends the activity without cancelling the delivery. Respect system-disabled activities and continue tracking in the app. These features need existing shipment data, not new contacts, location, camera or tracking access. Request any later protected access only at the feature that needs it.

## Bounded delivery Live Activity

An 80-minute delivery is suitable for an ongoing bounded activity, unlike a periodic pickup widget. Start after a confirmed active delivery event and the person's tracking choice. Use one evolving activity per related delivery task; deduplicate starts by opaque event ID. The brief alone is insufficient to start one.

| Presentation | Fresh example (illustrative) | Stale supplied-data treatment |
| --- | --- | --- |
| Compact Dynamic Island | Leading package symbol; trailing “12 min” only with validated ETA | Leading package + warning mark; trailing “Old” |
| Minimal / multiple activities | Package plus phase mark, or validated short ETA; informative rather than logo alone | Package + warning mark; accessible label “Delivery update delayed” |
| Expanded | Package / “Delivery” leading; ETA trailing; phase below; freshness last | “Delivery”; “Update delayed”; “Last update 35 min ago”; “Open for latest status” |
| Lock Screen | Same identity and relative positions; large phase, ETA, freshness | “Delivery”; prominent “Update delayed”; “Last update 35 min ago” |

Both compact halves and the expanded/Lock Screen body deep-link to that delivery's authenticated details. Hold compact/minimal to expand using system behavior. No Accept or Cancel targets on external surfaces: these consequential actions belong in the app with current server state and confirmation where appropriate. “Details” is the body destination, not an imitation button. This design needs no in-place action; HIG's preference for one essential action does not require adding one.

Fit compact/minimal content to the limited-width 28-pt circle where needed, simplifying to the package/warning symbol with a full accessible state label. Never shorten a stale warning into an apparent ETA.

### Event and freshness model

The following thresholds and deadlines are proposed product policy, not Apple requirements. Validate them against service telemetry before release.

| Condition / transition | Visible behavior |
| --- | --- |
| No cache / initial load | “Checking pickup status” or “Checking delivery status”; neutral placeholder framing; no fabricated count/ETA |
| Fresh server event, age ≤5 min | Show confirmed phase/count; ETA only if the server supplies a still-valid estimate |
| Age >5 min | Mark stale; keep useful last-known context explicitly qualified; remove countdown, current-location implication and unqualified readiness claim |
| Supplied age 35 min | “Update delayed” / “Check status” plus last update age; no assumed phase or readiness |
| Confirmed connection failure | Add “Offline” and retain last update time; never infer offline solely from age |
| Offline without cache | “Offline · Status unavailable”; open app destination remains available; no successful-action claim |
| Refresh in progress with cache | Keep qualified cached content; do not replace useful data with loading blocks |
| Reconnect | Request authoritative snapshot; stay stale until a newer valid response arrives; connection recovery alone does not make data fresh |
| Out-of-order or duplicate event | Ignore older revisions; preserve terminal state; refresh age derives from server event time, not render/retry time |
| Confirmed delivered / cancelled / failed | End immediately with matching terminal summary; remove active ETA; retain safe Lock Screen summary for 15 minutes where supported, then dismiss |
| No terminal signal | At confirmed start +80 min, change to “Taking longer · Check status”; never infer delivered. At start +120 min, end tracking with “Tracking ended · Check app”; delivery outcome stays unknown |
| User stops tracking / signs out | End immediately; no retained personal summary on sign-out; no automatic restart of the stopped session |

Require authoritative start time and terminal events; carry a local ending deadline so missed pushes cannot deliberately leave indefinite tracking. If start time is missing, show stale details in the app and do not launch the activity. SDK/system ability to enforce expiry without execution must be verified. Late terminal events update app history without restarting an ended activity.

Widgets request timelines for meaningful events and the stale boundary, plus a proposed 15-minute refresh opportunity during expected pickup hours. These are requests under system budgets, not delivery guarantees. Server event frequency is a separate backend contract, currently unknown. Use system date/time text where appropriate and always retain an absolute localized update timestamp as an accessible/fallback reference. Never promise second-by-second reloads. Live Activity updates change only affected content; no synthetic moving progress bar. Alert only on a fresh crucial event such as confirmed arrival, with deduplication so there is no parallel push alert for the same event. Stale retries are silent.

## Appearance and adaptation decisions

Use actual text, system text styles and medium-or-stronger primary type. Layout adapts to family/container size; preserve status and freshness before secondary labels at accessibility sizes. Avoid shrinking everything to fit. Default widget margins follow contextual system guidance (commonly 16 pt); Lock Screen activity uses 14-pt margins, adapted only for grouping. No fixed production canvas is assumed.

Full color uses semantic light/dark colors. In accented mode, status is primary and the package symbol is accent; wording carries every state. Vibrant uses intentional grayscale emphasis, not opacity alone. HomeView backgrounds are removable; large status and age survive background removal, tinting and red Night Mode. Lock Screen accessories retain meaning after desaturation and Always On reduction. Avoid persistent animation; optional update transitions stay within 2 seconds and do not communicate essential state only through motion.

StandBy scales safe content with margins and red-mode legibility checks. Watch Live Activity defaults to combined compact halves; use safe generic status and stale mark. With no watch app, use the system full-screen view and paired-iPhone launch path. CarPlay uses a status-only layout meaningful with controls disabled. Paired Mac activation uses iPhone Mirroring, subject to availability. Do not promise Live Activities on tvOS or visionOS. Household HomeView gets only the pickup widget, never the personal delivery activity.

Intended spoken order: surface title → status → qualified ETA if fresh → last update → destination. Treat decorative symbols as decorative; expose warning meaning in words. Inline remains one accessible activation. Localize plural counts, relative/absolute dates and units; mirror directional layout appropriately and test long translations. These are design requirements, not verified accessibility behavior.

## Acceptance audit

**Passed — static design inspection only:** Separate household/personal scopes; supplied 35-minute age explicitly stale; no invented readiness/ETA; sensitive fields excluded from external payload contract; one inline destination; system-small HomeView distinguished from watch; all four iPhone activity presentations specified; terminal and timeout paths bounded; stale/offline distinguished; rendering and deep-link contracts documented.

**Failed — supplied proposal:** Per-second widget refreshing conflicts with system-limited periodic updates; full address/code on shared face exposes private information; inline Accept/Cancel/Details cannot be independent targets. Replacement contracts above resolve these in the design; no implementation fix is claimed.

**Not executed — release acceptance checks:**

- Inject updates at 0, 5 and 35 minutes, no cache, offline, reconnect, clock skew, duplicate/out-of-order events and missed terminal pushes. Verify stale warning remains visible, old estimates disappear, and no retry changes the event timestamp.
- Run an 80-minute session, delayed session through 120 minutes, terminal events, stop tracking, sign-out and opt-out. Verify one activity, immediate terminal ending, chosen retention, timeout semantics and no restart after stopping.
- Activate every widget/activity region: correct household or delivery, authentication enforced, no cross-account access. Inspect payloads, URLs, caches, previews and spoken labels for excluded private fields. Test sharing revocation on a disconnected household display.
- Render realistic preview fixtures (clearly labeled simulated), placeholders, signed-out “Sign in to view pickups,” no-shared-items, stale/offline and redacted states. Signed-out activation goes to sign-in and then the authorized destination; never retain another account's values.
- Check smallest supported iPhone, non-Island iPhone, 28-pt limited-width Island, multiple activities, long text, large counts, Dynamic Type Large through AX5, light/dark, tinted/clear, vibrant, background removal, Always On and red Night Mode. Preserve freshness before decorative detail; do not truncate warnings.
- Verify VoiceOver order, labels and single-target inline behavior on device; measure contrast and physical glance readability on phone, shared display and optional watch. Test StandBy margins and CarPlay without controls. Check all selected watch slots and static placeholders.

## Evidence still missing

No source code, framework/version targets, signed build, screenshots, SDK references, timeline traces, push pipeline, server event schema or device results were supplied. Need confirmed pickup readiness semantics, event timestamps/revisions, ETA validity, 80-minute start/end meaning, terminal and expiry delivery guarantees, household membership/consent model, offline shared-cache revocation strategy, authentication/secret storage evidence and watch app availability. The 5/15/120-minute policies and copy need product/backend validation. Current API availability and native support must be checked against target SDK documentation before implementation; local HIG alone cannot prove them. Security, household comprehension and accessibility execution remain unverified.

## Guidance and read audit

Installed package root: `.agents/skills/apple-hig/`. Explicitly read root `SKILL.md`, then `subskills/apple-hig-system-experiences/SKILL.md`; then that family's `.topics/apple-hig-widgets/SKILL.md`, `.topics/apple-hig-live-activities/SKILL.md` and `.topics/apple-hig-complications/SKILL.md` before their respective `references/widgets.md`, `references/live-activities.md`, `references/complications.md`. Also read `subskills/apple-hig-foundations/SKILL.md`, its `.topics/apple-hig-privacy/SKILL.md`, then `references/privacy.md`. Each read used a separate `cat` command. Official links below identify the local snapshot's source; none were browsed.

- [Widgets — updating content, interactivity, rendering modes and platform considerations](https://developer.apple.com/design/human-interface-guidelines/widgets): periodic refresh, one inline target, contextual families, shared HomeView privacy and adaptive rendering.
- [Live Activities — best practices, presentations, starting/updating/ending](https://developer.apple.com/design/human-interface-guidelines/live-activities): bounded tasks (ideally no more than 8 hours), minimized sensitive content, all iPhone layouts, crucial alerts only, immediate end and shorter retained summaries (commonly 15–30 minutes). The 80-minute task fits that guidance; 120-minute timeout is our policy.
- [Complications — best practices and visual design](https://developer.apple.com/design/human-interface-guidelines/complications): meaningful watch glances, limited reloads, tint/Always On privacy and family-specific adaptation.
- [Privacy — best practices, requesting permission, protecting data](https://developer.apple.com/design/human-interface-guidelines/privacy): minimum necessary data, contextual access and established secret protection.

The widget guide has an accented-Mac table/prose conflict; no Mac widget capability is promised here. The complication guide flags conflicting legacy inline dimensions; this design specifies modern families without relying on those dimensions. Neither conflict is silently resolved.
