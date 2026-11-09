Use a **pickup widget for periodic summaries** and a **Live Activity for the roughly 80-minute delivery**. Replace the proposed second-by-second widget refresh, remove private details from the shared face, and give the inline Lock Screen accessory one tap destination.

The supplied data establishes a parcel for Sam and a server update 35 minutes ago. It does **not** establish pickup readiness, delivery stage, connectivity, or ETA; the design must not invent those.

**Surface design**

| Surface | Proposed content and hierarchy | Interaction |
|---|---|---|
| iPhone Home Screen, small widget | `Pickup` → `Parcel for Sam` → `Status needs updating` → `Updated 35 min ago` | Whole widget opens this parcel’s pickup details. |
| iPhone Home Screen, medium widget | Same summary, adding the last confirmed pickup stage and pickup window **when available**. Optional address display through personal configuration. | Parcel opens its details; avoid adding controls merely to fill space. |
| Lock Screen, inline accessory | Parcel symbol + `Pickup · Updated 35m ago` | **One tap target**, opening the parcel. Remove the drawn Accept, Cancel, and Details buttons. |
| Lock Screen, rectangular accessory | `Pickup` / `Status needs updating` / `Updated 35m ago` | Opens parcel details. Default to no recipient or address on the locked surface. |
| Shared Apple HomeView Modular face, small-family widget | `Household parcels` → `1 parcel` → `Status needs updating` → `Updated 35 min ago` | Opens a safe household summary where supported. Personal details require authorized access. |
| Delivery Live Activity | `Delivery` → confirmed stage or `Status needs updating` → fresh ETA when trustworthy → update age | Opens this delivery; no Accept or Cancel in the initial design. |

