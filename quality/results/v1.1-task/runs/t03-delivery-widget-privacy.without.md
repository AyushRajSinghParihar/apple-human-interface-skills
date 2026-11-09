Use a **pickup widget for the next task** and a **Live Activity for the active delivery**. Change the proposal in three places: remove per-second widget refreshes, remove private details from the shared face, and replace the inline accessory’s three controls with one tap destination.

**Design by surface**

| Surface | Content and layout | Interaction |
|---|---|---|
| iPhone Home Screen | Small: parcel symbol, “Pickup,” parcel count, freshness. Medium: add recipient and last confirmed pickup status. Show “Sam” only with personal-details enabled. | Tap opens that pickup. Medium may offer a supported, clearly labeled quick action once its meaning is defined. |
| iPhone Lock Screen widget | Inline: `Parcel · Updated 35m ago`. Rectangular: “Pickup” plus last confirmed status and freshness on separate lines. | One destination to pickup details. No separate Accept, Cancel, and Details targets in the inline family. |
| iPhone delivery Live Activity | Parcel symbol, confirmed delivery stage, valid arrival window, and a compact milestone strip. Freshness appears beside the status. At present: **“Delivery · Update delayed” / “Last update 35 min ago.”** | Tap opens delivery details. Put consequential changes behind an authenticated app flow. |
| Shared HomeView Modular face | Small widget: **“Household parcel” / “Update delayed” / “Updated 35m ago.”** Use large, simple typography and a layout that survives background removal and scaling. | Open a household-safe summary. Private details require an authorized personal flow. |
| Watch-face complication | Optional persistent entry: parcel symbol and count; rectangular variant can add freshness or a short confirmed stage. | Opens the watch delivery/pickup screen. |
| Watch Smart Stack Live Activity | Preferred watch tracker during the active delivery: stage, valid ETA window, and freshness. Use a watch-specific layout. | Open the appropriate watch detail screen, or an explicitly identified iPhone handoff. |

The supplied data establishes a parcel for Sam, but **does not establish its current stage, pickup readiness, or ETA**. Those values must remain unknown until confirmed.

A compact state sketch:

```text
PERSONAL PICKUP                 SHARED HOUSEHOLD
[parcel] Pickup                 [parcel] Household parcel
Sam                             Update delayed
Status unavailable              Updated 35m ago
Updated 35m ago

DELIVERY TRACKER — CURRENT
[parcel] Delivery
Update delayed
Last update 35 min ago
[Open delivery]
```

**Decisions and state behavior**

- **Protect shared information.** Never show `14 Willow Road` or gate code `9182` on the household face. Default shared copy also omits Sam’s name; household sharing requires an explicit choice. Show the address in authorized personal details, and reveal the gate code only on deliberate request. OS privacy redaction supplements this policy; it does not establish household authorization.
- **Treat freshness and connectivity separately.** Thirty-five minutes without a server update means stale data, not proven offline. Use “Update delayed.” Show “Offline · Last update 35 min ago” only when connectivity failure is actually known.
- **Propose a five-minute freshness threshold for active tracking**, subject to operational validation. Once stale, retain confirmed milestones with “Last known” wording; suppress the current ETA and stop advancing progress. Do not calculate “45 minutes remaining” from the typical 80-minute duration.
- **Offline with cached data:** retain the timestamped snapshot. **Offline without cached data:** “Delivery unavailable · Connect to load.” Never replace missing data with sample progress.
- **Recover on confirmed success.** A network reconnection alone does not make data fresh. Clear stale/offline messaging after a successful server response; preserve it after a failed retry.
- **Use event-driven updates.** WidgetKit schedules and budgets widget refreshes; every-second reloads are unsuitable. Request reloads after meaningful changes and schedule freshness transitions in the timeline. Relative timestamps can update through system time rendering without a new server fetch. Refresh timing remains system-controlled. citeturn533808search0turn533808search1
- **Use a Live Activity for the roughly 80-minute delivery.** This is a bounded ongoing task within ActivityKit’s eight-hour active limit. Send meaningful status/ETA updates, set a stale date, and end the activity when completion or cancellation is confirmed. The Smart Stack is the primary watch presentation for Live Activities; the complication remains an optional persistent shortcut. citeturn533808search4turn259203search4
- **Adapt the HomeView widget.** Its Modular placement scales the widget and removes its background, so essential grouping and contrast must survive that presentation. citeturn533808search5

**Acceptance checks**

- With the supplied 35-minute-old record, every surface communicates age; none invents a delivery stage, ETA, or offline diagnosis.
- Simulated network loss, server failure, empty cache, and successful recovery produce the distinct states above.
- Stale progress never advances to “Delivered” merely because time passes.
- Shared screenshots, accessibility labels, previews, and deep-link destinations expose neither the address nor gate code.
- The inline Lock Screen accessory has one coherent tap destination; it contains no three-button imitation.
- Accept/Cancel flows revalidate authorization and current server state. Offline attempts never appear successful.
- Delivery completion ends the Live Activity; dismissal does not cancel the delivery.
- Test all selected families with large text, VoiceOver, tinted/monochrome appearances, Always On, and HomeView’s removed background. Status remains understandable without color.
- Device tests confirm tolerable update latency under throttling, Low Power Mode, delayed pushes, and interrupted phone–watch connectivity.

**Evidence still missing**

The design still needs the actual pickup/delivery lifecycle and ETA source; the operational freshness SLA; what “Accept” commits to and who may cancel; household sharing permissions; and supported OS/device versions and HomeView SDK availability.

Before release, obtain physical-device evidence for refresh latency, watch handoff and fallback behavior, privacy during household/person changes, and glance readability on the scaled Modular face. These are acceptance targets, not checks already passed.