Use a **pickup summary widget for periodic checks** and a **Live Activity for the active delivery**. Replace the proposed second-by-second refresh, shared secrets, and three inline controls.

**Surface design**

The current data supports “Updated 35 min ago.” It does **not** establish a pickup status, delivery stage, ETA, or offline connection. Examples below avoid inventing those facts.

| Surface | Content and hierarchy | Interaction |
|---|---|---|
| iPhone Home Screen, small widget | **Pickup** → **1 parcel** → “Updated 35 min ago · May be outdated.” On a personal configuration, optionally show “For Sam.” | Whole widget opens that parcel’s pickup detail. |
| iPhone Home Screen, medium widget | Same summary, plus last confirmed pickup status and pickup window **when supplied**. Extra space adds useful information. | Parcel row opens its detail. |
| iPhone Lock Screen, rectangular accessory | Parcel symbol + **Pickup: 1 parcel** / “Updated 35m ago.” | One precise parcel destination. |
| iPhone Lock Screen, inline accessory | **“Pickup · Updated 35m ago”** | **One tap target** opening details. Remove the drawn Accept, Cancel, and Details controls. |
| Shared HomeView Modular face, small family | **Parcel update** → **1 parcel** → “Updated 35 min ago.” No recipient, address, code, or personal identifier. | Only a household-safe destination; private detail continues on an authenticated personal device. Verify the supported handoff before implementation. |
| iPhone delivery Live Activity | **Delivery** → current confirmed stage → ETA/window when reliable → freshness. For the supplied snapshot: **“Update delayed” / “Last update 35 min ago.”** | Opens this delivery. Keep Accept and Cancel in the authenticated detail flow until their meaning and consequences are established. |

