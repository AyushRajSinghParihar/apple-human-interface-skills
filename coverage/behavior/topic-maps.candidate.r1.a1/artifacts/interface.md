# Festival venue finder — revised iPhone specification

Platform: iOS. Retain the existing custom map stack, venue list, and manual search dataset. The task is to identify a festival venue and inspect its location without requiring personal location access. This is an interaction specification, not an implemented app.

## Data and state contract

- Use one stable venue ID across annotations, list rows, search results, and details. Required display data: venue name; use address and category only when supplied. Coordinates must be validated before rendering. Missing coordinates produce a searchable row with “Map location unavailable,” never a fabricated pin.
- Keep query, selected venue ID, list scroll position, and camera separately from authorization status. Permission changes must not clear venue data or search state.
- On first entry, fit all valid festival venue coordinates with surrounding street context. If there are none, open the venue list with “Venue map locations unavailable.” Restore the previous camera on return during the session.
- The map provider, framework, deployment target, festival boundary, and actual dataset schema are unspecified. Bind these contracts to the existing implementation; do not assume Apple map data, routing, live opening hours, indoor floors, or offline tile availability.

## Main surface and finding venues

1. Show an interactive map with labeled “Show Venues” and “Show Festival” actions outside the map gesture area. Preserve pan, pinch zoom, and rotation. “Show Festival” fits the valid festival venues and clears selection while retaining the query.
2. “Show Venues” opens the existing venue list as a full-screen navigation destination. Above its rows, place an inline search field with placeholder “Search festival venues.” It is initially unfocused. Search covers the whole supplied festival dataset, independent of camera region and location permission.
3. Match venue-name text using case-insensitive substring matching; trim query-edge whitespace. Add address matching only if addresses exist. Update rows as local text changes; sort by venue name with stable ID as tie-breaker. Empty query shows all venues. Suggested name completions can come from current matches; no query history is stored by this repair.
4. Each row displays the full venue name and supplied address/category beneath it. Row activation opens that exact venue's detail, including its map when coordinates exist. Back restores query and list position. A separate “Show on Map” action returns to the main map and selects the same ID. Disable that action with the visible reason above when coordinates are missing.
5. Zero matches shows “No venues match ‘[query]’” and “Clear Search.” Clearing restores all rows; Cancel ends editing, dismisses the keyboard, clears the query, and restores the all-venues list. Back to the map preserves the query. If the dataset is empty, show “No venues available” rather than an empty map presented as a successful result.

## Annotation identity and selection

- Replace unlabeled dots with coherent pin-shaped markers and venue-name labels. Use a category symbol only where category metadata exists; category or selection must never depend on color alone. The selected pin has a visible outline plus its full name and a selected semantic state.
- Cluster markers when their selectable regions would overlap. A cluster shows a count and accessible name such as “3 venues.” Activation fits its member coordinates. If co-located venues cannot separate at maximum zoom, open the venue list filtered to those IDs, with an explicit “All Venues” action that removes that restriction. Do not silently select an arbitrary member.
- Pin, list, and search selection call the same `selectVenue(ID)` transition. On the map, reveal inline nonmodal venue details below the map: name, supplied address/category, and “Close Details.” Keep the selected pin visible in the map above those details. Do not duplicate a second place card over these details.
- Selection must never recenter on the user's position, an unrelated default coordinate, or a geocoded name guess. If the selected pin already fits in the unobscured viewport, retain camera center, zoom, and bearing. Otherwise pan the minimum distance needed to reveal its stored coordinate with 24 pt clearance from controls and viewport edges; retain zoom and bearing. Apply this same policy to offscreen venues selected from the list. These clearance and camera policies are product decisions.
- Recompute the usable viewport after details or keyboard/layout changes. Details occupy layout space rather than covering the map. If space is insufficient, use the full-screen venue detail with its own map and a Back action; never hide the selected pin behind details. “Close Details” clears selection and leaves the current camera unchanged. A later user pan is respected; no continuous automatic recentering.

## Attribution and map presentation

- Restore the active provider's required attribution and functional legal links. For Apple-sourced maps, preserve the Apple logo and legal link, visible and stable relative to the map. Do not recreate, recolor, or replace provider marks with festival branding.
- Apply the local Maps guide's suggested 7 pt side and 10 pt vertical padding. This product keeps attribution on every displayed map; the guide permits omission below 200 × 100 px, but the repair must not shrink a map to exploit that exception. If a future movable card is introduced, keep attribution 10 pt above its lowest resting position and verify that it stays readable throughout movement.
- Attribution belongs to the map, not inside dismissible venue details. Keep it visible on main maps and maps inside venue detail, including with keyboard, safe-area changes, and large text. Controls and labels must not intercept its links.
- Retain ordinary map emphasis because this repair adds annotations rather than rich area overlays. Do not obscure road names or surrounding geographic context with opaque festival overlays. Give labels and controls a readable backing against changing geography.

