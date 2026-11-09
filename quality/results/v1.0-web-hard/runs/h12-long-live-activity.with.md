Your plan needs changes to its lifetime, content, compact layout, navigation, and CarPlay behavior.

| Current plan | Correction |
|---|---|
| Start at booking and cover the 10-hour trip | A single Live Activity can remain active for **at most 8 hours**. Keep booking details in the app; use a bounded activity such as boarding or the final approach. Don’t promise continuous coverage for the whole journey. |
| Keep an arrival summary for 8 more hours | End the activity at arrival. The Lock Screen can retain ended content for **up to 4 hours**; I recommend 15–30 minutes. Keep the permanent summary in the app. |

These are platform lifetime limits, and users can dismiss the activity earlier. [ActivityKit lifecycle documentation](https://developer.apple.com/documentation/activitykit/displaying-live-data-with-live-activities)

| Current plan | Correction |
|---|---|
| Hotel promotion and full app icon | Remove the promotion. Use a small, uncontained brand mark if needed; avoid the full app icon. |
| Entire arrival sentence in compact trailing | Put only the essential changing value there. Limited-width content must fit within a **28-point circle**; use an abbreviated value or meaningful graphic, or use leading-only content if necessary. |
| Compact halves open different screens | Both halves should open the **same trip detail screen**. |
| Check In and Seat Map work in CarPlay | CarPlay disables Live Activity buttons and toggles. Make its layout useful through status alone. A custom `.small` activity-family layout is shared with Apple Watch. |

These corrections follow Apple’s [Live Activities guidance](https://developer.apple.com/design/human-interface-guidelines/live-activities).

**Proposed design**

Use a final-approach Live Activity, starting around two hours before expected arrival. This is a product recommendation; the eight-hour cap still applies if delays extend it.

```text
[Bus mark]  Service 482
Arrives 14:35
Destination terminal · On time
────────────●───────  Journey progress
```

| Presentation | Content |
|---|---|
| Lock Screen / expanded | Service and destination, prominent arrival time, progress, and current status. Show Gate 12 only when relevant and confirmed. |
| Compact leading | Bus symbol with a small progress indicator. |
| Compact trailing | `14:35`, without the gate or status sentence. |
| Limited width / minimal | Bus symbol with changing progress; omit the trailing view when it cannot fit legibly. |
| CarPlay / shared small layout | Large arrival time, destination, and brief status; no essential interaction. |
| Ended summary | “Arrived 14:35 · Destination terminal,” retained for a proposed 20 minutes. |

For a separate boarding activity, offer **Check In** as the single primary action while check-in is available. Show a pending state, prevent duplicate submissions, and report success only after confirmation. Keep **Seat Map** in trip details. Every compact tap opens that same trip; the expanded and Lock Screen backgrounds also open it.

Update on confirmed ETA, gate, delay, and arrival changes. Mark stale information instead of continuing to claim “On time.” Reserve alerts for crucial changes and avoid duplicating the same alert with a separate notification. [Apple’s update and interaction guidance](https://developer.apple.com/design/human-interface-guidelines/live-activities)

**Review result:** The supplied plan fails the documented constraints above; the revised specification addresses them. Native rendering, narrow-width fitting, large text, Always On/StandBy appearance, push delivery, deep links, and disabled CarPlay controls remain untested and need device or simulator verification.