The shared HomeView Modular face is a household surface, distinct from an Apple Watch Modular face. Use its small-family widget placement, removable background, and large glanceable text. A member’s personalized HomeView Home Screen can have different configuration, but the shared face must retain the household-safe policy. These surface and interaction choices follow Apple’s [Widgets guidance](https://developer.apple.com/design/human-interface-guidelines/widgets).

**Private detail contract**

Keep `Sam`, `14 Willow Road`, and gate code `9182` in the authorized parcel-detail flow by default. Show the gate code only after an explicit reveal in an authenticated personal context; exclude it from widget and Live Activity payloads, previews, and accessibility labels. A personal Home Screen widget may optionally show the address; never carry that preference automatically onto the shared face.

Household configuration selects parcels explicitly shared with the household. If none are shared, show `No shared parcels`; don’t infer sharing from household membership. This is the proposed product policy, grounded in Apple’s [privacy guidance](https://developer.apple.com/design/human-interface-guidelines/privacy) and widget guidance on shared HomeView exposure.

**Delivery tracker and watch decision**

An 80-minute delivery is a good bounded Live Activity: it has a meaningful start, changing progress, and a definite end. Start when delivery tracking actually begins, offer an opt-out, update when meaningful content changes, and end immediately on confirmed completion or cancellation. Retain a safe completion summary for about 15 minutes where supported. Eighty minutes is an expected duration, **not** an automatic completion signal.

For iPhone, supply all presentations:

- **Lock Screen and expanded:** delivery identity, confirmed stage, trustworthy ETA, freshness. Preserve relative positions when expanding.
- **Compact:** parcel symbol/stage on the leading side; ETA on the trailing side only while fresh. Substitute a freshness warning when stale.
- **Minimal:** parcel symbol with a meaningful state indicator, including a stale warning; avoid a logo-only presentation.

Do not animate route progress or calculate delivery percentage from elapsed time. Alert only for crucial changes, such as arrival, without duplicating the same Live Activity alert with a push notification. See [Live Activities](https://developer.apple.com/design/human-interface-guidelines/live-activities).

| Watch option | Best use | Proposed design and tradeoff |
|---|---|---|
| Watch-face complication | Recurring pickup summary across the day | Prefer accessory rectangular: `Pickup` / `1 parcel` / `Updated 35m ago`. Inline can use `Pickup · Stale`; circular can use a parcel count plus warning symbol. User must allocate a face slot; refresh remains system-budgeted. |
| Delivery Live Activity in Smart Stack | **Recommended for the active 80-minute delivery** | `Delivery` / confirmed stage or `Status needs updating` / update age. Temporary, timely presence without asking the person to dedicate a face slot. Tap opens matching Watch details if a Watch app exists; otherwise use the system’s full-screen handoff to iPhone. |

Offer the complication as an optional recurring entry point; use the Smart Stack Live Activity for the active delivery. Keep both free of address and gate code, including wrist-down states. A custom Watch Live Activity layout must also remain useful when reused in CarPlay with controls disabled. See [Complications](https://developer.apple.com/design/human-interface-guidelines/complications) and [Designing for watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos).

**Freshness and connectivity**

Use separate fields for last server confirmation and connectivity. A 35-minute-old update proves age; it does not prove the device is offline.

| State | Visible behavior |
|---|---|
| Fresh | Show confirmed status and valid ETA, with update age where useful. |
| Stale, connectivity unknown | `Status needs updating` + `Updated 35 min ago`. Preserve last confirmed information, explicitly labeled. Suppress live ETA/countdown. |
| Offline with cached data | `Offline · Showing saved information` + `Updated 35 min ago`. Preserve useful cached details. |
| Refreshing | Keep cached content and its freshness label; don’t replace it with a skeleton. |
| No cached data | `Status unavailable` + `Open app to try again`. Never substitute zero parcels. |
| Signed out | `Sign in to view pickups`; shared surfaces reveal no cached personal data. |

Propose a **five-minute stale threshold during active delivery**, pending evidence about backend cadence. Pickup summaries need a separate threshold based on their operational urgency. These thresholds are product decisions, not HIG requirements; this 35-minute-old record should be treated as stale for active tracking.

Replace every-second reloads with meaningful timeline entries and system-budgeted refresh requests. Use system date/time text for age; changing displayed age does not mean new server data arrived. Configure the Live Activity’s stale deadline, and clear staleness only after a successful server confirmation. On reconnection, reconcile the latest state before enabling consequential actions.

Accept and Cancel belong in parcel details until their meaning and authorization are defined. Cancellation should show the affected parcel and consequence before submission. While offline, don’t claim either action succeeded.

**Acceptance checks**

| Check | Current verdict |
|---|---|
| Widget refresh promise respects system scheduling | **Failed in proposal:** every-second refresh is unrealistic. Revised design removes it. |
| Shared face excludes full address and gate code | **Failed in proposal.** Revised design uses a household-safe summary. |
| Inline accessory has one activation target | **Failed in proposal:** three separately drawn targets are misleading. |
| Supplied 35-minute record cannot appear live or show a fresh countdown | **Pass in specification; runtime not done.** |
| Offline and stale are distinct; refresh preserves cached information | **Pass in specification; runtime not done.** |
| All taps open the correct parcel and enforce current authorization | **Not done:** test signed-out, locked, revoked-sharing, and removed-parcel cases. |
| Delivery ends on confirmed completion/cancellation; stale updates cannot revive it | **Not done:** lifecycle and out-of-order update tests required. |
| Layout remains readable without color or background | **Not done:** test Home Screen light/dark, tint/clear, Lock Screen vibrant/Always On, HomeView background removal/Night Mode, and Watch tint/Always On. |
| Accessibility preserves status and freshness | **Not done:** test supported Dynamic Type sizes, long/localized text, VoiceOver order, and labels without private data. |
| Watch content is readable during a physical wrist glance | **Not done:** device testing required. |

**Evidence still missing**

- Actual pickup stage, delivery stage, ETA source, pickup window, and what “Accept” means.
- Backend update cadence, timestamp reliability, connectivity detection, and measured push latency; these determine stale thresholds.
- Supported OS/device versions and SDK availability, especially for HomeView and Watch Live Activity behavior.
- Household sharing and account authorization rules, including cache clearing after access is revoked.
- Rendered prototypes, real-device timeline/lifecycle tests, VoiceOver results, and household comprehension testing.

This is a design specification based on the supplied brief and the installed HIG snapshot; no implementation or device behavior has been verified.