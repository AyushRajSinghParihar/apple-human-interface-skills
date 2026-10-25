# Pickup summary and delivery activity

Design specification based on `interface.md` and the installed local Apple HIG snapshot. No web research, implementation, SDK compilation, GUI, device, or accessibility execution was performed. Example copy below is simulated; the brief supplies a parcel and a 35-minute-old update, but does not establish pickup readiness or a current ETA.

## Concrete result

The household glance answers **“Is there a pickup to check?”** The personal Live Activity answers **“What is happening with the delivery I’m following?”** They have separate content payloads and lifecycles.

### Household pickup widget

Choose a **system-small** widget for iPhone Home Screen and the shared Apple HomeView Modular face. This is a supported combination in the supplied snapshot; do not substitute a Lock Screen accessory family on the Modular face. Gallery title: “Household pickups”; description: “Check your household pickup summary.”

Small layout, in reading order:

```text
[parcel symbol] Household pickups
Pickup status unknown
Updated 35 min ago
Open app to check
```

After fresh, confirmed readiness, example content becomes “1 pickup ready” and “Updated just now.” A confirmed empty result reads “No pickups ready.” Never derive readiness from the presence of a parcel. Multiple authorized parcels aggregate into a count; the widget does not enumerate people or locations. The primary state occupies the largest text, with freshness directly beneath it. Use flexible system styles and margins rather than a fixed production canvas.

| Destination | Family and content | Activation |
|---|---|---|
| iPhone Home Screen | System small; same household-safe summary | Opens household pickup list, preserving household selection |
| Shared HomeView Modular face | System small; large primary status, short freshness line; removable background | Opens safe summary through the supported host route; personal details require the authorized personal app session |
| iPhone Lock Screen | Accessory inline: “Pickups · status unknown” when stale; fresh example “1 pickup ready” | One target to pickup list; freshness is the first detail there |
| iPhone Lock Screen | Accessory rectangular: “Pickup status unknown” / “Updated 35 min ago” | One target to pickup list |
| Paired Watch | Use delivery Live Activity in Smart Stack for this bounded event | Native system route described below; no separate watch complication in this design |

