Make this an **“Approaching arrival” Live Activity**, with boarding and the full 10-hour journey tracked in the app.

| Current plan | Revised design |
|---|---|
| Start at booking and run for 10 hours | Keep booking confirmation in the app. Start the Live Activity for a useful, bounded phase—for example, the final two hours. A single Live Activity supports **up to eight active hours**. |
| Stay on the Lock Screen eight hours after arrival | End immediately at arrival. Show a final summary for about **15–30 minutes**; the system permits at most **four hours after ending**, with a maximum total lifetime of 12 hours. |

These limits mean one Live Activity can’t provide live tracking throughout your 10-hour trip. Keep the full trip status and history available in the app. [ActivityKit lifecycle documentation](https://developer.apple.com/documentation/activitykit/displaying-live-data-with-live-activities)

Use this content hierarchy:

| Presentation | Proposed content |
|---|---|
| Lock Screen | Small brand mark · route/destination; prominent **“Arrives 14:35”**; journey progress; **“On time · Arrival bay 12”** when confirmed |
| Expanded Dynamic Island | Same hierarchy and relative placement, with destination, ETA, progress, and relevant arrival information |
| Compact leading | Recognizable bus/brand symbol |
| Compact trailing | **14:35**, with arrival context conveyed accessibly |
| Minimal | Recognizable symbol with a small progress indicator, where legible |
| Ended summary | **“Arrived 14:32 · Central Station”**, linking to trip details |

Remove the hotel promotion. Use a small logo mark without an enclosing app-icon container. Both compact halves must open the **same trip-details screen**. Keep meaningful text legible, preserve a consistent layout between presentations, and communicate delays with text as well as color. [Apple’s Live Activities design guidance](https://developer.apple.com/design/human-interface-guidelines/live-activities)

For constrained Dynamic Island widths, drop secondary content instead of squeezing in “Arrives 14:35 · Gate 12 · On time.” If both compact elements still won’t fit, use a recognizable leading view—such as the minimal design—and an **empty trailing view**. [ActivityKit layout guidance](https://developer.apple.com/documentation/activitykit/displaying-live-data-with-live-activities)

For actions and CarPlay:

- Offer **Check In** only during a separate, relevant boarding phase, as a single quick action on supported interactive surfaces.
- Put **Seat Map** in trip details; it needs room for inspection.
- Design CarPlay around readable status, ETA, and destination. Its default presentation combines the compact halves; a custom small-family layout can improve readability.
- **Check In and Seat Map buttons won’t work in CarPlay:** the system deactivates Live Activity buttons and toggles there. A shared custom layout must remain useful without them. [Apple’s CarPlay guidance](https://developer.apple.com/design/human-interface-guidelines/live-activities)