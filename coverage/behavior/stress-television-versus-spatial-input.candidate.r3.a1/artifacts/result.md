# Shared gallery: Apple TV and Vision Pro contracts

Design specification based on `interface.md` and the installed apple-hig snapshot. No implementation, SDK, GUI, accessibility, or device execution was supplied or performed. Official links below identify the local guides’ sources; no web browsing was used.

## Shared product contract

The task remains browse 20 objects → deliberately choose one → read its detail → return to the same gallery location. Assume an ordered image-and-title gallery, one detail per object, and no editing, playback, authentication, or 3D inspection requirement. Actual titles, artwork, detail length, and framework are unknown.

Use stable object IDs, not cell indices. Store `orderedIDs`, `scrollAnchorID + offset`, `lastActivatedID`, and `route = gallery | detail(id)`. Keep platform targeting state separate from these shared values. Selection here means the deliberately opened object; it does not imply a favorite or multiselect feature.

On activation, save gallery position and the activated ID before changing route. Repeated activation while a transition is pending must not push duplicate details. Returning clears the detail route but retains lastActivatedID and gallery position. Merely navigating or looking never changes route, records an object as viewed, or commits selection. Keep ordering stable during this flow. If an object disappears, preserve remaining identities and explain unavailability; do not show another object's detail under the missing ID.

