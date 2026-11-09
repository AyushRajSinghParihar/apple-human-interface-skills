Make the set answer two questions: **“When should I leave?”** and **“How is my journey going?”** Replace the prominent logo with departure time, destination, and service status.

| Surface | Proposed design | Tap behavior |
|---|---|---|
| Home Screen small | Saved commute, next departure in large type, destination, platform, and delay: **“08:24 · +6 min”** | Open that departure |
| Home Screen medium | Next three departures for a configured station and direction; prioritize cancellations, platform changes, and delays | Each departure opens its details |
| Home Screen large | Next departures plus a useful disruption summary and alternatives | Open the relevant service or alternative |
| Lock Screen inline | One concise line: **“Central 08:24 · +6 min”** | One target opening the commute |
| Lock Screen circular | Train symbol and **“8 min”**, with a short station label where space permits | Open the next departure |
| Lock Screen rectangular | Station → destination, next departure, platform, and status | Open the next departure |

These should be distinct layouts, with fewer details at smaller sizes. The inline accessory must have **one tap target**; remove its three separate targets. Keep branding subtle and use configuration for station, direction, and saved commute. [Apple’s widget guidance](https://developer.apple.com/design/human-interface-guidelines/widgets)

**Departures and delays**

- Remove the every-second refresh promise. Use WidgetKit timelines for known schedule changes, request reloads when new data arrives, and use supported widget push updates opportunistically. The system controls update delivery; a countdown changing onscreen does not mean fresh train data was fetched. [Widget update guidance](https://developer.apple.com/documentation/widgetkit/keeping-a-widget-up-to-date)
- Show the expected departure prominently and the delay explicitly: **“08:24 · 6 min late”**, with **“Scheduled 08:18”** on larger layouts. Show **“Cancelled”** instead of a departure countdown.
- Define freshness from the transport feed’s validity window. Once expired, replace **“Live”** with **“Updated 5 min ago”** or **“Updates unavailable.”** Label timetable fallback **“Scheduled.”** Never silently present an old prediction as current.
- Do not infer that a train departed merely because its predicted time passed. When unconfirmed, show **“Departure unconfirmed”** and the last update time.

**The 50-minute active journey**

Use a **Live Activity** for the journey, alongside the reusable departure widgets. Start it when the person starts tracking a journey. Show destination, next stop, expected arrival, and delay on the Lock Screen; use compact train/status information in the Dynamic Island and more detail when expanded.

Update on meaningful events: boarding, next-stop changes, revised arrival, platform changes, cancellation, and arrival. Use date-based countdowns between updates. Set a `staleDate` so lost updates produce an honest stale state; reserve alerts for actionable changes. Fifty minutes fits comfortably within ActivityKit’s eight-hour active limit. End on confirmed arrival, cancellation, or the person ending tracking, with a brief final status. [ActivityKit guidance](https://developer.apple.com/documentation/activitykit/displaying-live-data-with-live-activities)

**Appearance and empty states**

- Support tinted rendering with clear foreground hierarchy, readable symbols, and text labels. **“Delayed”** and **“Cancelled”** must remain understandable without color.
- Adapt backgrounds and text to dark appearance. In StandBy night mode, let the system apply its treatment; ensure the layout remains readable in monochrome, at a distance, and with reduced brightness.
- Replace the signed-out blank rectangle with **“Set up your commute”** and a tap into setup or sign-in. If public departures work without an account, offer **“Choose a station.”**
- Test every size in tinted and dark appearances, StandBy night mode, larger text, and fresh, stale, cancelled, offline, and signed-out states. [Apple’s widget appearance guidance](https://developer.apple.com/design/human-interface-guidelines/widgets)