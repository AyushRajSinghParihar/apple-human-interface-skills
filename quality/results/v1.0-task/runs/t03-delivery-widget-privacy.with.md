Use a **pickup summary widget for periodic information** and a **Live Activity for the roughly 80-minute delivery**. Replace the one-second refresh promise, remove private details from the shared face, and give the inline Lock Screen accessory one destination.

The parcel’s current pickup/delivery stage and ETA weren’t supplied. The designs below therefore show “Status unavailable” rather than inventing progress.

**Surface design**

| Surface | Content and hierarchy | Interaction |
|---|---|---|
| iPhone Home Screen, small widget | **Pickup** → “Parcel for Sam” → “Status unavailable” → “Updated 35 min ago” | Entire widget opens this parcel’s details. |
| iPhone Home Screen, medium widget | Same hierarchy; add the next confirmed pickup instruction or deadline when available. | Precise parcel destination; additional space adds useful information. |
| Lock Screen, rectangular accessory | **Parcel · Check status** / “Updated 35 min ago” | Opens this parcel after required authentication. |
| Lock Screen, inline accessory | “Parcel · Updated 35 min ago” | **One tap target**, opening details. Remove the drawn Accept, Cancel, and Details controls. |
| Shared Apple HomeView Modular face, small family | **Parcels** → “1 parcel” → “Status needs updating” → “Updated 35 min ago” | Safe household summary only; private details require an authenticated personal context. |
| iPhone delivery Live Activity | **Delivery** → last confirmed stage → current ETA when trustworthy → freshness | Opens delivery details. Expanded and Lock Screen layouts expose more context. |

HomeView has one household Modular face with up to four widgets; it is distinct from each member’s personalized Home Screen. Explicitly select which parcels are shared. Until sharing is configured, show “Choose shared parcels” rather than publishing Sam’s parcel automatically.

The full address, **14 Willow Road**, belongs in authorized parcel details. Keep the gate code **9182** behind an explicit “Show gate code” action in the authenticated app. Exclude it from widgets, activity payloads, previews, and accessibility labels. Hide Sam’s name and address by default on shared and lock-visible surfaces. These are deliberate product privacy choices supported by Apple’s [widget guidance](https://developer.apple.com/design/human-interface-guidelines/widgets#Apple-HomeView) and [privacy guidance](https://developer.apple.com/design/human-interface-guidelines/privacy).

**Freshness and delivery behavior**

Use server timestamps independently of device connectivity. A 35-minute-old update establishes age; it does **not** establish that the device is offline.

| State | Visible treatment | Behavior |
|---|---|---|
| Fresh | Confirmed stage, trustworthy ETA, update time | Present only server-confirmed progress. |
| Stale | “Status may have changed · Updated 35 min ago” | Retain last confirmed information; suppress an expired ETA or countdown. |
| Offline with cached data | “Offline · Updated 35 min ago” | Preserve cached information and its age. |
| Offline without cached data | “Offline · Status unavailable” | Offer details/retry in the app; show no invented stage. |
| Refreshing | Existing information stays visible | Do not replace useful cached content with a skeleton. |
| Reconnected | Keep stale/offline treatment until a successful response | Connectivity alone does not make data fresh. |
| Completed or canceled | Confirmed terminal summary | End the Live Activity immediately; propose retaining a safe summary for 15 minutes. |

For the initial design, treat **more than 10 minutes without confirmation as stale during an active delivery**. That threshold is a product assumption to validate against the backend’s update cadence, not an Apple requirement. At 35 minutes, this delivery would be stale.

Request widget updates for meaningful changes and stale-state transitions under system scheduling. Use system date/time presentation for age where supported; do not poll or promise refreshes every second. A Live Activity also receives meaningful updates—it does not guarantee continuous server delivery. See [Widgets: Updating widget content](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content).

Start the Live Activity when delivery actually begins, with an easy opt-out. Eighty minutes fits Apple’s bounded-event model. Never calculate remaining time as “80 minutes minus elapsed”: typical duration is not an ETA or a completion signal.

For Dynamic Island:

- **Compact:** parcel symbol plus confirmed ETA; replace ETA with a stale/offline indicator when needed.
- **Minimal:** parcel symbol with a meaningful current-state marker.
- **Expanded / Lock Screen:** delivery identity, confirmed stage, ETA or uncertainty, and update age.

Keep relative positions consistent across expansion. Alert only for crucial events, such as arrival or required intervention, without duplicating the same push notification. See [Live Activities](https://developer.apple.com/design/human-interface-guidelines/live-activities).

**Watch choice**

| | Watch-face complication | Delivery Live Activity in Smart Stack |
|---|---|---|
| Best purpose | Recurring pickup summary throughout the day | Temporary progress during this delivery |
| Design | Rectangular: “1 parcel / Updated 35 min ago.” Circular: parcel count plus stale marker. Inline: concise status. | “Delivery / Status needs updating / Updated 35 min ago”; show stage and ETA when confirmed fresh. |
| Updates | Budgeted timelines; no continuous-refresh promise | Meaningful event updates during the bounded activity |
| Tap | Relevant parcel or pickup list in watch app | Relevant watch app when available; otherwise the system’s full-screen activity with paired-iPhone launch option |
| Recommendation | Optional for frequent logistics users | **Preferred delivery glance for this 80-minute event** |

The complication remains useful outside an active delivery; the activity ends with the event. Neither shows the address or gate code. See [Complications](https://developer.apple.com/design/human-interface-guidelines/complications) and [Live Activities: watchOS](https://developer.apple.com/design/human-interface-guidelines/live-activities#watchOS).

**Acceptance checks**

- At 35 minutes without confirmation, active delivery displays stale status; it never implies a live courier position.
- Test stale-but-online, offline-with-cache, offline-without-cache, and reconnection before a successful response separately.
- Delayed or out-of-order updates cannot overwrite newer confirmed state. Terminal events end the activity; elapsed time alone never marks delivery complete.
- Every inline accessory has exactly one activation target. Accept and Cancel live in authenticated parcel details, with server validation and explicit failure feedback.
- Shared-face, signed-out, locked, preview, and accessibility content disclose no gate code or full address. Sharing changes and account removal clear affected cached summaries.
- Every tap opens the correct parcel; missing authorization reveals no private content.
- Test system text styles, long/localized text, supported accessibility sizes, VoiceOver reading order, contrast, and comfortable activation areas.
- Verify light/dark, Home Screen tint/clear, Lock Screen vibrant rendering, HomeView background removal and red Night Mode, and watch tint. Text and symbols preserve meaning without color.

**Evidence status and gaps**

The supplied proposal **fails design review** on its refresh promise, shared disclosure, and separate inline tap targets. The replacement specification addresses those issues on paper. **No runtime, rendering, accessibility, or device checks have been executed.**

Still needed: actual pickup stage and instructions; delivery start/end signals and ETA semantics; backend update cadence and push reliability; household sharing authorization and revocation rules; the meaning of Accept and Cancel; target OS/device support, including HomeView; and whether a native watch app exists. Validate SDK availability and test real devices before committing to platform behavior. The recommendations use the installed October 2026 HIG snapshot; current online guidance was not independently verified.