# Game controls

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/game-controls) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Support a platform’s built-in input even when controllers enhance play: not everyone owns or can use one. All listed platforms except watchOS support physical controllers.

<a id="Touch-controls"></a>
## Touch controls
For iOS/iPadOS, use direct manipulation where it fits and TouchController virtual controls when movement or numerous actions require them. Keep common buttons near thumbs, clear of movement/camera areas, Home indicator, Dynamic Island, and safe-area obstructions; put secondary menus higher. Frequent controls need at least 44 × 44 pt, less important ones at least 28 × 28 pt. Give a visible pressed state that remains perceivable under the finger plus appropriate haptic/audio feedback. Depict actual actions rather than arbitrary A/X/R1 labels. Hide irrelevant controls and consider revealing movement controls only on touch. Combine related actions and use hold/double-tap variants instead of demanding complex button combinations. Conventionally left controls movement and right controls camera; maximize their input regions, place a movement thumbstick at the thumb’s landing point, and prefer direct camera panning over a second virtual stick.

<a id="Physical-controllers"></a>
## Physical controllers
Keep default-input alternatives: touch, keyboard/pointer, remote, or eye/hand gestures. tvOS/visionOS games can require a controller with the appropriate App Store badge, but must gracefully detect absence and request connection. Detect paired controllers and profiles automatically. Show glyphs/labels for the actual active controller and correct player in multiplayer, not framework-generic lettering; symbols usually beat prose for quick recognition.

Outside gameplay, map A to activation, B to cancel/back, shoulders to previous/next section, thumbsticks and D-pad to selection, and Menu to settings/pause. Home/logo remains reserved for the system. The source assigns no universal UI action to X, Y, or either trigger. Handle several connected controllers and combined labels when referring to more than one.

<a id="Keyboards"></a>
## Keyboards
Prefer quick single-key bindings, nearby keys for related/frequent actions, and large easy-to-reach keys such as Space for a primary action. Test on Apple keyboards: Command beside Space can be more comfortable than a borrowed Control mapping for WASD play. Provide customization for ability, comfort, and play style.

<a id="Platform-considerations"></a>
## Platform considerations
No extra iOS/iPadOS/macOS/tvOS rules; watchOS is marked unsupported.

<a id="visionOS"></a>
### visionOS
For spatial controllers such as PlayStation VR2 Sense, preserve hand-input semantics: look then press either trigger for indirect action, or reach to an object then press a trigger for direct interaction.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/game-controls) for linked Apple design assets and implementation resources.

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
Source revision dates: June 9, 2025, June 10, 2024.
