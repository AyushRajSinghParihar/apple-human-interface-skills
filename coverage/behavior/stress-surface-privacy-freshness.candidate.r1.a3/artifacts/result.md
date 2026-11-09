# Pickup summary and delivery activity

Design specification based on `interface.md` and the installed HIG snapshot (2026-10-25). No implementation or Apple runtime was supplied. Official links below identify the local guides’ sources; no web access was used.

## Concrete result

Two separate experiences answer two different questions:

- **Household pickup summary:** “Is there a household pickup to check?” A periodic widget, explicitly configured with household-approved parcels.
- **Personal delivery Live Activity:** “What is happening with the delivery I’m following?” A bounded activity for the supplied 80-minute delivery, started on the person’s iPhone. “Personal” describes ownership, not a guarantee that a Lock Screen is private.

The supplied parcel belongs to Sam, with a full street address and gate credential. None of those fields appears on widgets, complications, activity payloads, previews, URLs, accessibility labels, or shared caches. Details are available only inside the authenticated app after an authorization check. This is an application privacy policy, stricter than simply marking displayed fields sensitive. [Privacy — protecting data](https://developer.apple.com/design/human-interface-guidelines/privacy#Protecting-data), [Live Activities — best practices](https://developer.apple.com/design/human-interface-guidelines/live-activities#Best-practices).

The brief supplies no actual pickup readiness, arrival estimate, or delivery milestone. Do not invent them from the parcel’s existence or the 80-minute duration. The immediate supplied-data rendering is therefore:

```text
Household pickups                 Delivery
Status unavailable                Updates delayed
Updated 35 min ago                Last update 35 min ago
Open to check                     Open delivery
```

The pickup view may show the timestamp only if that server update actually covers the household summary; otherwise use “No recent summary.” “1 pickup ready” is a simulated preview, usable only after a readiness signal and household-sharing approval exist.

## Surface and interaction contract

| Surface | Family and hierarchy | Activation |
|---|---|---|
| iPhone Home Screen | System small: “Household pickups”; large confirmed count/status; freshness; short “Open to check” cue. No additional sizes until they add useful information. | Whole widget opens authorized household pickup list. One eligible item may resolve directly to its summary. |
| Shared Apple HomeView Modular face | System small, separate household-safe configuration. Large count/status, shorter freshness line; removable background. Never inherit the current phone owner’s private parcel feed. | Open household-safe summary on that surface where supported. Private details require continuation to the person’s authenticated iPhone; exact handoff remains unverified. |
| iPhone Lock Screen | Accessory inline: “Pickups · update delayed” now; “1 pickup ready” only with fresh approved data. Accessory rectangular alternative adds last-update line. | **One target** opens the relevant pickup summary. Remove the proposed independent Accept, Cancel and Details targets. |
| Watch glance | Accessory rectangular Smart Stack widget: pickup status then freshness. Optional rectangular complication in supported face slots uses the same safe data and precise destination. Do not label this a HomeView Modular face. | Open corresponding Watch pickup summary. If no Watch app exists, omit the optional complication until its useful destination exists. |

Family support and single-target inline behavior come from [Widgets — anatomy](https://developer.apple.com/design/human-interface-guidelines/widgets#Anatomy) and [adding interactivity](https://developer.apple.com/design/human-interface-guidelines/widgets#Adding-interactivity). Shared Modular uses a small-family widget, and has different exposure from personalized Home Screens: [Apple HomeView](https://developer.apple.com/design/human-interface-guidelines/widgets#Apple-HomeView). Watch complications use face-selected supported slots, with bounded timeline budgets: [Complications](https://developer.apple.com/design/human-interface-guidelines/complications#Best-practices).

Accept and Cancel belong in authenticated parcel detail, subject to current server eligibility. Opening an old widget must not execute either action. On return from interruption, retain the selected parcel; if removed or authorization changed, show “Delivery no longer available” with a route to the current list. [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices).

## Freshness and availability

These thresholds are proposed product defaults, not Apple timing requirements: summary stale after 15 minutes; active delivery stale after 5 minutes without an authoritative update. Store event ID, server observation time, revision, expiry, safe status and optional confirmed estimate. Arrival time is an estimate, never a completion signal. Reject older revisions and timestamps in the future; show unavailable rather than negative ages.

| State | Widget | Live Activity | Recovery |
|---|---|---|---|
| Fresh | Confirmed summary plus update age | Confirmed milestone and optional estimated arrival window | Update changed content only. |
| Refreshing with cache | Keep existing status and age | Keep last confirmed milestone; age remains visible | Do not replace useful data with skeletons. |
| Stale, connection unknown | “Update delayed”; previous value explicitly labeled “Last known” if present | “Updates delayed”; “Last known: [milestone]” if present; remove expired ETA/countdown | Successful newer server snapshot restores fresh state. |
| Known offline | “Offline · last update [time]”; last-known safe summary | “Offline · status unconfirmed”; last-update time, no moving delivery progress | Only display offline with actual connectivity/fetch evidence. Retry in app; system delivery of updates is not guaranteed. |
| No cache | “Status unavailable · Open to check” | Start only when an authorized active event is known; otherwise show app fallback | Explain failure in app; no fabricated zero pickups. |
| Signed out/no household selected | “Sign in to view pickups” / “Choose household in app” | End personal activity on sign-out or lost authorization | Clear caches, including household cache when membership is revoked. |
| Fresh confirmed empty | “No pickups ready” plus freshness | Not applicable | Distinguish this from missing data. |

At 35 minutes old the supplied update is stale under both thresholds. Its age alone does not prove offline. Retain observation time while refreshing; a fetch attempt must not reset it. Schedule widget timeline entries for meaningful status changes, freshness boundaries and expiry; request reloads for changed data subject to system budgets. No one-second refresh promise. Use system date/time presentation where appropriate; it does not fetch new server data. [Widgets — updating content](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content).

## Delivery Live Activity

**Start:** the person selects “Follow delivery” in authenticated delivery detail after seeing that status can appear on Lock Screen and connected displays. Start only for an authorized active delivery; offer “Stop following” in the same app view. Dismissing or stopping following does not cancel delivery. If Live Activities are unavailable or disabled, retain equivalent app status.

**Progress:** use server-confirmed stages, for example “Preparing → On the way → Arrived → Delivered”; these labels are proposed, not observed. No percent ring or simulated movement based solely on elapsed time. The expected duration is 80 minutes, well within the local HIG recommendation for bounded events ideally no longer than 8 hours. A late delivery can remain active with confirmed delayed status; do not declare it delivered when the expected duration elapses.

**Bound:** set a product tracking deadline at start + 120 minutes. At 80 minutes without confirmation, replace any expired estimate with “Taking longer than expected”; stale/offline wording takes precedence. At the 120-minute deadline, end with “Tracking ended · Check delivery in app,” explicitly leaving delivery outcome unconfirmed. This is a proposed fallback requiring service approval. A later app visit can offer a new follow session for a still-active delivery, never silently restart an ended one.

**End:** on confirmed delivery, cancellation or failure, end immediately with safe matching summary; remove from Dynamic Island. Retain an ordinary terminal Lock Screen summary for 15 minutes where supported, then dismiss. On sign-out, revoked access, or privacy opt-out, request immediate removal without a retained personal summary. Reject subsequent nonterminal updates for ended event revisions. Reconciliation must handle missed completion pushes; deadline handling and remote ending require SDK/backend verification. [Live Activities — starting, updating and ending](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity).

| Presentation | Content contract |
|---|---|
| Compact | Leading parcel/status symbol; trailing short meaningful status or confirmed ETA. Both halves open the same delivery. Stale replaces ETA with warning symbol and short “Delayed” label where space allows. |
| Minimal / competing activities | Parcel plus current-state badge: movement, check, or warning; accessibility name includes safe status and freshness. Never a static logo alone. Limited-width fallback uses a meaningful status symbol; do not force text into a 28-pt circle. |
| Expanded | Parcel identity at leading, status at trailing, preserving relative positions; “Delivery” heading, milestone, freshness, optional confirmed arrival window. Whole presentation deep-links; no additional direct-action button is necessary for this monitoring task. |
| Lock Screen | Same semantic hierarchy in a distinct task banner; no address/code/name. Default contextual background, 14-pt standard margins as a starting point. |
| StandBy | Large status, shortened freshness, removable nonessential background details; check 2× scaling and red Night Mode. No private details across the room. |
| Paired Watch Smart Stack | Status plus freshness; default combined compact content or tailored read-only small layout. Tap opens Watch delivery detail when available; otherwise system full-screen continuation to paired iPhone. |
| CarPlay / paired Mac | Read-only safe status remains useful with CarPlay controls disabled. Mac activation follows system iPhone Mirroring behavior. No claim of HomeView Live Activity support. |

Only Lock Screen allows custom Live Activity background color; keep Dynamic Island backgrounds system-controlled. Use essential alerts only for a newly confirmed arrival requiring action or a delivery failure; deduplicate by event/revision and do not send a duplicate push notification. Staleness transitions are quiet. [Live Activities — presentations and interactivity](https://developer.apple.com/design/human-interface-guidelines/live-activities#Presentation).

## Privacy, rendering and access decisions

| Data | Purpose and permitted exposure |
|---|---|
| Household-approved count/readiness | Shared pickup glance, after explicit household selection and approval. Default unconfigured state reveals no parcel information. Sharing preview says “Everyone who can see the household display can see this summary.” Withdrawal removes shared data. |
| Event ID, stage, update time, optional estimate | Personal activity’s minimal safe payload. Use opaque routing IDs and recheck authorization after activation. |
| Recipient, full address, gate credential | Authenticated app delivery detail only. Fetch only when needed; minimize caching and protect any retained secrets with established system protections. No credentials in logs or links. |
| Phone location, contacts, camera | No need established by this feature; request no access for these glances. Courier/server updates do not require tracking the recipient’s phone. |

Use actual text, system styles and aligned symbols. Primary status gets strongest emphasis; freshness remains legible. In accented mode, status is primary and parcel glyph is accent; no meaning depends on hue. In vibrant/grayscale, distinguish hierarchy using appropriate grayscale brightness, not only reduced white opacity. Support full-color light/dark, Home Screen tint/clear, Lock Screen vibrant, background-removed HomeView and StandBy, HomeView red Night Mode, and Watch tint. These follow [Widgets — rendering modes](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes).

On supported Always On devices, retain stable status/freshness positions, dim secondary detail, show no secrets and avoid continuous movement. Tap or wrist raise returns to the same object. Provide the same safe information when privacy redaction is enabled, or “Open app for delivery” if system policy hides even the safe state. Do not assume every iPhone supports Always On. [Always On](https://developer.apple.com/design/human-interface-guidelines/always-on#Best-practices).

At large text sizes remove secondary decoration before status or freshness; use the rectangular alternative when inline capacity is insufficient. Never shrink essential content to force a fit. Preview long translations and plural counts. The whole widget is one semantic activation with safe status and timestamp; decorative glyphs are hidden from accessibility. App actions use native controls with a 44 × 44 pt default target and adequate separation. Verify iPhone text enlargement at least 200% and Watch 140%, plus supported widget Dynamic Type sizes through AX5. Status has text/symbol equivalents; no sound or animation is necessary. [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision), [Watch glance conventions](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices).

Gallery description: “Check household pickups.” Simulated preview: “1 pickup ready · Updated 2 min ago.” Placeholder: stable heading and neutral blocks, with no real identity or credentials; never show a fake ready count while loading.

## Acceptance checks and evidence

**Passed — specification/static review only:** inspected the supplied brief; replaced three inline targets with one destination; removed sensitive fields from every external-surface contract; selected families from local support tables; separated periodic refresh from bounded delivery tracking; classified 35-minute-old data as stale without asserting offline; defined completion and unknown-outcome timeout separately.

**Failed — supplied proposal:** second-by-second widget refresh promise; full address/code on the shared face; separate inline Accept/Cancel/Details targets. These are design findings from the brief, not measured software defects.

**Not executed — implementation acceptance gates:**

| Check | Required observable result |
|---|---|
| Fresh → 35-minute stale → offline → reconnect | No live ETA or readiness assertion from stale data; correct observation age; offline only with evidence; newer authoritative snapshot restores state. |
| Cache/account matrix | Loading, fresh empty, no data, signed-out, wrong household and revoked membership remain distinct; no cross-account residue or private field leakage. |
| Lifecycle replay | Start once; handle duplicate/out-of-order pushes; end at confirmed terminal signal; expired estimate never claims delivery; unknown-outcome deadline ends tracking; no resurrection after end. |
| Destinations and interruptions | Every tap reaches the selected authorized object; inline exposes exactly one target; removal/revocation gives useful fallback; resume preserves context. |
| Layout/render matrix | Each selected family fits actual device sizes, longest strings/counts, supported text sizes, light/dark, tint/clear, vibrant, background removal, red mode and Always On. State remains identifiable without color. |
| Accessibility | Measure real contrast and hit areas; VoiceOver reads safe state and freshness in useful order; supported assistive activation reaches the same destination; no clipped essential text. |
| Connected contexts | Shared HomeView contains only approved household summary; Watch wrist raise/dim state and app continuation work; CarPlay remains useful without controls; competing Dynamic Island activities retain meaningful minimal state. |
| Backend/energy | Delayed/missing pushes, meaningful timeline entries, stale deadlines, offline reconciliation and remote ending work within actual platform budgets; no assumed continuous polling. |

Still missing: target OS/device matrix and installed SDK availability; native layouts/code and screenshots; pickup readiness and sharing authorization model; service stage/ETA contract and server timestamps/revisions; consent and revocation propagation; confirmation of the proposed freshness thresholds and 120-minute tracking deadline; authenticated deep-link and secret-storage implementation; actual HomeView handoff capability; Watch app scope; update/termination delivery evidence; measured contrast, localization fit, accessibility and physical-device results. No SDK compilation, GUI, simulator, device, VoiceOver, push, household, or accessibility execution is claimed.

## Local guidance audit

Read the installed root `.agents/skills/apple-hig/SKILL.md`, then searched `references/topic-index.md`. Read owning family routes before topic procedures, and topic procedures before their source guides: Getting started → Designing for iOS / Designing for watchOS; System experiences → Widgets / Live Activities / Complications; Foundations → Privacy / Accessibility; Technologies → Always On. Every file read used its installed package path in a separate `cat`, `head`, or `rg` command. References are dated local guidance, not SDK availability verification. No external source or browsing was used.
