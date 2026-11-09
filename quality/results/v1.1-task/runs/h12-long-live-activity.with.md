Use the Live Activity for a bounded phase of the journey, with arrival progress as its primary information. The current plan needs these changes.

| Current plan | Correction |
|---|---|
| Start at booking and run throughout the 10-hour trip | Keep booking details in the app. A Live Activity can be active for at most **8 hours**. For this trip, offer arrival tracking during the final portion—for example, the last 6 hours—with an easy opt-out. Don’t promise continuous coverage of the whole trip. |
| Hotel promotion and full app icon | Remove the promotion. Use a small, uncontained brand mark if useful; avoid the full app icon. |
| Keep the arrival summary for 8 more hours | End the activity immediately at arrival. The system can retain its ended presentation on the Lock Screen for **up to 4 hours**; choose a shorter useful period, such as **15–30 minutes**. Dynamic Island and CarPlay remove it when it ends. |
| Full sentence in compact trailing | Show only the essential changing value, such as `14:35`. Move gate and status into expanded and Lock Screen presentations. Limited-width content must fit a **28-point circle**; use a meaningful symbol or abbreviated value, or leading-only content. |
| Compact halves open different screens | Both halves must open the **same trip’s live-status screen**. |
| Check In and Seat Map work in CarPlay | CarPlay disables Live Activity buttons and toggles, including in the custom layout shared with Apple Watch. Make the presentation useful through status alone. |

These corrections follow Apple’s [Live Activities HIG](https://developer.apple.com/design/human-interface-guidelines/live-activities); the active-duration limit is documented in [ActivityKit](https://developer.apple.com/documentation/activitykit).

**Proposed layout**

Example Lock Screen and expanded presentation:

```text
[bus mark]  City A → City B         Arrives
            En route                14:35

──────────── journey progress ─────────────
Next stop: Central Station
On time
```

Before boarding, a separately scoped boarding activity could show `Gate 12`, boarding time, and one **Check In** action while check-in is available. End that phase when boarding finishes. Keep **Seat Map** in the trip screen; if it simply opens information, treat it as navigation rather than a direct-action button.

For the arrival activity:

| Presentation | Content |
|---|---|
| Compact leading | Bus mark or symbol identifying the journey |
| Compact trailing | Arrival time, `14:35` |
| Limited width | Meaningful bus/progress symbol; omit trailing content if it cannot fit legibly |
| Minimal | Bus symbol with a small progress treatment, rather than a static logo alone |
| Expanded / Lock Screen | Route, arrival time, progress, next stop, and explicit delay status |
| CarPlay / watch custom layout | Large arrival time, short destination, and status; no dependency on controls |
| Ended Lock Screen | `Arrived · City B · 14:32`, retained briefly |

Keep identity and relative positioning consistent as the presentation expands. Gate information belongs to the boarding phase unless it remains useful later. These presentation choices follow the [layout and destination guidance](https://developer.apple.com/design/human-interface-guidelines/live-activities).

**State and update contract**

Use confirmed trip events to transition from tracking → approaching → arrived or canceled. End immediately on arrival or cancellation. Update only changed information; reserve alerts for crucial changes such as boarding-location changes or major disruption, without duplicating the same alert through a separate push. If updates become stale, show that clearly instead of continuing to claim “On time.”

Before release, verify narrow and multiple-activity presentations, long destination names, enlarged text, VoiceOver, Always On contrast, StandBy Night Mode, and CarPlay with controls disabled. These are design acceptance checks; native rendering and delivery behavior remain untested.