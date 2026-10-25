# Revised nearby-item finding specification

## Scope and decisions

Target: iOS on an eligible iPhone, finding a user-selected physical accessory. `interface.md` is the entire supplied product description: accessory support is unestablished; the current UI claims exact centimeter distance always, points through walls without uncertainty, and breaks when direction disappears. Permission denial and loss of the nearby device must be recoverable.

This is a framework-agnostic interaction contract, not an SDK implementation. An accessory being present does not establish ranging compatibility. Ship live finding only after verifying the specific phone/accessory combination, connection protocol, permission requirements, and available distance/direction outputs. Unknown support uses the fallback. Do not infer compatibility from the phone model alone. These feasibility checks remain open.

Decisions:

- Use proximity to help find the explicitly selected item. Bind a session to that item through a verified accessory association; never identify an item from distance or a session-scoped random identifier alone.
- Present estimates, never guaranteed centimeter precision. Render “About 2 m away” only from fresh, usable data. Display resolution must be no finer than the integration's validated accuracy; if accuracy cannot support a number, show “Nearby · distance uncertain.” More precise feedback near the item is conditional on validated quality, not merely a small reported number.
- Show an arrow only with a fresh usable bearing. It means an estimated direction relative to the phone, not a walkable route or evidence of a clear path. Never draw a through-wall path. Persistent helper: “Estimates can change around people and obstacles. Follow a safe, clear path.”
- Keep finding useful with distance alone. Use “Direction unavailable” plus a subtle phone-holding illustration and “Try holding your iPhone upright and slowly turning it.” Do not require a specific posture or movement to use the fallback.
- Treat denied permission, unsupported hardware, interruption, and signal loss as explicit states. Keep the selected item and a way to finish or stop the task in every state.

