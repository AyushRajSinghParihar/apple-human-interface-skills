# Spatial layout

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/spatial-layout) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Use spatial position, scale, and depth to support useful work while preserving comfort and awareness.

<a id="Field-of-view"></a>
## Field of view
Field of view is what someone sees without moving the head; it varies with Light Seal configuration and individual vision, and the system does not expose its dimensions. Center important content and avoid bright or moving peripheral distractions. Anchor content to the surrounding space rather than rigidly to the head, allowing natural looking around and stable passthrough.

<a id="Depth"></a>
## Depth
Depth perception depends on consistent distance, occlusion, reflections, color temperature, and shadow cues. SwiftUI gives window elements subtle depth automatically; RealityKit supplies 3D objects, including within frameless volumes. Use depth for meaningful hierarchy, such as bringing a sheet forward while its window recedes. Avoid floating text and depth effects on tiny button glyphs that hurt reading. Repeated or rapid depth changes force tiring refocusing; reserve depth for important elements and provide physically coherent cues.

<a id="Scale"></a>
## Scale
Dynamic scaling increases a window’s physical scale as it moves farther away, preserving its apparent size and interactivity. Fixed-scale objects keep real-world size and therefore appear smaller at distance. visionOS points are angular measurements supporting dynamic scale. Reserve fixed scale mainly for noninteractive objects needing true physical dimensions, such as life-size products; interactive content generally benefits from dynamic scaling.

<a id="Best-practices"></a>
## Best practices
Limit windows so the app does not block surroundings or become cumbersome to reposition. Prioritize indirect gestures with resting hands; direct interaction suits nearby objects inspected briefly. Let the system Digital Crown action recenter content without recreating this behavior. Space regular buttons at least 60 pt center-to-center, leaving at least 16 pt between them, and avoid overlapping interactive targets or hover feedback. Support stationary use unless movement is essential. Align floor-based large immersive content to a flat horizontal plane matching the real floor.

<a id="Platform-considerations"></a>
## Platform considerations
This guidance is visionOS-specific; the source marks it unsupported on the other five platforms.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/spatial-layout) for linked Apple design assets and implementation resources.

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
Source revision dates: March 29, 2024, June 21, 2023.
