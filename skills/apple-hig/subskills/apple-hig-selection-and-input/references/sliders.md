# Sliders

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/sliders)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A slider uses a thumb on a track to adjust a bounded value. The filled leading portion indicates progress from the minimum, and endpoint glyphs can clarify the quantity.

<a id="Best-practices"></a>
## Best practices

Customize track, thumb, tint, or endpoint imagery only when that improves meaning or integration. Horizontal minimum is at the leading side and maximum at the trailing side; vertical minimum is below maximum. Pair a wide-range slider with a numeric field for exact values and a stepper for convenient increments when helpful.

<a id="Platform-considerations"></a>
## Platform considerations

Sliders are unsupported in tvOS.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

For audio output volume, use a volume view, which combines a volume slider with an output-device control.

<a id="macOS"></a>
### macOS

Linear sliders have a narrow lozenge thumb and optional ticks; circular sliders have a small circular thumb and optional evenly spaced dot ticks. Provide live result feedback when feasible. Use a linear control for a fixed bounded interval, such as 0–100% opacity, and a circular control for repeating or continuing values, such as 0–360° rotation or multiple full turns (4 turns = 1440°).

A sentence-case introductory label normally ends in a colon. Ticks improve precision; label the endpoints or selected ticks instead of every tick unless all labels are needed. Nonlinear scales need enough intermediate labels to explain their mapping. A thumb tooltip can expose the exact current value.

<a id="visionOS"></a>
### visionOS

Prefer horizontal movement because side-to-side gestures are generally easier than vertical ones.

<a id="watchOS"></a>
### watchOS

A slider can show discrete steps or a continuous bar over a finite range. Buttons at its sides adjust by a defined amount. Replace the default plus/minus glyphs when custom glyphs better explain the function.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Steppers](https://developer.apple.com/design/human-interface-guidelines/steppers)
[Pickers](https://developer.apple.com/design/human-interface-guidelines/pickers)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/Slider> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UISlider> — UIKit
<https://developer.apple.com/documentation/AppKit/NSSlider> — AppKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 21, 2023.