Use a familiar grid with one image-and-title action per object, rather than tiny independent controls. Reflow for longer titles and enlarged text; preserve ID and location when column count changes. These are product decisions consistent with [Collections — Best practices](https://developer.apple.com/design/human-interface-guidelines/collections#Best-practices).

## Contract 1: Apple TV / tvOS

**Presentation.** Use an across-room gallery with large recognizable artwork and legible titles. Initial design: five columns, four rows, vertically scrollable when necessary; reduce columns for large text instead of compressing labels. This count is a design starting point, not an Apple requirement. Reserve space for system focus enlargement without clipping adjacent artwork or titles. Prefer native focus-capable collection items and system focus effects. [Designing for tvOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos#Best-practices), [Focus and selection — tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS).

| State / action | Required transition and feedback |
|---|---|
| First gallery entry | Focus first available object; show an unmistakable system focus treatment. No detail opens. |
| Directional clickpad movement / swipe | Move focus through visible grid neighbors and scroll the destination into view. Left/right move within the row; up/down use the nearest column in the adjacent row. No wrap at boundaries. For an incomplete last row, use its nearest available column. No mouse cursor or pinpoint aiming. |
| Focus object | Raised/highlighted appearance identifies the target. Focus movement does not change lastActivatedID or route. |
| Select press | Immediate pressed feedback; save ID and position, then open that object's detail. |
| Detail entry | Title, image, and text identify the chosen object. Initial focus is a visible “Back to Gallery” action; a standard focusable text scroller, when needed, is reachable below it and has a directional exit back to the action. |
| Back button or Back to Gallery | Return to parent gallery, restore scroll position, reveal and focus lastActivatedID. Restoration is tied to the user's return action. |
| Back at gallery root / hold Back | Preserve system Home behavior. Do not create a gallery loop or override the hold. |
| Focused object removed during directional browsing | Choose a nearby one-step remaining target; if none remain, expose a readable empty state. |
| Opened object removed before return | Restore saved neighborhood; focus next surviving object in saved order, otherwise previous. Announce/explain that the original is unavailable. This fallback is a product decision for explicit return, not arbitrary focus movement. |

All interactive controls must be directionally reachable and escapable. Detail route is not a persistent “selected” highlight on every focus move. If a last-opened badge is displayed, label it “Last opened” and keep it distinct from focused and pressed appearances. Unavailable cells are inactive and excluded from focus. Preserve [remote press, swipe, and Back meanings](https://developer.apple.com/design/human-interface-guidelines/remotes#Best-practices). Play/Pause receives no unrelated gallery action; no media behavior is specified.

## Contract 2: Vision Pro / visionOS

**Presentation.** Browse and read detail within one movable standard Shared Space window. Replace the window's gallery content with detail and an explicit “Back to Gallery” control; retain the window's placement. A volume or Full Space adds no demonstrated value for the supplied task, so neither is part of this design. Let the system position and dynamically scale the window. Do not head-lock it. [Designing for visionOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos#Best-practices).

Use a responsive grid, initially four columns with vertical scrolling; reduce columns as usable width or text sizing requires. Do not spread 20 objects around the person's body. Treat image and title as one stable rounded target and one containing hover region. Start controls at the local accessibility guide's visionOS default of 60 × 60 pt, with larger gallery cards as content needs. Space targets using the Eyes guide's at least 16 pt margin around bounds or at least 60 pt between centers; inspect actual geometry before declaring compliance. [Eyes — Making items easy to see](https://developer.apple.com/design/human-interface-guidelines/eyes#Making-items-easy-to-see), [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility).

| State / action | Required transition and feedback |
|---|---|
| Gallery entry | Restore saved position, or start at first row. Do not programmatically assign gaze to an object. |
| Look toward a card | System-owned subtle hover feedback on the containing image/title region. Keep artwork and target bounds stable; no automatic expansion into neighbors. No route, stored state, or business logic change. |
| Finger-thumb tap with target indicated | Activate using standard indirect interaction with hands in lap or at sides; save object ID and position, then open detail. Either hand works. |
| Browse beyond visible cards | Standard indirect scroll gesture moves the gallery; visible Previous/Next row controls also provide a simple activation route, clamped at ends. Scrolling never opens detail. |
| Detail | Title and detail remain in the window; use standard scrolling for long content. Provide visible Back to Gallery, plus Previous/Next section scrolling actions if text exceeds the viewport. No raised-arm gesture is required. |
| Activate Back to Gallery | Restore the same object into view at the saved position. An optional stable “Last opened” label identifies context without pretending to restore gaze. |
| Keyboard/controller focus | Maintain its genuine component-focus state independently from eye hover. Explicit activation opens detail; return restores that input's prior object focus where available. |
| Object removed / layout resized | Preserve IDs and scroll neighborhood; indicate unavailable detail and retain Back. On return show next surviving neighbor, otherwise previous or empty state. Do not synthesize a gaze target. |

The app receives deliberate activation, not pre-tap gaze coordinates or hover callbacks for navigation. Define hover appearances declaratively through standard system behavior. Looking alone never opens detail. [Eyes — Custom hover effects](https://developer.apple.com/design/human-interface-guidelines/eyes#Custom-hover-effects), [Focus and selection — visionOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#visionOS).

Direct touch may supplement nearby interactions but cannot be required for browse, select, scroll, or return. No custom hand recognition, hand-data permission, two-hand gesture, prescribed handedness, wrist UI, or body movement is needed. Keep system overlays available. [Gestures — visionOS](https://developer.apple.com/design/human-interface-guidelines/gestures#visionOS).

## Accessibility and state decisions

Expose each card as one named action, “Open [object title]”; provide meaningful artwork descriptions where the image adds information. Back and scrolling controls have names, roles, enabled states, and visible labels. Preserve logical object order and access to all 20 items through supported assistive navigation. Vision Pro alternatives must cover hand/head Pointer Control, Switch Control, and VoiceOver; ordinary gaze is not the only route. Use platform components as the starting point, then verify their actual behavior.

Support at least 200% text enlargement with reflow and scrolling; no essential title or Back action may disappear. Starting body text follows local defaults of 29 pt on tvOS and 17 pt on visionOS, subject to real layout validation. Do not communicate target or last-opened state by color alone. Honor Reduce Motion with reduced scaling/parallax and transitions that retain clear target/state information. Measure contrast in actual appearances and Increase Contrast; no contrast measurement is available here. [Accessibility — Vision, Mobility, Cognitive, visionOS](https://developer.apple.com/design/human-interface-guidelines/accessibility).

## Acceptance checks and evidence status

**Passed — specification inspection only:** both contracts cover browse, explicit activation, detail, and return; the TV contract replaces pinpoint cursor input with directional navigation; the Vision Pro contract separates hover from focus and removes look-to-open and raised-arm requirements; stable-ID restoration and missing-item fallback are specified. These passes establish completeness of this document, not working behavior.

**Failed — supplied proposal at design level:** `interface.md` explicitly proposes look-to-open, treats gaze hover as remote keyboard focus, requires pinpoint TV cursor movement, loses focus on return, and requires raised arms for every Vision Pro action. Each conflicts with the task/input contracts above. No runtime failure was observed.

**Not executed — implementation acceptance gates:**

| Check | Observable pass condition | Evidence still needed |
|---|---|---|
| TV reachability | Traverse all 20 cards and every detail control by remote; enter/exit each region; boundary directions do not strand focus. | Implemented focus graph and Siri Remote hardware traversal. |
| TV activation and restoration | Focus/swipe never opens detail; Select opens correct ID; Back from object 17 restores its position and visible focus; root Back reaches Home. | tvOS build and recorded device scenarios. |
| TV visual states | Focus, pressed, last-opened, and unavailable states differ; enlarged edge cells do not clip; titles are legible across the room. | Actual artwork/layout and TV viewing from representative distance, including 8 feet or farther. |
| Vision hover privacy | Looking across all cards causes no navigation, viewed-state write, or application gaze tracking; only explicit activation opens detail. | Implementation inspection and supported execution; system hover behavior observed on device. |
| Vision resting interaction | Browse all 20, open object 17, scroll detail, and return with hands resting; repeat with either hand and varied seated/standing postures. | Worn Vision Pro testing for targeting, responsiveness, fatigue, comfort, and distraction. |
| Return under changes | Resize/reflow, remove opened/focused item, and test an odd count of 19 plus empty data; preserve identity and use stated fallback. | State tests and native layout execution. |
| Alternative input | Complete the same browse/select/return task using supported keyboard/controller and assistive methods; scroll actions and Back remain reachable. | Apple-platform assistive execution, including VoiceOver/Switch Control and visionOS Pointer Control/Zoom. |
| Content and preferences | Long titles/details, 200% text, Increase Contrast, and Reduce Motion retain content, actions, and understandable state. | Real content, measured geometry/contrast, accessibility inspection and preference testing. |

Only a brief and local instructions were available. Missing implementation/framework, target OS/SDK versions, real assets, screenshots, build evidence, hardware observations, and assistive test results prevent stronger claims. Current API availability and native rendering remain unverified. Local snapshots support these design choices; they do not establish current SDK feasibility or device performance.
