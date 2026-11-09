# Documentary app: revised tvOS Top Shelf interaction specification

## Decisions and source basis

The supplied `interface.md` reports unrelated advertisements opening checkout, loud autoplay, documentary selections opening generic home, and previous-account history visible after sign-out. Replace this with useful documentary discovery on the Apple TV Home Screen.

Use a **dynamic sectioned content row of silent 16:9 documentary images**, labeled “Explore documentaries.” Documentaries often need context before a viewing commitment; each focused item reveals its title and a concise subtitle such as “Nature · 52 min · 2026.” Selection opens that exact documentary’s details. No preview audio or video starts on focus. This image-only choice is a product decision, not a claim that Apple prohibits autoplay. A details carousel could also supply context, but the row supports comparing several titles without preview playback.

The local [Top Shelf guide](https://developer.apple.com/design/human-interface-guidelines/top-shelf#Best-practices) favors dynamic, fresh, relevant content and direct links, advises avoiding ads and prominent prices, and permits a [sectioned row](https://developer.apple.com/design/human-interface-guidelines/top-shelf#Sectioned-content-row). Remove unrelated promotions and checkout destinations. Show purchase or subscription requirements on the selected title’s details when relevant; do not present a purchase as a viewing action.

Design for a shared television, recognizable imagery, titles readable across the room, and standard system focus behavior. The [tvOS guidance](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos#Best-practices) supports matching the app profile to the current viewer. The [privacy guidance](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices) supports minimizing data use. The isolation and opt-in policy below is an additional product safeguard, not a quoted tvOS permission requirement.

## Content and account contract

- Default, including signed-out, unknown-viewer, and unresolved-profile states: public editorial recommendations only. No history, progress, personalized ranking, account names, or personal artwork.
- Signed-in viewers may explicitly enable “Personalize Top Shelf” in app settings. Explain: “Show documentary recommendations based on this profile’s viewing history on the shared Apple TV Home Screen.” Default off per profile. Signing in alone does not enable it.
- Eligible items are documentaries available in the current region, age/profile restrictions, and catalog window, with validated artwork and a stable title identifier. Rank eligible new releases and editorial picks; when personalization is enabled, rank by that profile’s interests. Deduplicate by title ID. Exclude completed titles; intentionally omit resume history from this version. No paid ranking, unrelated ads, or prominent price graphics.
- Publish enough validated items to fill at least one screen-width row, with the contextual section label. Do not invent a fixed item count: verify capacity against the eventual platform presentation. If a complete row cannot be supplied, use static fallback.
- Refresh on catalog changes, app foreground, account/profile changes, personalization changes, and expiry. Product policy: catalog snapshots expire after 24 hours or the earliest included rights expiry, whichever comes first. This is a freshness limit, not an asserted tvOS refresh guarantee. Revalidate availability again at activation.

Data-purpose boundary: public catalog IDs, metadata, artwork, region and rights support editorial discovery; profile restrictions support eligibility; profile history supports ranking only after the app preference is enabled. Keep recommendation caches separated by opaque profile ID and account generation. Do not put history, names, credentials, or progress in routes. No new camera, microphone, contacts, or tracking permission is needed for this design. Existing collection and disclosure practices are not supplied and remain unassessed.

On sign-out, viewer change, profile change, or disabling personalization: increment account generation, cancel outstanding personalized work, invalidate its cache and published payload, and request immediate replacement with public content or neutral fallback. Unknown viewer mappings fail closed to public content. Late callbacks from the previous generation must never publish. Do not reuse old personalized snapshots offline. A renderer adapter must establish how to replace system-cached content; until privacy-safe replacement is demonstrated, ship public editorial content only.

## Assets and fallback

Use consistent 16:9 layered imagery, with descriptive title/subtitle metadata separate from artwork. Keep faces and essential subjects visible in both crops. From the local [16:9 row specifications](https://developer.apple.com/design/human-interface-guidelines/top-shelf#169):

| State | Points | Pixels at 1× | Pixels at 2× |
| --- | --- | --- | --- |
| Actual asset | 908 × 512 pt | 908 × 512 px | 1816 × 1024 px |
| Focused / safe zone | 852 × 479 pt | 852 × 479 px | 1704 × 958 px |
| Unfocused | 782 × 440 pt | 782 × 440 px | 1564 × 880 px |

Validate both state crops; placement within the focused safe zone alone does not establish visibility in the smaller unfocused crop. Avoid mixing aspect ratios, which can cause scaling. Supply clear focus enlargement using the system presentation; do not implement hover-only actions.

If dynamic content is unavailable, expired, incomplete, or unsafe for the current account context, publish neutral static documentary showcase art. Supply 2320 × 720 pt (2320 × 720 px at 1×; 4640 × 1440 px at 2×). The guide describes system flipping/blurring into a 1920-pixel-wide 16:9 context. Keep it free of private data and essential edge text. It is **nonfocusable**: no painted Play, Sign In, or other fake buttons. Launching the app through its ordinary icon remains separate from this artwork.

## Interaction and destination contract

The system owns Home Screen navigation. Left/right movement traverses the row using standard focus behavior; focus reveals the title/subtitle and never launches, purchases, or starts media. A deliberate Select press activates the focused title. Preserve the system’s exit path to the Dock/Home Screen; do not trap navigation or intercept held Back. These mappings follow [Remotes](https://developer.apple.com/design/human-interface-guidelines/remotes#Best-practices); actual system traversal still needs device verification.

Each dynamic item has a route equivalent to `documentary/{stableTitleID}/details`. This is a logical route, not an SDK API. Cold and warm launch both resolve the selected ID before showing the title’s details, never generic home. Details show the title, synopsis, duration, availability, and applicable access requirement. Starting playback or acquiring access requires an explicit action there. If sign-in is required, preserve the intended ID through authentication and then recheck current eligibility. Cancellation must not trigger checkout or playback.

If the title was removed or became region/restriction-ineligible, show “This documentary is no longer available” with an explicit “Browse documentaries” action. Do not silently substitute another film or open checkout. Invalid routes show a recoverable unavailable state. Details belong under the documentary catalog: Back returns to that parent; Back at app root returns Home, and held Back retains system behavior. A stale personalized activation after account change is re-resolved using the new context with no disclosure of the previous profile’s state.

Framework-agnostic state sketch:

```text
onContextChange(newContext):
    generation += 1
    cancelPendingPersonalizedWork()
    invalidateOldPersonalPayloads()
    requestPublish(neutralStaticFallback)
    refresh(newContext, generation)

refresh(context, capturedGeneration):
    mode = public
    if context.viewerResolved && context.signedIn && context.personalizationOptIn:
        mode = personalized(context.profileID)
    candidates = fetchEligibleCatalog(mode)
    payload = buildCompleteValidatedRow(candidates) or neutralStaticFallback
    if capturedGeneration != generation: discard(payload); return
    publishAtomically(payload, generation, expiry)

onActivate(titleID):
    context = currentContext()  // never trust a cached account identity
    result = resolveTitleAndEligibility(titleID, context)
    if result.available: openExactTitleDetails(result)
    else: openUnavailableState()  // explicit route onward to catalog
```

`requestPublish` and `publishAtomically` express required adapter behavior; they do not claim immediate control over a system cache or any available Apple API. At refresh failure, retain only a nonexpired snapshot valid for the same context; otherwise use public fallback.

## Worked before / after

Illustrative fixture, not an actual catalog record: “Ocean Witness,” ID `doc-042`, Nature, 52 minutes, released 2026, available in the current region.

| Moment | Supplied before | Revised after |
| --- | --- | --- |
| App highlighted in Dock | Unrelated ads; loud preview autoplay | Silent documentary row with “Explore documentaries” label |
| Focus on Ocean Witness | Preview behavior is reported generally; title-specific behavior is unknown | Focus treatment reveals “Ocean Witness” and “Nature · 52 min · 2026”; no playback |
| Select Ocean Witness | Documentary selection opens generic home | Cold or warm launch resolves `doc-042` and opens its details; any access requirement is visible there |
| Interest in paid content | Advertisement launches checkout | Viewer first sees the selected film’s details; only an explicit subsequent access action may begin acquisition |
| Account A signs out | Previous account’s private history remains visible | Invalidate A’s generation and payload, publish public recommendations or neutral art, reject A’s delayed callbacks |
| Network unavailable after sign-out | No supplied evidence | Never reuse A’s personalized cache; use valid public content or neutral static art |

## Acceptance checks and evidence status

**Passed — specification inspection only:** this document defines the tvOS surface, content eligibility, account boundary, exact-item destination, silent behavior, asset states, static fallback, freshness policy, and failure transitions. Installed root, selected families, topic procedures, and supporting local guides were read; no web browsing was used.

**Failed — supplied baseline description:** unrelated ads leading to checkout conflict with useful content discovery; generic-home destinations fail exact-title linking; signed-out history fails the proposed account boundary. Loud autoplay fails this revision’s silent policy, but the supplied local guide does not establish a universal ban on preview sound. These are reported behaviors from `interface.md`, not reproduced runtime failures.

**Not executed — implementation acceptance gates:**

| Check | Required observable result |
| --- | --- |
| Full row and metadata | Eligible fixtures fill a screen-width row, context label is visible, IDs are unique, completed titles and ads are absent |
| Remote navigation | Every item is reachable with visible focus; focus never activates; deliberate Select opens the item; system exit and held Back work |
| Direct linking | Cold/warm activation of `doc-042` opens its details; sign-in retains ID; cancellation does not buy or play |
| Availability race | Expired rights, restricted region/profile, removed title and invalid ID produce the unavailable state with explicit catalog recovery |
| Silent presentation | Initial display, focus changes, idle time, and return to Home produce no app preview video or sound |
| Account isolation | Sign-out, A→B switch, unknown viewer, preference off, offline state and delayed A callback reveal no A history or personalized ranking |
| Freshness and errors | Expiry and failed fetch choose a current context-valid snapshot or fallback; obsolete generations cannot overwrite current content |
| Asset validation | Dimensions and both crops match the table; no essential subject is lost; focus enlargement and distant legibility are checked on TV |
| Fallback | Dynamic unavailability yields neutral static artwork, correct sizes, no focus targets or fake controls |
| System cache boundary | Real Home Screen evidence confirms old personalized content disappears across account transitions; otherwise release editorial-only mode |

## Evidence limits

Only a one-line interface description and installed local guidance were available. No app code, catalog, artwork, account implementation, tests, screenshots, SDK, or device results were supplied. No device, SDK compilation, GUI, playback, remote, accessibility, security, or privacy execution is claimed. The checks above are proposed gates, not test passes. Accessibility behavior remains unverified and requires a dedicated review before implementation acceptance.

The local guides identify themselves as derived snapshots dated 2026-10-25, not API documentation. Official links above identify the source guidance; they were not opened. Current API availability, system refresh timing, cache invalidation guarantees, supported target OS versions, actual rights rules, and content supply remain implementation questions. No source conflict was identified in the selected local passages. The specification deliberately uses logical states and routes without assuming an Apple SDK is installed.
