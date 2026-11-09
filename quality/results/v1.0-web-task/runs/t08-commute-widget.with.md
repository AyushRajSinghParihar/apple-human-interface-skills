Design around two questions: **“Which train should I catch?”** in widgets, and **“How is my journey going?”** in a Live Activity.

The layouts and freshness thresholds below are proposed product decisions. Example departures are simulated.

**Widget set**

| Surface | Content and hierarchy | Tap destination |
|---|---|---|
| Home Screen small — **Next train** | Large **08:42**; `Central → Riverside`; `Platform 4 · +7 min`; freshness below | That departure’s details |
| Home Screen medium — **Commute options** | Selected route, next departure prominently, two later alternatives, one relevant disruption | Each departure opens its details |
| Lock Screen rectangular | `Central → Riverside` / **08:42 · +7 min** / `Platform 4` | Selected departure |
| Lock Screen circular | Train symbol, **8 min**, short station identifier; replace countdown with a warning when stale | Selected route’s departures |
| Lock Screen inline | `Train 08:42 · +7 min` | One destination: selected departure |

Remove the dominant app logo. Use a restrained identifying mark only if needed. Each size adds useful information without shrinking a station list. **Inline accessories support one tap target**, so remove the three separate targets. These choices follow Apple’s [widget guidance](https://developer.apple.com/design/human-interface-guidelines/widgets).

Let people configure origin, destination/direction, and outbound or return commute. Keep that selection stable rather than silently changing routes.

**Delays and freshness**

Replace “refreshes every second” with **“Updates as new information becomes available.”** Widget refresh timing is system-controlled. Use timelines for known departure transitions and system-rendered time text for countdowns; a changing countdown does not mean fresh train data arrived. Request reloads when relevant data changes, without promising immediate delivery. See [Keeping a widget up to date](https://developer.apple.com/documentation/widgetkit/keeping-a-widget-up-to-date).

Use this state contract:

| State | Display and behavior |
|---|---|
| Fresh prediction | `Expected 08:42 · +7 min`, with `Updated 08:34`; delay compares expected against scheduled time |
| Timetable only | `Scheduled 08:35`; never label it “Live” |
| Prediction expired | `Updates unavailable · Checked 08:34`; label retained values “Last expected” and stop the actionable countdown |
| Cancelled | Explicit **Cancelled**; retain the affected service identity and promote the next usable alternative |
| No service | `No more trains today`, with the next scheduled service if known |
| Refreshing | Keep useful existing content and its timestamp |
| No cached data | `Departures unavailable · Open app` |

Use the operator’s validity window; an initial fallback is **stale after two minutes**, subject to feed validation. Schedule an expiry timeline entry, but retain the absolute timestamp because rendering can be deferred. Avoid an evergreen “Live” badge.

**Active journey: use a Live Activity**

A 50-minute journey is a bounded event suited to a Live Activity and comfortably within ActivityKit’s eight-hour active limit. Update it through ActivityKit/APNs when journey facts change; delivery is not a second-by-second guarantee. See [ActivityKit’s lifecycle guidance](https://developer.apple.com/documentation/activitykit/displaying-live-data-with-live-activities).

- **Start:** When the person chooses “Start journey”; offer an easy way to stop tracking.
- **Lock Screen / expanded:** Destination, next stop, expected arrival, delay, and transfer/platform changes.
- **Dynamic Island compact:** Train/route identity and arrival countdown.
- **Minimal:** A meaningful remaining-time or disruption indicator, rather than only a logo.
- **Updates:** Apply changed arrival estimates, stops, cancellations, and platform information. Mark expired estimates as stale; don’t infer arrival merely because a timer reaches zero.
- **Alerts:** Reserve attention for actionable changes, such as cancellation or a platform change. Avoid duplicate notification and Live Activity alerts.
- **End:** End on confirmed arrival, cancellation, or the person ending tracking. Retain a brief arrival summary for 15 minutes, then dismiss. Handle lost tracking explicitly.

All presentations deep-link to the current journey. Apple’s [Live Activities guidance](https://developer.apple.com/design/human-interface-guidelines/live-activities) supports this focused lifecycle.

**Appearance and account states**

Use semantic light/dark colors. In tinted mode, separate primary information from accents; preserve `+7 min`, **Cancelled**, and warning symbols without relying on route colors. Lock Screen accessories need a clear monochrome hierarchy. StandBy should adapt the small widget to large, glanceable text, removable backgrounds, and red monochrome night presentation.

Signed-out people should see public departures where available. If authentication is required, show **“Sign in to see your commute”**, with a tap opening sign-in and returning to setup. Unconfigured widgets show **“Choose a station.”** Gallery previews use realistic sample departures; loading placeholders preserve layout without inventing live values.

Use actual text and system text styles. At larger accessibility sizes, remove secondary departures before shrinking essential information.

**Validation status:** The supplied proposal fails the design review for low utility, separate inline targets, the refresh promise, misleading freshness, and blank signed-out state. The revised specification addresses those issues. Device rendering, VoiceOver, deep links, delayed updates, long station names, tinted/dark appearance, and StandBy night mode remain untested and are acceptance checks for implementation.