# Camera Control

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/camera-control) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

The source describes Camera Control on iPhone 16 and 16 Pro. A light press opens a bezel-adjacent overlay, a light double press reveals controls, and sliding adjusts the selected control.

<a id="Anatomy"></a>
## Anatomy
Use sliders for a continuous/value range and pickers for discrete choices. System zoom and exposure controls can accompany custom controls in the overlay.

<a id="Best-practices"></a>
## Best practices
- Represent each function with an available SF Symbol; custom symbols are unsupported and the symbol represents function rather than live state.
- Keep names short because Dynamic Type can enlarge labels over the viewfinder. Include units such as EV/% or a useful localized value string for sliders, and declare frequently used or regularly spaced prominent values for easier settling.
- Leave overlay/label space next to the hardware control in portrait and landscape. Maximize the viewfinder, allowing the overlay over it, and hide duplicate app controls while the overlay is present.
- Enable/disable the fixed set of controls according to capture mode; controls cannot be added/removed at runtime.
- Put common controls near the middle and rare ones at either end. The system remembers the last control when reopening.
- Provide a locked camera capture extension so people can launch the camera experience from lock screen, Home Screen, and other apps.

<a id="Platform-considerations"></a>
## Platform considerations
The source marks Camera Control unsupported outside iOS.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/camera-control) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Change-log"></a>
## Change log
Source revision dates: September 9, 2024.
