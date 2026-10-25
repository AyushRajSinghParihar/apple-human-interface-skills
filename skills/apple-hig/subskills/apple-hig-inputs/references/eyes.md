# Eyes

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/eyes) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Looking identifies a target in visionOS; system hover feedback signals that an indirect gesture can act on it. A tab can highlight before its bar expands to reveal labels, and a button may reveal a tooltip. Gaze before a tap remains private: the app does not receive its location. Connected-keyboard/controller focus is a separate system.

<a id="Best-practices"></a>
## Best practices
Support assistive technologies and alternative input methods. Keep needed content within comfortable view; initial windows/volumes are placed by the system, while Full Space can request head-pose information for 3D placement. Avoid repeated large eye movements or rapid refocusing across depth. Sustained reading/content should normally sit at least 1 m away; close placement suits brief interactions only. Prefer standard components’ familiar hover responses.

<a id="Making-items-easy-to-see"></a>
## Making items easy to see
Reduce noise, peripheral motion, and new content that pulls attention away from an intended target. Space items with at least a 16 pt margin around their bounds or at least 60 pt between centers. Avoid full-view repeating patterns/textures that can create ambiguous perceived depth; constrain them to smaller areas.

<a id="Encouraging-interaction"></a>
## Encouraging interaction
Guide attention with centered placement and gentle contrast, color, scale, or movement instead of harsh flashing. Rounded shapes are easier to target than corners. For a single interactive object made of an image and label, define a containing hover region encompassing both.

<a id="Custom-hover-effects"></a>
## Custom hover effects
Define normal and hovered appearances; the system applies them outside the app process and does not reveal current gaze/state or run gaze-dependent app code. A predefined favorite indicator can appear on hover, but hover cannot itself favorite an item.

Reserve customization for distinctive moments. Use no delay for subtle affordances, a short delay when people may act quickly before expansion, and a longer delay for optional information such as tooltips. Keep at least one primary visual stable across states. Test on a worn Vision Pro for responsiveness, comfort, and distraction.

<a id="Platform-considerations"></a>
## Platform considerations
This source is visionOS-specific and marks the other platforms unsupported.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/eyes) for linked Apple design assets and implementation resources.

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
Source revision dates: June 10, 2024, March 29, 2024, October 24, 2023, June 21, 2023.
