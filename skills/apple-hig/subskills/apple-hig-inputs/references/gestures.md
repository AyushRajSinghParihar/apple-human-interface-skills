# Gestures

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/gestures) · Retrieved 2026-11-09.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Basic tap, swipe, and drag concepts work across touchscreens, air gestures, and input-device surfaces even though physical movements differ.

<a id="Best-practices"></a>
## Best practices
Offer alternatives through voice, keyboard, Switch Control, or visible controls. Preserve standard gesture meanings rather than repurposing tap/swipe for unexpected actions. Give immediate, predictive manipulation feedback, including movement extent and unavailable/locked states.

<a id="Custom-gestures"></a>
## Custom gestures
Add custom gestures only for frequent specialized tasks unsupported by standard ones. Make them discoverable, simple, distinct, and supplementary to another way to perform important actions. Explain them through simple words/graphics and test in real use; hard-to-explain gestures often need redesign. Keep standard navigation such as Back alongside shortcuts. Avoid system-edge/overlay gesture conflicts; specialized immersive/game contexts may defer system behavior using supported APIs.

<a id="Platform-considerations"></a>
## Platform considerations
<a id="iOS-iPadOS"></a>
### iOS, iPadOS
Three-finger swipe left/right invokes undo/redo; three-finger pinch inward/outward copies/pastes selected text. Four-finger swipe switches iPad apps. Shake supports undo/redo. Simultaneous recognition can support games with concurrent movement/fire controls; integrate Pencil according to its specific guidance.

<a id="macOS"></a>
### macOS
Keyboard and pointing device are primary. Standard gestures also work on Magic Trackpad, Magic Mouse, and game controllers with a touch surface. On a Mac with a touch display, or an iPad connected through Sidecar, direct touch is a secondary input mode.

- Keep the layout and size of interface elements unchanged when you support touch. People switch inputs often, so the interface must stay stable and predictable.
- Enlarge tap targets, not controls, so that a touch that starts slightly outside the visible bounds still hits. Standard controls get a suitable tap target automatically.
- Consider expandable controls for small or densely packed controls: a temporary touch-sized variant appears on tap, stays easy to see and operate while held, and remains briefly after the finger lifts. Standard steppers, sliders, and dials do this automatically.
- Never make touch the only route to a control or feature; every function needs keyboard and pointer access. Conversely, give touch equivalents for pointer-only actions such as modifier-drag (Shift-drag) or menus that appear on hover (see [Pointing devices](pointing-devices.md#macOS)).
- Preserve gestures people already know from your iPhone or iPad app, or from a trackpad or Magic Mouse, and test that they do not conflict with macOS system gestures.
- Make custom gestures work for both direct touch and the trackpad, adding modifier keys where needed.

<a id="tvOS"></a>
### tvOS
Preserve standard remote/Siri Remote/controller touch-surface gestures for navigation.

<a id="visionOS"></a>
### visionOS
Indirect input uses looking to target and a finger-thumb tap/hold/drag from rest; direct input physically touches nearby virtual objects. Prefer indirect UI interactions and reserve sustained direct work to avoid fatigue. Offer both where possible and alternatives to required posture/body movement.

Direct touch activates; touch-and-hold reveals context; touch-and-drag moves; double touch previews or selects a word; swipe reveals/dismisses/scrolls; two-hand pinch apart/together zooms, and a two-hand circular pinch movement rotates.

<a id="Designing-custom-gestures-in-visionOS"></a>
#### Designing custom gestures in visionOS
Custom hand gestures require Full Space and hand-data permission. Test ergonomics repeatedly. Avoid sustained raised arms, repeated strenuous movements, complex finger/two-hand requirements, and a prescribed left/right hand; provide simpler alternatives.

<a id="Working-with-system-overlays-in-visionOS"></a>
#### Working with system overlays in visionOS
Since visionOS 2, looking at the palm and hand gestures reveal Home/Control Center; the older look-up behavior remains an accessibility option. Reserve the immediate hand/wrist region for these overlays, positioning any necessary hand-anchored game content farther away. In Full Space, supported deferral can require a tap before revealing Home, useful for virtual gloves/hands. Apps built for visionOS 1 defer by default. Rolling the hand/wrist/forearm conflicts with reserved overlays, which the app cannot detect and which appear above its content; test carefully.

<a id="watchOS"></a>
### watchOS
<a id="Double-tap"></a>
#### Double tap
Since watchOS 11, double tap scrolls lists/views and advances vertical tabs. Do not assign a primary control that conflicts in those containers. On a non-scrolling view, designate the most frequent button/toggle, such as play/pause; the system highlights then acts. Widgets/Live Activities in Smart Stack can expose a primary action. Notifications use their first nondestructive custom action.

<a id="Specifications"></a>
## Specifications
<a id="Standard-gestures"></a>
### Standard gestures
Tap activates or selects, swipe reveals actions, dismisses, or scrolls, drag moves UI, and touch (or pinch) and hold reveals extra functions on all six platforms. Double tap zooms or toggles zoom on all six, opens an item on a Mac with a touch display, and performs the primary action on Apple Watch Series 9 and later and Apple Watch Ultra 2 and later. Zoom and rotate are listed for all except watchOS. See [Pointing devices](pointing-devices.md), Remotes, and Game controls for device-specific input.

<a id="macOS-trackpad-and-touch-display-gestures"></a>
### macOS trackpad and touch display gestures
Standard gestures perform these common actions on both a trackpad and a Mac with a touch display:

|Action|Trackpad|Touch display|
|---|---|---|
|Select|Primary click|Tap|
|Open|Double click|Double tap|
|Scroll|Slide two fingers up or down|Slide one finger up or down|
|Zoom|Pinch|Pinch|
|Rotate|Move two fingers around each other|Move two fingers around each other|
|Open a context menu|Secondary click|Touch and hold|
|Drag|Click and drag|Touch and hold, then drag|

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/gestures) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Videos"></a>
#### Videos
Apple’s linked design sessions provide demonstrations and additional implementation context; no video review is implied here.

<a id="Change-log"></a>
## Change log
Source revision dates: October 28, 2026, September 9, 2024, September 15, 2023, June 21, 2023.
