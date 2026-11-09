Use a **pickup summary widget for planning** and a **Live Activity for the active delivery**. Remove the every-second refresh, keep the address and gate code off shared surfaces, and replace the inline accessory’s three controls with one link to details.

The supplied data establishes neither pickup readiness nor delivery progress. With the last server update **35 minutes ago**, the initial design must show uncertainty rather than invent an ETA.

**Surface design**

| Surface | Layout and content | Interaction |
|---|---|---|
| iPhone Home Screen, small | Parcel icon → **Pickup** → “Sam’s parcel” → “Status unavailable” → “Updated 35 min ago” | Whole widget opens that parcel’s details. |
| iPhone Home Screen, medium | Same hierarchy, with last confirmed pickup status or collection window when supplied. Freshness stays visible. | Parcel-specific details link. Add a simple action only once its meaning and authorization are established. |
| Lock Screen, rectangular accessory | **Pickup · Update delayed** / “Last update 35 min ago.” Hide recipient by default. | Opens parcel details, with authentication as needed. |
| Lock Screen, inline accessory | Parcel icon + **Pickup · Update delayed** | **One tap target** opening details. Put Accept and Cancel in the app. Inline accessories support only one target. [Apple widget guidance](https://developer.apple.com/design/human-interface-guidelines/widgets?changes=_3) |
| iPhone delivery Live Activity | **Delivery** → last confirmed stage → ETA range when trustworthy → freshness. For this snapshot: **Update delayed** / “Last update 35 min ago” / “Arrival estimate unavailable.” | Opens delivery details. |
| Shared HomeView Modular face | Large parcel icon → **Parcel update delayed** → “Updated 35 min ago.” Show a household parcel count only if household sharing is enabled. | Open a household-safe summary; private details require an authenticated personal flow. |

Use system typography, generous spacing, and a clear reading order: **task → status → freshness**. Pair warning text with an icon; color alone must never carry meaning. Avoid decorative maps or continuously moving trucks that imply current location.

For HomeView, prototype the Modular layout with its background removed, at room-viewing distance, and in tinted and Night Mode appearances. Treat final geometry and rendering as validation work against the current SDK and [Apple’s widget guidance](https://developer.apple.com/design/human-interface-guidelines/widgets).

**Watch decision**

| | Watch-face complication | Delivery Live Activity in Smart Stack |
|---|---|---|
| Best use | Persistent pickup awareness | Temporary delivery tracking |
| Content | Parcel icon/count; rectangular version can include “Update delayed” | Delivery stage, reliable ETA, and freshness |
| Tradeoff | Requires someone to allocate a face slot; very limited space | More room, but visibility depends on device support and user settings |
| Recommendation | Optional for frequent pickup users | Primary watch delivery glance |

An approximately **80-minute delivery** fits Apple’s short-to-medium-duration Live Activity guidance. Provide a tailored watch layout; supported paired watches can display the iPhone activity in the Smart Stack. End it on confirmed delivery or cancellation—not merely because 80 minutes elapsed. [Live Activity guidance](https://developer.apple.com/design/human-interface-guidelines/live-activities), [Apple Watch integration](https://developer.apple.com/videos/play/wwdc2024/10068/)

**Freshness, offline, and privacy decisions**

- **Fresh:** Show confirmed status and a trustworthy ETA range. Do not derive progress from elapsed time alone.
- **Stale:** Provisionally mark active-delivery data stale after **10 minutes without server confirmation**; validate this threshold with operations. At 35 minutes, show “Update delayed,” retain clearly labeled last-known information, and suppress the countdown and live-location treatment.
- **Offline with cached data:** Show “Offline · Last update 35 min ago.” Preserve the cached summary. If connectivity is unknown, say “Update delayed”; an old timestamp does not prove the device is offline.
- **Offline without cached data:** Show “Offline · Open app to try again,” with no fabricated status.
- **Reconnected:** Clear the warning only after successful server confirmation, not simply when connectivity returns.

Replace per-second widget reloads with timelines for known changes and event-driven reload requests. Use system-rendered relative timestamps. Widget refresh scheduling is system-controlled; Live Activities receive meaningful delivery updates through ActivityKit or push. Set a stale date for each activity update. [Widget refresh behavior](https://developer.apple.com/documentation/widgetkit/keeping-a-widget-up-to-date), [ActivityKit updates and staleness](https://developer.apple.com/documentation/ActivityKit/displaying-live-data-with-live-activities?language=_5%2C_5)

Keep **14 Willow Road** in authenticated parcel details. Reveal **gate code 9182** only through an explicit, authorized action there. Neither belongs in widget timelines, Live Activity payloads, shared previews, or accessibility labels. Sam’s name may appear on an opted-in personal Home Screen widget; shared and locked views default to generic parcel wording. Apply system privacy-sensitive redaction as an additional safeguard. [WidgetKit privacy protections](https://support.apple.com/guide/security/widgetkit-security-secbb0a1f9b4/web)

**Acceptance checks**

- The provided 35-minute-old snapshot displays a stale warning everywhere, without an invented readiness state, ETA, or progress percentage.
- Stale-online, confirmed-offline, connectivity-unknown, and offline-without-cache scenarios produce distinct, truthful copy.
- Aging data changes to the stale presentation when updates stop; test with the app suspended and pushes interrupted.
- No widget requests a one-second reload loop. Relative timestamps remain useful when reloads are delayed.
- The inline accessory exposes exactly one actionable target and opens the correct parcel.
- Accept and Cancel validate current server state in the app; cancellation requires confirmation. Offline actions never appear completed without acknowledgment.
- Shared, locked, preview, VoiceOver, and watch Always On presentations reveal neither address nor gate code.
- Delivery completion ends the activity; an overdue delivery stays explicitly uncertain until confirmed.
- Text survives supported sizes, localization, accessibility settings, tinted rendering, and HomeView viewing distances.
- Disabled Live Activities or unavailable watch mirroring leave a usable widget/app fallback.

**Evidence still missing**

The remaining inputs are the actual pickup status and collection window; delivery start, stage, and ETA source; expected server update frequency; household-sharing consent and permissions; and what “Accept” and “Cancel” mean.

Before release, validate the proposed stale threshold with delivery operations, confirm supported OS/SDK versions and HomeView behavior, and test comprehension, privacy, legibility, push delays, and battery use on real devices. These are design recommendations and acceptance criteria; they have not yet been demonstrated by a working prototype.