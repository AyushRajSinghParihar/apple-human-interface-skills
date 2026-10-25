# Gallery adaptation: Apple TV and Vision Pro

Design specification based on `interface.md` and the installed local HIG snapshot. No web lookup or executable app was used. The supplied brief describes 20 objects with details, gaze-triggered opening, pinpoint TV cursor input, lost return focus, and required raised-arm interaction. Those are brief-level findings, not observed runtime failures.

## Shared task and state

Browse the same ordered 20 objects, explicitly open one object's details, then return to the same place. Assume a read-only visual gallery; “select” means open details, not multi-select, purchase, or save. No evidence establishes 3D assets or a need for immersion.

Maintain stable object IDs and `route = gallery | detail(id)`, plus a return record containing object ID, displayed order, and scroll anchor/offset. Capture it immediately before activation. Hover/focus changes never open details or change persistent selection. Detail identity follows the activated ID, not a recycled cell index. Returning restores the recorded gallery location; do not reset to object 1. This restoration policy is a product decision consistent with preserving collection identity.

Use a familiar image-and-title grid with each image/title pair forming one action. Keep order stable throughout the browse/detail/return cycle. Allow label wrapping and fewer columns when necessary rather than hiding titles. [Collections, Best practices](https://developer.apple.com/design/human-interface-guidelines/collections#Best-practices).

## Contract 1 — Apple TV / tvOS

**Surface:** Full-screen gallery and a hierarchical detail screen. Initial layout proposal: four columns, five rows, vertically scrolling as needed. Large recognizable images and readable titles take priority over displaying all 20 at once. Validate legibility at 8 feet or farther; this column count is a design starting point, not an Apple requirement. Use system focus effects with clearance for enlarged artwork. [Designing for tvOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos#Best-practices).

| State/event | Required behavior |
|---|---|
| First gallery entry | Focus object 1 visibly. All 20 remain directionally reachable. |
| Left/right | Move one card in the same row; stop at the row edge without wrapping. |
| Up/down | Move one row in the same column; scroll the destination into view. Stop at first/last row. |
| Swipe on Siri Remote | Use standard directional focus/scroll behavior with visible feedback and system momentum. No free cursor or precision aiming. |
| Focus arrives | System raised/highlighted appearance identifies the target; route stays gallery. |
| Select press | Immediate pressed feedback; capture return record; open details for the focused ID exactly once. Incidental movement does not activate. |
| Detail entry | Title and content identify that ID. Initial focus is a visible “Back to Gallery” control; any scrollable detail content and other controls have directional routes to and from it. |
| Remote Back or Back to Gallery | Return to gallery, restore scroll position, then visibly focus the originating card after layout completes. |
| Back at gallery root / holding Back | Preserve system Home behavior. Do not trap navigation. |

Focus map: `card(row,column) ↔ adjacent cards`; `Select → detail → Back → same card`. Unfocused, focused, pressed, and unavailable appearances are distinct. Opening details is transient navigation, not a persistent selected badge. If persistent selection is added later, represent it independently of focus. Reserve surrounding space so enlargement never obscures neighboring titles. [Focus and selection, tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS), [Remotes](https://developer.apple.com/design/human-interface-guidelines/remotes#Buttons).

If the originating item is removed, restore to the nearest surviving item in the captured order and show that item in view; an empty gallery shows an explicit empty state. This return fallback is a product policy. During live discrete directional navigation, a disappearing focused item moves to a nearby one-step target, following the focus guidance. No spontaneous focus jumps occur for unrelated data updates.

## Contract 2 — Apple Vision Pro / visionOS

**Surface:** One movable, resizable standard glass window in Shared Space. Gallery and details reuse that window and its placement. Ordinary browsing and reading do not justify Full Space; no volume is specified without evidence that multi-angle 3D inspection benefits the task. Preserve system move/resize/close controls and dynamic scaling. Window content is anchored in space, never rigidly to the head. [Designing for visionOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos#Best-practices), [Windows, visionOS](https://developer.apple.com/design/human-interface-guidelines/windows#visionOS).

Start with a four-column scrollable grid; reduce columns on narrowing/enlarging text while retaining object identity and scroll anchor. Each whole image/title card is one stable containing hover and activation region. Use standard hover effects, not a simulated TV focus cursor. Design regular buttons with a 60 × 60 pt default activation area, at least 60 pt center spacing and 16 pt gaps; cards are larger and their hover effects must not collide. These are visionOS values, not TV dimensions. [Eyes](https://developer.apple.com/design/human-interface-guidelines/eyes#Encouraging-interaction), [Spatial layout](https://developer.apple.com/design/human-interface-guidelines/spatial-layout#Best-practices), [Accessibility, Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility).

| State/event | Required behavior |
|---|---|
| Gallery entry | Show gallery at the saved location. Do not assign a synthetic gaze-focus ID. |
| Look at a card | System supplies subtle hover feedback only. Image/title and target bounds stay stable; no navigation, viewed flag, selection mutation, or dwell timer in app logic. |
| Look + finger/thumb tap | Deliberate indirect activation opens that ID's details and captures the return record. Works with either hand resting in lap or at the side within tracking conditions. |
| Indirect drag in scroll container | Standard scrolling, with immediate content feedback; dragging must not open a passing card. |
| Detail | Replace gallery content in the same window; expose a labeled “Back to Gallery” action near the detail heading. Keep reading and controls near a coherent depth plane. |
| Activate Back to Gallery | Restore gallery and originating card's scroll anchor. The card is visible; subsequent hover follows the person's actual targeting. Do not force gaze or synthesize hover. |
| Resize while in details | On return, resolve the originating ID into the new grid layout and reveal it; exact pixel offset is secondary to identity. |
| Close window | Use system close behavior. Retain the route and return record for reopening this gallery session; reopening restores the same object/context without spawning duplicate detail windows. |

Gaze before activation is private and unavailable to app business logic. Connected keyboard/controller focus is a separate input state; when used, provide visible focus, deliberate activation, and return focus to the originating card. Gaze hover does not drive that focus state. [Eyes](https://developer.apple.com/design/human-interface-guidelines/eyes#Custom-hover-effects), [Focus and selection, visionOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#visionOS).

All essential actions use standard controls that can be targeted and activated through supported assistive input, including hand/head Pointer Control and Switch Control. No action requires speech, custom hand tracking, two hands, reaching overhead, walking, or repeated direct touch. Direct touch may supplement nearby brief interactions; it is never required for this task. Preserve system palm/wrist overlays and recentering. Sustain reading normally at least 1 m away while allowing system placement and user repositioning; do not enforce a head-locked viewing distance. [Gestures, visionOS](https://developer.apple.com/design/human-interface-guidelines/gestures#visionOS), [Eyes, Best practices](https://developer.apple.com/design/human-interface-guidelines/eyes#Best-practices), [Accessibility, visionOS](https://developer.apple.com/design/human-interface-guidelines/accessibility#visionOS).

If an object disappears during detail, show its unavailability with Back still available. On return reveal the nearest surviving item by captured order, without inventing a gaze target; if empty, show the empty state.

## Acceptance checks and evidence status

**Passed — document inspection only:** Both contracts preserve the same 20-object browse/open/return task; separate targeting from activation; specify return identity/location; replace the brief's pinpoint TV cursor, gaze auto-opening, and mandatory raised-arm actions. Platform and component procedures were read before their supporting source guides. These passes establish specification coverage only.

**Failed — supplied proposal against this contract:** Gaze-triggered detail opening conflates hover with activation; pinpoint TV cursor movement replaces ordinary directional navigation; disappearing return focus loses TV location; mandatory raised-arm actions prevent resting interaction. These failures are reported from the brief, not device execution.

**Not executed — implementation acceptance:**

| Check | Pass condition / required evidence |
|---|---|
| TV traversal | On Apple TV with Siri Remote, reach and exit every card and detail control using directions; edge presses do not wrap unexpectedly; no focus trap. |
| TV activation | Browse across all 20 without opening details; one deliberate Select opens the correct ID once. Check both directional clicks and swipes. |
| TV return | Open objects 1, 8, and 20; Back restores the correct card visibly and its scroll position. Root Back and held Back retain system behavior. |
| TV visual states | At 8 feet or farther, read titles and distinguish focused/pressed/unavailable states; enlarged edge cards and neighbors remain unclipped. |
| Vision targeting | On worn Vision Pro, look across all 20 with no route/data mutation; deliberate tap opens only the intended object. Neighbor hover regions do not collide. |
| Vision resting flow | Seated and standing, with hands in lap/at sides, browse, scroll, open, read, and return without sustained reach, head turns, or body movement. Assess tracking, fatigue, and depth refocusing. |
| Vision return/lifecycle | Open object 20, resize/move window, return, close/reopen: same object/context remains identifiable; no duplicate windows or forced hover. |
| Identity changes | Remove the originating item while in detail, then return; nearest surviving item is revealed; empty collection remains understandable. Test odd counts and long titles. |
| Alternative input | Complete the same task using supported assistive navigation/activation and connected keyboard/controller where supported. Names identify object title and action, roles expose controls, and traversal follows displayed order. Verify on supported Apple systems. |
| Readability/preferences | At 200% text, retain titles, Back, and access to every object through reflow/scrolling. Measure actual contrast and activation geometry; verify accessibility preferences without losing state. |

## Missing evidence and boundaries

Only the textual brief and installed guidance were available. Missing: gallery assets/titles and stable IDs; detail structure; implementation/framework and deployment versions; rendered dimensions and target bounds; runtime state restoration; native focus/hover behavior; SDK/API availability and compilation; device recordings; worn comfort/hand tracking; accessibility semantics and assistive execution; measured contrast, text reflow, and across-room legibility. Column counts, navigation topology, and persistence policies above are concrete design decisions awaiting implementation validation.

No device, simulator, SDK build, GUI, accessibility tool, or physical comfort testing was performed. Official links above identify the local snapshot's sources; they were not opened or independently verified online.

Audit route: installed `apple-hig/SKILL.md` → Getting started family → tvOS and visionOS procedures → platform references; topic-index search → Inputs family (Focus and selection, Remotes, Eyes, Gestures), Layout and organization (Collections), Presentation (Windows), Foundations (Spatial layout, Accessibility) → each selected topic procedure → its supporting reference. All paths were resolved beneath `.agents/skills/apple-hig/` and consumed with one file per shell command.