Remove the proposed inline Accept, Cancel and Details targets. Inline has one tap target; render a single summary, with no button-like subdivisions. Accept/Cancel, if the backend supports these operations, belong in the authorized parcel detail flow after current status is obtained. A tap never implicitly accepts or cancels anything. [Widgets: interactivity and supported families](https://developer.apple.com/design/human-interface-guidelines/widgets#Adding-interactivity).

### Privacy and configuration

Default household configuration is “Not sharing pickups / Set up in app.” The account holder chooses an authorized household and explicitly enables **“Share pickup summary”**, with explanation: “People in your household can see pickup counts and status. Names, addresses and access codes stay private.” This is a product sharing choice, not a fabricated OS permission alert. Until configured, expose no parcel existence or count. Personalized HomeView Home Screens still use the safe payload; the shared Modular face must never inherit private preferences.

| Data | Purpose and exposure |
|---|---|
| Authorized aggregate readiness/count and server timestamp | Household summary, only after sharing is enabled |
| Recipient name and full street address from the brief | Personal parcel detail after authorization; omitted from widget and activity payloads, previews, labels, and public caches |
| Gate/access code from the brief | Reveal only deliberately in the authorized app detail flow; store with established protected mechanisms, never in widget/activity snapshots or deep-link parameters |
| Opaque parcel ID | Personal activity routing; app checks account authorization on every entry |
| Device location, contacts, camera | No dependency for these glances; request no new access |

The Live Activity is personal to the followed delivery, **not a confidential screen**: Lock Screen, paired devices and across-room presentations can expose it. Even unlocked presentations use “Delivery” and a nonsecret icon rather than name/address/code. A “Hide delivery status” app setting reduces exposed content to “Delivery active / Open app”; it also applies to cached presentations. Revoking sharing/signing out clears local shared data and requests replacement with “Set up in app”; do not promise instantaneous remote cache erasure. Purge requests and propagation require verification. These are deliberate product privacy choices grounded in [Privacy: data minimization and protection](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices) and [Widgets: Apple HomeView](https://developer.apple.com/design/human-interface-guidelines/widgets#Apple-HomeView).

### Private bounded delivery Live Activity

An **80-minute** delivery is a bounded frequently changing event suited to a Live Activity; it is not a reason to reload a widget every second. Start after the person chooses “Follow delivery” on an authorized active delivery. Explain where status can appear and provide “Stop following” in that delivery view. If activities are unavailable/disabled, keep the same status in the app without blocking delivery. Do not start from a stale cached state as though the event is confirmed active. [Live Activities: best practices and lifecycle](https://developer.apple.com/design/human-interface-guidelines/live-activities#Best-practices).

| Presentation | Fresh, confirmed in-transit example | Stale/offline replacement |
|---|---|---|
| Compact | Leading parcel glyph; trailing “20 min” only with a valid estimate | Parcel with warning glyph; “Stale”; no expired countdown |
| Minimal / multiple activities | Parcel plus changing remaining-minutes value when space permits | Parcel plus warning mark; accessible meaning “Delivery status out of date”; never logo alone |
| Expanded | Parcel upper leading, “Delivery”; status/ETA in consistent relative position; update age beneath | “Status out of date”; “Last confirmed: in transit”; “Updated 35 min ago” |
| Lock Screen | Same hierarchy, distinct task banner; optional supported Lock Screen background only | Same stale copy plus “Offline” only when positively known; one “Open delivery” link |
| StandBy | Enlarged safe status/ETA; secondary age; adequate margins | Large “Status out of date”; no misleading timer; red Night Mode preserves meaning |
| Watch Smart Stack | Default compact-halves composition, shortened status; no action dependency | Warning + stale status; full freshness on opening |
| CarPlay projection | Read-only compact status, useful without controls | Warning + stale status; controls disabled by platform |
| Paired Mac | Compact/minimal/expanded safe content | Same stale policy; activation uses iPhone Mirroring |

Both compact halves and all other app links resolve to the same opaque delivery ID. With no Watch app assumed, Watch tap opens the system full-screen activity with paired-iPhone launch button; do not promise an installed Watch app. HomeView receives the widget, not a newly invented Live Activity destination. tvOS/visionOS Live Activities are excluded by the snapshot. Preserve app context across interruption, rotation, authentication and return. [Live Activities: presentations and platform considerations](https://developer.apple.com/design/human-interface-guidelines/live-activities#Presentation), [iOS conventions](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices), [watchOS glances](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices).

No direct delivery-changing action is needed on the activity. “Open delivery” is the sole essential path; stopping tracking in the app never cancels delivery. Do not add promotional content.

## Freshness and event contract

The following thresholds are **product proposals**, not Apple refresh guarantees: household summary fresh for 15 minutes; active delivery fresh for 5 minutes after its last authoritative event. Use server `updatedAt`, a monotonic event version, confirmed phase, optional estimate with validity deadline, and event ID. Reject older versions; future/invalid timestamps yield unknown freshness. Keep transport connectivity separate from server age.

| Condition | Widget | Live Activity / transition |
|---|---|---|
| No cached data | “Pickup status unavailable / Open app to check”; no invented count | No start until confirmed active; existing activity shows “Status unavailable” |
| Fresh authoritative result | Count/readiness and update age | Confirmed phase; ETA only while valid; phase changes only from authoritative events |
| Refresh pending | Keep last useful summary and age | Keep confirmed phase; freshness clock continues; no full replacement spinner |
| Beyond freshness deadline | “Pickup status unknown / Updated … ago” | “Status out of date”; mark last phase as last confirmed, suppress expired ETA |
| Positively known offline | Add “Offline” where space permits, retaining age | “Offline · updated … ago”; no assertion that courier stopped |
| Old data but network unknown | Say stale/unknown, never infer offline | Same; reconnect alone does not make data fresh |
| Reconnect + newer valid event | Restore confirmed state after response | Restore phase/ETA only after accepted update; no fabricated progress during outage |
| Signed out / revoked / no authorization | “Set up in app”; clear cached count | End activity and clear personal caches; app route authenticates or explains unavailable access |
| Delivered / cancelled / failed terminal event | Reflect new aggregate on next system opportunity | End immediately; safe “Delivered”, “Delivery cancelled”, or “Delivery ended” summary retained for 15 minutes where allowed, then removed |
| 80-minute expected end reached without terminal evidence | Remain truthful about unknown pickup state | End tracking with “Tracking ended · check delivery”; never infer delivered |

The 80-minute expected end is a proposed tracking deadline from confirmed start. A newer authoritative delay may extend it with a new explicit bounded deadline, up to a product cap of 2 hours total; at that cap, end tracking as unconfirmed and leave the app available. Stopping following ends immediately with no retained summary. Once ended, ignore late nonterminal events for that activity; obtain current state before offering a new follow session. Apple guidance favors bounded events ideally no more than 8 hours; the 2-hour cap is our shorter product decision, not a platform limit.

For the supplied **35-minute-old update**, both freshness thresholds have expired: show unknown/stale status, preserve age, do not assert readiness, arrival time, or offline connectivity.

Request widget timeline entries at meaningful known boundaries (including freshness expiry), plus reload opportunities after accepted data changes. System scheduling controls actual delivery; no per-second polling or visible-update guarantee. Use system time presentation for age when supported. Deliver changed Live Activity content from the authoritative event channel; schedule stale/ending handling through supported lifecycle mechanisms to be validated against SDKs. A ticking estimate is not evidence of server updates. If platform scheduling cannot guarantee a transition on time, expire ETA validity and use conservative snapshot wording rather than promise exact execution. Alert only for a verified crucial event such as arrival; deduplicate by event ID with notification channels so there is no parallel push for the same update. [Widget updating](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content), [Activity ending and update policy](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity).

## Rendering and accessibility decisions

Use actual text, system styles and semantic colors. State is always expressed in words and a symbol; color is supporting information. Full-color uses light/dark semantic treatment. Accented rendering keeps status primary and the parcel glyph accent; it must survive a single user tint and clear treatment. Vibrant rendering uses grayscale brightness for hierarchy, with opaque light primary text and darker secondary text, rather than opacity alone. HomeView/StandBy remove background; test Modular Night Mode red monochrome. Keep essential status before secondary age/detail when text enlarges; inline uses its deliberately shortened status, with full detail on opening. No text is shrunk to force multiple actions into an accessory. [Widgets: rendering modes and text](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes).

Active and Always On layouts retain the same content positions. Dim secondary details and rest animations; no pulsing courier marker or continuously moving map. Safe status stays readable; secrets remain absent in both states. On supported devices, test reduced-luminance grayscale and dismissal-control contrast. Device support must be checked, not inferred for every iPhone from the older Always On reference. [Always On](https://developer.apple.com/design/human-interface-guidelines/always-on#Best-practices).

Acceptance targets include text enlargement of at least 200% on iPhone and 140% on Watch, appropriate system widget text-size support, no essential clipping, and a task path usable without sound, color or precise gestures. Prefer standard system links; give status meaningful accessible text and label warning state explicitly. App controls use the iOS 44 × 44 pt default target as the starting point, with adequate separation; this is not a reason to invent accessory subtargets. Measure actual foreground/background contrast using the local guide’s stated Accessibility Inspector guidance (up to 17 pt: 4.5:1; 18 pt or bold: 3:1), preserving its scope rather than claiming universal conformance. [Accessibility: vision and mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

## Acceptance and evidence audit

**Passed — specification inspection only:** read the supplied brief; explicitly read installed root skill, searched topic index, and followed family → topic procedure → supporting guide for iOS/watchOS, widgets, Live Activities, privacy, accessibility and Always On. The proposed contract separates household/personal payloads, removes secrets, has one inline target, assigns supported surface families, treats the 35-minute sample as stale, and defines starts, ends and recovery. These passes establish design coverage, not functioning software.

**Failed — supplied proposal:** per-second widget refresh promise; address/access-code exposure on the shared face; three independent inline targets. Each has a concrete replacement above. No implemented correction can be verified because no implementation was supplied.

**Not executed — acceptance scenarios for implementation:**

| Check | Required evidence / pass condition |
|---|---|
| Family and deployment support | SDK/OS capability review and native previews validate HomeView small, Lock Screen accessories, activity destinations and availability fallback |
| Freshness | Clock-controlled tests at 5/15-minute boundaries and the 35-minute sample; stale data cannot appear current; unknown network never becomes “Offline” |
| Event integrity | Out-of-order, duplicate, future timestamp, reconnect, delayed and terminal events preserve truth; no duplicate arrival alerts |
| Bounded lifecycle | End at terminal event, stop-following, unknown expected end and cap; validate actual expiry/push failure behavior and 15-minute retained summary removal |
| Privacy | Inspect serialized payloads, snapshots, previews, accessible text and routes; no name/address/code leakage; test sharing revoke, sign-out, account switching and paired caches |
| Destinations | Activate every target, both compact halves and minimal presentation; correct authorized object opens, authentication resumes context; removed parcel has useful fallback |
| Appearance | Native previews/device evidence for light/dark, tint/clear, vibrant, removable background, HomeView/StandBy red mode, Always On, Watch wrist transitions, wallpapers and dismiss-button contrast |
| Size and access | Long/localized copy, large counts, iPhone text enlargement and Watch scale preserve state; measured contrast and targets; VoiceOver, Voice Control and Switch Control complete the same task |
| Interruption and projection | Resume same delivery after lock/rotation/app switch; multiple activities remain informative; Watch fallback works; CarPlay remains useful with all controls disabled |
| Household comprehension | Household participants understand shared scope, unknown versus empty, and stale versus offline without revealing private details |

Missing evidence: actual delivery/readiness schema, authoritative phase/terminal events, ETA validity rules, latency and offline signals, household authorization/revocation semantics, chosen minimum OS/device targets, SDK documentation and capability verification, native source/project, timeline/push budget behavior, cached-data protection and purge behavior, actual rendering and contrast measurements, assistive-technology results, device energy behavior, and household usability findings. The supplied local HIG files are dated application guidance, not SDK references or proof of execution. Official links above are attribution to those local sources; they were not browsed.
