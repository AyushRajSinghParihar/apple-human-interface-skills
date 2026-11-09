Use an **arrival-focused Live Activity**, with booking and check-in handled in the app.

| Current plan | Correction |
|---|---|
| Start at booking and run through a 10-hour trip | A Live Activity can be active for **at most 8 hours**. For this trip, start when approaching the destination—for example, 2 hours before arrival. Keep the full itinerary in the app. |
| Keep the summary for 8 hours after arrival | End immediately on arrival. The system allows **up to 4 additional hours** on the Lock Screen; choose a shorter dismissal, such as 30 minutes. It disappears immediately from Dynamic Island and CarPlay. |

The active and post-end limits are separate: the extra Lock Screen time doesn’t extend live tracking. [ActivityKit duration limits](https://developer.apple.com/documentation/activitykit/displaying-live-data-with-live-activities)

Apply these changes to the visual and interaction plan:

- **Remove hotel promotions.** Live Activities must contain relevant activity information.
- **Replace the full app icon** with an optional logo mark without its surrounding container.
- **Open the same trip-details screen** from both compact halves.
- **Use one essential action at most as a design preference.** Keep Seat Map in trip details; offer Check In only during a relevant boarding phase.
- **Make CarPlay informational.** The system disables Live Activity buttons and toggles there, including in custom layouts. A custom `.small` supplemental activity family also serves Apple Watch. [Apple’s Live Activity guidance](https://developer.apple.com/design/human-interface-guidelines/live-activities)

Proposed layout, using illustrative trip details:

| Presentation | Content |
|---|---|
| Lock Screen | **Arrives 14:35** · Destination terminal · On time · Journey progress |
| Expanded Island | Same hierarchy, with next stop and relevant terminal information |
| Compact leading | Bus symbol |
| Compact trailing | `14:35` |
| Minimal | Bus symbol with a simple progress indicator |
| Limited width | A recognizable bus/progress graphic in the leading view; leave trailing empty |
| CarPlay / Watch small | Destination, large arrival time, short status; no controls |
| Ended | **Arrived 14:35** · Destination |

For boarding, replace arrival information with **departure time and Gate 12**; don’t keep the boarding gate prominent throughout the journey.

Limited-width compact and minimal content must fit within a **28-point-diameter circle**. Detect `isDynamicIslandLimitedInWidth` and switch layouts instead of truncating the long string or shrinking its text. Keep compact content balanced and close to the camera. [Layout guidance](https://developer.apple.com/design/human-interface-guidelines/live-activities)

Before shipping, verify limited-width landscape, light/dark and Always-On appearances, and CarPlay simulator sizes. Show delay status in text as well as color, and avoid displaying booking references or ticket codes on the Lock Screen.