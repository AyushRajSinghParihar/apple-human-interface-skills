# Revised nearby-item finding specification

## Scope and decisions

Replace the behavior described in `interface.md`: an iOS finder that always claims exact centimeter distance, points through walls without uncertainty, and breaks when direction disappears. The task is finding a selected physical item using an available accessory. Accessory presence alone does not establish ranging compatibility, identity, permission, accuracy, or direction support.

This is a framework-agnostic interaction contract, not SDK implementation. The following source links identify the official articles underlying the installed local guidance; no web retrieval was performed.

| Decision | Concrete behavior | Basis |
|---|---|---|
| Gate precision by capability | Resolve selected accessory identity and phone/accessory compatibility before offering live guidance. Unknown support shows “Checking finding support…”; unsupported shows “Nearby guidance isn’t available for this item.” Never infer UWB from iPhone eligibility alone. | [Nearby interactions](https://developer.apple.com/design/human-interface-guidelines/nearby-interactions#Best-practices); product gating decision |
| Separate distance and direction | Show only fresh, usable measurements. Distance alone never generates an arrow. Reacquire direction without restarting the task. | [Nearby interactions: Device usage](https://developer.apple.com/design/human-interface-guidelines/nearby-interactions#Device-usage) |
| Communicate uncertainty | Use “About … away,” with precision limited by validated measurement quality. No universal centimeter claim, wall penetration claim, floor identification, or navigable route. Bearing means relative direction, not a safe path. | [Nearby interactions](https://developer.apple.com/design/human-interface-guidelines/nearby-interactions#Best-practices); conservative product interpretation |
| Ask at invocation | Request only access actually needed when the person taps “Find nearby.” Denial leaves item details and manual finding usable. | [Privacy: Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission) |
| Keep an alternative through completion | “Find without nearby guidance” opens a manual checklist and explicit “I found it” completion. This does not promise physical recovery. | [Nearby interactions](https://developer.apple.com/design/human-interface-guidelines/nearby-interactions#Best-practices) |
| Preserve handheld context | Keep selected item, Back, and Stop available. Resume with new capability/permission/signal checks; never reuse a pre-interruption arrow. Support portrait and landscape. | [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices) |

## Entry, screen, and completion

Item details show the item’s existing name and identifying description/photo, if supplied. Selection identifies the intended item; a transient sensing identifier must not become its permanent identity. Primary action: **Find nearby**. Secondary action: **Find without nearby guidance**. Do not invent a last-known location, map, sound command, or pairing capability.

On Find nearby, check capability without starting protected sensing. If supported, request required permission if undetermined, then connect to the selected accessory. Example purpose copy, subject to actual integration review: “Use nearby interactions to estimate this item’s distance and direction while you find it.” Use the real platform authorization mechanism when available; do not simulate consent. Omit a custom pre-alert because this entry already explains the task. If no authorization mechanism or sensing provider exists, use the unsupported state.

Finding screen, in order: item name; persistent state text; available distance; available relative direction and matching text; short contextual guidance; actions. Keep **Stop finding** and **Find without nearby guidance** reachable, generally in the middle/lower display. Back stops the session and returns to the same item. **I found it** ends sensing and shows “Finding complete” until explicitly dismissed; proximity alone never marks success.

## Capability and signal-state feedback map

These states are mutually exclusive display modes; permission and capability failures take precedence over signal data.

| State / trigger | Display and actions | Next transition |
|---|---|---|
| Checking / unknown support | “Checking finding support…”; no numeric estimate or arrow; manual option and Stop remain available | Capability result → unsupported, permission, or connecting |
| Unsupported | “Nearby guidance isn’t available for this item.” Manual option; Retry support check; item details | Retry rechecks rather than assuming success |
| Permission undetermined | Real authorization request after invocation; no ranging before grant | Grant → connecting; denial/restriction → access unavailable |
| Access unavailable | “Nearby guidance is unavailable with current access.” Manual option; show “Review access” only if a verified settings route exists | Explicit Retry rechecks access; never repeatedly prompt on its own |
| Connecting / no usable sample yet | “Connecting to [item]…”; no estimate or arrow | Valid sample → corresponding live state; failure → disconnected |
| Distance and direction usable | “About 2.5 m away” and arrow with “To your right,” for example; “Direction points toward the item, not a route around obstacles.” | Re-evaluate on every sample or validity expiry |
| Distance only | “About 2.5 m away · Direction unavailable.” Remove arrow immediately. “Try holding iPhone upright and gently turning toward the item.” A simple upright-phone illustration may supplement this text. | Direction returns → full guidance; distance fails → uncertain |
| Direction only | Relative arrow/text only if independently valid; “Distance unavailable.” Do not imply proximity | Distance returns → full guidance; bearing fails → uncertain |
| Uncertain / degraded | “Can’t estimate reliably right now.” No live number or arrow. “People or large objects between you and the item can affect guidance. Try a clearer position.” | Usable data → live state; explicit connection loss → disconnected |
| Disconnected / accessory lost | “Connection lost. Move closer if possible, then try again.” No frozen live measurements. Retry and manual option | Retry → capability/access checks, then connecting |
| Interrupted / app inactive | Stop presenting live data and release active sensing as integration permits; retain selected item and manual checklist | Return → “Resume finding” → fresh checks; no automatic permission prompt |
| Found / stopped | End session; clear samples and session identifiers | Done returns to selected item |

Do not treat an obstacle as detected: the obstruction copy describes a possible cause. Do not tell the person to walk through a wall or infer an unobstructed path from bearing. Holding guidance is optional assistance, never a required gesture or a substitute for the manual path.

### Provider contract and rendering pseudocode

The integration must supply independently qualified values, connection state, timestamps, and verified identity binding. If it cannot qualify freshness/quality, treat that value as unavailable. Session identifiers are temporary and must be bound to the selected accessory using a verified integration mechanism before guidance begins.

```text
on FindNearby:
    preserve selectedItem
    check phone + accessory + provider compatibility
    if unknown or unsupported: render corresponding state; return
    request only required access if undetermined
    if not granted: render accessUnavailable; return
    start new session bound to selectedItem

on sample or validity-expiry timer:
    reject samples from old sessions or a different item
    d = finite nonnegative distance AND provider-qualified quality AND fresh
    b = valid relative bearing AND provider-qualified quality AND fresh
    if not active, authorized, compatible, connected, identityBound:
        clear all live guidance; render applicable non-live state
    else:
        render full / distanceOnly / directionOnly / uncertain from (d, b)

on Stop, Back, Found, access revocation, or session replacement:
    end active session; invalidate samples and scheduled feedback
```

Freshness expiry, quality thresholds, and display rounding are integration parameters requiring hardware validation, not HIG numbers. Until a provider supplies validated limits, suppress live guidance. Proposed formatting policy: use localized units, “About,” and no more precision than the validated uncertainty supports; become more detailed only when quality supports it as the person approaches. Distance is straight-line separation, not walking distance. Do not translate decreasing distance into “warmer” unless the change exceeds validated noise. Update continuously from usable samples; remove expired guidance even if no further sample arrives.

## Alternative, privacy, and sensory access

Manual finding opens the same item’s identifying details plus a checklist: “Check where you last used it,” “Check pockets, bags, and nearby surfaces,” and an optional user-entered search note. Provide **I found it**, **Keep looking**, and **Back to item**. This path works with denied permission, unsupported hardware, a disconnected accessory, and no sensing provider. Notes survive interruption; do not claim a recorded location exists. An optional **Play sound** may be added only after accessory support, command delivery, and permissions are established; command failure must retain the checklist. It is outside the baseline contract.

Data-purpose/access matrix:

| Data | Purpose / access | Retention decision |
|---|---|---|
| Selected item identity/details | Identify the intended target; existing app data | Preserve under existing item-data policy |
| Relative distance/direction, quality, timestamps | In-use guidance, after required consent | Process locally; keep only current session samples; no server transfer or history in this proposal |
| Session identifier | Bind active sensing to selected item | Clear at session end; never use as persistent identity |
| Manual checklist/note | Continue a user-directed search; no sensor access | Keep locally until user clears it or item is removed |

No GPS, camera, microphone, contacts, or background tracking is assumed necessary. Verify any transport-specific access before implementation and update actual privacy disclosures if collection changes. These minimization choices follow [Privacy: Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices).

All essential state and direction information has text equivalents; color and an arrow alone are insufficient. Use labeled actions with iOS default activation areas of at least 44 × 44 pt as the design target. Permit at least 200% text enlargement with reflow, keeping all actions available by scrolling. Controls need meaningful names, roles, enabled states, and current values; dynamic guidance must remain available to assistive technology without moving focus on every sample. Do not require hearing, speech, or device rotation to finish the manual path. Baseline feedback is visual/text with accessible semantics; sound and haptic patterns are not specified or assumed. These requirements derive from [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), with geometry and runtime behavior still untested.

## Worked before → after

**Before, from the supplied brief:** With the item behind a wall, the UI asserts an exact centimeter distance and an unqualified arrow. When the phone turns and bearing disappears, the flow breaks. Permission denial and loss of the accessory have no defined recovery.

**After, illustrative inputs rather than measurements:** The person selects “Keys,” taps Find nearby, grants access, and the verified provider reports usable distance 2.47 m with quality supporting 0.5 m display increments and a valid rightward bearing. The screen reads “About 2.5 m away · To your right,” with the obstacle/route qualification. It does not claim to detect the wall. On turning the phone, direction becomes invalid while distance remains usable: the arrow disappears and text becomes “About 2.5 m away · Direction unavailable,” with upright-holding guidance. Connection then drops: both live values disappear and “Connection lost” offers Retry and manual finding. The person opens the checklist, finds the keys in a bag, and taps I found it. If access had been denied, the same manual route would complete without sensing or repeated prompts.

## Acceptance checks and audit status

**Passed — document inspection only:** The specification replaces the three supplied problem behaviors; independently models distance/direction; specifies permission denial, unknown support, accessory loss, interruption and explicit completion; includes a complete manual route and provider-independent pseudocode. Installed root → family → topic → supporting reference was read for iOS, nearby interactions, privacy, and accessibility; the topic index was searched before finalizing the route.

**Failed — supplied baseline, based on its description:** unconditional exact precision; unqualified directional guidance; inability to continue without direction. No implementation failure is inferred beyond that supplied description.

**Not executed — implementation acceptance scenarios:**

1. Unknown or incompatible accessory never produces a live estimate. Selecting a different item invalidates the old session; delayed old samples cannot reappear.
2. Undetermined access is requested only after Find nearby. Denial, restriction, and mid-session revocation clear sensing guidance and preserve manual completion. No unrelated access is requested.
3. Feed full → distance-only → no usable values → full. Arrow disappears on bearing loss, distance disappears on expiry, and recovery requires no task restart. Also test independently valid direction-only data.
4. Stop delivering samples while connected. At the provider’s validated expiry, live values disappear without waiting for another callback. Poor-quality, negative, nonfinite, wrong-item, and old-session values never render.
5. Disconnect and retry; interrupt and resume; rotate portrait/landscape. Preserve selected item and notes, discard old guidance, and recheck access/capabilities before new sensing.
6. Complete the manual path with permission denied, no provider, and accessory unavailable. Confirm I found it ends any active session and that close distance never auto-completes.
7. On eligible paired hardware, validate precision, freshness, field-of-view transitions, obstruction behavior, and distance formatting against measured error. Fail any confident precision unsupported by those results.
8. In an actual rendered interface, check 200% text, light/dark contrast, 44 × 44 pt targets and separation, portrait/landscape reflow, and reachable Stop/Back/manual actions. Measure rather than infer geometry or contrast from this document.
9. On supported Apple environments, test screen-reader and assistive activation through selection, access failure, degraded guidance, manual finding, and completion. Confirm updates do not repeatedly steal focus and essential information is available without sight or hearing. Check physical reach and comfort on iPhone.

## Evidence limits

Only `interface.md` and installed skill instructions/local reference articles were used. The local nearby-interactions reference lists a June 21, 2023 source revision and a 2026-10-25 retrieval date; it is design guidance, not an accessory compatibility list or accuracy guarantee. No newer-release claims are made. The references establish neither this accessory’s protocol nor supported models, authorization categories, API availability, quality metadata, or numerical accuracy. Those remain integration prerequisites.

No application code, SDK, connected device, GUI, accessibility runtime, physical measurement, audio, or haptic execution was supplied or exercised. The pseudocode and worked values are proposed contracts/examples. Document review cannot establish implementation correctness, native rendering, touch comfort, security compliance, or actual ability to recover a lost item. No web, linked video, or original media was reviewed.
