Make this a **phase-based trip companion** focused on boarding and arrival, with the full itinerary always available in the app.

| Current plan | Correction |
|---|---|
| Start at booking; run throughout the 10-hour trip | Start when boarding becomes relevant, with an easy opt-out. Apple recommends bounded events ideally no longer than 8 hours; ActivityKit limits an individual activity to 8 active hours. Don’t promise continuous 10-hour coverage. Use distinct boarding and arrival activities when those phases become useful, rather than restarting merely to bypass the limit. |
| Hotel promotion and full app icon | Remove the promotion. Use a small, uncontained brand mark or recognizable bus symbol; avoid the full app icon. |
| Keep the arrival summary for 8 more hours | End immediately on arrival. Choose a short Lock Screen summary, such as **20 minutes**. Post-end retention is at most **4 hours**, subject to earlier dismissal. |
| Put the whole arrival sentence in compact trailing | Show only the essential changing value, such as **14:35**. Move gate and status into expanded and Lock Screen presentations. |
| Open different screens from compact leading and trailing | Both halves should open the **same active-trip screen**. |
| Expect custom buttons to work in CarPlay | CarPlay disables Live Activity buttons and toggles. Its presentation must remain useful entirely through status information. |

These corrections follow Apple’s [Live Activities guidance](https://developer.apple.com/design/human-interface-guidelines/live-activities) and [ActivityKit lifecycle documentation](https://developer.apple.com/documentation/activitykit).

**Proposed presentation**

| Surface | Boarding phase | Arrival phase |
|---|---|---|
| Lock Screen / expanded | Destination and service identifier; “Boarding · Gate 12”; departure time; one **Check In** action when available | Destination; **Arrives 14:35**; “On time” or delay; next stop and journey progress |
| Compact leading | Bus symbol with a short service identifier if it fits | Same identity and relative position |
| Compact trailing | Departure time | **14:35** |
| Limited-width / minimal | A meaningful boarding or progress graphic | A simple journey-progress graphic |
| CarPlay | Destination, boarding state, departure time and gate | Destination, ETA and delay status; no required interaction |
| Ended Lock Screen summary | — | “Arrived · [destination] · 14:35”; dismiss after about 20 minutes |

In limited-width contexts, design compact/minimal content to fit a **28-point circle**. If the trailing information cannot fit meaningfully, use a leading-only presentation instead of shrinking the full sentence.

**Interaction and state contract**

- **Check In:** offer only during the valid window. Show pending feedback, prevent duplicate submissions, and replace it with “Checked in” only after confirmation. If more input is required, open the trip’s check-in flow.
- **Seat Map:** keep it in the active-trip screen, reached by tapping the activity. This preserves room for status and one essential direct action.
- **Updates:** update for changed boarding, gate, ETA, delay, or arrival information. Alert only for crucial changes; avoid duplicating the same alert with a separate push.
- **Stale data:** show “Last updated…” and stop asserting “On time” when freshness is uncertain.
- **Arrival or cancellation:** end immediately and show the corresponding brief final state.

Use system button styles and accessible labels; follow Apple’s [button guidance](https://developer.apple.com/design/human-interface-guidelines/buttons).

The revised specification resolves all six supplied issues. Native rendering and behavior remain untested: verify narrow and multiple-activity layouts, enlarged text, Always On contrast, StandBy Night Mode, lifecycle expiration, and CarPlay with controls disabled.