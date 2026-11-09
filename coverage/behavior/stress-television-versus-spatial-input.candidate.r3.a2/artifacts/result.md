# Shared gallery: Apple TV and Vision Pro contracts

Design specification based on `interface.md` and the installed local apple-hig snapshot. No web access, implementation, SDK build, GUI, device, or accessibility execution was performed. Official links below identify the sources represented by the local guides; they were not fetched.

## Shared product contract

Preserve the same 20 objects, their supplied order, identity, and details. Assume “select” means deliberately open one object's details; no multi-select, save, playback, or 3D manipulation requirement is supplied. Object media and names remain unspecified. Browse → activate object → read detail → return to the same gallery location is the common task.

Use stable object IDs, never grid indices, for identity. Store `{route, detailID, returnID, orderedIDs, scrollAnchorID, anchorOffset}`. TV additionally stores its focused ID; Vision Pro does not store gaze or hover. Before opening detail, capture return state. Neither focus movement nor hover changes the route or commits selection. Detail ID changes only on deliberate activation. Prevent duplicate navigation while an activation is in progress.

Return restores the stored order and scroll anchor, with the originating card visible. A “Last opened” text/badge may identify the return item independently of transient focus/hover; it is app history, not a favorite or multi-selection. If data changes, resolve by ID. If the return item is removed, use the next surviving item in saved order, otherwise the preceding item; an empty gallery shows “No objects” and keeps parent navigation available. This fallback is an application decision, not a claim about automatic platform behavior. Never reorder the collection just because someone looks or moves focus. Familiar grids and space for feedback follow [Collections — Best practices](https://developer.apple.com/design/human-interface-guidelines/collections#Best-practices).

## Contract 1 — Apple TV / tvOS

**Surface:** A full-screen gallery, initially a four-column, five-row vertically scrolling grid. Four columns are a starting product choice, subject to television legibility checks. Each card is one focusable image-and-title action. Allow clearance for system focus enlargement; titles and neighboring cards must remain readable. Start with platform text styles (local guidance lists 29 pt default tvOS text) and controls at least the 66 × 66 pt default size; cards will be larger. Across-room readability takes priority over fitting all 20 items onscreen. [Designing for tvOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos#Best-practices), [Accessibility — Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility).

| State/input | Required transition and feedback |
| --- | --- |
| First gallery entry | Put visible system focus on the first available card. Restored entry uses the saved focused/return ID. |
| Directional clickpad input or swipe | Move focus predictably through rows and columns; scroll the focused row into view. Horizontal edges do not wrap. Up/down keeps the column where possible; at the first/last row, stay at the boundary. A smaller final row uses its nearest available column. |
| Focus on a card | System raised/highlighted focus treatment identifies location and available action. Do not open details. Unfocused, focused, pressed, last-opened, and unavailable appearances remain distinguishable. |
| Deliberate Select press | Show pressed feedback, capture gallery state, and open `Detail(id)`. Incidental surface contact does not open detail. |
| Detail entry | Show the object's title and content; give initial focus to a visible “Back to Gallery” action. Long detail has standard remote scrolling. Up from its scroll region returns to Back; down from Back enters scrollable content when present. |
| Back press in detail OR activate Back to Gallery | Return to the gallery parent, restore scroll and visible focus to `returnID`. Do not reset to object 1. |
| Back at gallery root | Allow normal system Home behavior. Holding Back keeps its system meaning. |

Every card and detail action must be reachable and escapable using the Siri Remote alone. There is no tiny mouse cursor or pinpoint target requirement. A future app-level navigation region must have an explicit directional entry/exit route before it is added. [Focus and selection — tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS) supports system effects, directional reachability, and distinct states. [Remotes — Best practices, Gestures, Buttons](https://developer.apple.com/design/human-interface-guidelines/remotes) supports deliberate presses, swipe navigation, and hierarchical Back.

## Contract 2 — Apple Vision Pro / visionOS

**Surface:** One movable, dynamically scaled standard window in Shared Space. Gallery and detail replace the content within that window, retaining its placement. Use a familiar adaptive grid, initially three columns with vertical scrolling. On narrower windows or enlarged text, reduce columns while preserving item identity and scroll anchor. Ordinary browse/read work has no demonstrated need for a volume or Full Space; “objects” alone does not establish 3D assets. A future 3D inspection feature needs a separate contract. [Designing for visionOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos#Best-practices).

| State/input | Required transition and feedback |
| --- | --- |
| Gallery entry | Show the saved gallery location. Do not invent an initial gaze target or force the eyes toward a card. |
| Look at card | System hover provides subtle targeting feedback over one containing image-and-label region. Keep the main visual and hit area stable. Looking alone does not open detail, mark viewed, change selection, scroll, or generate app gaze analytics. |
| Look + indirect finger-thumb tap | Deliberately activate the card, capture return state, and open `Detail(id)`. Activation works with either hand resting in the lap or at the side within tracking conditions. |
| Browse beyond visible cards | Standard indirect pinch-and-drag scrolls the gallery with immediate content feedback. Also expose labeled Previous/Next row controls when overflow exists, using standard activation for an alternative to dragging. Disable them visibly at boundaries. |
| Detail | Title, object content, and persistent “Back to Gallery” action occupy the same window. Standard scrolling handles long content; it does not require direct reaching. |
| Activate Back to Gallery | Restore the card and its scroll position; show “Last opened” on it. Hover follows the system's current targeting, with no forced hover or synthetic gaze restoration. |
| Keyboard/controller or assistive input | Provide ordinary focus/navigation and explicit activation of cards, scroll controls, and Back. Connected-device focus is separate from eye hover. Assistive activation reaches the same state transitions. |

Use standard controls and hover wherever possible. VisionOS controls start at the local guide's 60 × 60 pt default. Regular buttons have at least 60 pt center spacing and 16 pt gaps; card target regions and hover effects must not overlap. Maintain readable labels rather than shrinking targets to retain columns. [Eyes — Making items easy to see and Custom hover effects](https://developer.apple.com/design/human-interface-guidelines/eyes) distinguishes private system hover from app events; [Focus and selection — visionOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#visionOS) distinguishes connected-device focus.

Let the system place the window initially and let people reposition it; anchor it to space, never rigidly to the head. Use dynamic scaling, coherent reading depth, no unnecessary floating text, and no forced head turns or body movement. Sustained reading should normally be at least 1 m away according to the local Eyes guide; this is comfort guidance, not an app-enforced fixed distance. Preserve system recentering and hand/wrist overlays. All required actions use indirect input from rest; optional brief direct touch must never become necessary. No custom hand tracking or gesture permission is required by this design. [Spatial layout](https://developer.apple.com/design/human-interface-guidelines/spatial-layout), [Eyes — Best practices](https://developer.apple.com/design/human-interface-guidelines/eyes#Best-practices), [Gestures — visionOS](https://developer.apple.com/design/human-interface-guidelines/gestures#visionOS).

## Acceptance checks and evidence status

**Passed — specification inspection only:** Both contracts preserve the 20-object browse/select/return task; TV uses directional focus plus deliberate Select; Vision Pro separates hover from activation and supports resting hands; both define identity-based return restoration. These are properties of this document, not demonstrated runtime behavior.

**Failed — supplied proposal against the design contract:** `interface.md` explicitly proposes auto-opening on look, equating gaze with remote/keyboard focus, pinpoint TV cursor movement, lost return focus, and raised arms for every Vision Pro action. Those specified behaviors conflict with the routed guidance and are replaced above. No running product defect was observed.

**Not executed — required implementation acceptance:**

| Check | Pass condition / evidence needed |
| --- | --- |
| TV traversal | From first card, reach all 20 by remote, scroll through boundaries, reverse direction, and exit each region. No invisible focus or traps. Record hardware traversal. |
| TV activation/return | Focus objects 1, 10, and 20 without opening them; Select each, then return through both Back paths. Origin is visible and focused, with scroll preserved. Test repeat entry and rapid presses. |
| TV rendering | Inspect across-room titles, long labels, focused corner cards, enlargement clearance, pressed feedback, and detail scrolling on an actual television. |
| Vision hover/activation | On worn Vision Pro, look across all cards without route or stored-state changes; tap deliberately to open exactly one detail. System hover remains distinct from keyboard focus. Review implementation for absence of pre-tap gaze assumptions. |
| Vision rest and comfort | Complete browse, scrolling, select, read, and return seated and standing with either hand at rest. No compulsory raised arms, reach, repeated turns, or depth refocusing. Record targeting and posture findings. |
| Restoration and data change | Return after window resize/reflow and after deleting the origin. Correct ID, anchor, fallback, and empty-state behavior remain coherent. Test a 19-item fixture and long labels without changing the production 20-object requirement. |
| Alternative access | Complete the same task with VoiceOver and supported switch/keyboard navigation; on Vision Pro also verify Pointer Control and Zoom. Each card exposes its object name and action role; Back and scroll controls have meaningful labels. No speech or gaze-only route is required. |
| Enlarged text and geometry | At 200% text, essential labels/actions remain available through reflow/scroll. Measure actual activation bounds, gaps, focus/hover overlap, and foreground/background contrast in supported appearances. |

Accessibility checks and standard-control decisions follow [Accessibility — Vision, Mobility, Speech, and visionOS](https://developer.apple.com/design/human-interface-guidelines/accessibility). They are pending, not accessibility conformance claims.

## Evidence still missing

Only a short behavioral brief was supplied. Missing: source implementation/framework and deployment versions; object assets, titles, detail lengths and loading behavior; screen/window dimensions and rendered layouts; stable-ID and restoration implementation; actual focus engine and system hover integration; SDK compilation; device recordings; measured geometry/contrast; assistive semantics and execution; television viewing-distance and worn Vision Pro comfort results. Native components are the design preference, but API availability is unverified. No runtime pass is inferred from this specification.

## Local routing audit

Read the installed root `.agents/skills/apple-hig/SKILL.md`, then the getting-started family and both platform topic procedures before their platform source guides. Searched `references/topic-index.md` for tvOS, visionOS, focus, eyes, gestures, and collections. Read the inputs and layout-and-organization families and procedures for Focus and selection, Remotes, Eyes, Gestures, and Collections before their source guides. Followed the spatial/alternative-input handoffs through the foundations family, Spatial layout and Accessibility procedures, then their guides. Each read/search used one local file per shell command. All paths resolved within this installed package; no external source verification or independent media review is claimed.
