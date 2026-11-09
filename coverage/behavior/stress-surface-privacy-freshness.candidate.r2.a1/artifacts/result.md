# Pickup summary and delivery activity design

Design specification based on `interface.md` and installed local HIG guidance. No web browsing, SDK verification, implementation, simulator, device, GUI, or assistive-technology execution was performed. Examples below are proposed copy; the brief establishes only one parcel, private recipient/destination/access details, a server update 35 minutes ago, and an 80-minute delivery. It does not establish pickup readiness, departure time, ETA, or connectivity.

## Concrete result

The widget answers **“What pickup information should the household check?”** The Live Activity answers **“What is happening with my current delivery?”** Household visibility is an explicit sharing choice; possession of a connected household device does not authorize sharing a person's parcels.

### Household-visible widget

Use a dedicated **Household pickups** configuration, system small on iPhone Home Screen and the shared Apple HomeView Modular face. The latter uses the small family, not a watch Modular complication. No medium/large variant is required for this scope. Show only parcels explicitly included in household sharing. Before selection, show `Choose shared pickups` with setup guidance; never automatically publish Sam's parcel.

After authorized inclusion of the supplied parcel, the current example is:

```text
[parcel symbol] Pickups
1 parcel
Status unconfirmed
Updated 35 min ago
```

This count means one shared record, not one parcel ready for pickup. With no authorized shared records, show `No shared pickups`; do not infer zero pickups from a failed request. Header is secondary, count/status primary, freshness immediately beneath. No recipient, address, gate code, tracking number, merchant, parcel contents, precise destination, or route appears on household surfaces, including previews and accessibility labels. Configuration copy: `Show a parcel count and pickup status to your household. Names, addresses and access codes stay private.` Sharing off returns to a neutral setup state and clears shared cached content.

On verified fresh data, show `1 pickup ready` only if the backend actually confirms readiness; otherwise use `1 parcel · Check status`. Larger counts use pluralized strings. Do not reinterpret delivery progress as pickup readiness. Tap opens the selected household pickup summary, scoped to the viewer's authorization. It never directly opens credentials or performs Accept/Cancel. An unavailable app destination should retain the safe summary and explain how to check details on the originating iPhone; HomeView activation capability requires validation.

### iPhone Lock Screen and watch glance

| Context | Family and proposed content | Activation |
|---|---|---|
| iPhone Lock Screen | Accessory inline: `Pickups: status unconfirmed`; fresh confirmed example `1 pickup ready` | One target opens pickup summary; no drawn Accept, Cancel, or Details buttons |
| iPhone Lock Screen | Accessory rectangular: `Pickups · 1 parcel` / `Status unconfirmed` / `Updated 35 min ago` | Same authorized summary |
| Watch Smart Stack | Accessory rectangular, same safe hierarchy; relevance rises around an actual pickup window if supplied | Opens watch pickup summary; if no watch app exists, do not promise this widget until that destination is implemented |
| Optional watch face | Modern WidgetKit accessory rectangular complication with the same safe content; support only compatible face slots | Opens its pickup summary, not generic app home |

The inline accessory drops count before dropping the uncertainty label. It cannot fit three actions or detailed freshness. Its accessible description includes the last-update time. Defer circular/corner and legacy ClockKit variants rather than inventing slot support or using ambiguous legacy inline dimensions. A watch face is distinct from the shared HomeView Modular face.

### Private bounded delivery Live Activity

An 80-minute delivery is appropriate for a bounded Live Activity, unlike ordinary pickup summaries. Start when the person follows a delivery and the server confirms an active dispatch; do not start from an old parcel record. Provide `Track on Lock Screen` and a corresponding stop-tracking option in delivery details. Disabled/unavailable Live Activities leave in-app tracking usable. “Private” means an individually scoped event with minimized public content, not a guarantee that nobody can see a Lock Screen.

The activity contains only an opaque event identifier, verified phase, optional ETA range, source timestamp, freshness deadline, and event deadline. Exclude the recipient, full address, code, tracking number, and detailed route from the activity payload as well as its UI. Privileged delivery details remain behind account authorization and appropriate device/app authentication. Links carry opaque identifiers, never credentials. Authentication failure shows safe content and no secret flash.

| Presentation | Fresh verified example (illustrative, not supplied status) | Supplied 35-minute-old data |
|---|---|---|
| Compact | Leading parcel/phase symbol; trailing `20–30m` only with a valid estimate | Leading parcel/warning symbol; trailing `Stale` |
| Minimal, including multiple activities | Parcel plus meaningful phase badge; stale uses warning badge | Warning state, accessible label `Delivery update overdue` |
| Expanded | Leading `Delivery` and phase; trailing ETA; below, last-update time and `Details` link | `Delivery` / `Update overdue` / `Last update 35 min ago` / `Details` |
| Lock Screen | Same hierarchy in a distinct task layout | Same explicit uncertainty; no running ETA |

