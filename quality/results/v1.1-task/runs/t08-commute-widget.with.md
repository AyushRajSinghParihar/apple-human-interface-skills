Make the widget answer **“When is my next useful train, and has anything changed?”** Use a Live Activity for the 50-minute journey.

The following examples use simulated departures.

| Surface | Content and hierarchy | Tap destination |
|---|---|---|
| Home Screen small | **08:18** · Central → Riverside · Platform 4 · **Delayed 6 min** · Updated 08:10 | That departure |
| Home Screen medium | Same prominent departure, plus two later alternatives with departure time, platform, and status | Each departure opens its details |
| Lock Screen rectangular | **08:18 to Riverside** / Platform 4 · Delayed 6 min | That departure |
| Lock Screen inline | Train symbol · **Riverside 08:18 · +6 min** | One target: that departure |
| Lock Screen circular | Train symbol, **8 min**, short route identifier; use **“!”** for a disruption requiring attention | Departure or disruption details |

Keep branding subordinate to departure information. Offer configuration for origin, destination or direction, and a preferred route. Avoid a large variant until there is a clear need beyond more stations. These choices follow Apple’s [widget purpose, sizing, and interaction guidance](https://developer.apple.com/design/human-interface-guidelines/widgets).

**Updates and delays**

Remove the every-second refresh promise. WidgetKit controls refresh opportunities; request updates around meaningful timetable changes and use system date/time views for relative times where appropriate. An advancing countdown represents time passing, not a newly verified train prediction.

Adopt this explicit product policy, then tune it to the operator’s actual feed:

| Data state | Display behavior |
|---|---|
| Recent prediction | Show predicted departure, delay relative to schedule, and “Updated 08:10.” |
| Prediction older than 2 minutes | Mark **“Updates delayed · checked 08:10.”** Replace the countdown with an absolute last-known estimate. Remove “Live.” |
| Prediction older than 5 minutes | Stop treating it as current. Show **“Live times unavailable”** and separately labeled scheduled departures, if available. |
| Cancellation | Show **“Cancelled”** prominently; use medium-widget space for the next viable service. |
| Refresh underway | Retain useful existing information and its freshness label. |
| No usable data | Show **“Departures unavailable”** with a route-specific app destination. |

The two- and five-minute thresholds are proposed product decisions, not Apple requirements. Never infer “departed” solely because an old estimate passed. Apple recommends [meaningful refreshes and freshness information](https://developer.apple.com/design/human-interface-guidelines/widgets).

**A 50-minute active journey**

Use one [Live Activity](https://developer.apple.com/design/human-interface-guidelines/live-activities), starting when the person chooses **“Track journey”**, with an easy way to stop tracking. Fifty minutes is appropriate for a bounded event.

- **Lock Screen and expanded:** destination, **“Arrive 09:08 · 6 min late,”** next stop, and confirmed journey progress. Indicate when progress or arrival is estimated.
- **Compact Dynamic Island:** train/route identity on the leading side; arrival time on the trailing side. Both open the active journey.
- **Minimal:** train symbol with remaining minutes, or a disruption indicator when that is more useful.
- **StandBy:** enlarge arrival time and next stop; preserve meaning in red Night Mode.

Update when arrival estimates, stops, platforms, or disruption status change. Use ActivityKit updates rather than widget polling; delivery timing remains system-controlled. Mark stale estimates clearly and stop implying live movement when updates are lost.

Alert only for consequential changes such as cancellation, an imminent platform change, or a threatened connection. Avoid a duplicate push for the same Live Activity alert.

End on confirmed arrival, cancellation, or the person stopping tracking. Remove it from Dynamic Island immediately; retain a concise arrival summary on the Lock Screen for about **15 minutes**. If arrival cannot be confirmed, show **“Journey status unavailable”** and use a bounded tracking timeout instead of claiming arrival.

**Appearance, setup, and accessibility**

Follow Apple’s [rendering and placeholder guidance](https://developer.apple.com/design/human-interface-guidelines/widgets):

- **Tinted:** separate primary and accent groups. Time, route, and disruption must remain readable without brand colors.
- **Dark:** use semantic foreground/background colors and verify supporting text contrast.
- **StandBy:** adapt the small family, allow background removal, and prioritize large time/status text. Verify red monochrome at night.
- **Lock Screen and Always On:** use symbols plus words for status; verify grayscale and reduced-luminance legibility.
- **Signed out:** show public timetable information if authentication is unnecessary. Otherwise show **“Sign in to see your commute”**, opening sign-in and returning to widget setup.
- **Unconfigured:** show **“Choose your commute”**, opening route selection. Use realistic gallery previews and brief loading placeholders.
- Use actual text, system styles, and meaningful VoiceOver labels. At larger text sizes, remove secondary alternatives before shrinking primary information. Offer a privacy option to hide personal destination names on the Lock Screen.

Design acceptance requires checking long station names, large accessibility text, cancellations, stale/offline states, precise deep links, all rendering modes, and Live Activity completion. **This is a proposed specification; native rendering, VoiceOver, refresh delivery, and device behavior have not been tested.**