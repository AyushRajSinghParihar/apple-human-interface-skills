# Shared gallery: Apple TV and Apple Vision Pro contracts

Design specification based on `interface.md` and the installed apple-hig package. No implementation or runtime evidence was supplied. Official links below identify the articles behind the local snapshots; no web access was used.

## Shared behavior and decisions

The task remains: browse 20 objects, deliberately select one to read its details, then return to the same place. “Select” means open details; no multiselect, saved choice, authentication, collaboration, or 3D inspection is implied. Assume image-led cards with titles and ordinary text/image details. A shared gallery means a shared dataset, not a multiuser session.

Keep stable object IDs and ordering. Store `route`, `detailObjectID`, and a browse bookmark containing the originating object ID, its ordinal, and scroll anchor/offset before opening details. TV additionally stores its focused object ID. Hover is never stored as selection. Returning clears the detail route but retains the browse bookmark. No auto-opening, auto-advancing, or timed dismissal.

Use familiar grids with one activation target containing each image and title. Keep the card identity and label stable during focus/hover feedback. Do not reorder during browsing. Missing artwork retains a labeled card. These are product decisions supported by [Collections — Best practices](https://developer.apple.com/design/human-interface-guidelines/collections#Best-practices).

The brief's current idea would open details without deliberate activation, require TV precision pointing, lose TV focus on return, and require raised arms on Vision Pro. The contracts below replace those behaviors. These are findings about the supplied idea, not observed device defects.

## Contract 1 — Apple TV / tvOS

**Presentation.** A full-screen Gallery with a proposed four-column, five-row grid in stable reading order, scrolling vertically as needed. Do not shrink all 20 objects to fit one screen. Cards show recognizable imagery and readable titles; proposed baseline title size is 29 pt and activation bounds are at least 66 × 66 pt. These are tvOS defaults from the local accessibility guide, not a claim that these sizes alone establish distant readability. Long titles may wrap; enlarged text may reduce columns while preserving object identity and reading order. Reserve space for native focus enlargement at edges and between cards. Use the platform focus treatment and immediate pressed feedback. [Designing for tvOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos#Best-practices), [Accessibility — Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility).

**Input and state transitions.**

| State/event | Required result |
|---|---|
| First Gallery entry | First available object receives visible focus; details remain closed. |
| Directional clickpad input/swipe | Moves focus predictably through cards and scrolls the focused row into view; never opens details. |
| Select press on focused card | Save bookmark; give pressed feedback; open that object's Detail. |
| Detail entry | Show object title/content and a visible “Back to Gallery” action; initially focus that action. Detail content scrolls vertically where necessary. |
| Remote Back or activation of Back to Gallery | Navigate to parent Gallery; restore scroll and visible focus to originating ID in one restoration transaction. |
| Back at Gallery root | Allow standard Home behavior. Holding Back retains system behavior. |

Focus map for four columns: left/right move one card within the current row; up/down move one row in the same column. Do not wrap at edges. At a partial final row, down chooses the closest existing column; at the outer boundary retain visible focus. Swipes use platform directional navigation and scrolling rather than a mouse cursor. After reflow, apply the same rule to the current column count. All 20 cards are reachable and exitable by direction alone. In Detail, Up reaches Back to Gallery from the scrollable content and Down enters the content; Back works at every scroll position. Do not introduce invisible focus targets. [Focus and selection — tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS), [Remotes — Best practices and Buttons](https://developer.apple.com/design/human-interface-guidelines/remotes).

**Return and exceptional state.** Restore by ID, not the old cell index. If the originating object was removed, on this deliberate return focus the nearest surviving object at the old ordinal, preferring the following item and then the preceding one; scroll it into view. If none remain, show “No objects” and a focusable Back action. If a focused item disappears during directional browsing, choose a nearby one-step target. Do not steal focus for asynchronous refreshes. Focus, pressed feedback, and the currently opened detail ID are distinct; moving focus does not persist a selection. [Focus and selection — Best practices](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices).

## Contract 2 — Apple Vision Pro / visionOS

**Presentation.** Browse and Detail occupy one movable standard window in Shared Space. Ordinary gallery browsing does not need a volume or Full Space. Objects are not assumed to have 3D assets. The window is anchored in space, dynamically scaled by the platform, and user repositionable; it is never head-locked. Detail replaces the window's browse content without changing its spatial placement. Prefer a compact horizontal grid, initially three columns, with vertical scrolling rather than spreading 20 targets around the room. Reflow to fewer columns when needed; retain the browse anchor. Keep controls/content within comfortable central view, with no required walking or repeated turns. Sustained reading should normally be at least 1 m away; allow system placement and user adjustment rather than imposing a fixed distance. [Designing for visionOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos#Best-practices), [Spatial layout — Field of view and Scale](https://developer.apple.com/design/human-interface-guidelines/spatial-layout), [Eyes — Best practices](https://developer.apple.com/design/human-interface-guidelines/eyes#Best-practices).

**Target geometry.** Use standard card/button hover responses. Each image/title pair has one containing hover region and one action; no tiny nested hotspot is necessary. Keep a primary image stable and hover feedback contained. Proposed controls use at least 60 × 60 pt activation areas and 17 pt baseline text. Provide at least 16 pt clear separation between interactive bounds and at least 60 pt center spacing for regular buttons; prevent hover overlap. The Eyes guide offers margin or center-distance guidance; this design conservatively satisfies both where applicable. Do not transfer these visionOS point values to TV. [Eyes — Making items easy to see and Encouraging interaction](https://developer.apple.com/design/human-interface-guidelines/eyes), [Spatial layout — Best practices](https://developer.apple.com/design/human-interface-guidelines/spatial-layout#Best-practices), [Accessibility — Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility).

| State/event | Required result |
|---|---|
| Gallery entry | Show saved viewport or first row. No object is opened merely by looking. |
| Look at card | System supplies subtle hover feedback only. No app route, stored selection, viewed flag, or data request is driven by pre-activation gaze. |
| Look + indirect finger/thumb tap | Activate the card, store its browse bookmark and open Detail for its ID. |
| Browse/detail scrolling | Standard indirect pinch-and-drag scrolling works with hands resting in lap or at sides. Provide labeled Previous row/Next row controls for discrete browse scrolling, disabled at boundaries. |
| Activate “Back to Gallery” | Restore bookmarked viewport and object context; show a persistent “Last opened” text marker on that card until another object is opened. Do not force gaze or synthesize hover. |
| Connected keyboard/controller use | Treat actual navigation focus separately from gaze hover; restore originating focus when returning through that input mode. |

The app declares hover appearances; the system applies them without exposing pre-tap gaze to the app. There is no custom gaze dwell-to-open timer. User-enabled system Dwell Control remains an alternative activation path. Essential actions work through standard semantic controls with supported assistive activation, including hand/head Pointer Control and Switch Control. Direct touch can supplement nearby brief use, but never gates browse, open, scroll, or return. No custom hand tracking, raised-arm requirement, prescribed hand, or wrist gesture is needed. Preserve system overlays and recentering. [Eyes — Custom hover effects](https://developer.apple.com/design/human-interface-guidelines/eyes#Custom-hover-effects), [Gestures — visionOS](https://developer.apple.com/design/human-interface-guidelines/gestures#visionOS), [Accessibility — visionOS](https://developer.apple.com/design/human-interface-guidelines/accessibility#visionOS).

If the originating object is gone, restore the nearest surviving ordinal and show “Previously opened object is no longer available”; do not simulate a new gaze target or automatically open its replacement. Empty Gallery retains a labeled Back route. Detail lookup failure shows an explanatory message and Back to Gallery rather than a blank scene.

## Acceptance checks and evidence status

**Passed — specification inspection only:** Both contracts preserve the 20-object browse/open/return task, distinguish targeting from activation, specify stable return state, and replace each of the four problematic ideas in the supplied brief. The installed root, relevant family routes, platform procedures, input/collection/spatial/accessibility procedures, and their source guides were read in that order. These checks establish document coverage only.

**Failed — supplied concept against the proposed contracts:** Gaze automatically opens details; TV requires pinpoint pointing; return loses focus; Vision Pro requires raised arms for every action. No executable implementation was available to establish runtime failures.

**Not executed — required implementation acceptance:**

| Check | Pass condition |
|---|---|
| TV traversal and activation | With Siri Remote, reach all 20 cards in both directions, including edges; movement alone never opens details; Select opens the correct ID. No focus enlargement clips labels or neighbors. |
| TV return | Open object 17 after scrolling, then Back: same ID has visible focus and restored viewport. Repeat from scrolled Detail and after removal/reflow; fallback is deterministic and root Back retains system behavior. |
| Vision Pro targeting | Look across every card without activating: no detail opens or app state changes. Deliberate indirect tap opens only the targeted object. Verify no app dependence on private gaze data. |
| Vision Pro return | Open object 17, read/scroll, return: same window placement, same browse location and Last opened marker; no fabricated hover. |
| Resting use and comfort | Complete all 20 open/return cycles on a worn Vision Pro, seated and standing, hands resting, either hand; no required reach, large turn, or repeated depth refocusing. Validate target separation and reading comfort. |
| Alternative access | On supported Apple environments, complete browse/open/scroll/return with VoiceOver and applicable Switch Control/Pointer Control/Dwell Control. Card name identifies the object, role is an activation control, and detail headings/Back have meaningful semantics. |
| Adaptation and readability | Long titles, missing images, empty/odd counts, removed originating item, resized window, and 200% text preserve all content/actions. Measure actual contrast in relevant appearances and Increase Contrast; do not rely on color alone. TV is readable across the room, including at 8 feet or farther. |

Missing evidence: object assets/titles/detail lengths, actual layout geometry and contrast, implementation and framework/OS targets, SDK/API availability and compilation, focus-engine/restoration behavior, accessibility semantics/order, remote traversal recordings, and worn-device gaze/gesture/comfort results. No device, SDK, GUI, simulator, accessibility execution, or visual-media review was performed. Numerical values above are design inputs from local guidance, not measurements of a rendered interface.
