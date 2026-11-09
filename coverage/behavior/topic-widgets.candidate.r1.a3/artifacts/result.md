# Train commute: revised interaction specification

Design contract for iPhone, based on `interface.md`. Framework agnostic; all train data below is simulated. The glance question is **“When is my next train, and has anything changed?”** During a journey it becomes **“What happens next, and when will I arrive?”**

## Decisions and surface contract

Replace the logo and tiny station list with departure information. Offer Home Screen small and medium, and Lock Screen inline, circular and rectangular variants. Do not stretch one layout across families. Large adds no necessary commute value and is out of scope. The small Home variant also supplies a simplified StandBy layout. These family/context choices and useful-information hierarchy follow the local [Widgets guide: anatomy and best practices](https://developer.apple.com/design/human-interface-guidelines/widgets#Anatomy).

Configuration selects origin, direction/destination and optional line; defaults may use a previously selected route, never inferred sensitive travel history without choice. A widget stays bound to that route even while another journey is active. Public departures do not require an account; signed-in saved routes are optional product functionality.

| Surface | Content in priority order | Activation |
|---|---|---|
| Home small | `Central → Riverside`; `08:18`; `Delayed +6 min`; `Checked 08:10` | Entire surface opens that departure's detail; if unavailable, route departures with an explanation |
| Home medium | Same first departure with platform if confirmed; second departure and disruption summary | Each distinct departure row opens its service detail; remaining area opens route departures |
| Lock inline, above clock | `Riverside 08:18 · +6 min` | Exactly one target: selected departure detail; no separate station, time or alert controls |
| Lock circular, below clock | Train symbol, `08:18`, `+6m`; accessible name includes route and freshness | One target: selected departure detail |
| Lock rectangular, below clock | Route; `08:18 · Delayed +6m`; `Checked 08:10` | One target: selected departure detail |
| StandBy small | Large `08:18`; `Riverside`; `Delayed +6m`; compact freshness | Opens selected departure detail; no tiny controls |

Every variant reserves space for freshness/error wording. In inline/circular layouts, stale state replaces the delay detail with `Old` or `Check`; full accessible text gives last check time. No countdown in these smallest variants: absolute time leaves room to explain uncertainty. Widget tap behavior follows [Adding interactivity](https://developer.apple.com/design/human-interface-guidelines/widgets#Adding-interactivity).

## Departure data and update policy

The following thresholds are product decisions, not Apple refresh guarantees. Store service ID, route ID, scheduled and predicted times, cancellation, confirmed platform, source observation time, receipt time, validity deadline, and source revision. Validate route/service identity and reject older revisions. Source observation age determines freshness; receipt time alone must not make old observations fresh.

- Fresh: valid observation no older than 2 minutes and before any earlier source expiry. Show predicted departure, delay relative to scheduled departure, and `Checked HH:mm`. Use `On time` only if explicitly supported by the source. Do not use the word `Live` in the widget set.
- Stale: expiry reached, observation older than 2 minutes, or invalid clock metadata. Show `Updates delayed · checked HH:mm`; label retained prediction `Last estimate 08:18`. Drop unsupported platform certainty. Never silently revert to an on-time claim.
- Unavailable: no usable observation, or last observation older than 10 minutes. Show `Live times unavailable`; a valid separate timetable may show `Scheduled 08:12`, clearly distinguished from a prediction. Without a timetable show `Open departures`.
- Cancelled: show `Cancelled`, preserving scheduled service identity. Medium shows the next eligible service separately. Do not replace a cancelled service with an unlabelled later train. Departures that pass their usable time leave the next-train slot; without fresh confirmation do not claim they departed. Show the next usable train or unavailable state.

Request reload opportunities for meaningful feed changes and timeline boundaries: freshness expiry, departure selection change, commute viewing window, and unavailable transition. Request a fresh fetch when the app opens. Keep available content during fetch; only a first load uses placeholders. Source feed delivery frequency, reload requests, and actual system rendering are separate. The system controls widget refresh; no every-second or exact delivery promise. Use system time presentation for any optional Home countdown, suppress it once stale, and never use its ticking as evidence of fresh train data. See [Updating widget content](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content).

```text
onObservation(observation):
  if identityValid(observation) and newerThanStored(observation):
    persist(observation)
    requestWidgetReload()                 // opportunity, not a delivery guarantee
    if followedJourney exists and visibleContentChanged:
      requestActivityUpdate(deriveJourneyState())

render(now, stored):
  status = classify(stored.sourceTime, stored.validUntil, now)
  if status == fresh: return confirmedOrPredictedDeparture(stored)
  if status == stale: return lastEstimateWithTimestamp(stored)
  return clearlyLabelledTimetableOrUnavailable()
```

Freshness expiry must be included in the requested timeline and activity stale policy. If the system leaves an older snapshot visible, its absolute `Checked` time still exposes its age. The product cannot guarantee timely stale-label rendering when execution is deferred.

## Active journey: one bounded Live Activity

The 50-minute journey warrants a Live Activity, not a faster-refreshing widget. In the service detail, `Follow journey` starts one activity for the selected service and opens the active-journey screen. Start on explicit selection; provide `Stop following` there. No activity starts just because someone viewed a widget. If activities are disabled/unavailable, explain that in the app and keep the same journey screen usable; widget refresh promises remain unchanged. Use one activity through boarding, travel and arrival. This follows [Live Activities: best practices and lifecycle](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity).

| State/event | Visible result and transition |
|---|---|
| Following, before departure | Service, expected departure, confirmed platform, delay; `Departing 08:18` |
| Source confirms departure or user confirms boarding in app | Traveling: `Next: East Junction 08:36`; `Riverside arrival 09:08 · +6m` |
| Changed prediction/platform/cancellation | Update only changed meaningful content; preserve service identity and layout anchors |
| Feed becomes stale | `Updates delayed · checked 08:40`; `Last arrival estimate 09:08`; suppress countdown/progress implying confirmed movement |
| Arrival estimate passes without confirmation | `Arrival unconfirmed · last estimate 09:08`; do not infer completion from a timer |
| Arrival confirmed or user ends in app | End immediately; optional Lock Screen summary `Arrived Riverside 09:08` or `Following ended`, retained 15 minutes; active presentations disappear |
| Service cancelled | Terminal `Cancelled · open alternatives`; end activity, retain summary 15 minutes; app offers alternatives, never auto-follows another train |
| No confirmation by 2 hours after scheduled arrival | Product timeout: end with `Tracking ended · arrival unconfirmed`; no false arrival claim |

Lock Screen/expanded presentation shows next stop, arrival estimate, delay and checked time. No map, full station list or promotions. Tapping opens this exact journey. No inline action is necessary; ending remains in the app to avoid accidental loss. Compact Dynamic Island: train/line identity and arrival `09:08`; minimal: abbreviated changing arrival time, cancellation symbol or stale `?`, with accessible service/state label. Both compact halves open the same journey; hold uses system expansion. Expanded preserves identity and timing positions. StandBy scales the Lock Screen content with large timing and no extra detail; supporting mirrored presentations must retain the same state meaning, with no required interactive controls. Support and fit require implementation verification. See [Live Activities: presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Presentation).

Request an activity alert only for cancellation, a changed boarding platform before departure, or an arrival/departure estimate worsening at least 5 minutes since the last alerted estimate. These are product thresholds; coalesce simultaneous changes and deduplicate by service/revision. Recovery updates silently. Do not send a parallel push for the same activity alert. A feed outage changes status without an urgent alert. Activity updates are event-driven, not per-second network polling; local date presentation may tick without new feed data. No guaranteed delivery latency. Animations, if used, last at most 2 seconds and convey a changed value; no animation dependency in Always On. See [transitions and updates](https://developer.apple.com/design/human-interface-guidelines/live-activities#Adding-transitions-and-animating-content-updates).

## Appearance, privacy and exceptional states

Use real text, system text styles, flexible margins and container-relative shapes. Prefer at least 11 pt in widgets rather than shrinking to fit. At large accessibility sizes remove platform, secondary departure, then optional line detail; preserve destination, time, disruption and freshness. Long names wrap where possible; configured short station names must remain unambiguous in the app and accessible labels. Spoken order: route, departure/next stop, delay/cancellation, freshness, action. Proposed labels require actual assistive-technology validation.

Full color supports semantic light/dark foreground/background pairs. In accented tint/clear mode, time is primary and route/symbol accents are subordinate; no preserved full-color logo. Vibrant Lock Screen content uses grayscale brightness hierarchy, not reduced white opacity alone. `Delayed`, `Cancelled` and `Updates delayed` carry meaning independently of red/green. StandBy removes the background, enlarges time, drops the second departure, and preserves state in red monochrome Night Mode. Always On must remain understandable without animation. Sources: [Widgets: rendering modes](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes), [text](https://developer.apple.com/design/human-interface-guidelines/widgets#Displaying-text-in-widgets), and [StandBy](https://developer.apple.com/design/human-interface-guidelines/widgets#StandBy-and-CarPlay).

Privacy defaults: no passenger names, ticket codes, account identifiers, or inferred Home/Work labels. Lock Screen and StandBy initially show `Train 08:18 · +6m`, withholding route and station names until the user explicitly enables travel details on those surfaces. Redacted activity shows `Journey in progress · open for details`, including accessible text. App activation requires normal system authentication where applicable. User-selected public route information may appear on Home Screen; explain that exposed screens can be seen by others. See [Live Activities: best practices](https://developer.apple.com/design/human-interface-guidelines/live-activities#Best-practices).

Signed out with a configured public route: continue showing public departures. If a saved route cannot be recovered: `Choose your commute`, opening route selection with optional sign-in to restore saved routes. Never a blank rectangle. Initial unconfigured state uses the same setup destination. First-load placeholder preserves route framing briefly; failed fetch becomes unavailable, not an indefinite shimmer. Gallery description: `Check your next train`; previews show realistic simulated delayed, normal and unavailable states, not placeholder blocks. See [Widgets: previews and placeholders](https://developer.apple.com/design/human-interface-guidelines/widgets#Previews-and-placeholders).

## Worked before/after

Before, per the supplied brief: each widget is a logo plus tiny station list; inline draws three targets, refresh is promised every second, old departures remain `Live`, and signed-out content is blank.

After, simulated route with travel details enabled: at 08:10 the source reports service C12 scheduled 08:12, predicted 08:18, arrival scheduled 09:02 and predicted 09:08 (a 50-minute ride). Small Home shows `Central → Riverside / 08:18 / Delayed +6 min / Checked 08:10`. Inline shows `Riverside 08:18 · +6m` with one departure destination. Medium adds the separately identified 08:32 service. At 08:13 without another observation, the next available render shows `Last estimate 08:18 / Updates delayed · checked 08:10`; inline substitutes `Riverside 08:18 · Old`. By 08:21 it shows unavailable or a clearly labelled timetable, never an old live prediction.

In a separate continued-feed branch, the user follows C12 at 08:11. A new observation at 08:18 confirms departure; the activity shows next stop and `Arrival 09:08 · +6m`. At 08:40 the feed revises arrival to 09:14 (+12m); request one crucial delay alert and update the activity, without a duplicate push. Fresh source observations continue. At 09:14 arrival is confirmed: end the activity immediately and retain `Arrived Riverside 09:14` on Lock Screen until 09:29. Without confirmation, use `Arrival unconfirmed`, not `Arrived`.

## Acceptance checks and evidence limits

**Passed — specification inspection only:** separate useful surface contracts replace logo/list layouts; inline has one destination; system refresh limits are explicit; timestamped stale/unavailable states replace `Live`; account/setup states are nonblank; a bounded journey has start, update, stale, cancellation and end transitions. Worked values preserve the 50-minute initial journey and distinguish scheduled/predicted times. No runtime pass is implied.

**Failed — supplied proposal inspection:** useful glance hierarchy, inline target count, refresh promise, stale labelling, and logged-out state. No source code or screenshot was supplied to establish any other existing defect.

**Not executed — acceptance matrix for implementation:**

| Check | Expected observable result |
|---|---|
| Feed ages through 2 and 10 minutes; expires early; arrives out of order | Fresh → stale → unavailable; earlier expiry wins; old revision cannot restore freshness |
| Refresh request delayed/offline; app opens | Available snapshot persists with absolute check time; app requests current data; no false live claim |
| Prediction passes; cancellation; no next departure | No false departure/arrival assertion; cancellation remains identified; clear empty/unavailable result |
| Follow, departure, revised estimate, stale, arrival, stop, timeout | One activity with defined transitions; exact journey deep link; no restart after dismissal without user action |
| Alert revision repeated, then recovery | One alert per qualifying change; no duplicate push; recovery silent |
| Tap every variant and each medium row | Exact route/service/journey destination; inline always one target; missing object has explained fallback |
| Small/medium/accessories with long station names, localized time, midnight/time zone change and accessibility sizes | No lost critical status, misleading abbreviation, overlapping text or clipped freshness; absolute times use departure station zone, labelled if different from device zone |
| Light/dark, tint/clear, vibrant Lock Screen, Always On, StandBy day/red Night Mode | Time/state/freshness readable without color or background; no reliance on animation |
| Signed out, unconfigured, first load, feed error and privacy redaction | Useful explanation and correct destination; no blank or leaked station/accessibility text |
| VoiceOver, supported iPhone sizes, Dynamic Island and non-Island presentations, mirrored destinations | Correct spoken order and targets; fit and contrast verified on supported platform; activity state consistent |

Only local `interface.md` and installed guidance were used; official links above identify the guides, not web verification. Audit read order: installed root `SKILL.md` → system-experiences family `SKILL.md` → widgets topic `SKILL.md` → widgets reference. Attempted the family's Live Activities topic path before its source; it is missing. A hidden-file search and the topic-index entry confirmed the same unresolved installed path. The Live Activities reference was read as a documented fallback, so its topic-procedure audit is **incomplete**, not passed.

The local guides identify a 2026-10-25 snapshot. Product freshness thresholds, alert thresholds, public-data availability and privacy defaults are design choices requiring backend/product confirmation. No SDK, device, GUI, rendering, timeline delivery, feed integration, accessibility, contrast measurement or compilation was executed. Platform/API availability and system-delivery behavior remain implementation evidence gaps; this specification does not establish them.
