# Pickup summary and delivery tracking design

Design specification based on `interface.md` and the installed local HIG snapshot dated 2026-10-25. No web sources were fetched. Official links below identify the articles supporting the local guidance; they were not independently checked online. This is a design, not an implemented or device-tested interface.

## Concrete result

Use a periodic **Pickup summary** widget for “Does our household have anything to collect?” Use a separate, personal **Delivery** Live Activity for “What is happening with my current delivery?” Treat pickup readiness and delivery progress as separate server facts: a parcel being delivered does not establish that a pickup is ready.

The brief supplies one parcel, a recipient, an address, a gate code, a 35-minute-old server update, and an 80-minute delivery duration. It supplies no pickup-ready status, delivery phase, ETA, or connectivity result. Consequently, the initial design fixture shows **Status unavailable · Updated 35 min ago**, not “Ready,” “On the way,” or an invented arrival time.

| Surface | Family/presentation | Concrete content and activation |
|---|---|---|
| iPhone Home Screen | System small | `Pickups` / `Status unavailable` / `Updated 35 min ago`. Entire widget opens the authorized pickup list. |
| Shared Apple HomeView Modular face | System small, dedicated household configuration | Same hierarchy, with only explicitly shared pickup aggregates. Before sharing is configured: `Household pickups` / `Choose shared pickups in app`. No private parcel is included automatically. Activation opens safe household pickup context where supported; private access requires authentication and authorization on the personal device. Exact host handoff requires validation. |
| iPhone Lock Screen | Accessory rectangular | `Pickups · Status unavailable` / `Updated 35 min ago`; opens pickup list after required unlock. |
| iPhone Lock Screen | Accessory inline | `Pickups: check status`; one target opens pickup list. No independently drawn Accept, Cancel, or Details controls. |
| Optional Watch face glance | WidgetKit accessory rectangular complication | `Pickups` / `Check status · 35 min old`; opens the Watch pickup list, with cached summary and update time available without the phone. Requires a Watch app; defer shipping this variant until that destination exists. |
| Delivery Live Activity | Lock Screen and Dynamic Island | Personal event summary, described below. No household publication of this activity. |

On a fresh, authorized pickup-ready event, system small becomes `Pickups` / `1 ready to collect` / `Updated just now`. This is an illustrative future state, not a fact established by the brief. Fresh zero results read `Nothing to collect`; unavailable data never becomes zero. Larger widget families are out of this release's scope.

