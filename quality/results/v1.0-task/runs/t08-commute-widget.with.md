Build the set around **“When is my next train?”** Use a **Live Activity for “How is my journey progressing?”** Branding stays secondary.

The following examples use simulated departures.

| Surface | Content and hierarchy | Tap destination |
|---|---|---|
| Home Screen small | **8 min** → Central; Riverside · Platform 3; **Delayed +5 min**; updated time | That departure |
| Home Screen medium | Same next-train emphasis, plus two later departures with expected times and status | Each departure row opens its details |
| Home Screen large | Next train, later alternatives, and a relevant disruption or transfer warning | Selected train or disruption |
| Lock Screen inline | `Central · 8 min · +5 late` | **One target** opens the selected departure; remove the three separate targets |
| Lock Screen rectangular | `Riverside → Central` / **8 min · Platform 3** / `Delayed +5 min` | Selected departure |
| Lock Screen circular | Train symbol, **8**, `min`; replace countdown with a warning symbol when cancelled or stale | Selected departure |

Configure origin, direction, and optional route filter through widget configuration. Keep the chosen commute stable. Large variants add useful alternatives rather than more tiny station names. These choices follow Apple’s [widget guidance](https://developer.apple.com/design/human-interface-guidelines/widgets).

**Updates and delays**

Remove the every-second refresh promise. WidgetKit schedules refreshes under system limits; system time views can advance a countdown without fetching new train information.

- Request updates around meaningful events: expected departures, commute periods, changed predictions, cancellations, and platform changes. Delivery timing remains system-controlled.
- Show the **expected** departure prominently. For example, `08:47 · Delayed +5 min`, with `Scheduled 08:42` where space permits.
- Keep available information visible while refreshing.
- Never treat a countdown reaching zero as proof that a train departed. Without confirmation, show `Departure time passed · Check status`.
- A cancellation replaces the countdown with **Cancelled**; larger widgets offer the next alternative.

Use this proposed freshness contract; its thresholds are product decisions to validate against the operator’s feed:

| Data condition | Presentation |
|---|---|
| Valid real-time prediction, source observation ≤2 minutes old | `Updated just now` or `Updated 1 min ago` |
| Older than 2 minutes, or operator validity expires sooner | **Updates delayed**; show last-known absolute time and update timestamp; stop the confident countdown |
| Timetable only | **Scheduled**; no “Live” label |
| No usable data | **Departures unavailable · Open app** |

Measure age from the operator’s observation time, not merely when the app downloaded it. Prepare expiry states in advance so freshness does not depend on another network response.

**The 50-minute journey**

A 50-minute train trip is an appropriate bounded [Live Activity](https://developer.apple.com/design/human-interface-guidelines/live-activities). Start it when the person selects **Start journey**, with an easy way to stop tracking.

- **Lock Screen and expanded Dynamic Island:** destination, next stop, expected arrival, and delay. Example: `Central · Arrive 09:35` / `Next: Oak Park` / `Delayed +5 min`.
- **Compact:** train/route identity on one side; arrival time on the other.
- **Minimal:** meaningful changing status, such as minutes remaining or a disruption symbol—not just the logo.
- Tapping opens the active journey. Keep detailed route changes in the app.

Update when predictions, next stop, platform, cancellation, or journey state change, using ActivityKit updates and push delivery where available. This also carries no per-second network guarantee. A timer may count toward the latest estimate; label it as an estimate and never imply measured train position.

On stale updates, show **Updates delayed · Last arrival estimate 09:35**. Alert only for consequential changes such as cancellation or a platform change, and avoid duplicating the same alert with a separate notification.

End immediately on confirmed arrival, cancellation, or the person ending tracking. Retain an arrival summary for 15 minutes. If confirmation never arrives, expire tracking at a defined deadline—for example, 30 minutes after the last expected arrival—and say **Tracking ended · Arrival unconfirmed**.

**Appearance and account states**

Use semantic text/background colors and readable system text. Status must survive loss of color: always include words such as **Delayed**, **Cancelled**, and **Scheduled**.

- **Tinted Home Screen:** deliberately separate primary and accent groups; preserve countdown and warning hierarchy under any tint.
- **Dark appearance:** use adaptive colors and assets, with measured contrast.
- **Lock Screen/Always On:** optimize grayscale emphasis and reduced luminance.
- **StandBy:** adapt the small widget for distance, prioritize the large departure value, allow background removal, and verify red monochrome Night Mode. Avoid tiny alternatives.
- **Signed out:** if public departures work without an account, keep showing them. Otherwise show `Sign in to see your commute`, linking to sign-in and returning to widget setup afterward.
- **Not configured:** `Choose a station`, linking to setup.
- **Loading:** use a brief structured placeholder only before usable data exists. Gallery previews show realistic example content.

These treatments follow Apple’s [rendering-mode guidance](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes), [Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode), and [accessibility guidance](https://developer.apple.com/design/human-interface-guidelines/accessibility).

The proposed specification addresses all listed defects. Device checks remain unexecuted: verify long station names and enlarged text, VoiceOver labels and destinations, stale/offline transitions, tint and contrast, StandBy red mode, and Live Activity completion and expiry.