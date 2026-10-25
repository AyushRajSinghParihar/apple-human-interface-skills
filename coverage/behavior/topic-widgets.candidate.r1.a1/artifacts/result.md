# Train commute: revised interaction specification

Design only; framework agnostic. Target: iPhone Home Screen, Lock Screen and the small widget’s StandBy presentation. All example stations and services below are simulated. The glance question is **“When is my next train, and what changed?”** During a followed journey it becomes **“What is my next step and expected arrival?”**

## Decisions and surface contract

Replace the app-logo-and-station-list design with departure-first content. A restrained train symbol identifies the service; the full app icon is unnecessary. Offer small and medium Home widgets, plus inline and rectangular Lock Screen accessories. Do not add a large or circular version until it adds demonstrated value. These family/surface choices follow the local [Widgets anatomy and best practices](https://developer.apple.com/design/human-interface-guidelines/widgets#Anatomy).

| Surface | Content in priority order | Activation |
|---|---|---|
| Home small | Expected departure `08:19`; `Delayed 7 min`; `Oakfield → Central`; platform if confirmed; `Updated 08:10` | Whole surface opens selected service departure detail |
| Home medium | Same lead departure; next two services with expected times and status; shared source timestamp | Each departure row opens that service; header opens configured route departures |
| Lock inline | `Central 08:19 · +7 min`, or `Central · Updates unavailable` | Exactly one target opens configured route departures; no separate station, delay or refresh controls |
| Lock rectangular | `Central 08:19`; `Delayed 7 min · Platform 2`; `Updated 08:10` | Whole surface opens selected service |
| StandBy small | Large `08:19`; `Delayed 7 min`; short destination; compact freshness line | Opens selected departure; keep this hierarchy when background is removed |

Absolute departure times are primary so an aging snapshot cannot retain a misleading fixed countdown. Display local station time and show the date when the departure is on another day. No scrolling, refresh button, route picker or sign-in form inside widgets. Exact destinations and the inline single-target constraint follow [Adding interactivity](https://developer.apple.com/design/human-interface-guidelines/widgets#Adding-interactivity).

Configuration in the app/widget configuration selects origin, destination/direction and optional line. Start with an explicitly selected recent route when available; otherwise show `Choose your commute`, opening setup. Never silently infer “home” or “work” from location. Public departures should work without an account; account-synced routes can require sign-in. Signed out with no local route: `Choose a route` plus `Sign in to restore saved commutes` where space allows, opening setup with sign-in available. Never show a blank rectangle. Signing out clears private saved names and active journey content.

## Data and update contract

The following freshness thresholds and retry choices are product decisions, not Apple requirements. A departure record contains stable service ID, route ID, scheduled and expected times, confirmed platform, cancellation state, source observation time, received time and optional source validity deadline. Journey records also carry next stop, predicted arrival, phase and revision. Reject older revisions; validate timestamps and never replace newer data with delayed network responses.

* Fresh: source observation age is at most 2 minutes and its validity deadline has not passed. Show `Updated HH:mm`, never an unqualified `Live` badge.
* Stale: older than 2 minutes, explicitly expired, or latest refresh failed. Show `Updates unavailable · Checked HH:mm`; label retained estimates `Last estimate 08:19`. Remove platform from compact stale layouts to prioritize uncertainty. Do not claim “on time” from stale data.
* Older than 15 minutes: suppress actionable estimates/platforms. Show `Check departures in app`; medium may retain separately labelled `Scheduled 08:12` if still relevant. No data: `Departures unavailable`, opening route detail with retry.
* Refreshing with cached content: keep that content and its freshness state. Only initial loading uses text-shaped placeholders; loading must resolve to data or an explanatory unavailable state.
* Cancellation takes precedence over delay: `Cancelled`, retaining service identity. Medium shows the next available alternative; small/Lock activation opens cancellation detail with alternatives. A passed estimate alone is not proof of departure; if unconfirmed after that time, show `Departure unconfirmed` rather than negative time or `Departed`.

Source transport and system rendering are separate. When execution is granted, fetch near expected commute viewing, at meaningful departure boundaries and after known service changes; request a new widget timeline after accepted changes. Failed requests retry with backoff (1, 2, 5, then 15 minutes) only when execution is available. Prepare expiration entries at freshness boundaries. These are requests, not delivery promises; system scheduling can defer them. Use system-managed time presentation where supported rather than fetching every second. No per-second refresh promise remains. See [Updating widget content](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content).

Framework-neutral reducer:

```text
on accepted observation:
  merge by service/journey ID and monotonic revision
  persist snapshot with source time and expiry
  request widget render at meaningful boundaries, including expiry
  if a followed journey exists and displayed content changed:
    request activity update

render(snapshot, now, surface):
  if privacyHidden: return "Commute hidden" with authenticated app destination
  if no configured route: return setup state
  if no usable snapshot: return unavailable state
  freshness = classify(sourceTime, validityDeadline, refreshFailure, now)
  choose cancellation / unconfirmed departure / journey phase / departure
  remove unsupported certainty and age-dependent details
  fit surface hierarchy; retain status text when color disappears
```

Render-time age evaluation and expiration requests express the desired behavior; an adapter must establish what the host can actually refresh while the app is suspended. A displayed `Updated HH:mm` timestamp remains an explicit age cue even if the system delays expiration. Runtime acceptance must reject a shipped design that leaves stale estimates claiming current certainty.

## Active journey and delays

Use one Live Activity for an explicitly followed journey, beginning when the person taps `Follow journey` on service detail. Do not automatically start one for every commuter departure. Provide `Stop following` in the journey view; dismissal must not cause automatic recreation. If unavailable or disabled, retain widgets and offer the journey detail screen without promising continuous updates. A 50-minute trip is a bounded event suited to this surface, following [Live Activities best practices](https://developer.apple.com/design/human-interface-guidelines/live-activities#Best-practices).

| Phase/event | Activity content and transition |
|---|---|
| Waiting | Departure time, destination, delay and confirmed platform; `Boarded` action records the person’s explicit confirmation |
| Boarded | Next stop, expected destination arrival and delay; hide boarding action |
| Transfer | Next service/platform and connection risk if supported by current data; retain same journey activity |
| Delay/platform change | Update expected time/platform and textual change reason; preserve layout positions |
| Stale/offline | `Updates unavailable`, last observation time and labelled last arrival estimate; suppress countdown and invented next-stop progress |
| Cancelled before boarding | `Train cancelled · View alternatives`; end activity with cancellation summary; app opens alternatives |
| Arrived or user ends journey | End immediately; retain `Arrived 09:09` or `Journey ended` summary for a requested 15 minutes, then remove |

Do not infer arrival from the scheduled end time. Require fresh arrival evidence or explicit user completion. If neither arrives, stop tracking at a product timeout of 2 hours after the last expected arrival, ending with `Tracking ended · Arrival unconfirmed`. A revised confirmed journey can extend that timeout. Do not expose a forever-running journey.

Lock Screen/expanded activity: destination and arrival first, then next step, delay and freshness. Compact Dynamic Island: train symbol plus short arrival time; minimal: train symbol plus delay marker when it fits, otherwise a meaningful warning symbol for disruption. All activity regions open that journey; holding compact/minimal expands through system behavior. A fresh expanded waiting view may contain the single `Boarded` action; unavailable contexts fall back to app activation. Do not add controls to minimal content. StandBy preserves the large arrival/next-step hierarchy and margins. Platform-specific presentation and interaction behavior is grounded in [Presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Presentation).

Update the activity only when its displayed content changes; source events may be frequent, but delivery remains system-controlled. Alert for a confirmed cancellation, changed boarding platform, or an arrival/departure estimate worsening by at least 5 minutes since the last alerted estimate. These thresholds are product choices; deduplicate by event/revision. No parallel push notification for the same activity alert. Minor delay changes update silently. End and summary behavior follows [Starting, updating, and ending](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity).

## Appearance, privacy and flexible layout

Use actual text, semantic system text roles and adaptable margins/container rounding. Preserve time, status and destination before secondary platform/alternative rows; reduce detail before shrinking text. Abbreviate station names only with unambiguous configured short names; expose the full names in accessible descriptions. Spoken order: route, expected time, status, platform if valid, source timestamp. A proposed accessible phrase is “Oakfield to Central, expected 8:19, delayed 7 minutes, platform 2, updated 8:10.” Execution with assistive technology remains untested.

Full color: semantic foreground/background in light and dark. Accented/tinted and clear Home appearances: time/status in primary group, restrained route symbol/accent; labels survive loss of brand color and background. Vibrant Lock Screen: opaque grayscale emphasis rather than opacity-only hierarchy. Always On: no dependence on animation or bright color. StandBy: removable background, larger time, fewer details, red monochrome night layout. Delay/cancellation always has words or a distinct meaningful symbol. See [Rendering modes](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes), [Displaying text](https://developer.apple.com/design/human-interface-guidelines/widgets#Displaying-text-in-widgets) and [StandBy](https://developer.apple.com/design/human-interface-guidelines/widgets#StandBy-and-CarPlay).

Default sensitive-content policy: hide personal route aliases, ticket identifiers and journey details when the system requests privacy redaction; offer an app setting to hide commute details on Lock Screen/StandBy entirely. Redacted activation authenticates before revealing the journey. No precise user location is necessary for this design. Provide a realistic simulated gallery preview, separate from real user data, described as `Check your next train`; use loading placeholders only for initial loading. Privacy and concise activity content follow [Live Activities best practices](https://developer.apple.com/design/human-interface-guidelines/live-activities#Best-practices).

## Worked before/after

Simulated Tuesday, Oakfield → Central, scheduled 08:12, scheduled arrival 09:02 (50 minutes).

**Before:** Every surface shows an app logo and tiny station list. At 08:10, a seven-minute delay is unclear. Inline draws three independent targets. At 08:16 during a feed outage, cached departures still say `Live`; the proposed refresh guarantee says every second. Signing out leaves a blank rectangle.

**After:** At 08:10 a fresh observation reports expected departure 08:19 and arrival 09:09. Home small reads `08:19 / Delayed 7 min / Oakfield → Central / Platform 2 / Updated 08:10`. Medium adds the 08:28 and 08:42 alternatives. Inline reads `Central 08:19 · +7 min`, with one route destination. The person follows the service, creating a waiting activity with `Boarded`.

At 08:16, with no observation since 08:10, the desired next rendered state is `Updates unavailable / Last estimate 08:19 / Checked 08:10`; inline drops the estimate for `Central · Updates unavailable`. No stale `Live` label exists even if a reload is delayed. At 08:18 a fresh observation confirms platform 4: the activity changes platform and issues one crucial alert. At 08:19 the person selects `Boarded`; the activity prioritizes `Arrive Central 09:09` and the next confirmed stop. At 09:09 fresh arrival confirmation ends it immediately, requesting removal of its arrival summary at 09:24. Signed out with no local route, the widget instead explains `Choose a route`, opening setup.

## Acceptance checks and evidence status

**Passed — static specification review only:**

- Each chosen family has a distinct useful content hierarchy and precise destination; inline has one target.
- Signed-out, unconfigured, loading, failed, stale, cancelled, privacy-hidden and completed states have explicit outcomes.
- Source observations, refresh requests and system delivery are separated; no unbounded or per-second widget promise remains.
- Fifty-minute journeys have start, phase changes, opt-out, alert deduplication, end and unconfirmed-arrival timeout rules.
- Tint, dark, clear, grayscale/Always On and StandBy red monochrome have explicit content-preservation requirements.

**Failed / unresolved evidence:** The installed system-experiences family and topic index route to `.topics/apple-hig-live-activities/SKILL.md`, but that file is missing. An explicit `cat` failed and package file searches found only its source guide. Therefore the routed Live Activities procedure could not be consumed; no claim of complete procedural compliance is made. Its available local guide was read as a documented fallback.

**Not executed — implementation acceptance gates:**

- Inject the worked event sequence and check every rendered state and exact deep-link object, including stale boundaries at 2 and 15 minutes, reordered responses and midnight/time-zone changes.
- Suspend the app, defer refreshes and disconnect networking: confirm visible timestamps remain honest and expiry handling cannot leave current-sounding estimates. Measure refresh behavior rather than asserting a delivery interval.
- Exercise sign-out, privacy redaction, locked activation, activity opt-out, unsupported activity fallback, duplicate alert events and terminal removal.
- Preview every selected family with long station names, localized times, large supported accessibility text sizes, cancelled trains and missing platforms. Retain time/status; no overlapping targets or clipped critical labels.
- Check light/dark, Home tint/clear, background removal, Lock vibrant, reduced-luminance Always On and StandBy red night rendering. Confirm meaning without color and legibility against varied wallpapers.
- On actual supported devices, verify tap targets, VoiceOver reading/activation, Dynamic Island presentations, StandBy distance legibility and alert behavior. These are required future checks, not results from this host.

## Evidence limits

Inputs inspected: `interface.md`; installed root `apple-hig/SKILL.md`; system-experiences family; widgets topic procedure; topic-index Live Activities route; local widgets and Live Activities source guides. Root → family → widgets procedure → widgets guide was followed using file reads. The missing activity procedure is recorded above. No web browsing was performed; official links identify guidance referenced in the local snapshot, not newly verified web pages. Local guides state snapshot date 2026-10-25 and are not SDK documentation or independent validation. The Mac accented-mode conflict in the widgets guide does not affect this iPhone-only contract.

No app implementation, SDK compilation, device/GUI rendering, assistive-technology execution, feed reliability measurement or timeline delivery test was performed. Timing thresholds, route defaults, alert policy, privacy choices and sample data are explicit design decisions to validate with implementation and users; they are not asserted Apple mandates.
