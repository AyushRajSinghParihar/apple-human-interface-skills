# Train commute: revised interaction specification

Design specification for iPhone; framework agnostic. Examples below are simulated. The supplied `interface.md` is the complete observed proposal; no application implementation was supplied.

## Decisions and surface contract

The glance question is **“When is my next train, and has anything changed?”** During an explicitly followed journey it becomes **“What happens next on this journey?”** Replace the app-logo-and-tiny-list design with departure-first content. A small train symbol supplies recognition; branding must not displace useful data. Larger sizes add relevant departures rather than stretch the small layout. These choices follow [Widgets: Best practices](https://developer.apple.com/design/human-interface-guidelines/widgets#Best-practices).

| Surface / family | Content in priority order | Activation |
|---|---|---|
| Home, system small | `Central → Riverside`; large `08:18`; `Delayed 6 min · Platform 4`; `Checked 08:10` | Whole widget opens the selected service detail, preserving station, direction and service ID. |
| Home, system medium | Same primary departure; next two services with expected time and cancellation/delay text; freshness | Primary service and each secondary row open their own service detail; background opens the configured departure board. No nested targets. |
| Lock, accessory inline | `Riverside 08:18 · checked 08:10`; if stale, `Riverside · Check times` | Exactly one target opens the configured departure board, with selected service highlighted when known. No independently tappable text segments. |
| Lock, accessory rectangular | Route/destination; large expected departure; delay or cancellation; compact `Checked 08:10` | One target opens that service detail; fallback is the configured board. |
| StandBy, system small adaptation | Large `08:18`; destination; `+6 min`; freshness/status | Same service destination. Remove optional platform and logo before reducing essential text. Background is removable; do not use the medium layout. |

Do not ship circular or large variants in this first set: they add no essential new use case. Home system families and Lock accessory families are distinct, per [Widgets: Anatomy](https://developer.apple.com/design/human-interface-guidelines/widgets#Anatomy). No in-widget refresh, station picker, scrolling list or journey-start control. Configure origin, direction/destination and preferred service in the app/widget configuration; default to a recently chosen route only when one exists. If none exists, show `Choose your commute`, opening route setup. Do not infer a home/work address.

## Data and update contract

Separate operator-feed arrival from system presentation opportunities. A backend may receive frequent events; a widget cannot promise to display them every second. Request updates on meaningful service changes, scheduled departure boundaries, expiry and likely commute viewing periods; coalesce identical data. Actual delivery remains system-controlled. Use system-provided date/time presentation where available, with absolute expected departure as the fallback. Never derive train movement or boarding from a clock alone. [Widgets: Updating widget content](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content).

The following thresholds are product decisions, not Apple rules. Start with a two-minute freshness window; validate against the actual operator's feed before release. `observedAt` is the operator observation time, not the time a cached response was downloaded. Missing or implausible observation times cannot qualify as fresh.

```
service = {id, route, destination, scheduledDeparture, expectedDeparture?,
           platform?, status, observedAt?, receivedAt, version}

onFeed(event):
  reject older versions for the same service
  preserve service identity; apply cancellation/platform/expected-time changes
  validUntil = observedAt + 2 minutes, if observation is trustworthy
  publish changed snapshot; request presentation update, without timing guarantee
  request expiry presentation at validUntil

render(snapshot, now):
  if signedOut: return signInExplanation
  if noConfiguration: return chooseCommute
  if noSnapshot: return unavailableOrInitialLoading
  if now >= validUntil OR observation unknown OR feed disconnected:
    return lastKnownTime + "Last known" + "Checked [time]" + "Check times"
  if cancellation: return "Cancelled" + scheduledTime + nextKnownService
  return expectedTimeOrScheduledTime + explicitDelayOr"Scheduled" + checkedTime
```

Keep useful cached content while refreshing; do not replace it with skeletons. Never label stale data `Live`. In fact, omit `Live` entirely: show `Checked [time]` on normal departures. A schedule-only time says `Scheduled`, not `On time`. A stale cancellation remains `Last known: cancelled`; do not silently reinstate the train. Unknown platform says `Platform unconfirmed` where space permits, otherwise omit it. If an expected departure has passed without a confirmed departure event, show `Departure status unknown · Check times`; do not roll automatically to the next train as if departure were confirmed. Once confirmed departed, select the next eligible service.

Expiry rendering and refresh requests are desired behavior, not a guarantee that the system will redraw at the deadline. Therefore every displayed estimate carries an absolute check time, including a compact form in constrained layouts; a delayed redraw must still disclose the observation time. When space cannot hold both status and freshness, replace the estimate with `Check times`, not an apparently current countdown. App activation fetches current data and shows the cached state immediately with its age.

Account and data states apply to every size:

- Signed out: `Sign in for your commute`, with a train symbol and sign-in destination. Preserve pending route destination through sign-in; never show a blank rectangle or another account's cache.
- Initial loading: route framing with text placeholders only while awaiting the first response. On fetch failure or after 10 seconds without data, show `Times unavailable · Open departures`; no indefinite empty skeleton.
- No service: `No more trains today`, only if supported by a valid schedule; otherwise `Times unavailable`.
- Offline/stale: keep labelled last-known data; never imply that opening the app guarantees connectivity.
- Privacy: no account names, ticket codes or home/work labels. Offer “Hide route on Lock Screen”; redacted accessories say `Commute · Open app`, and activity content says `Journey in progress`. Unlocking opens the authenticated detail. Sign-out clears personal snapshots and ends the activity.

## Active journey: one bounded Live Activity

A 50-minute journey is a bounded event suitable for a Live Activity rather than continuous widget reloads. Begin when the person chooses `Track this journey` on service detail; show that tracking is active and provide `Stop tracking` there. If Live Activities are unavailable or disabled, retain the app journey view and ordinary widgets; explain this once in context. Widgets remain departure boards rather than switching purpose unexpectedly.

Use one activity for the whole journey, including transfers. States are `waiting → aboard → transfer (if needed) → arriving → completed`; cancellation changes to `disrupted`, with an app route to alternatives. Feed events or explicit user confirmation drive aboard/arrival/completion. An ETA passing does not prove arrival. Manual stop ends tracking immediately. Confirmed completion ends immediately and leaves a `Journey complete` summary on the Lock Screen for 15 minutes, requesting removal thereafter. With no confirmation, at latest known arrival plus 15 minutes show `Arrival unconfirmed · Check journey` and end tracking; do not claim completion. This timeout is a product policy, extended by a trustworthy revised arrival received before expiry.

| Activity presentation | Essential information |
|---|---|
| Lock Screen / expanded | Route; next event (`Depart 08:18`, `Next: Oak Street`, or `Change at Central`); expected arrival; `Delayed 6 min` or disruption; checked time. Keep positions stable across updates. |
| Compact | Train/route shorthand leading, expected arrival trailing; both halves open the same journey. Replace time with `Check` when stale. |
| Minimal | Train symbol plus delay indicator/short arrival time when it fits; stale state uses an uncertainty symbol with a spoken label. Never only the logo. |
| StandBy | Scaled, simplified next event and arrival; removable/unobtrusive background, generous margins, red monochrome Night Mode. |

All activity activation opens the tracked journey. System press-and-hold expansion remains available where supported. No action button is necessary; stopping in the app avoids accidental termination. Update on changed departure/arrival, platform, cancellation, next stop, phase or freshness state, not every elapsed second. Any timer is an estimate tied to an absolute timestamp; it cannot indicate actual progress when the feed is stale.

Request an activity alert only for cancellation, a platform change before boarding, or a newly increased delay of at least five minutes. Deduplicate by event ID and suppress a parallel push for the same event. Smaller changes update silently. Unknown/stale data is silent. Alert delivery is also system-controlled. The five-minute threshold is a product choice. These lifecycle, interaction and alert decisions follow [Live Activities: Starting, updating, and ending](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity) and [Offering interactivity](https://developer.apple.com/design/human-interface-guidelines/live-activities#Offering-interactivity).

## Appearance and accessible content contract

Use actual text, system text styles and flexible containers; no rasterized station list or fixed device canvas. Preserve expected time, destination, status and freshness as text grows; medium drops secondary services first. Long names wrap in Home/rectangular variants; inline abbreviates an unambiguous configured destination before omitting secondary delay detail. Full destination and time remain in its accessibility label and app destination. Never shrink everything to fit. Layout feasibility still requires previews on target devices.

Full-color light/dark uses semantic foreground/background roles. In Home tint/clear modes, primary time/status forms the primary group and route/secondary information the supporting accent group; verify hierarchy after system recoloring. Lock accessories use meaningful grayscale brightness, not opacity alone. Delay is always text (`Delayed 6 min`), cancellation includes `Cancelled`, and uncertainty includes `Last known`/`Check times`; color and symbols are supplemental. StandBy removes decorative backgrounds and retains large time/status in red monochrome Night Mode. Always On must preserve status and age without animation. These decisions follow [Widgets: Rendering modes](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes), [Displaying text](https://developer.apple.com/design/human-interface-guidelines/widgets#Displaying-text-in-widgets), and [StandBy](https://developer.apple.com/design/human-interface-guidelines/widgets#StandBy-and-CarPlay).

Specify spoken order as route/destination, expected or last-known time, delay/cancellation, platform, observation time, action. Example: `Central to Riverside. Expected departure 8:18 AM. Delayed six minutes. Platform four. Checked 8:10 AM. Open service details.` Localize time, units and pluralization; include date when crossing midnight. Respect reduced motion; changes need no animation. If used, transitions last at most two seconds and convey no information unavailable in static text. [Live Activities: Transitions](https://developer.apple.com/design/human-interface-guidelines/live-activities#Adding-transitions-and-animating-content-updates).

Gallery description: `Check your next train`. Use simulated Central/Riverside departures clearly identified as preview data in the design assets, with realistic delay and signed-out examples. Do not display a fictitious “live” feed.

## Worked before / after

**Before (observed brief):** Every surface is a logo plus tiny stations; inline pretends to offer three targets; updates are promised every second; stale departures say Live; signed-out state is empty.

**After (simulated scenario):** At 08:10, the scheduled 08:12 service is reported expected at 08:18, platform 4, arriving 09:08. Small Home shows `Central → Riverside / 08:18 / Delayed 6 min · Platform 4 / Checked 08:10`. Inline shows `Riverside 08:18 · checked 08:10` with a single board destination; its accessible label includes the observation time. Where that timestamp cannot fit visibly, use the rectangular variant for a time-bearing glance or reduce inline to `Riverside · Check times`.

At 08:12, no newer observation exists. Requested expiry changes Home to `Last known 08:18 / Check times / Checked 08:10`; inline becomes `Riverside · Check times`. If expiry delivery is late, the existing `Checked 08:10` still discloses its age. At 08:13, a new cancellation observation replaces the departure with `Cancelled · 08:12 service`, medium adds the next known train, and the active journey changes to `Service cancelled · View alternatives`, with one crucial activity alert and no duplicate push.

Alternative successful branch: the person tracks the service and confirms boarding at 08:18. The activity shows `Next: Oak Street / Riverside 09:08 / Checked 08:18`. This is a 50-minute journey, not a promise of 3,000 widget refreshes. A confirmed arrival at 09:08 ends the activity; the Lock Screen summary expires at 09:23. Ordinary widgets continue showing next departures.

## Acceptance checks and evidence status

**Passed — static specification inspection only:** All offered families match the local iPhone context table; each has useful changing content and a concrete destination. Inline has exactly one activation. No second-by-second refresh promise remains. Fresh/stale/schedule/cancellation, authentication, setup and unavailable states are explicit. The journey has start, change, disruption, end and fallback rules. Tint, dark, clear, StandBy and Always On have specified treatments. The worked trace is consistent with the two-minute expiry and 50-minute journey policies.

**Failed — supplied proposal, by direct textual inspection:** Logo-first tiny lists do not answer a useful glance; inline has unsupported separate targets; every-second refresh is promised; stale data is labelled Live; logged-out content is blank. These findings describe `interface.md`, not a tested app. The revised specification replaces each behavior.

**Not executed — required implementation acceptance:**

1. Render every variant with fresh, two-minute-old, offline, cancellation, no-platform, signed-out, loading and missing-service data. Verify actual expiry behavior under delayed/denied system refresh; visible timestamps must remain honest.
2. Replay out-of-order and duplicate feed events; verify identity, version rejection, cancellation retention, no automatic boarding/arrival and alert deduplication. Confirm stale compact/minimal activity views disclose uncertainty.
3. Activate every target with valid, deleted and expired service IDs; verify precise detail or board fallback, authentication return path, and one inline target.
4. Preview light/dark, tint/clear, grayscale Lock, Always On and red StandBy. Check removable backgrounds, contrast, no clipping and understandable status without color. Verify long/localized station names, midnight, extreme delay and no remaining services.
5. Exercise supported accessibility text sizes through the largest available size and VoiceOver order/labels, including inline freshness and minimal uncertainty. Confirm meaningful labels, no inaccessible secondary targets, and no essential information conveyed by motion alone.
6. Exercise a full 50-minute journey, cancellation, transfer, manual stop, disabled activity support, sign-out, missing completion and summary removal. Verify system presentation/alert behavior on supported iPhones, with and without Dynamic Island.

## Sources and evidence limits

Only supplied local files were used; no web browsing, SDK, device, GUI, accessibility execution, runtime simulation or compilation occurred. Official links above identify the source sections recorded locally; they were not fetched. Thresholds, wording, route configuration and timeout rules are proposed product decisions rather than HIG mandates. Feed quality, operating-system support/version floor, background delivery and runtime capability detection remain implementation dependencies.

Auditable reading route: installed `apple-hig/SKILL.md` → `subskills/apple-hig-system-experiences/SKILL.md` → `.topics/apple-hig-widgets/SKILL.md` → `references/widgets.md`. The routed `.topics/apple-hig-live-activities/SKILL.md` was explicitly attempted and is absent. A search of installed files and `references/topic-index.md` confirmed the same missing path; the available `references/live-activities.md` was then read as a qualified fallback. The Live Activities procedure could not be consumed, so this is not a claim of full procedural coverage. Both available source guides report snapshot 2026-10-25; their existence does not prove independent review or current SDK availability. The widget guide's conflicting Mac accented-mode statements do not affect this iPhone scope; no Mac behavior is inferred.