HomeView’s Modular face is shared by the household; it must have an explicitly safe configuration rather than inheriting someone’s personal widget. Its small-family layout needs removable backgrounds, scaled readable content, tint support, and red Night Mode treatment. These surface and interaction choices follow Apple’s [widget guidance](https://developer.apple.com/design/human-interface-guidelines/widgets).

**Delivery tracker and watch choice**

An approximately 80-minute delivery is a good fit for a bounded Live Activity, comfortably within ActivityKit’s eight-hour active limit. Start when tracking begins, update on meaningful server changes, and end on confirmed delivery or cancellation. Retain a safe completion summary for a proposed 15 minutes where supported. Elapsed time alone must never mark it delivered. See Apple’s [Live Activities guidance](https://developer.apple.com/design/human-interface-guidelines/live-activities) and [ActivityKit constraints](https://developer.apple.com/documentation/activitykit/displaying-live-data-with-live-activities).

| Watch option | Best use | Proposed content | Decision |
|---|---|---|---|
| Watch-face complication | Recurring pickup awareness across the day; person chooses a face slot | Rectangular: “1 pickup / Updated 35m ago.” Circular: parcel count plus stale indicator. Tap opens the relevant watch detail. | Optional for frequent logistics users. Periodic timeline updates; no continuous-refresh promise. |
| Delivery Live Activity in Smart Stack | Temporary progress during the 80-minute delivery | “Delivery / Update delayed / Updated 35m ago”; replace with confirmed stage and reliable ETA when fresh | **Preferred active-delivery glance.** No permanent face-slot commitment. |

On supported paired watches, Live Activities appear in the Smart Stack. With a watch app, tapping should open its delivery detail; without one, account for the system’s full-screen presentation and iPhone continuation. If supplying a custom supplemental layout, keep it useful when its controls are disabled in CarPlay. See [Apple’s watch Live Activity design session](https://developer.apple.com/videos/play/wwdc2024/10098/) and [complication guidance](https://developer.apple.com/design/human-interface-guidelines/complications).

For Dynamic Island, preserve the same identity and state: compact shows parcel symbol + ETA or warning; minimal conveys a delivery state or stale warning, rather than only a logo; expanded adds stage and freshness. Never show a live-looking countdown from an expired estimate.

**Freshness, offline, and privacy contract**

Use server timestamps for freshness, independently of connectivity. A proposed initial stale threshold is **10 minutes during active tracking**, subject to the carrier’s actual update cadence.

| State | Presentation and behavior |
|---|---|
| Fresh | Confirmed stage and valid ETA, with update time available. |
| Stale—current snapshot | **“Update delayed · Last update 35 min ago.”** Keep useful cached facts, label stage as last known, and suppress an unreliable countdown. |
| Confirmed offline, cached data | **“Offline · Last update 35 min ago.”** Preserve cached summary; refresh when connectivity returns. |
| Server unavailable | **“Can’t update · Last update 35 min ago.”** Do not label this “Offline” merely because a request failed. |
| No cached data | **“Delivery status unavailable.”** Tap opens an explanation and retry path. |
| Refreshing | Keep existing content and timestamp until newer data arrives. |
| Signed out / no parcel | “Sign in to view pickups” / “No upcoming pickups,” each with the appropriate destination. |

Schedule widget timelines around meaningful changes and freshness boundaries, with reload requests when new data arrives. Refresh opportunities remain system-controlled. Use system date/time rendering for aging timestamps; it does not fetch new server data. Live Activities also use event updates rather than one-second polling. See [Keeping a widget up to date](https://developer.apple.com/documentation/widgetkit/keeping-a-widget-up-to-date).

Treat **Sam**, **14 Willow Road**, and **gate code 9182** as private detail. Default Lock Screen, watch, and shared presentations to an innocuous summary. Offer recipient display only through deliberate personal configuration. Keep the full address in authorized detail and reveal the gate code only when needed after authentication. Exclude the code from widget/Live Activity payloads, previews, accessibility labels, and deep-link URLs. This is the proposed product privacy policy, supported by Apple’s [privacy guidance](https://developer.apple.com/design/human-interface-guidelines/privacy).

**Acceptance checks**

| Check | Required result |
|---|---|
| Supplied 35-minute snapshot | Every applicable surface exposes freshness; none implies current live tracking or infers offline. |
| Connectivity transitions | Offline, stale, and server failure remain distinguishable; successful recovery uses a newer server timestamp. |
| Inline accessory | Exactly one activation target, opening the correct parcel. |
| Household exposure | Modular face, previews, spoken labels, and tap destination disclose no Sam, address, or gate code. Revoking sharing clears cached shared content. |
| Delivery lifecycle | Confirmed completion ends the activity; missing updates or an 80-minute timer do not imply completion. |
| Navigation and actions | Correct parcel survives sign-in and interruptions. Accept/Cancel report success only after server confirmation; offline failure cannot look successful. |
| Rendering | Meaning survives light/dark, tint/clear, Lock Screen grayscale, Always On, HomeView background removal and Night Mode, and watch tint. |
| Accessibility | Status uses text/symbols as well as color; freshness is spoken meaningfully; enlarged text preserves the essential glance; controls and destinations work with assistive input. Test physical watch readability. |

Use system typography and semantic colors, with status before secondary metadata. Test supported Dynamic Type sizes and relevant accessibility preferences against Apple’s [accessibility guidance](https://developer.apple.com/design/human-interface-guidelines/accessibility).

**Evidence still missing**

- Actual pickup status, delivery stage, pickup window, ETA, and definitions of Accept and Cancel.
- Carrier update cadence, ETA expiry rules, reliable completion events, and measured push latency.
- Minimum OS/device support, watch-app availability, and HomeView configuration/handoff behavior.
- Household authorization rules and how sharing is revoked.
- Rendered prototypes, contrast measurements, VoiceOver tests, device refresh behavior, and lifecycle tests.

**Review status:** the supplied proposal fails the inline interaction constraint, realistic widget refresh expectations, and the proposed household privacy policy. The revised specification addresses those issues on paper. Runtime, rendering, accessibility, and privacy checks have **not been executed**.