## Location access and recovery

Opening the finder, browsing, searching, and selecting venues never requests location. Location is an optional one-shot “show my position” task, not a prerequisite for map data.

| State/event | Required result |
|---|---|
| Entry with unknown, denied, restricted, or disabled location | Render the festival region and all venue-finding actions. No automatic permission prompt. |
| Person invokes location | Prefer the system one-time location button where supported by the existing stack and deployment target. Preserve its allowed title/glyph styling and all localized text. Verify API availability before implementation. If unavailable, use a labeled “Show My Location” button with a foreground-only authorization request at activation. Never request background access. |
| System authorization needs purpose copy | “Your location is used to show your position on the festival map.” No custom pre-alert; no claims about nearby sorting or navigation. |
| Authorization granted and a usable fix arrives | Show the reported position and accuracy indication; center once for this explicit action. Keep festival pins and selected venue data. Stop acquiring after the fix; no follow mode. Approximate access is sufficient. |
| Denied/restricted/services disabled | Keep the festival camera, pins, search, and details. Show nonblocking “Your location is unavailable. You can still search festival venues.” Do not repeatedly request access or force a Settings detour. |
| Acquisition fails or times out after 10 seconds | Stop waiting, keep existing content, show “Couldn't find your location. You can still search venues.” Offer “Try Again” for a new explicit attempt. This timeout is a product choice. |
| Return after permission changes | Re-read status; retain query and selection. Obtain a fresh fix only on another explicit location action. |
| Basemap fails independently of permission | Show “Map unavailable” with “Retry Map” and “Show Venues.” Preserve the supplied venue list/search and exact venue details. Never label a tile/service failure as location denial. |

Data-purpose boundary: venue coordinates are supplied public venue data; user coordinates serve only the one-shot display. Keep the user fix in memory for that display/session, discard it when leaving the finder, and do not add analytics, query logging, server transfer, or background collection. Existing provider data flows and privacy disclosures require implementation review; this specification cannot certify them.

## Controls and access

- Prefer system buttons, search field, list rows, and navigation behavior within the existing framework. Main actions are ordinary nondestructive commands with visible press feedback; none commits an irreversible action. Only the intentional location action changes the camera to the user position.
- Give app action controls and selectable annotations at least 44 × 44 pt activation regions, with no overlapping targets. Cluster dense pins rather than shrinking targets. “Retry Map” retries only map loading; “Try Again” retries only location acquisition. Suppress duplicate attempts while each is pending and keep its initiating control visibly busy.
- Name every pin with its venue name and role; expose its selected state. Cluster names include their count. List rows and detail headings preserve the same identity. Provide the list as the complete alternative to visually locating or precisely tapping a pin; it supports the same venue details and map selection.
- Use semantic system headline text for venue names and body text for addresses, messages, and action labels (iOS body default 17 pt). Support Dynamic Type and Bold Text. At 200% text size and the largest supported accessibility sizes, grow rows and stack actions; allow full names/addresses to wrap. If map labels collide, cluster and retain full names in the list/details. Essential text and actions must remain reachable.
- Check light/dark appearances and Increase Contrast against actual rendered geography. Measure contrast before accepting styling; color alone must convey no essential identity or selection information. Exact colors and measured ratios are not supplied.

## Design basis

These links identify the official articles behind the installed local guidance; they were not fetched for this task. Camera rules, timeout, deterministic search, layout clearance, and data retention are product decisions applying that guidance.

- [Maps — Best practices and Custom information](https://developer.apple.com/design/human-interface-guidelines/maps#Best-practices): interactivity, selection, clustering, and attribution; [Place cards](https://developer.apple.com/design/human-interface-guidelines/maps#Displaying-place-cards-in-a-map): preserve selected-location context and include a map in outside-map place details.
- [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission) and [Location button](https://developer.apple.com/design/human-interface-guidelines/privacy#Location-button): contextual, minimal access and suitable one-time location use.
- [Search fields](https://developer.apple.com/design/human-interface-guidelines/search-fields#Search-as-an-inline-field), [Searching](https://developer.apple.com/design/human-interface-guidelines/searching#Best-practices), and [Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables#Best-practices): explicit scope, identifiable results, and coherent row selection.
- [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility), and [Typography](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type): action naming, comfortable activation regions, non-color distinctions, and scalable text.