Source basis: [Nearby interactions — Best practices and Device usage](https://developer.apple.com/design/human-interface-guidelines/nearby-interactions#Best-practices) supports meaningful proximity, continuous feedback, alternatives, changing precision, missing direction, and obstacle guidance. Its iOS section describes distance and direction on compatible devices; it does not establish this accessory's support or promise accuracy. The display wording, quality policy, and state model below are product decisions applying that guidance.

## Screen and actions

Entry: selected item's detail page → **Find nearby**. Always also offer **Search manually**. The finding screen shows, in order: item name; connection/signal status; estimated distance and direction text when usable; optional arrow; helper text; actions **Search manually**, **I found it**, and **Stop finding**. Keep frequent actions toward the middle/lower display, preserve Back, and let Back stop sensing and return to the same item. Do not automatically claim success because distance approaches zero.

Manual search is an included product flow, not a link to another unavailable sensor feature: show the selected item's existing name/description/photo if supplied, allow the person to enter a place to check, display a persistent checklist of places they choose to inspect, and let them mark places checked. Offer **I found it** and **Finish for now** throughout. Persist this checklist and selected item across interruptions. Physical inspection and explicit “I found it” can complete the task without sensing, sound, an account, or permission; “Finish for now” saves an unresolved search. Do not invent a last-known location. If no identifying details exist, show the item name and allow the person to add a description. This alternative cannot guarantee recovery of a lost object.

No accessory sound command is assumed. Add **Play sound** only in a later specification after verifying that accessory capability and its authorization. Do not make sound, haptics, or color the sole carrier of an instruction.

## Permission and data contract

| Data/access | Purpose | Scope and lifetime |
| --- | --- | --- |
| Selected item association | Range the intended accessory | Existing verified association; session identifiers are temporary, not permanent identity |
| Nearby measurements | Estimate relative distance/direction | Only during active, foreground finding after required authorization; no measurement history or server transfer in this design |
| Manual places/checklist | Continue a manual search | Store locally until the person clears it; never treat user-entered places as sensor observations |

Request only access verified necessary by the eventual integration. Do not request camera, microphone, geographic location, or tracking merely because this is a finder. On **Find nearby**, check support without starting protected collection, then request required authorization if not determined. Proposed purpose sentence: “Use nearby interaction to estimate your accessory’s distance and direction while you find it.” Final copy must match actual collection. Use the real authorization mechanism supplied by the integration/platform; never simulate system consent.

No custom pre-permission alert is needed: the item and Find nearby action provide context. On denial show “Nearby access is off. You can search manually.” Offer **Search manually**, **Stop finding**, and a settings route only if the integration supplies one. Do not reprompt on every return or block item details. On a later explicit retry, recheck authorization; revoked access stops collection and clears live guidance immediately.

These choices apply [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission) and [Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices). The HIG's location-button example does not establish a need for geographic location in this flow.

## Capability and signal state contract

The integration must supply support = unknown/unsupported/supported, authorization, item association validity, session identity, measurement timestamp, per-channel usability, and any validated accuracy/quality information. Missing information is unknown, never affirmative. A monotonic clock and a documented `freshnessLimit` are required before live finding ships. Its numeric value and rounding bands require hardware evidence; they are not specified by HIG. If these parameters are unvalidated, live numerical/directional guidance stays disabled.

| State | Presentation | Recovery/transition |
| --- | --- | --- |
| Checking support | “Checking nearby finding…”; no estimate/arrow | Cancel anytime; unknown/unsupported → Unavailable; supported → authorization check |
| Unavailable | “Nearby finding isn’t available for this iPhone and accessory.” | Manual search; explicit Retry rechecks support |
| Permission needed | Real authorization request after Find nearby | Grant → Connecting; deny/restrict → Access off |
| Access off | Permission explanation above; no live guidance | Manual search; settings if supported; explicit retry |
| Connecting | “Connecting to [item]…”; no old measurements | Verified session → Waiting; connection failure → Lost; cancel anytime |
| Waiting | “Waiting for a nearby signal…” | Fresh channel(s) → appropriate active state; failure → Lost |
| Distance + direction | Estimated distance, arrow, matching direction text | Recompute independently as channels change |
| Distance only | Estimated distance; “Direction unavailable”; no arrow | Fresh bearing restores arrow without restarting |
| Direction only | “Distance unavailable”; estimated bearing and text if usable | Fresh distance restores number; never infer distance |
| Uncertain | “Signal uncertain”; no unusable number or arrow | Explain obstacles/holding; recover automatically when usable |
| Lost | “Nearby signal lost. Move closer if you can, or search manually.” | Clear all live guidance; Retry reconnects; manual path remains available |
| Paused | “Finding paused”; no live guidance | On foreground return preserve item, recheck access/support, reconnect with a new session |
| Found / Stopped | Stop sensing and discard live measurements | Found confirms “Marked as found”; Stop returns to item without marking found |

A failed connection or explicit disconnect enters Lost immediately. Silence invalidates each channel at `freshnessLimit`; if neither channel is fresh, enter Lost. Fresh but explicitly poor-quality data enters Uncertain. Never freeze the previous arrow while reconnecting. Retry remains cancellable; no fabricated progress percentage or automatic timeout claim is required.

```text
on(event):
  if stop, back, found, background, permission_revoked, or disconnect:
    stopSession(); invalidateAllLiveMeasurements()
    transition according to event; return
  if event is measurement:
    reject unless event.session == activeSession
      and event.item == selectedVerifiedItem
      and authorizationGranted and foreground
    distance = usableFiniteNonnegativeDistance(event) if fresh else absent
    bearing = usableBearing(event) if fresh else absent
  on every render and freshness deadline:
    expire each stale channel independently
    render only currently usable channels
    choose distance+direction / distance-only / direction-only /
      uncertain / lost from channel validity and connection status
  on resume or retry:
    clear old measurements; recheck support, association, authorization
    start a new session only when all gates pass
```

Do not convert absent values into zero. Discard late callbacks from old sessions, including after changing items. If item association is lost, stop and return to item selection rather than guiding toward an unidentified nearby device.

## Perception, input, and interruption

Every live state has readable status text. Direction text conveys the same estimate as the arrow, such as “Estimated direction: ahead and to your left”; distance-only text never implies a bearing. Expose item, status, measurement text, and labeled actions in that logical order with appropriate control roles/states. Keep focus on the person's current action during updates; do not repeatedly move it to the changing estimate. Offer a labeled **Read current guidance** action through the implementation's accessible output mechanism so updates can be requested without inspecting the arrow. If that mechanism is unavailable, do not claim nonvisual live guidance is complete; keep manual search accessible and block release on assistive testing.

Use text and shape in addition to color. No continuous sound/haptic encoding is included in this revision. Support at least 200% text enlargement with a stacked, scrollable layout and all actions reachable; use 17 pt as the iOS default text starting point and 44 × 44 pt activation areas as the control default, with adequate separation. These are platform defaults, not claims of measured rendering. Preserve item and search state across portrait/landscape and app interruptions. Show a static direction indicator rather than decorative pulsing, spinning, or zoom effects.

Basis: [Accessibility — Vision, Hearing, Mobility, Speech, and Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility) and [Designing for iOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices). Reachability, assistive input, and spoken behavior need implementation verification.

## Worked before → after

Illustrative inputs, not measured device results: the person selects “Keys”; support has been verified; they grant access. The adapter reports a usable distance of 2.37 m with quality sufficient only for whole-meter presentation, plus a usable leftward bearing. Then direction disappears while distance remains, followed by a disconnect near a wall.

Before (as described in the brief): “237 cm” appears as exact; the arrow implies a certain path through the wall; missing direction breaks finding.

After: “Keys · About 2 m away” and “Estimated direction: left” appear with an arrow and the safe-path helper. When bearing disappears, the arrow is removed immediately; “About 2 m away · Direction unavailable” and holding guidance remain. On disconnect, both estimates disappear and “Nearby signal lost” appears with Retry, Search manually, I found it, and Stop finding. The person chooses Search manually, adds “Hall table” and “Coat pockets,” checks them physically, and chooses I found it after finding the keys. If permission had been denied initially, the same manual completion would be available without starting sensing.

## Acceptance checks and results

**Passed — specification inspection only:** all failures explicitly named in `interface.md` have replacement behavior; accessory support is gated; distance and bearing are independent; denial/loss have recovery; manual search has an explicit completion; no SDK dependency or guaranteed accuracy is asserted. Root skill, selected families, topic procedures, and their local source guides were read in that order per route, one file per command.

**Failed — supplied baseline description:** unconditional exact-distance claims, confident obstacle guidance, and failure when direction is absent conflict with the revised contract. These findings concern the supplied prose; no running baseline was inspected.

**Not executed — implementation acceptance scenarios:**

| Scenario | Required observable result |
| --- | --- |
| Unknown/unsupported accessory, including capable phone | No ranging promise or authorization collection; manual path can reach Found |
| Grant, deny, restricted access, later revoke | Request only at entry; no pre-consent collection; denial remains usable; revoke clears measurements |
| Distance-only, direction-only, invalid/negative values | Only valid channels shown; no invented bearing, distance, or zero |
| Bearing leaves sensor field then returns | Arrow disappears and recovers; distance continues when usable |
| Obstruction, poor quality, disconnect, silence | Uncertainty or loss shown; stale guidance cleared by expiry; no obstacle-crossing instruction |
| Retry, change item, late callback, resume | Old session cannot update screen; selected item preserved; capability/access rechecked |
| Very close distance | Only validated precision shown; no automatic Found |
| Entire manual path with access denied | Add/check places, stop/resume, and mark found without sensing or sound |
| 200% text, portrait/landscape, light/dark | Essential text/actions remain usable; actual contrast measured; adequate activation areas and separation measured |
| VoiceOver, Switch Control, Full Keyboard Access, AssistiveTouch | All necessary actions reachable/activatable; meaningful names/status; stable focus; current guidance accessible without sight |
| Compatible physical phone/accessory trials | Verify support, association, accuracy, freshness/rounding choices, field loss, obstructions, interruption, and physical comfort |

## Evidence limits

Only `interface.md` and installed local HIG instructions/references were used; no web browsing occurred. Official links above identify the source articles referenced by the installed snapshot, not pages checked live. The nearby reference records a June 21, 2023 source revision and retrieval on October 25, 2026; existence of a local guide does not establish independent review or current SDK support.

There is no implementation, accessory model, protocol documentation, measurement trace, screen, or runtime evidence here. No device, SDK compilation, GUI, accessibility, accuracy, contrast, touch geometry, or physical-comfort test was executed. The contract is reviewable, but live finding is not release-ready until compatibility and signal policies are validated. Manual search assists physical recovery; it cannot promise to locate every lost item. No conflicting passages were identified in the selected local guides.
