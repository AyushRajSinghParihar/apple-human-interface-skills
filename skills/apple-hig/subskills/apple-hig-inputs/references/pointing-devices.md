# Pointing devices

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/pointing-devices) · Retrieved 2026-11-09.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

A pointer provides precision and complements keyboard input on Mac and touch/eye/hand input on iPad and Vision Pro. It adds a way to interact; it does not replace touch, eyes, or gestures. Preserve a coherent experience when people switch inputs.

<a id="Best-practices"></a>
## Best practices
Keep mouse/trackpad gestures consistent with their system meanings and user-customized mappings, such as Swipe between pages. Do not redefine systemwide gestures, even in games; people expect the Dock and Mission Control gestures everywhere. Keep one experience across gestures, eyes, pointer, and keyboard so people need not relearn interactions. Let pointer movement/hover reveal and hide minimized bars and playback controls. Keep modifier-plus-drag results consistent across touch and pointer, such as Option-drag duplication.

<a id="Platform-considerations"></a>
## Platform considerations
No additional iOS rules are given; tvOS/watchOS are marked unsupported.

<a id="iPadOS"></a>
### iPadOS
The pointer adapts to context and gives rich feedback, but it supplements touch rather than replacing it. Support click-drag rectangular multi-selection in custom views when needed; standard nonlist collection views provide it by default (`UIBandSelectionInteraction` for custom views). Distinguish pointer from finger only for a concrete benefit, such as precise click-to-seek alongside touch dragging.

<a id="Pointer-shape-and-content-effects"></a>
#### Pointer shape and content effects
The default pointer is an arrow; text-entry areas use an I-beam, and other regions can use system or custom shapes. Content effects change the element under the pointer:

- **Highlight** materializes a Liquid Glass shape between the pointer and the control, with subtle movement. Default for bar buttons, tab bars, segmented controls, and edit menus.
- **Lift** scales the element up with subtle parallax, a shadow below, and a soft specular highlight, so it seems to float. Default for standalone Liquid Glass controls, app icons, and Control Center buttons.
- **Hover** applies custom scale, tint, or shadow without transforming the default pointer shape.

<a id="Pointer-accessories"></a>
#### Pointer accessories
Small supplementary icons, such as resize arrows, can accompany any pointer to show how it can interact (`UIPointerAccessory`). Keep them simple and use accessory transitions to show changed state or behavior, such as `plus` becoming `circle.slash` when add becomes unavailable.

<a id="Standard-pointers-and-effects"></a>
#### Standard pointers and effects
Support the system content effects and match their intent: highlight for a group of controls inside a Liquid Glass container, lift for a standalone Liquid Glass control or a small element with an opaque background, and hover for large elements with customized scale, tint, and shadow. Preserve standard pointer appearances for buttons and text-entry areas. Pad interactive elements for comfortable hit regions: about 12 pt around elements with a bezel and about 24 pt around the visible edges of elements without one. Too small feels demanding; too large makes leaving the element effortful. Make adjacent custom bar-button hit regions contiguous so the highlight does not flicker between buttons.

<a id="Customizing-pointers"></a>
#### Customizing pointers
Use standard effects for custom elements that behave like standard ones; a custom toolbar without highlight can look broken. Apply effects consistently across equivalent surfaces, such as every drawing area. Avoid decorative effects. Keep custom shapes simple and instantly understandable. Useful annotations, such as graph coordinates or object dimensions, can help; instructional text attached to the pointer suggests unnecessary complexity. Reserve scaling for elements that can grow without crowding neighbors; tight rows can use tint alone. Do not use shadow without scale, because an unscaled element does not appear closer.

<a id="macOS"></a>
### macOS
Respect configurable clicks, secondary-click regions, and gesture combinations. Mouse and trackpad both support primary click, secondary click for context menus, scrolling, smart zoom, swiping between pages and between full-screen apps, and Mission Control (double-tap the mouse with two fingers, or swipe up on the trackpad with three or four fingers). Trackpad only: lookup and data detectors (force click or three-finger tap), tap to click, force click (click, then press firmly to show a Quick Look or lookup window, with variable pressure for pressure-sensitive controls such as variable-speed media controls), pinch to zoom, two-finger rotation, edge swipe for Notification Center, App Exposé (swipe down with three or four fingers), Apps (thumb-and-three-finger pinch), and Show Desktop (thumb-and-three-finger spread).

