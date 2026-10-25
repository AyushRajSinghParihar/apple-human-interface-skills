# Motion

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/motion) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

System components already provide motion adapted to input and accessibility. For example, Liquid Glass responds more strongly to direct touch than to trackpad input. Evaluate custom movement by what it communicates.

<a id="Best-practices"></a>
## Best practices
Use motion only when it supports the task, and allow a reduced or optional experience. Never make motion the sole carrier of important information; pair it with suitable visual, tactile, or audio feedback.

<a id="Providing-feedback"></a>
## Providing feedback
Follow gestures and physical expectations so entering and leaving views form a coherent relationship. Keep feedback brief, precise, and tied to action; avoid added delays for frequently repeated UI operations. Let people interrupt animations rather than waiting for completion. Consider SF Symbol animations when their meaning fits.

<a id="Leveraging-platform-capabilities"></a>
## Leveraging platform capabilities
For games, consistent 30–60 fps generally provides smooth results; select device-appropriate defaults rather than making players repair settings. Allow visual/performance/battery tradeoffs, including power-mode choices when external power is present.

<a id="Platform-considerations"></a>
## Platform considerations
No extra iOS/iPadOS/macOS/tvOS rules are listed.

<a id="visionOS"></a>
### visionOS
Avoid motion at the field-of-view edges. If peripheral motion is necessary, keep its brightness close to the surrounding content. Large moving objects can be mistaken for moving surroundings; lower contrast or increase translucency to preserve passthrough, and keep movable windows reasonably small. Fade an object between positions if tracking its travel adds no useful information. Avoid rotating an entire virtual world; use instantaneous reorientation during a quick fade instead. Provide a stationary reference around moving areas. Avoid sustained oscillation, particularly near 0.2 Hz; if needed, use low amplitude and consider translucency.

<a id="watchOS"></a>
### watchOS
Use SwiftUI for layout/appearance motion; WatchKit supports layout, appearance, and image-sequence animation. Built-in easing at the start and end of layout/appearance animations cannot be disabled or customized.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/motion) for linked Apple design assets and implementation resources.

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
Source revision dates: September 9, 2025, June 10, 2024, February 2, 2024, June 21, 2023.
