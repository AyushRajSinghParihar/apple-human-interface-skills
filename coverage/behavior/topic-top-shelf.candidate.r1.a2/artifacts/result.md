# Revised documentary Top Shelf interaction specification

## Scope and evidence

Design contract for the tvOS Home Screen Top Shelf of a documentary app. `interface.md` is the entire supplied product evidence: unrelated ads launch checkout, previews autoplay loudly, documentary selection opens generic home, and signed-out viewers see the previous account’s private history. These are reported behaviors, not independently reproduced defects. No catalog, assets, code, SDK, device, or live account was supplied.

Use a **dynamic full-screen image carousel with details**. Documentaries often need a short synopsis to support a choice; the simpler actions carousel is better suited to familiar content needing little explanation. This is a product judgment based on [Top Shelf — Carousel details and actions](https://developer.apple.com/design/human-interface-guidelines/top-shelf#Carousel-details).

## Decisions

1. **Feature documentaries, not advertisements.** Publish up to five distinct, currently available editorial selections, prioritizing new releases and rotating useful older titles. Each has a short title, release year, duration, one-sentence synopsis, and recognizable content imagery. No unrelated promotions, checkout destinations, prominent prices, account names, viewing timestamps, or progress badges. Prefer titles playable without a purchase where the catalog permits. Five is a product cap, not an Apple requirement. Apple advises fresh relevant content, avoiding ads and prominent prices, and linking directly to content. [Top Shelf — Best practices](https://developer.apple.com/design/human-interface-guidelines/top-shelf#Best-practices)
2. **Keep the shared Home Screen public.** Use the same public editorial feed for signed-in and signed-out viewers; do not export history, saved lists, personalized ranking, or resume positions into Top Shelf. Resume remains useful after an explicit playback action inside the app, using only the verified current profile. This deliberately conservative product policy addresses the reported leak; Apple’s general privacy guidance does not prescribe this exact feed architecture. Minimize the data needed for the feature and handle changing viewers deliberately. [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices), [Designing for tvOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos#Best-practices)
3. **Show still images only.** Supply no preview video or audio. Focusing, waiting, browsing, or highlighting the app must not start sound. Play explicitly requests the full documentary. This product choice removes the reported loud-preview behavior without assuming a mute preference or autoplay-control API exists. Image carousels are a supported design option in the local guide. [Top Shelf — Dynamic layouts](https://developer.apple.com/design/human-interface-guidelines/top-shelf#Dynamic-layouts)
4. **Use real content destinations.** Each carousel entry has Play and More Info actions associated with its stable documentary ID. More Info opens that documentary’s details. Play starts or resumes that documentary after validating the current viewer and access. Neither action opens generic home or directly initiates a purchase. [Top Shelf — Best practices](https://developer.apple.com/design/human-interface-guidelines/top-shelf#Best-practices)
5. **Use system-owned presentation and focus.** Keep identity near the top and synopsis concise; let the platform present and focus carousel actions. Do not paint buttons into artwork. Ordinary remote navigation must expose the current item and action clearly, with an exit back to Home Screen navigation. Exact carousel focus movement belongs to the eventual host implementation and must be verified on tvOS. Design for legibility across the room. [Top Shelf — Carousel details](https://developer.apple.com/design/human-interface-guidelines/top-shelf#Carousel-details), [Designing for tvOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos#Best-practices)

## Content, assets, and refresh contract

Each published entry contains:

```text
item = {
  contentID, title, year, duration, synopsis,
  publicArtworkVersion, publicAvailabilityExpiry,
  infoIntent: { action: "details", contentID },
  playIntent: { action: "play", contentID }
}
```

Intents are semantic contracts, not SDK identifiers or literal URL formats. Never put credentials, profile IDs, history, or resume offsets in public intents. Resolve the ID against the current catalog at launch. Editorial feed inputs are public metadata, release date, availability, supported locale, and approved artwork; authentication and purchase checks happen only inside the app. No new data collection or permission prompt is needed for this specification.

Prefer layered content imagery. Keep essential subjects and identity visible in focused and unfocused presentations; use carousel metadata for text rather than baking synopsis or controls into images. The installed guide does **not** supply carousel image dimensions or safe zones. Obtain the appropriate implementation template before asset export; do not substitute the guide’s row or banner dimensions. Focused/unfocused crops remain an acceptance dependency.

Refresh on catalog changes and availability expiry; attempt a refresh when the host requests content. As a product freshness limit, reuse a public cached feed only while its entries remain available and its age is under 24 hours. Remove expired, duplicate, or invalid entries before publishing. Do not reorder an active browsing session merely because a background fetch completed; stage routine replacements for the next presentation, subject to host capabilities. Unavailable content is revalidated on activation regardless of cache age.

If no valid dynamic entry remains, provide public static fallback art: **2320 × 720 pt**, **2320 × 720 px at 1×** or **4640 × 1440 px at 2×**. Use an app/documentary montage without private text, prices, painted controls, or “select to play” instructions. The fallback is **nonfocusable**; launching the app icon opens its ordinary landing screen. Account for the system’s flip/blur into a 1920-pixel-wide 16:9 context. These dimensions and behavior come from [Top Shelf — Best practices](https://developer.apple.com/design/human-interface-guidelines/top-shelf#Best-practices).

## Interaction and state contract

```text
onPublicFeedRequest:
  choose valid public editorial entries
  if none: publish noninteractive static fallback
  else: publish image carousel with per-item details and actions

onAccountChangeOrSignOut:
  invalidate pending profile-dependent requests and increment accountGeneration
  erase any legacy personal Top Shelf cache and request public replacement
  clear in-app previous-profile state before accepting another action
  ignore responses tagged with an older accountGeneration

onIntent(action, contentID):
  resolve public content by stable ID; prepare content-specific exit context
  if missing or no longer available:
    show named-content unavailable state with Back and Browse documentaries
    do not substitute another film or start checkout
  else if action == details:
    open that content's details without requiring sign-in for public metadata
  else if action == play:
    verify current app viewer; never infer the previous signed-in viewer
    if viewer is needed and unknown: ask for sign-in/profile selection in app
    preserve contentID + action through completion; cancellation returns to details
    if current viewer lacks access:
      open that documentary's details explaining access requirements
      any subscription/purchase is a separate deliberate in-app choice
    else:
      read only that viewer's current resume state
      start that documentary at saved position, or start at zero if none/completed
```

An account change during launch invalidates the old access/resume result and rechecks using the new generation. Signed-out playback never reads another viewer’s position. A public editorial title may coincidentally be a previously watched title: it has no “because you watched” or progress disclosure. Completed titles are not re-promoted as unfinished; the public feed cannot exclude watched titles without using private viewing data.

Play prepares the matching detail screen before playback starts, so an immediate playback exit has a coherent destination. Exit returns there with Play/Resume as appropriate. More Info and Play are distinct intents. Preserve ordinary player controls and original aspect ratio; prefer system player behavior when implemented. This applies the continuity pattern by product choice; the guide’s TV-app-specific entry requirements are not claimed as mandatory Top Shelf rules. [Playing video — Best practices and Exiting playback](https://developer.apple.com/design/human-interface-guidelines/playing-video#Exiting-playback)

## Worked before / after

Illustrative fixture, not a supplied catalog item: **The Living Reef**, ID `doc-reef`, 2026, 54 minutes, synopsis “Follow scientists restoring a damaged coral reef.” Current profile B has stopped at 18:20; previous profile A has unrelated private history.

| Trigger | Before, as reported | Revised result |
|---|---|---|
| Highlight app | Unrelated advertisement; loud preview | Public reef still, title, duration, synopsis; silence |
| Choose More Info | Documentary selection reaches generic home | Details for `doc-reef`, with its actual access state |
| Choose Play, B has access | No precise documentary destination | `doc-reef` resumes at B’s 18:20; immediate exit reaches reef details |
| Choose Play without access | Promotion launches checkout | Reef details explain access; checkout requires a separate explicit choice |
| Sign out A, then view shelf | A’s private history remains | Public editorial shelf only; no A metadata or progress |
| Sign out, then Play | Previous viewer may leak into flow | Verify viewer if needed; never resume from A; preserve reef intent through sign-in |
| Feed unavailable and cache expired | Not described | Honest noninteractive static art; no fake Play control |

## Acceptance checks and status

**Passed — document inspection only:** All four supplied problems have explicit replacement behavior above. The specification identifies layout, public content policy, fallback assets, precise intents, access recovery, resume ownership, and account-change races. Root skill, topic index, owning families, routed procedures, and supporting local guides were read; official links are references copied from those local guides, not browsed evidence.

**Failed — supplied baseline against this contract:** The reported ad-to-checkout flow, loud autoplay, generic destination, and previous-account history each fail the corresponding revised requirement. These are failures in the supplied description, not results of executing the app.

**Not executed — implementation acceptance:**

| Scenario | Required observable result |
|---|---|
| Signed out, signed in A, switch to B, sign out | Shelf contains only public editorial fields in every state; no prior-profile frames or cache data; delayed A response cannot republish |
| Inspect feed and cache | No account IDs, resume offsets, personalized recommendations, ads, prominent prices, or credentials |
| Focus every entry and action using remote | Identity/action remain clear, essential artwork survives crops, all actions and exits reachable; no focus-triggered playback |
| Leave highlighted for an extended period; browse adjacent entries | No preview sound or moving preview supplied; full playback starts only from Play |
| Cold/warm launch both actions for every ID | More Info reaches exact details; Play reaches exact film with verified viewer and correct resume position |
| Access missing, sign-in cancelled, viewer changes during launch | Named documentary context retained; no automatic checkout or previous-viewer progress |
| Title removed after publication | Named unavailable state, deliberate Browse/Back recovery, no silent substitution |
| Completed item, no resume, interrupted playback, immediate exit | Completed/no-resume starts at zero; interruption retains current viewer’s progress; exit context exists immediately |
| Offline with valid public cache; expired cache; empty feed | Valid public entries only, then static fallback at expiry; fallback has no focus or pretend actions |
| Focused/unfocused assets and television distance | Identity readable, subject uncropped; fallback dimensions verified; carousel template/export validation completed |

## Evidence limits

This is a framework-agnostic design artifact, not implemented software. No device, SDK compilation, GUI, Home Screen refresh, remote traversal, playback/audio routing, crop rendering, accessibility, or security execution occurred. Host refresh timing, old Home Screen snapshot eviction, carousel asset requirements, supported metadata limits, and viewer-change integration require implementation verification. Public-only publication prevents future personal shelf payloads; it cannot by itself prove immediate removal of previously cached system snapshots. Migration from the reported private feed must demonstrate cache replacement on actual tvOS before the privacy fix is accepted.

The local guidance is a dated 2026-10-25 snapshot and an independent synthesis, not an API reference or evidence of independent source review. No web access was used. Product choices such as five entries, still-only previews, public-only selection, and a 24-hour cache limit are explicitly proposed here rather than attributed to Apple requirements.