Maintain parcel/phase identity and relative leading/trailing positions during expansion. In a limited-width 28-pt Dynamic Island context, use the phase/warning symbol rather than clipped text; it must convey state beyond a static logo. Both compact halves and the activity body open this delivery's details. No direct Accept/Cancel controls: those consequences and authorization belong in the app. One clearly named Details destination is sufficient; no action is essential to understanding status.

StandBy reuses the safe Lock Screen layout at system scale, with cropping and red Night Mode checks. Paired watch uses the combined compact information in Smart Stack; tapping follows the documented watch-app or paired-iPhone fallback. CarPlay must remain understandable with controls disabled. Paired Mac uses system presentations and iPhone Mirroring activation. Do not claim Live Activity support on HomeView, tvOS, or visionOS.

## Freshness and lifecycle contract

The following thresholds are **product decisions proposed for validation**, not HIG or OS refresh guarantees. Widget freshness expires 15 minutes after the last verified server snapshot; active delivery freshness expires after 5 minutes. Thus the supplied 35-minute-old snapshot is stale on both surfaces. Connectivity and data freshness are independent.

| Condition | Behavior and copy |
|---|---|
| No successful snapshot | `Status unavailable` / `Open app to check`; no invented count, phase, or ETA |
| Refresh underway with cached data | Keep available content and its timestamp; preserve any stale warning |
| Fresh | Render verified status; ETA only while its validity interval remains current |
| Freshness deadline passed | `Status unconfirmed` on widget; `Update overdue` on activity. Keep safe count/last known record; remove countdown and present-tense progress claims |
| Confirmed connection failure | `Offline · Updated 35 min ago` on full layouts; inline `Pickups: offline`. Explain in the app that displayed data is last known. Do not call stale data offline without connection evidence |
| Connection restored | Fetch and validate first. A network connection alone never makes cached content fresh |
| Signed out, account removed, or sharing revoked | Clear scoped cached values, stop private tracking, and show `Sign in to view pickups` privately or neutral setup on shared surfaces |
| No pickups, confirmed by fresh response | `No pickups scheduled`; preserve last-update context |

Store absolute `lastVerifiedAt`, validity deadlines, monotonically ordered event version, and terminal state. Reject out-of-order updates and prevent an older push from reviving an ended event. Render freshness using system time presentation and scheduled validity transitions; request reloads at meaningful state/window/deadline changes and after accepted data changes. Source changes and system refresh opportunities are separate. No second-by-second widget network refresh or guaranteed redraw cadence. Ensure expired cached entries cannot be selected as fresh; if the system defers rendering, the visible timestamp still exposes age. Validate actual expiry behavior before release.

Delivery state flow: `not tracking → active → arrived → delivered`, with `cancelled` and `failed` terminal alternatives. Fresh/stale/offline are overlays on nonterminal states. A confirmed delivered/cancelled/failed event ends the activity immediately. Keep a safe terminal summary such as `Delivery complete` for 15 minutes where retention is supported, then remove it; Dynamic Island removes on ending. Arrival alone is not completion. Alert only for a verified crucial event such as arrival requiring attention or failure, with no duplicate notification for the same event. Routine progress and staleness are quiet.

For this brief, set an absolute tracking deadline at confirmed start + 80 minutes. At that boundary, absent a terminal signal, end tracking with `Tracking ended · Check delivery status`, never `Delivered`. A delay requires a newly confirmed bounded extension that the person chooses in-app; no silent indefinite extension. If fresh ETA expires earlier, show `Arrival time unavailable` until revalidated. Backend end delivery and a platform-supported end fallback must be engineered and tested; a displayed countdown cannot guarantee removal during disconnection.

## Visual and privacy decisions

Use actual localized text, system text styles, SF Symbols with text equivalents, flexible margins and container-relative corners. Follow contextual margins rather than fixing a production canvas to reference dimensions. As local guide starting points, most widgets use 16 pt and Lock Screen activities 14 pt; adapt with native layout and supported sizes. Keep widget text generally at least 11 pt, and reduce secondary detail before shrinking status text.

Full-color light/dark uses semantic foreground/background roles. In accented mode, accent only the count or phase symbol; keep status and freshness in the primary group. In vibrant mode, use grayscale brightness for hierarchy, not white opacity alone. Meaning survives removed backgrounds, tint, clear appearance, grayscale, Always On and low-light red. Dynamic Island backgrounds remain system-controlled; customize only the Lock Screen activity background where supported. No map, promotional copy, color-only warning, or decorative motion. Accessibility reading intent is title → count/phase → uncertainty → update time → destination; no private information in hidden labels. Physical rendering and reading order remain untested.

