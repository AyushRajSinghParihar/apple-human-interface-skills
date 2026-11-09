Use the Live Activity for **boarding and arrival updates**, with the full journey available in the app. One Live Activity cannot cover a 10-hour trip.

| Current plan | Revised plan |
|---|---|
| Start at booking; run for 10 hours | Keep booking confirmation in the app. Offer a boarding activity near departure, ending when boarding completes, and a separate arrival activity near the destination. Each has a meaningful start and end. ActivityKit caps active duration at **8 hours**. |
| Hotel promotion and full app icon | Remove the promotion. Use a small, uncontained brand mark or bus symbol; Apple advises against ads and the entire app icon. |
| Summary stays for 8 hours after arrival | End immediately at arrival. Request dismissal after **15–30 minutes**; ended activities can remain on the Lock Screen for at most **4 additional hours**, subject to earlier dismissal. |
| Full sentence in compact trailing | Show only the essential time or countdown. Move gate and service status into expanded and Lock Screen layouts. |
| Leading and trailing open different screens | Both open the **same trip details screen**. |
| Check In and Seat Map work in CarPlay | CarPlay disables Live Activity interactive controls. Use a read-only layout there. Keep Seat Map in the app; consider one Check In action on supported interactive surfaces during boarding only. |

These duration limits come from [ActivityKit](https://developer.apple.com/documentation/activitykit/displaying-live-data-with-live-activities); presentation and interaction guidance comes from [Apple’s Live Activities HIG](https://developer.apple.com/design/human-interface-guidelines/live-activities).

Suggested arrival layout, using your example data:

```text
[brand mark]  Your bus trip
Arrives 14:35                 On time
Destination
──────────────●───────────────
```

During boarding, replace arrival information with **departure time, Gate 12, and boarding status**. Show a gate only when it is relevant and confirmed.

| Presentation | Content |
|---|---|
| Compact leading | Recognizable bus/brand symbol |
| Compact trailing | `14:35` |
| Minimal | Small progress ring with bus symbol |
| Limited width | Bus/progress graphic in leading; leave trailing empty |
| Expanded / Lock Screen | Destination, prominent ETA, status, journey progress |
| CarPlay custom layout | Large ETA, destination, status; no action controls |

For limited width, switch layouts using `isDynamicIslandLimitedInWidth`: compact and minimal content must fit a **28-point circle**. Don’t shrink or truncate the long sentence. CarPlay’s custom small layout also serves Apple Watch, so verify both contexts. [Apple layout guidance](https://developer.apple.com/design/human-interface-guidelines/live-activities#Creating-Live-Activity-layouts)

Use medium-weight or heavier text, sufficient contrast, and status words alongside color. If updates become stale, show “Last updated…” instead of continuing to promise “On time.”