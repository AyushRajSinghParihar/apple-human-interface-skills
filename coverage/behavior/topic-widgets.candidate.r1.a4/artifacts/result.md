# Revised train-commute interaction specification

This is an iPhone design contract, based on `interface.md`, not an SDK implementation. The useful glance is **“When is my next train, and what has changed?”** Once a person follows a journey, it becomes **“What do I need to know next on this trip?”** All example trains and times below are simulated.

## Decisions and surface contract

Replace the logo and tiny station lists with departure time, route identity and explicit service status. Keep branding secondary. Periodic widgets serve planning; a Live Activity serves the bounded 50-minute journey. These choices follow [Widgets — Best practices and updating content](https://developer.apple.com/design/human-interface-guidelines/widgets#Best-practices) and [Live Activities — Best practices](https://developer.apple.com/design/human-interface-guidelines/live-activities#Best-practices).

| Surface / family | Content in priority order | Activation |
|---|---|---|
| Home small | Configured origin → destination; large expected departure `08:19`; `Delayed 7 min · Platform 4`; `Updated 08:10` | Entire widget opens that departure; with no selected service, opens configured route departures |
| Home medium | Same featured departure; two following services with expected times and cancellation/delay labels; freshness timestamp | Each service row opens its service; route heading opens route departures. Targets must remain distinct; drop secondary rows if space cannot support them |
| Lock inline, above clock | `R2 08:19 · +7 min` when fresh; `R2 · Updates unavailable` when stale | Exactly one target opens featured departure. No separate refresh, route or start controls |
| Lock rectangular, below clock | Route/direction; large expected departure; `Delayed 7 min` or `On time`; `As of 08:10` | Entire accessory opens featured departure |
| StandBy, small family | Same configured route and large departure; explicit delay/stale label and timestamp. Remove platform detail before shrinking the main time | Same destination as Home small; background removable |

Ship small and medium Home variants plus inline and rectangular Lock variants; omit large and circular variants until they add useful information. These families and placements are supported by the local [Widgets — Anatomy/platform guidance](https://developer.apple.com/design/human-interface-guidelines/widgets#Anatomy). StandBy uses the small family, not the medium layout stretched to fit.

Configuration: choose origin, destination/direction and optional line filter in app/widget configuration. Default to a recent explicitly selected route; do not infer “home” from location. With none selected, show `Choose a commute` and open route setup. Selection remains stable across refreshes; do not silently switch direction with time of day. Featured departure is the earliest eligible service by expected time. Keep a newly cancelled featured service as a labelled cancellation for 5 minutes alongside the next option in medium; small/Lock show `08:12 cancelled · View alternatives`. That 5-minute policy is a product choice.

A widget tap must carry route ID, service ID and service date, not only station names. If the service has expired, show its historical status plus current alternatives. After authentication, resume the original destination. The app preserves route/selection across interruption and orientation changes, following [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices).

## Data and update contract

All thresholds here are proposed product policies, not Apple refresh guarantees. The actual operator feed, cadence and transport are unspecified.

Data record: `serviceID, serviceDate, routeID, scheduledDeparture, expectedDeparture?, expectedArrival?, platform?, status, sourceObservedAt, receivedAt, revision`. Journey adds `journeyID, selectedServiceID, phase, nextStop?, startedAt, hardEndAt`. Store timezone-aware instants; display local station time, with day/date when crossing midnight. Unknown values remain unknown, never `0 min` or `Platform 0`.

- The source may deliver changed data whenever available; neither its polling nor delivery interval is established here. Request widget reloads for material feed changes and timeline entries for known departure boundaries, freshness expiry and configured commute windows. The system decides actual execution. No second-by-second network or widget promise.
- Use absolute expected time and `Updated HH:mm`, rather than a persistent “Live” badge. System-supported date/time presentation may update elapsed time without fetching; it cannot make an old prediction fresh. Avoid seconds precision.
- Fresh means a valid operator observation no older than 2 minutes. If the feed has an earlier validity deadline, use that deadline. Receipt of the same old observation does not reset age. A timetable-only record always says `Scheduled`, never `On time`.
- After freshness expiry, retain useful last-known time with `Last estimate 08:19 · Updates unavailable · As of 08:10`. Compact accessories replace the time with `Updates unavailable` if a qualifier cannot fit. Suppress countdowns, definitive next-stop claims and “On time” on stale data. Fresh platform data says `Platform 4`; stale data says `Last platform 4` only where space permits.
- No data: `Departures unavailable · Open for options`. Refreshing with cached data keeps that data and its age; first load uses a brief structural placeholder, then explicit unavailable/setup content. No endless blank or loading rectangle.
- A predicted departure passing does not prove the train departed. Without confirmation, show `Departure unconfirmed` and alternatives; do not count below zero. Confirmed departure removes it from planning widgets. Cancellation always replaces the departure claim with `Cancelled`.

These policies apply [Widgets — Updating widget content](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content); the 2-minute threshold requires validation with the actual provider.

```text
onRecord(record):
    reject mismatched service/date, older revision, or invalid future observation
    retain last valid record on fetch error
    derive freshness from sourceObservedAt and provider validity, not receivedAt
    request periodic-widget update if rendered content changed
    if matching active journey and rendered content changed:
        request activity update; attach crucial alert only once per event key

render(record, now, surface):
    if signedOutAndAccountRequired: return signInExplanation(surface)
    if privacyHidden: return safeSummary(surface)
    if noConfiguration: return chooseCommute(surface)
    if noValidRecord: return unavailable(surface)
    if cancelled: return cancelledWithObservationTime(surface)
    if expiredPredictionWithoutConfirmation: return departureUnconfirmed(surface)
    if stale: return qualifiedLastKnownOrUnavailable(surface)
    return expectedOrScheduledTimeWithStatusAndTimestamp(surface)
```

Prepare freshness-expiry content and activity expiry metadata where the eventual platform supports it. A delayed system render can still leave an older snapshot visible: always-visible observation timestamps are the fallback. Do not claim a guaranteed wall-clock stale transition without runtime evidence.

## Active journey lifecycle and presentations

In the departure detail, `Follow journey` starts one activity for the selected trip, with an easy `Stop following` action in the same app view. Following does not assert boarding. Phases are `Waiting → On train → Arrived`; cancellation can terminate Waiting, and stopping can terminate any active phase. Enter On train only from a reliable boarding/departure signal appropriate to this person, or their explicit `I'm on this train` action. Do not treat an operator departure alone as proof the person boarded.

A 50-minute trip is a bounded event suited to the local Live Activity guidance. Live Activity availability/permission is checked at integration time. If unavailable or dismissed, the app journey detail remains fully usable and widgets retain their periodic contract; no widget is converted into a promised real-time tracker.

| Presentation | Essential content |
|---|---|
| Compact leading / trailing | Train/line identifier / expected arrival `09:09`; if stale, trailing becomes unavailable symbol with meaningful accessible text. Both halves open the same journey |
| Minimal, including multiple activities | Train symbol plus remaining whole minutes when fresh, or `!` for disruption/staleness; accessible text distinguishes these states. Never logo alone |
| Expanded | Route/line in stable leading position; phase and expected arrival in stable trailing position; next confirmed stop and delay text below |
| Lock Screen banner | Same hierarchy with full labels: `On train · R2`, `Central arrival 09:09`, `Delayed 7 min`, `Next: Riverside`, observation time |
| StandBy | Scaled Lock layout, large arrival and explicit status, no crowded secondary list; safe margins and red night treatment |

Use no in-place activity button in this release; tap opens journey detail with boarding/stop actions. Hold behavior remains system-owned expansion. Keep the current journey identity stable through expansion and interruption. System-controlled Dynamic Island backgrounds are not customized. These choices follow [Live Activities — Presentation and interactivity](https://developer.apple.com/design/human-interface-guidelines/live-activities#Presentation).

During Waiting, show expected departure/platform; during On train, show expected arrival and next stop only when supported by fresh evidence. Delay is expected minus scheduled time, labelled `Delayed N min`; unknown estimate says `Delay · Time unknown`. Early trains say `Expected HH:mm`, not negative delay. Update changed fields only. Keep a stable, nonanimated layout; no continuous progress animation or timer-driven fake location.

Alert only for a confirmed cancellation, platform change while Waiting, or arrival estimate worsening by at least 5 minutes since the last alerted estimate. Coalesce simultaneous changes into one event and deduplicate by journey/revision/event type. Routine improvements and minute changes update silently. Use the activity alert path where available; never issue a duplicate push for the same event. If that path is unavailable, show the change in app without promising a notification. This is a product threshold applying [Live Activities — Lifecycle](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity).

End immediately on confirmed arrival at the selected destination, user stop, or cancellation of the followed trip. A passing ETA alone cannot assert arrival. Retain `Arrived 09:09` or `Journey cancelled` on Lock Screen for 15 minutes where permitted; remove active Island presentation. User stop removes the retained summary immediately. Without any terminal signal, end at `startedAt + 3 hours` with `Tracking ended · Arrival unconfirmed`, retaining for 15 minutes. This product safety bound accommodates the nominal 50-minute trip and delays without an indefinite activity. Ignore late updates after termination; following another train requires an explicit new selection.

## Appearance, access and account states

Home full color uses semantic light/dark foregrounds and backgrounds. In accented/tinted or clear treatment, expected time and status retain primary emphasis; route glyphs may use the accent group. Meaning never depends on red/green. In vibrant Lock/StandBy modes, use grayscale brightness for hierarchy rather than varying white opacity alone. StandBy removes backgrounds, enlarges primary information and preserves `Delayed`/`Unavailable` in red monochrome. Verify all required modes, per [Widgets — Rendering modes](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes).

Use actual text with semantic title/headline/body/supporting roles, regular through bold weights, and system sizing equivalents. At enlarged text, drop following services first, wrap route names where possible, then omit platform detail; preserve time, status, freshness qualifier and access to full detail. Inline uses concise text with a full accessible description and precise detail destination. Do not shrink everything to fit. See [Typography — Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type) and [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility).

Signed-out account-required state: `Sign in to see your commute`, one activation to sign-in, followed by route restoration. Small accessories shorten to `Sign in for trains`. Do not show private cached trips after sign-out; end associated activities and clear their retained summaries. If public departures are available, permit manual station selection without an account. Gallery description: `Check your next train`; previews use the simulated route below and each surface's true hierarchy, including a stale example.

| Data / access | Purpose and policy |
|---|---|
| Manually chosen stations, route and service IDs | Retrieve relevant departures; no location permission needed; keep selection locally where practical |
| Account credentials, if required | Authenticate private saved routes; use established secure storage; never render credentials or identifiers on surfaces |
| Current location | Not collected for this release; manual selection and following work without it |
| Visible journey destination | Potentially sensitive; default Lock/StandBy to `Train journey · Arrival 09:09 · Delayed 7 min`, with station names hidden; offer explicit Show station names preference in app |

Home can show configured station names; explain that visible widgets can be seen by others. No passenger name, ticket code or “Home/Work” address appears. Respect system redaction with `Train journey · Open to view` when full content is hidden, including accessible output. On supported Always On devices, keep field positions, dim secondary detail, retain arrival/status subject to privacy preference, suppress motion and seconds, and restore the same journey on activation. The local [Always On](https://developer.apple.com/design/human-interface-guidelines/always-on) reference names particular iPhone Pro models; this specification makes no universal hardware claim. Data minimization follows [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices).

## Worked before / after

Before, as stated in `interface.md`: all surfaces show a logo and tiny station list; inline has three targets; updates are promised every second; stale times still say Live; signed-out content is blank.

After, simulated commuter example:

| Moment | Planning widget / accessory | Followed journey |
|---|---|---|
| 08:10, fresh observation | Riverside → Central; `08:12 · On time · Platform 2 · Updated 08:10`. Inline `R2 08:12 · On time`, one tap | Follow journey begins Waiting; expected arrival 09:02 for a scheduled 50-minute ride |
| 08:11, feed predicts +7 min and platform 4 | `08:19 · Delayed 7 min · Platform 4 · Updated 08:11`; inline `R2 08:19 · +7 min` | Arrival 09:09; one coalesced alert for delay/platform change, no parallel push |
| 08:14, no newer observation | `Last estimate 08:19 · Updates unavailable · As of 08:11`; inline `R2 · Updates unavailable` | Stale qualifier replaces confident countdown/next stop; no fabricated progress |
| 08:19, fresh data and user confirms boarding | Planning surfaces move to next eligible departure after confirmed departure | On train; arrival 09:09, next stop only if feed supplies it |
| 09:09, confirmed arrival | Route continues showing upcoming trains | End immediately; safe arrival summary retained 15 minutes, then removed |
| Sign-out at any point | Explanation and sign-in destination replace private data | End and remove private activity summaries |

## Acceptance checks and evidence limits

**Passed — static specification inspection:** all supplied defects have explicit replacements; inline has one target; Home/Lock families are distinct; no continuous widget-refresh promise remains; stale records cannot be rendered as fresh by the specified reducer; signed-out/setup/unavailable states have copy and destinations; the journey has start, terminal signals and timeout; all worked data is identified as simulated. These passes concern the written contract only.

**Failed — supplied proposal:** its stated static logo purpose, three inline targets, second-by-second refresh guarantee, stale Live label and blank signed-out state fail this design contract. No running implementation was supplied to test.

**Not executed — required implementation acceptance:**

- Feed fixtures: at exactly 2 minutes retain freshness unless provider expiry is earlier; after 2 minutes show stale. Repeated receipt, out-of-order revision, cancellation, missing platform/ETA, midnight and timezone changes produce the specified states. Past ETA never asserts departure/arrival. Terminal activity rejects later updates.
- Delay fixtures: +7 minutes/platform change creates one alert; duplicate delivery creates none; +1 minute after that is silent; another cumulative +5 minutes qualifies. Cancellation ends tracking immediately. No feed for 3 hours ends with arrival unconfirmed.
- Follow every Home/Lock/Island target through cold launch, sign-in, expired service and interruption; confirm precise object, retained route and accessible app actions. Dismissing/unavailable activity preserves app functionality.
- Preview/render matrix: small, medium, inline, rectangular; fresh, delayed, cancelled, stale, missing, setup and signed-out; light/dark, all Home tint/clear options, vibrant Lock, removable StandBy background/red night, supported Always On. Check longest station names, 12/24-hour time, 200% text, supported accessibility sizes through AX5 and Bold Text. Time/status/freshness must remain readable with a full-text route.
- Measure actual contrast in each rendering context and Increase Contrast; inspect activation geometry, targeting the iOS 44 × 44 pt default for app/custom targets while retaining system accessory sizing. No invented targets inside inline.
- VoiceOver/assistive navigation: each service conveys route, expected versus scheduled time, status and observation time in that order; decoration is omitted, redaction also applies to spoken output, and all required actions can be reached without speech or complex gestures. Verify with actual assistive technology.
- Verify real timeline expiry/reload behavior, activity transport, alert deduplication, end/removal, multiple-activity minimal presentation, no-Island devices, dim/active transitions, StandBy distance and red-mode legibility. Default watch/CarPlay projections, if enabled by integration, must remain useful with disabled controls; no additional support is asserted here.

Only local `interface.md` and the installed apple-hig package were consulted. The installed root, selected family routes, topic procedures and corresponding guides were read in that order per route; topic-index searches resolved widgets, Live Activities, iOS, privacy, accessibility and Always On. Typography was additionally routed for enlarged text. Official links above identify the source sections referenced by the local snapshot; they were not opened online. No device, GUI, SDK compilation, network/feed, rendering, accessibility or energy tests were executed. No actual font, contrast, touch-target or delivery measurements exist. Platform/API availability, operator reliability and threshold suitability remain implementation-validation work; this document is not proof of runtime behavior or current Apple API support.
