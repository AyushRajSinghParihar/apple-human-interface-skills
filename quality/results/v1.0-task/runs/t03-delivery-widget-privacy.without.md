Use a **pickup summary widget for persistent information** and a **Live Activity for the roughly 80-minute delivery**. Remove the every-second widget refresh, the shared address and gate code, and the inline accessory’s three separate controls.

**Design**

The supplied data establishes a parcel and its update age, but no confirmed pickup status, delivery stage, or ETA. The initial design must therefore say “Status unavailable” rather than inventing “Ready” or “On the way.”

| Surface | Proposed content and behavior |
|---|---|
| iPhone Home Screen, small | **Pickup · 1 parcel** / **Sam** / **Status unavailable** / warning symbol + **Updated 35 min ago**. One tap opens that parcel. Offer a privacy setting that replaces the name with “Your parcel.” |
| iPhone Home Screen, medium | Same hierarchy, plus the last confirmed pickup window or status when available. Use the added width for useful information, not more controls. |
| Lock Screen, inline accessory | Parcel symbol + **Update overdue · 35m**. The entire accessory is one tap target opening parcel details. |
| Lock Screen, rectangular accessory | **1 parcel** / **Update overdue** / **Updated 35 min ago**. No address or code. |
| iPhone delivery Live Activity | **Delivery** / confirmed stage and arrival window when fresh; **Updates delayed** when stale. Below: a compact milestone strip and update age. Tap opens delivery details. |
| Shared HomeView Modular face | **1 parcel** / **Update overdue** / **Updated 35 min ago**. Omit Sam, the full address, gate code, and transactional controls. |
| Authenticated iPhone details | **Parcel for Sam** / **14 Willow Road** / explicit **Reveal gate code** action, revealing **9182**. Show freshness beside operational details. |

HomeView’s Modular face is household-wide, including widgets connected from different members’ phones. Use a dedicated household-safe configuration; do not assume that the person looking at it owns the parcel. Its small widget scales up with its background removed, including a red monochrome night appearance. Inline accessories support only one tap target. [Apple widget guidance](https://developer.apple.com/design/human-interface-guidelines/widgets)

Use system typography, SF Symbols, generous spacing, and a dominant status line. Stale and offline states need words and symbols, so meaning survives monochrome rendering.

**Watch decision**

| | Watch-face complication | Delivery Live Activity in Smart Stack |
|---|---|---|
| Best purpose | Persistent pickup summary chosen by the wearer | Temporary tracking during this delivery |
| Content | Parcel count; short confirmed status or stale indicator | Delivery stage, arrival window, freshness |
| Tradeoff | Always glanceable on a configured face, but occupies a lasting slot | More room and appropriate temporary prominence; presentation remains system-controlled |
| Recommendation | Optional for frequent users | Primary watch delivery experience |

An 80-minute delivery fits Apple’s guidance for bounded Live Activities lasting under eight hours. Provide a custom watch layout and end the activity when completion or cancellation is confirmed. Keep its contents innocuous across devices. [Apple Live Activity guidance](https://developer.apple.com/design/human-interface-guidelines/live-activities)

**Freshness and interaction decisions**

- **Proposed freshness rule:** mark active-delivery data stale after 5 minutes without a server update. This is a product assumption requiring validation. At 35 minutes, the supplied record is stale.
- **Stale:** show “Updates delayed · Updated 35 min ago.” Retain the last confirmed stage with “Last known”; suppress countdowns and moving progress that imply current knowledge.
- **Offline:** show “Offline · Last update 35 min ago” only when connectivity failure is known. Age alone does not establish offline status.
- **No cached data:** show “Connect to load parcel status,” without a fabricated parcel count or stage.
- **Recovery:** retain the warning until a successful server response arrives. Reconnecting alone does not make data fresh.
- **Completion:** require a server-confirmed event. Elapsed time or an expired ETA must never imply delivery.

Replace second-by-second widget polling with timelines for predictable changes, reload requests when new data arrives, and supported widget pushes. Widget scheduling is system-controlled; Apple describes a typical frequently viewed widget budget of 40–70 daily refreshes, not a guaranteed cadence. System-rendered time labels can advance without fetching new data. Use ActivityKit updates for delivery events and meaningful ETA changes. [Widget update guidance](https://developer.apple.com/documentation/widgetkit/keeping-a-widget-up-to-date)

Move **Accept** and **Cancel** into the parcel’s app screen. Refresh and validate availability before committing; require confirmation for cancellation. Offline actions must show failure or pending status explicitly, never success before server acknowledgment.

**Acceptance checks**

- With this fixture, every surface exposes the **35-minute update age** and stale state; none invents an ETA or delivery stage.
- Stale-online, confirmed-offline, reconnecting, empty-cache, and recovered states render distinctly.
- Household widgets, gallery previews, VoiceOver labels, and snapshots expose no address or gate code; the shared configuration also omits Sam.
- Inline accessory has exactly one accessible tap target; it opens the correct parcel after any required authentication.
- Delayed or missing pushes never produce false arrival, completion, or fresh status.
- Accept/Cancel handle rejection, repeated taps, and network failure without duplicate operations or false success.
- Verify smallest supported layouts, large text, VoiceOver, Always-On dimming, tinted/clear appearances, and background removal.
- Verify HomeView at room-viewing distance and in night mode; verify complication and Smart Stack layouts on supported watches.
- Test refresh behavior with normal production budgets, not only developer mode.

**Evidence still missing**

The confirmed pickup/delivery status and ETA; server update cadence and reliability; an agreed freshness threshold; household sharing consent and authorization rules; supported OS/device versions and HomeView interaction behavior; and prototype results for readability, privacy comprehension, accessibility, battery use, and unreliable networks.

These are design specifications and proposed checks; no implementation or device validation has been performed.