# Pointing devices

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/pointing-devices) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

A pointer provides precision and complements keyboard input on Mac and touch/eye/hand input on iPad and Vision Pro. Preserve a coherent experience when people switch inputs.

<a id="Best-practices"></a>
## Best practices
Keep mouse/trackpad gestures consistent with their system meanings and user-customized mappings. Do not override systemwide gestures even in games. Let pointer movement/hover reveal and hide minimized bars and playback controls. Keep modifier-plus-drag results consistent across touch and pointer, such as Option-drag duplication.

<a id="Platform-considerations"></a>
## Platform considerations
No additional iOS rules are given; tvOS/watchOS are marked unsupported.

<a id="iPadOS"></a>
### iPadOS
Support click-drag rectangular multi-selection in custom views when needed; nonlist standard collections provide it since iPadOS 15. Distinguish pointer from finger only for a concrete benefit, such as precise click-to-seek alongside touch dragging.

<a id="Pointer-shape-and-content-effects"></a>
#### Pointer shape and content effects
Default is a circle and text areas use an I-beam. Highlight becomes a translucent rounded background with gentle parallax for bars, tabs, segments, and edit menus. Lift fades the pointer under a scaled, shadowed, highlighted element such as an app icon or Control Center button. Hover customizes tint/scale/shadow without transforming the pointer.

<a id="Pointer-accessories"></a>
#### Pointer accessories
Small supplementary icons, such as resize arrows, can accompany any pointer. Keep them simple and use accessory transitions to show changed behavior, such as add becoming unavailable.

<a id="Pointer-magnetism"></a>
#### Pointer magnetism
Extended hit regions start shape transformation before visible contact. A flick can attract the pointer to a likely target’s center. Highlight/lift receive magnetism; hover normally does not because unexplained attraction without shape change can feel like lost control. Text magnetism helps prevent accidental jumps between lines.

<a id="Standard-pointers-and-effects"></a>
#### Standard pointers and effects
Use highlight for small transparent controls, lift for small opaque ones, and hover for larger content. Preserve standard buttons/text pointer appearances. Around bezelled controls, roughly 12 pt padding often works; without bezels use roughly 24 pt around visible edges. Test both precision and ease of escaping the target. Make custom adjacent bar-button hit areas contiguous to avoid momentary pointer-shape flashes. Supply the correct corner radius for nonstandard lift shapes.

<a id="Customizing-pointers"></a>
#### Customizing pointers
Use standard effects for standard behavior and consistent effects for equivalent custom surfaces. Keep custom shapes useful, simple, and restrained. Useful annotations such as graph coordinates or object dimensions can help; instructions attached to the pointer generally suggest unnecessary complexity. Allow scale only where neighboring content will not collide; tight rows can use tint alone. Shadow without scale suggests elevation without physical movement and should be avoided.

<a id="macOS"></a>
### macOS
Respect configurable clicks and gesture combinations. Mouse and trackpad both support primary selection, contextual secondary click, scrolling, smart zoom, page/full-screen-space swiping, and Mission Control. Trackpad also offers lookup/data detectors (force click or three-finger tap), tap-to-click, force/pressure input, two-finger pinch and rotation, edge-swipe Notification Center, three/four-finger downward App Exposé, thumb-plus-three-finger pinch Launchpad, and spreading those fingers for desktop.

<a id="Pointers"></a>
#### Pointers
Use NSCursor roles rather than a decorative substitute: `arrow` selects; `openHand` offers content dragging and `closedHand` indicates dragging; `contextualMenu` signals a menu, usually with Control; `crosshair` precise rectangular selection; `disappearingItem` a dropped reference will disappear without deleting the original; `dragCopy` Option-drag duplication; `dragLink` Option-Command-drag alias; `iBeam` and `iBeamCursorForVerticalLayout` text insertion in the corresponding direction; `operationNotAllowed` invalid drop; `pointingHand` URL link; `resizeDown`, `resizeLeft`, `resizeLeftRight`, `resizeRight`, `resizeUp`, and `resizeUpDown` describe allowed resizing axes/directions.

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

<a id="Videos"></a>
#### Videos
Apple’s linked design sessions provide demonstrations and additional implementation context; no video review is implied here.

<a id="Change-log"></a>
## Change log
Source revision dates: June 21, 2023.