Small-family widgets are supported in HomeView according to the supplied snapshot; a shared Modular face and a personal Home Screen have different audiences. Watch complications are separate watchOS placements, not iPhone accessories. [Widgets — Anatomy and Apple HomeView](https://developer.apple.com/design/human-interface-guidelines/widgets#Apple-HomeView), [Complications](https://developer.apple.com/design/human-interface-guidelines/complications).

## Privacy and access contract

“Private Live Activity” means personal scope with minimized public content, not a guarantee that a Lock Screen is visible only to its owner. A nearby person may see it. No surface above displays the supplied name, street address, gate code, tracking number, map, or parcel contents. Never put these values in preview data, accessibility labels, links, or Live Activity payloads. Use opaque object identifiers for routing; authorize the object after navigation.

| Data | Purpose and permitted location | Access decision |
|---|---|---|
| Aggregate pickup count/status and observation time | Household glance | Include only explicitly shared pickups; explain that household members can see the aggregate. Default to unconfigured until chosen. |
| Delivery event ID, phase, estimated window, observation time | Personal live tracking | Only current account's followed delivery; not the household feed. |
| Recipient and full address | Identify delivery inside app | Fetch/display only in authorized delivery detail after unlock and account checks. |
| Gate code | Access instruction inside app | Reveal on explicit request in authenticated detail; protect stored secret using established secure storage. Exclude from widget/activity caches. |

In the app's pickup detail, offer `Share pickup summary with household`, explaining `Household members can see pickup counts and status. Names, addresses, and access codes stay private.` Opt-out removes the record from subsequent shared summaries and invalidates shared cached entries. Membership/account changes clear prior account data before presenting new content. Revocation propagation and residual host caches need implementation evidence; do not promise immediate remote erasure.

Starting live tracking is optional in delivery detail: `Track delivery` with `Shows delivery status on your Lock Screen and connected displays. Personal details stay in the app.` Respect system availability and user disablement; keep in-app tracking usable if unavailable. No contacts, location, camera, microphone, or tracking permission is needed for the specified server-fed summaries. Verify any actual platform entitlement/authorization flow against the target SDK. [Privacy — Best practices and Protecting data](https://developer.apple.com/design/human-interface-guidelines/privacy), [Live Activities — Best practices](https://developer.apple.com/design/human-interface-guidelines/live-activities#Best-practices).

## Freshness, offline, and refresh behavior

These are proposed product thresholds, not Apple timing guarantees: pickup summaries become stale after **15 minutes**, delivery progress after **5 minutes**, measured from the server observation time. Expired pickup windows also invalidate readiness even inside 15 minutes. Reject invalid/future timestamps as unknown freshness. Store observation time separately from fetch time; reopening a cache must not make it fresh.

| Condition | Widget copy | Delivery activity copy/behavior |
|---|---|---|
| Fresh data | Actual count/status plus update age | Actual phase and server estimate, labeled `Estimated`; no inferred percentage |
| Refresh in progress | Keep available content and timestamp | Keep last confirmed phase; no fabricated movement |
| Stale, connection unknown | `Status may have changed` / `Updated 35 min ago` | `Update delayed` / `Last update 35 min ago`; replace current ETA with `Arrival estimate unavailable` |
| Offline confirmed by failed connection | `Offline · Last known: 1 ready` / observation time, if that count exists | `Offline · Last known: [phase]` / observation time; no live ETA/countdown |
| No cached status | `Status unavailable` / `Open app to check` | `Status unavailable`; keep event identity without inventing progress |
| Signed out/account inaccessible | `Open app to sign in` with no cached account summary | End local activity and clear account content; authorize before restoring |
| Household sharing revoked | `No shared pickups` or unconfigured prompt | Personal tracking unaffected by household configuration |

For the supplied fixture, rectangular/small widgets use `Status may have changed` where space permits; because no actual status was supplied, their primary value remains `Status unavailable`. An inline stale/offline variant reads `Pickups: update delayed` or `Pickups: offline`. At tight Watch sizes, use `Check status`; the detail screen retains the observation time.

Plan widget timeline entries at known pickup-window boundaries and freshness expiry; request reloads after meaningful server changes and request another background refresh around 15 minutes while relevant. The OS controls actual execution and reload budget: no per-second network polling or refresh SLA. Use system date/time rendering for age where supported. A missed reload must not leave an unlabeled live claim: always include an observation time and validity context. Validate native expiry handling in implementation. Use changed-content pushes for Live Activity phases and ETA revisions; passage of time alone does not prove movement. [Widgets — Updating widget content](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content).

## Bounded delivery Live Activity

The 80-minute delivery is appropriate for a bounded activity. Start when the user follows an active delivery with a confirmed start and event ID; do not start from a stale generic parcel record. One activity follows this delivery through phase changes. Disabling tracking or dismissing the activity stops its presentation, not the delivery.

State model: `not started → active → delivered | canceled | failed`. Within active, a fresh server event can identify `Preparing`, `On the way`, or `Arriving`; stale/offline is an overlay on the last confirmed phase. Accept only newer events for the same account and delivery. Terminal states cannot regress because a delayed push arrives. Reconnection fetches authoritative state before restoring an ETA or restarting tracking.

At the confirmed start, record an expected end at start + 80 minutes. This is an estimate, not automatic proof of delivery. At that time, if no terminal event arrived, display `Taking longer than expected` when fresh status remains available, otherwise `Update delayed`. Proposed hard stop: start + **120 minutes**, ending with `Tracking ended · Open app for status` if unresolved. A start/end signal and a bounded fallback prevent indefinite activity; the 120-minute cap is a product decision needing operational approval, not an HIG limit. Configure an explicit expiry/end strategy and validate it against SDK/background delivery constraints; local timers alone cannot guarantee remote termination.

| Presentation | Fresh contract | Stale/offline contract |
|---|---|---|
| Compact leading/trailing | Parcel symbol + phase symbol / short estimated arrival time when supplied; both halves open the same delivery | Parcel + warning symbol / dash; spoken/text equivalent is `Update delayed` or `Offline` |
| Minimal, including multiple activities | Phase-specific symbol with parcel identity; changes with phase rather than static logo alone | Warning symbol; no old ETA presented as current |
| Expanded | Leading parcel symbol and `Delivery`; trailing estimated window; below, phase and observation time | Same relative positions; `Update delayed` or `Offline`, observation time, no live ETA |
| Lock Screen | `Delivery` / `[confirmed phase]` / `Estimated [window]` / update age | `Delivery` / `Update delayed` / `Last update 35 min ago`; optional last-known phase explicitly labeled |
| StandBy | Enlarge Lock Screen hierarchy; simplify supporting detail | Large freshness warning; preserve meaning in red Night Mode |
| Watch Smart Stack | Delivery phase and estimate/age, with safe status meaningful without a control | Last-known label and age; Watch detail if available, otherwise system paired-iPhone handoff |
| CarPlay | Status and estimate/age readable without interaction | Warning replaces estimate; no action dependency because controls are disabled |
| Paired Mac | Same safe compact/minimal/expanded status | Activation follows system iPhone Mirroring behavior; no private details in glance |

The activity's primary interaction is opening that delivery detail; no inline cancellation or acceptance. Cancel delivery remains an explicit in-app operation with current server status. Terminal delivery/cancellation/failure ends the activity immediately; retain a safe `Delivered`, `Canceled`, or `Delivery ended` summary for **15 minutes** where the system permits, then remove. Unknown timeout must never say `Delivered`. Alert only for an actionable arrival or failure, with no duplicate push notification for the same event. These alerts contain no address/code. [Live Activities — Starting, updating, and ending](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity), [Presentation and platform considerations](https://developer.apple.com/design/human-interface-guidelines/live-activities#Presentation).

## Appearance and accessibility decisions

Use actual text, system text styles, medium-or-stronger key status, and an aligned parcel symbol. Use flexible system margins and container-relative shapes, not fixed screenshot canvases. Keep status primary and update age secondary but legible. Remove decorative material and secondary ETA detail before reducing essential text. No color-only live/stale distinction, continuous animation, or moving courier indicator.

Specify full-color light/dark, accented tint/clear, vibrant Lock Screen grayscale, and reduced-luminance Always On variants. Shared HomeView removes the background on Modular; test its full-color/accented and red Night Mode treatments. Keep key values in the primary group and parcel accent secondary. Only the Live Activity Lock Screen uses a custom background; Dynamic Island backgrounds remain system-controlled. StandBy uses removable widget backgrounds and across-room legibility. Minimal/compact symbols must remain identifiable in the limited-width presentation rather than squeezing text into it.

At enlarged text, retain status and freshness, omit decorative identity repetition, and reflow detail views. Check iPhone widget Dynamic Type through AX5 where supported, at least 200% text enlargement for the in-app flow, and 140% on Watch. Use native activation areas; in-app actions target the 44 × 44 pt default for iOS/watchOS. Define the summary's accessible content as purpose, status, and observation time, with one activation to the matching context; decoration adds no repeated announcement. Privacy exclusions also apply to spoken content. No required gesture beyond ordinary activation, and no essential information carried only by sound. No automatic animation is required, so Reduce Motion loses no meaning. [Widgets — Rendering modes and text](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes), [Accessibility — Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [Designing for watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos).

## Acceptance and evidence

**Passed — static design checks only:** inspected `interface.md`; replaced the explicit second-by-second refresh promise, household address/code disclosure, and three inline targets. This specification distinguishes unknown from zero, stale from offline, personal from household scope, and expected end from confirmed delivery. It defines all iPhone activity presentations, terminal states, and precise navigation destinations. These are specification properties, not runtime results.

**Failed — supplied proposal:** full address/code on the shared face; one-second widget refresh contract; independently interactive Accept/Cancel/Details inside an inline accessory. No supplied implementation exists to establish a corrected runtime pass.

**Not executed — required acceptance checks:**

1. Feed an observation from 35 minutes ago with no connectivity result: show stale/unknown copy, no offline claim, no current ETA. Then supply confirmed connection failure and verify offline wording. Reconnect with a newer record; clear warnings only after authoritative refresh.
2. Feed zero pickups, missing data, signed-out, unconfigured, revoked sharing, and account switch fixtures. Zero appears only for a valid empty result. Search shared payloads, previews, caches, links, and accessibility output for recipient/address/code; none may appear. Verify revocation across household devices.
3. Follow every widget target to the authorized pickup list and both activity halves to the same event. Test locked-device entry, denied authorization, deleted event, interrupted/resumed navigation, and phone unavailable on Watch. Inline has exactly one activation target.
4. Exercise 80-minute expected-end, 120-minute unresolved timeout, delivery, cancellation, failure, dismissal, disabled activities, lost push, out-of-order pushes, and multiple activities. Terminal states never regress; no delivery inferred from elapsed time; retained summaries disappear after the selected interval where supported.
5. Preview chosen families with long localized/plural text, large counts, right-to-left layouts, AX text sizes, light/dark/tint/clear/grayscale, Always On, background removal, StandBy/HomeView red Night Mode, and Watch face/Smart Stack. Essential status and freshness remain readable. Measure actual contrast with a calculator and activation geometry; no measurements are available yet.
6. On Apple environments, validate WidgetKit timelines, ActivityKit availability/lifecycle and push delivery, Dynamic Island limited-width/minimal layouts, offline expiry, accessibility reading/activation, VoiceOver, Switch Control, Reduce Motion, and Watch wrist readability. Test CarPlay's disabled controls and Mac handoff if offered. Linux file inspection cannot establish any of these results.

**Evidence still missing:** target iOS/watchOS/host versions and SDK support; source implementation/build environment; actual pickup-ready and delivery event schemas, timestamps and ordering; backend update/termination reliability; confirmed delivery start/ETA; household membership and sharing authorization model; host cache revocation behavior; design approval for freshness thresholds and 120-minute cap; native previews, contrast/geometry measurements, Apple-device results, accessibility execution, and household comprehension/privacy testing. No SDK compilation, GUI, device, push, or assistive-technology execution is claimed.

## Local routing audit

Read the installed root `apple-hig/SKILL.md`, then the system-experiences family and searched `references/topic-index.md`. Before reading source guides, read Getting started → Designing for iOS and Designing for watchOS; System experiences → Widgets, Live Activities, Complications; Foundations → Privacy and Accessibility. Read the corresponding installed references after their procedures. Every file read used a separate `cat`, `head`, or `rg` command. No external package or online guidance was substituted. The widgets reference's conflicting Mac accented-mode statement does not affect this scope; it is not used to promise Mac widget support.
