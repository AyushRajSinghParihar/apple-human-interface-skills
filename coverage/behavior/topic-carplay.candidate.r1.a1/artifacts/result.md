# CarPlay fuel-stop finder: distraction audit

Decision: revise the driving flow before implementation approval. Remove mandatory enrollment and address typing from fuel-stop selection, remove promotional animation, and keep account administration on the phone for use before driving or when stopped. CarPlay category eligibility remains an unresolved release dependency. This is a framework-agnostic behavior specification, not a claim of CarPlay approval or SDK support.

## Evidence and scope

The entire supplied specimen is `interface.md`, line 1: a CarPlay prototype asks drivers to type a full address, shows an animated promotional map, exposes every iPhone account setting, requires six-step loyalty enrollment before route selection, and has no established product-category eligibility. These are verified statements about the supplied specification, not observed runtime behavior. No screenshot, implementation, control inventory, timing measurement, or car test was supplied.

The installed apple-hig root was read explicitly, followed by family routes, topic procedures, and their local source guides. Routes used: Technologies → CarPlay and Maps; Getting started → Designing for iOS (CarPlay's connected-phone platform context); Selection and input → Text fields; Foundations → Motion and Writing; Patterns → Managing accounts and Settings. CarPlay's driving-specific placement and interaction guidance governs the car surface; the iPhone guide's middle/lower reach advice applies to handheld phone use, not the vehicle display.

Links below identify official source articles/sections recorded by the installed guides. They were not opened online. The local material is derived guidance, not SDK documentation or independently verified current policy.

## Ranked verified findings

Priority reflects task obstruction and likely attention burden; no distraction duration or crash-risk estimate was measured.

| Rank | Verified evidence and effect | Source-backed decision and correction |
|---|---|---|
| 1 — High | Six-step loyalty enrollment is required before route selection. A secondary account task blocks the driver's immediate fuel-stop task. | Separate setup from driving and allow useful unregistered access unless accounts are essential. Make finding/selecting a fuel stop independent of enrollment; retain optional loyalty setup on the phone before driving or when stopped. The brief supplies no evidence that loyalty is essential to routing. [CarPlay: iPhone interactions](https://developer.apple.com/design/human-interface-guidelines/carplay#iPhone-interactions), [Managing accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts). |
| 2 — High | Drivers are asked to type a full address. Lengthy manual entry adds work before obtaining a useful result. | CarPlay should focus on quick, minimal interactions. Default to nearby fuel stops using already available location; permit selection from existing destinations where available. Do not require address entry to select a stop. This correction applies the driving guidance; it is not a claim that all CarPlay text entry is universally prohibited. [CarPlay](https://developer.apple.com/design/human-interface-guidelines/carplay). |
| 3 — High | The map is animated and promotional. It competes for attention with choosing a fuel stop. | Remove promotional animation from the driving surface. Keep geographic context and selected-stop information useful to the task; use only necessary system/template feedback. Motion should support the task and have reduced/optional behavior. Removing promotions entirely here is a product decision, not a cited universal advertising ban. [Motion: Best practices](https://developer.apple.com/design/human-interface-guidelines/motion#Best-practices), [CarPlay: Layout](https://developer.apple.com/design/human-interface-guidelines/carplay#Layout). |
| 4 — Medium | Every iPhone account setting is exposed. Broad administration increases scanning and navigation unrelated to the immediate task. | Omit account administration from the driving surface. Preserve account settings on the phone; synchronize useful existing preferences without requiring phone interaction. Only task-relevant options belong beside their effect. Exact setting-level defects cannot be asserted without an inventory. [Settings](https://developer.apple.com/design/human-interface-guidelines/settings), [CarPlay: iPhone interactions](https://developer.apple.com/design/human-interface-guidelines/carplay#iPhone-interactions). |

**Release dependency — eligibility unestablished:** the brief explicitly says category eligibility has not been established. Verify the actual product category, required authorization, and permitted templates before committing a CarPlay implementation. A fuel-stop finder name alone proves neither eligibility nor ineligibility. The local CarPlay guide calls for category-appropriate system templates but does not establish this product's category or supply a complete eligibility policy. Do not substitute an arbitrary custom car UI. This uncertainty remains open under the local-only evidence constraint. [CarPlay](https://developer.apple.com/design/human-interface-guidelines/carplay).

## Corrected behavior contract

The following choices are proposed corrections. Nearby-first, the row contents, and the explicit route action are design decisions, not mandated template names or API calls. Implementation must map them to permitted category-specific system templates once eligibility is verified.

1. Before driving, the phone may offer optional loyalty enrollment, account administration, and any necessary permission/configuration setup. Enrollment cancellation preserves ordinary fuel finding. Keep these phone capabilities available when safely stopped.
2. On CarPlay entry, present nearby fuel-stop results when usable location is already available. An existing route may supply an along-route search context if the product actually supports it; otherwise omit that choice. Never invent location, route, or station data.
3. Show concise station name and available distance/detour information. Include opening status only when supported by trustworthy data; unknown status must not imply open. Keep primary selectable content prominent, generally in the upper half within template constraints. No promotion, enrollment form, or full settings hierarchy appears. [CarPlay: Layout](https://developer.apple.com/design/human-interface-guidelines/carplay#Layout).
4. Selecting a station opens its concise summary with a clear `Route to stop` action and Back. Preserve the selected station and surrounding geography if a supported template includes a map. Do not cover necessary map context or attribution. Generic map-card guidance does not establish CarPlay card support. [Maps](https://developer.apple.com/design/human-interface-guidelines/maps).
5. `Route to stop` requests a route through the supported routing integration; selection alone does not silently replace an existing destination. On success, show the resulting route state. Back before commitment leaves the current route unchanged. Route ownership and any existing-route replacement/add-stop behavior require explicit integration design before implementation.
6. All ordinary selection and recovery must work with the connected phone locked and inaccessible. Account expiry does not gate public fuel results. If a phone-only repair is necessary, explain it in CarPlay and defer repair until stopped; never request immediate phone handling. [CarPlay: Error handling](https://developer.apple.com/design/human-interface-guidelines/carplay#Error-handling).

```text
enterCarPlay:
    preserve existing route context
    fetch public fuel stops using available search context
    -> Loading (Back available; no animation added for promotion)

Loading + results -> Results
Loading + no results -> Empty("No fuel stops found", Retry, Back)
Loading + service failure -> Unavailable("Fuel stops unavailable", Retry, Back)
Loading + missing location/context -> Unavailable(
    "Location unavailable. Set up location when stopped.", Retry, Back)
    // Offer existing saved context only if genuinely available and supported.

Results + select(station) -> StopSummary(station)
StopSummary + Back -> Results(preserve selection)
StopSummary + RouteToStop -> Routing(station)
Routing + success -> RouteResult(station)
Routing + failure -> StopSummary(station,
    "Route unavailable", RetryRoute, Back)

any state + loyalty/account unavailable:
    retain public fuel finding; defer optional account repair
any pending request + Back:
    leave pending state; ignore late response for that abandoned request
interruption/reentry:
    restore selection/context; revalidate stale data before route commitment
```

Messages and verbs describe outcomes without blaming the driver. Exact presentation must fit supported template capabilities; these logical states do not require custom alerts, sheets, or controls. [Writing](https://developer.apple.com/design/human-interface-guidelines/writing).

## Worked before/after

Scenario: a driver with no loyalty account wants a fuel stop; the connected phone is locked. Example station data below is fictional, solely to illustrate behavior.

**Before, supplied:** the driver is asked for a full address, sees an animated promotional map and the full account-settings surface, and must complete six enrollment steps before route selection. The brief does not specify the order of the address/map/settings surfaces, so no exact screen sequence or tap count is claimed.

**After, proposed:** CarPlay opens nearby results, including `Example Fuel — 2 km` from hypothetical available data. The driver selects Example Fuel, then `Route to stop`. A route request succeeds and the route result is shown. No address or loyalty information is required and the phone stays locked. If route retrieval fails, the station remains selected with `Route unavailable`, `Retry route`, and Back. No promotion interrupts either path. This example uses two selection actions after results load; it is not a measured timing or universal interaction-count requirement.

## Acceptance checks and status

**Passed — static review:** the supplied brief was inspected; each stated distraction concern was mapped to a ranked finding and correction. The proposed contract supplies guest access, cancellation, empty/error recovery, locked-phone independence, and explicit route commitment. These passes establish document coverage only.

**Failed — supplied specification:** route selection is gated by six-step enrollment; full-address typing is requested of drivers; promotional motion is present; all phone account settings are exposed. These failures are specification-level comparisons with the decisions above.

**Not executed — implementation acceptance:**

| Check to execute | Required observable result |
|---|---|
| No account; phone locked; usable location | Results → station → route succeeds without enrollment, address typing, unlock, or phone action. |
| Expired loyalty session | Public fuel selection still works; optional account repair waits until stopped. |
| Location missing, empty results, network failure | Distinct concise states offer Retry/Back; no fabricated results or immediate phone-use instruction. |
| Route failure, Back, rapid repeated actions | Selection survives failure; retry is deliberate; Back preserves the prior route; late responses do not reopen abandoned screens or duplicate commitments. |
| Interruption and reentry | Useful selection/context returns and stale station/route data is checked before commitment. |
| Motion preferences and repeated interaction | No promotional animation; necessary transitions preserve state without delaying the next action or relying on motion alone. |
| Template and real vehicle controls | Category-permitted templates render correctly across supported displays; touch/rotary/other supported controls can reach, select, and leave each action. |
| Day/night, sunlight, long/localized content | Primary information remains readable, with adaptive appearance and no lost essential action or selected stop. |
| Audio coexistence | Fuel browsing does not unnecessarily start an audio session or silence existing audio. No audio behavior is supplied, so no existing audio defect is asserted. |

Eligibility/authorization and actual template mapping are **unresolved**, not passed. Field labels, validation, focus order, map gestures/attribution, account deletion, exact setting persistence, and reduced-motion implementation cannot be judged from the one-line brief. The address field, map, account-settings collection, enrollment flow, and route-selection action were considered as candidate text-field, map/motion, settings/account, account, and CarPlay-template interactions respectively; absent markup does not establish additional control defects.

## Evidence limits

Only local instructions and supplied text were used. No web browsing, Apple SDK, compilation, device, simulator, GUI, vehicle, accessibility technology, map service, or routing execution occurred. No claim is made about native rendering, focus/screen-reader order, physical comfort, template availability, data freshness, audio interruptions, contrast, or actual distraction reduction. Real vehicle controls, lighting and supported runtime testing remain necessary; this Linux document review cannot establish driving usability. The local snapshot's existence is not evidence of independent source review or current product eligibility.
