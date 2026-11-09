# Train commute: revised interaction specification

Design artifact for iPhone Home and Lock Screens, based on `interface.md`. Framework agnostic; all train data below is simulated. The glance questions are **“When is my next train, and has it changed?”** before travel and **“What happens next on this journey?”** during travel.

## Decisions and source basis

Replace logo-led station lists with departure information. Offer Home small and medium, plus Lock Screen inline, circular and rectangular accessories. Small is also the StandBy variant; medium is not proposed for StandBy. Larger widgets add departure alternatives rather than stretch the small layout. These choices follow the local [Widgets: anatomy and best practices](https://developer.apple.com/design/human-interface-guidelines/widgets#Anatomy).

Separate periodic widgets from a bounded Live Activity for the 50-minute journey. Widgets have system-controlled refresh opportunities; remove the every-second promise. A Live Activity can convey frequently changing journey information, but its delivery is also not guaranteed. Follow [Widgets: updating content](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content) and [Live Activities: lifecycle](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity).

The inline accessory has exactly one target. All activation opens the corresponding departure or journey, preserving context across authentication and interruption, rather than opening a generic app home. See [Widgets: interactivity](https://developer.apple.com/design/human-interface-guidelines/widgets#Adding-interactivity) and [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices).

The freshness thresholds, refresh requests, delay alert thresholds and retention times below are product decisions, not Apple requirements. Validate them against the eventual transit feed and platform implementation.

## Surface contract

Configuration selects origin, destination/direction and service filter in the app or widget configuration. Manual station selection works without location permission. A widget remains pinned to its configured commute when a journey starts; its trip link gains “Journey in progress” when it matches the tracked train. It does not silently switch to a different route.

| Surface | Content in priority order | Activation |
|---|---|---|
| Home small | Direction “To Central”; “08:18”; “Delayed 6 min”; “Platform 3”; “Updated 08:11” | Whole surface opens this service’s departure detail; status and time are not separate controls |
| Home medium | Same first departure; origin; next two alternatives, each with time and status; shared freshness footer | First departure area and each alternative open their own service detail; remaining area opens configured route departures |
| Lock inline | “Central 08:18 · +6 min” when fresh; “Central · Check times” when stale | One target opens route departures, focused on the displayed service if still available |
| Lock rectangular | “To Central”; “08:18 · Delayed 6 min”; “P3 · Updated 08:11” | Whole accessory opens displayed service |
| Lock circular | Train symbol; “08:18”; “+6m” | Whole accessory opens displayed service; accessible description includes direction and delay |
| StandBy small | Large “08:18”; “To Central”; “Delayed 6 min”; short freshness line | Same destination as Home small; no miniature list or added controls |

Circular stale state replaces the time with “Check” and a status symbol; its description says “Departure information out of date. Open departures.” Never leave a plausible time without a stale indication. Omit circular platform detail to preserve legibility. The app destination always exposes full names and complete data.

Use actual text, adaptable margins and system text styles or equivalent scalable styles, not a fixed image/canvas. At enlarged sizes, remove platform and alternatives before reducing the main time, direction, status or freshness meaning. Inline/circular use the compact stale wording when full timestamps cannot fit. Full station names remain available in descriptions and the app. Gallery title: “Next train”; description: “Check your next train and service changes.” Previews use the simulated delayed departure above, with accurate per-family layouts. An initial loading placeholder preserves layout with neutral text blocks; it must not show invented times or “Live.”

## Data and update contract

Each service record carries `serviceId`, service date, route/direction, scheduled and predicted departure/arrival instants, platform, operational status, source observation time, receipt time and source revision. Use station-local display time and explicit date when the departure is not today. Never infer arrival, departure or cancellation solely because the clock passed a prediction.

Product freshness policy:

- Fresh: a validated observation is no more than 2 minutes old. Say “Updated 08:11,” not an unconditional “Live.” Predictions say “Expected” where their status is otherwise ambiguous.
- Stale: observation older than 2 minutes, disconnected source, or invalid timestamp. Retain useful data as “Last known 08:18 · Updated 08:11”; remove a running countdown. Small accessories use “Check times.”
- Expired: after 10 minutes without a valid observation, remove predictions/platform and show “Times unavailable · Check departures.” A separately identified timetable may say “Scheduled 08:12”; it cannot inherit a prediction label.
- Refreshing: preserve existing content and its age. No blanking or fresh-label reset on a request or failed response.

Request a new widget snapshot on accepted service changes, configuration/authentication changes and app refresh. During a configured commute window request opportunities roughly every 5 minutes; outside it request the next meaningful timetable/window change. Request entries at freshness/expiry boundaries and departure transitions. These are requests, never a cadence guarantee. Include an absolute update timestamp so delayed rendering still reveals age. Use system-managed time presentation when supported; no second-by-second application loop. Departures that pass without confirmation become “Check departure,” not “Departed.” Select the next eligible service only from valid data; retain a cancelled service as a visible cancellation while showing an alternative on medium.

```text
onRecord(record):
  reject wrong service/date, older revision, or impossible observation timestamp
  preserve cancellation unless a newer authoritative correction replaces it
  commit record; derive freshness from observationTime, never receiptTime
  render changed fields; request surface update if content changed
onRender(now):
  derive fresh/stale/expired using now and stored observationTime
  never restart freshness because a widget was opened
onFailure:
  retain last record; expose stale/unavailable state
```

Delay is `predicted - scheduled` for the same event; round to whole minutes for display. A delay of at least 1 minute says “Delayed N min”; an earlier prediction says “Expected HH:mm,” avoiding negative-delay shorthand. Unknown prediction says “Scheduled,” never “On time.” Cancellation overrides time emphasis with “Cancelled.” Platform changes say “Platform changed · 5” on surfaces with room; smaller surfaces show “Check platform.” Corrections update the same service rather than creating duplicate departures.

## Active journey lifecycle

Start only when the person chooses **Track journey** on a departure detail. This begins `waiting` and offers **Stop tracking** in the app. Do not start automatically from a widget glance. If Live Activities are unavailable, disabled or dismissed, the app journey remains usable and departure widgets continue normally; do not repeatedly restart the activity.

| State | Entry and essential content | Exit |
|---|---|---|
| Waiting | Chosen service; expected departure; delay/platform | Authoritative departure or user “I’m onboard” → travelling |
| Travelling | Destination, expected arrival, delay, next confirmed stop | Confirmed approach → arriving; disruption → disrupted |
| Arriving | “Arriving at Central”; expected time | Authoritative arrival or user “End journey” → completed |
| Disrupted | Cancellation, diversion or interruption, with last known progress and “Open journey” | New confirmed state resumes journey; cancellation with no continuation ends activity |
| Stale overlay | Any active state without fresh observations: “Updates paused · Last checked 08:25”; last known arrival explicitly qualified | Valid newer observation restores underlying state |
| Completed/cancelled/stopped | End activity immediately; retain a safe summary for 15 minutes where the system permits | Remove summary; app keeps journey detail |

A normal journey lasts 50 minutes, so it is a bounded event. As a product fallback, end tracking after 2 hours from start without completion; label the summary “Tracking ended · Check journey,” never “Arrived.” The app can offer explicit tracking of a continuing journey. Do not extrapolate physical progress or next-stop certainty from elapsed time.

Presentations follow [Live Activities: presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Presentation):

- Lock Screen and expanded: destination and arrival time stay in consistent relative positions; below, next confirmed stop, delay and freshness. Whole activity opens the tracked journey. No extra in-place controls are required.
- Compact: leading train identity/route abbreviation, trailing arrival time; both halves open the same journey. Stale replaces arrival with “Check.”
- Minimal, including multiple-activity contexts: train symbol plus remaining minutes when fresh and supported by a prediction; stale uses a warning symbol. This conveys changing state rather than only a logo. Tap opens journey; system hold expands.
- StandBy: scale the essential destination, arrival and disruption text; preserve margins and red Night Mode meaning. On any system-mirrored destination, status remains useful without controls; no dependency on CarPlay interaction is introduced.

Update only changed content from accepted feed events, user confirmations and stale transitions. A timer can display predicted time remaining where supported; it is not evidence of a new train observation. No update-delivery SLA is promised.

A cancellation, platform change before departure, or an arrival prediction worsening by at least 5 minutes since the last alerted prediction is a crucial update eligible for an activity alert, subject to system/user settings. Deduplicate by journey, event type and revision; do not also send a push for that event. Minor changes update quietly. The app retains the disruption text even if no alert arrives. Separate notification features are outside this specification.

## Appearance, access and privacy

Follow [Widgets: rendering modes](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes) and [StandBy guidance](https://developer.apple.com/design/human-interface-guidelines/widgets#StandBy-and-CarPlay). In full color, use semantic foreground/background colors for light/dark. In accented/tinted and clear appearances, primary time and status belong to the primary group; route glyph/secondary accent belongs to the accent group. Meaning never depends on a brand hue or red delay dot. In vibrant Lock Screen and StandBy Night Mode, use grayscale brightness hierarchy with opaque prominent text, rather than white-opacity variations alone. Backgrounds must be removable for StandBy. Avoid imagery behind train information.

Live Activity backgrounds are system-controlled outside Lock Screen; use no custom Dynamic Island background. Verify Lock Screen text and system dismiss-button contrast in light/dark and reduced-luminance Always On. State changes remain understandable without animation or sound.

Use [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision) as a design requirement: test text enlargement through supported accessibility sizes, including 200% readability, and preserve essential content rather than shrinking to fit. Home targets use the full clear content regions; do not add tiny pseudo-buttons. Retain system accessory activation geometry. Proposed spoken content: “To Central. Expected departure 8:18. Delayed 6 minutes. Platform 3. Updated 8:11. Opens departure details.” Decorative logo is omitted from the reading sequence. Runtime semantics remain to be implemented and tested.

Data-purpose/access decisions follow [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices): route selection needs station/service identifiers, not continuous location, contacts or calendar. This design requests none of those permissions. Store the configured route locally; send only service identifiers needed for feed requests. Account credentials are never widget content. Actual storage, network and authentication architecture are unresolved implementation work.

Assume account-backed saved commutes for the signed-out case: show “Sign in to see your commute,” with one destination to sign-in that resumes configuration. No blank rectangle. Signed-in but unconfigured shows “Choose your commute.” Empty service results say “No more trains today” only when the feed confirms that fact; feed failures say “Times unavailable.” Logout clears personal cached route/journey content and ends tracking without retaining its sensitive summary.

Default Lock Screen/StandBy content uses station names without personal “Home/Work” labels or passenger/ticket details. Offer “Hide route details on shared screens”; then show “Train update available” and open the authenticated journey/route. Apply system privacy redaction when requested. Do not treat an Always On display as proof of authentication. Previously rendered content may persist until system updates it; document this limitation in the app’s privacy setting rather than promising immediate remote erasure.

## Worked before → after

Simulated service R2: Riverside → Central, scheduled departure 08:12, scheduled arrival 09:02 (50 minutes).

| Moment | Existing proposal | Revised result |
|---|---|---|
| 08:11 feed predicts departure 08:18 | Logo and tiny station list, promised per-second refresh | Small: “To Central / 08:18 / Delayed 6 min / Platform 3 / Updated 08:11.” Medium adds 08:27 and 08:42 alternatives. Inline has one route target |
| 08:14 no newer observation | Old departure still labelled Live | When rendered: last known prediction and timestamp; inline “Central · Check times”; no live countdown. No claim that the system redraws at exactly 08:13 |
| 08:17 new revision moves platform to 5 | No defined delay behavior | Restore fresh data, show platform change; no separate push duplicate if an activity alert is used |
| 08:18 user tracks and confirms onboard | Widget expected to refresh continuously | Live Activity shows “Central / Expected 09:08 / Delayed 6 min”; next stop only if confirmed by feed |
| 08:35 feed moves arrival to 09:15 | Unspecified | Same activity updates to “Expected 09:15 / Delayed 13 min”; eligible crucial alert because worsening is 7 minutes |
| 09:15 arrival confirmed | Unspecified end | End activity immediately; “Arrived at Central · 09:15” summary retained for 15 minutes where supported; widget resumes its departure purpose |
| Logout | Blank rectangle | “Sign in to see your commute”; personal cache cleared and active tracking ended |

## Acceptance checks and evidence limits

**Passed — static specification inspection:** all supplied issues have explicit replacements; each family has content and activation; inline has one target; widget updates are system-controlled; stale data loses fresh claims; the 50-minute journey has a separate start/end model; signed-out content is defined; tint/dark/StandBy red behavior is specified. The worked example’s arithmetic is consistent: +6-minute departure/arrival, then +13-minute arrival and 7-minute worsening.

**Failed — supplied proposal, as documented in interface.md:** logo-led compressed lists lack a useful hierarchy; three inline targets conflict with the single-target surface; per-second widget refresh is an unsupported promise; stale “Live” wording misleads; blank signed-out state offers no recovery. These are brief-level findings, not observed running-app defects.

**Not executed — implementation acceptance matrix:**

| Check | Expected result |
|---|---|
| Replay fresh at 08:11, stale after 2 minutes, expired after 10; failed refresh and old revision | Age derives from observation; old revisions rejected; no misleading live label or countdown; expired prediction removed |
| Cancellation, reinstatement, platform change, midnight/time-zone crossing | Status precedence and service date preserved; no false on-time/departed/arrived state |
| Follow every target, then authenticate, interrupt and resume | Correct service/route/journey restored; medium targets distinct; inline remains one target |
| Feed loss, late arrival, user stop, dismissal, logout, 2-hour fallback | Lifecycle ends as specified; no automatic resurrection or fabricated completion |
| Replay duplicate crucial revisions and minor delays | One eligible alert per event; no parallel push; minor updates quiet |
| Each family: light/dark, tint/clear, Lock grayscale/Always On, StandBy day/red night/background removed | Time/status/freshness legible; meaning survives loss of color and background; no clipping |
| Long station names, localized times/status, largest supported text sizes and 200% reading test | Essential direction/time/status/age remain understandable; secondary content removed first |
| Device accessibility and geometry checks | Spoken description conveys status and destination; targets activate correctly with VoiceOver and supported assistive input; contrast measured on actual appearances |
| Multiple Live Activities and device without Dynamic Island | Minimal remains informative; Lock Screen carries complete essential status; no reliance on unavailable presentation |
| Preview, loading, unconfigured, signed-out, empty and unavailable states | Realistic previews; no fake live values; explicit recovery route in each state |

Only supplied local files and installed instructions were consulted. Root SKILL.md was explicitly read, then relevant family/topic procedures before their references: Getting started → Designing for iOS; System experiences → Widgets and Live Activities; Foundations → Accessibility and Privacy. The topic index was searched for widgets, live activities and related concepts. Official links identify the sources recorded in the local snapshot; they were not fetched. The source is derived guidance dated 2026-10-25, not independently verified current SDK documentation. No applicable iPhone source conflict was found; the widget guide’s Mac accented-mode conflict does not establish iPhone restrictions.

No app, transit feed, screenshots, SDK, device or GUI was supplied or executed. No native rendering, refresh timing, push delivery, accessibility execution, contrast measurement or physical readability is claimed. Thresholds and feed feasibility need implementation validation. Future implementation must verify OS availability and system lifecycle/update behavior against its actual supported environment; this document assumes no Apple SDK is installed.