<a id="Pointers"></a>
#### Pointers
Use the standard pointer that communicates the element's interactive state or the result of a drag:

| Pointer | Meaning | APIs |
|---|---|---|
| Arrow | Select and interact with content and controls | AppKit `arrow`; SwiftUI `default` |
| Open hand / Closed hand | Content can be dragged within a view / is being dragged | AppKit `openHand`, `closedHand`; SwiftUI `grabIdle`, `grabActive` |
| Context menu | A context menu is available, usually shown only with Control pressed | AppKit `contextualMenu` |
| Cross | Precise rectangular selection | AppKit `crosshair`; SwiftUI `rectSelection` |
| Disappearing item | A dragged item disappears when dropped; an original it references is unaffected | AppKit `disappearingItem` |
| Drag copy | Option during a drag duplicates instead of moving | AppKit `dragCopy` |
| Drag link | Option-Command during a drag creates an alias; the original stays | AppKit `dragLink` |
| Horizontal / Vertical I-beam | Text selection and insertion in horizontal / vertical layout | AppKit `iBeam`, `iBeamCursorForVerticalLayout`; SwiftUI `horizontalText`, `verticalText` |
| Operation not allowed | The dragged item cannot drop here | AppKit `operationNotAllowed` |
| Pointing hand | The content is a link to a webpage, document, or other item | AppKit `pointingHand`; SwiftUI `link` |
| Resize up, down, up-down | A horizontal divider moves only up, only down, or either way | `rowResize`, `rowResize(directions:)` (AppKit and SwiftUI) |
| Resize left, right, left-right | A vertical divider moves only left, only right, or either way | `columnResize`, `columnResize(directions:)` (AppKit and SwiftUI) |
| Resize north, south, east, west, and the four corners, plus their two-way pairs | Resize a window or frame by an edge or corner; a one-way form allows movement in one direction only, for example when a minimum or maximum size is reached | `frameResize(position:directions:)` (AppKit and SwiftUI) |
| Zoom in / Zoom out | Magnify or reduce a canvas or object | AppKit and SwiftUI `zoomIn`, `zoomOut` |

<a id="Touch-support-for-hidden-controls"></a>
#### Touch support for hidden controls
Controls that appear only under the pointer need another way to appear on a Mac with a touch display. See [Gestures](gestures.md).

- Add touch support only for essential hidden controls. Skip static information such as tooltips, and controls whose function touch already provides (a carousel that people can swipe needs no revealed arrows). Do not keep hidden controls permanently visible just for touch.
- Reveal a hidden control when someone taps its general location. Reveal only controls relevant to the current content, and hide them again when the person finishes or after a few seconds without use. Sidebars and tab close buttons follow their own rules below.
- Keep the current selection when someone taps to reveal a control and when they tap the revealed control; the control may act on that selection.
- Put essential hidden controls in a short context menu, which touch opens with touch and hold.
- In a sidebar, a tap on a section header or row performs the click action (for example, collapsing Favorites in the Finder sidebar) and reveals that item's hidden controls. Keep them visible until touch moves outside the sidebar or a pointing device is used again. A tap on a hidden control's area reveals it without activating it; the next tap activates it.
- In a tabbed window, any tap in the window reveals the selected tab's close button until a pointing device is used again. If the person closes that tab by touch, show the close button on the newly selected tab.

<a id="visionOS"></a>
### visionOS
People can combine external pointer/keyboard with eyes and hands. Looking at content then moving the pointer automatically transfers focus to the pointer target. Gaze changes which window/context hosts the pointer. During supported pointer-device gestures, the pointer hides and returns at the looked-at location when moved; the app need not recreate this behavior.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/pointing-devices) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Change-log"></a>
## Change log
Source revision dates: October 28, 2026, June 21, 2023.