| Data | Purpose and access policy |
|---|---|
| Shared count/status/timestamp | Explicit household opt-in, safe aggregate only; revoke and purge household cache |
| Private delivery phase/ETA/timestamp | Account-scoped tracking, minimized system-surface payload |
| Recipient/address | Authorized in-app delivery detail only |
| Gate credential | Reveal only when needed in authenticated app; use established secure storage and never widget/activity caches, previews, links, analytics or logs |

No additional location, contacts, HomeKit or tracking permission is justified by this design. If implementation adds protected access, request it at the relevant action with a specific purpose; household membership alone is not permission to disclose personal records. Verify storage, transfer and App Store disclosures against the eventual implementation.

## Acceptance checks and evidence

**Passed — static specification inspection only:** selected distinct supported families from the supplied local tables; separated household summary from private activity; removed shared personal data and independent inline targets; marked the 35-minute snapshot stale without inventing connectivity or readiness; defined all iPhone activity presentations, bounded expiry and terminal retention; included unavailable/auth/revocation states. These are design-contract checks, not runtime passes.

**Failed — supplied proposal:** full address/code on shared face; second-by-second widget refresh promise; three independent inline targets. Replacements are specified above. There is no implementation evidence establishing that those replacements execute.

**Not executed — required acceptance matrix:**

- Render Home Screen small, HomeView Modular, both Lock Screen accessories, watch rectangular and every activity presentation. Check smallest supported devices, long translations, pluralization, right-to-left text, Dynamic Type Large through AX5 where supported, and simultaneous activities. Preserve uncertainty before decorative/secondary details; no clipped actionable or status text.
- Inspect light/dark, accented, vibrant, clear, background removal, Always On and red Night Mode. Verify readable status, freshness and dismiss control against actual backgrounds. Test wrist and across-room readability on relevant hardware.
- With VoiceOver, verify intended reading order, meaningful phase/warning labels, one inline target and precise destinations; ensure labels contain no private fields. Audit contrast and accessibility settings on actual native output.
- Inject a 35-minute-old snapshot, expiry while idle, no cache, failed connection with fresh and stale cache, reconnect without new data, clock change, delayed/out-of-order pushes, restart and revoked sharing. No fabricated live phase/countdown, false offline state or stale terminal resurrection.
- Follow every link as authorized, unauthorized, signed-out and different household users. Inspect rendered UI, caches, payloads, logs and previews for secrets. Confirm revocation clears existing household snapshots as well as future updates.
- Exercise start, opt-out, delivery/cancellation/failure, arrival without completion, and the 80-minute boundary online/offline. Verify actual ending and 15-minute retained summary behavior, alert deduplication, watch fallback, CarPlay without controls and Mac mirroring.

Missing evidence: supported deployment OS/SDK and project framework; backend pickup/dispatch/ETA semantics and update cadence; start/terminal/push/fallback guarantees; household consent and viewer authorization model; actual HomeView and watch integration availability; privacy/storage implementation; localized strings and rendered previews; device, SDK build, timing, accessibility and household usability results. Product owners must validate the proposed freshness thresholds and hard 80-minute tracking window, especially delayed deliveries. Linux source inspection cannot establish any of these runtime results.

## Guidance and audit trail

Read the installed root `apple-hig/SKILL.md`, then `subskills/apple-hig-system-experiences/SKILL.md`, then its `.topics/apple-hig-widgets/SKILL.md`, `.topics/apple-hig-live-activities/SKILL.md`, and `.topics/apple-hig-complications/SKILL.md` before their respective `references/*.md` guides. Also read `subskills/apple-hig-foundations/SKILL.md`, its privacy topic procedure, then `references/privacy.md`. Paths were resolved under this project's installed `.agents/skills/apple-hig` package; reads used one file per shell command. Local reference snapshots, not newly verified official sources, support this specification.

Material source links from those guides:

- [Widgets: updating content](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content), [interactivity](https://developer.apple.com/design/human-interface-guidelines/widgets#Adding-interactivity), [Apple HomeView](https://developer.apple.com/design/human-interface-guidelines/widgets#Apple-HomeView), and [rendering modes](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes): periodic updates, single inline target, deliberate shared-surface privacy and appearance adaptation.
- [Live Activities: best practices](https://developer.apple.com/design/human-interface-guidelines/live-activities#Best-practices), [lifecycle](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity), and [presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Presentation): bounded task, minimized sensitive content, changed-content updates, immediate ending and short retained summary. The guide says ideally no more than 8 hours; this design's 80-minute bound is a product choice.
- [Complications](https://developer.apple.com/design/human-interface-guidelines/complications): relevant watch information, limited reloads, privacy and family-specific fit. Its conflicting legacy inline dimensions are deliberately unused.
- [Privacy: best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices) and [protecting data](https://developer.apple.com/design/human-interface-guidelines/privacy#Protecting-data): minimize data and use established authentication/storage protections. This design is not a security certification.
