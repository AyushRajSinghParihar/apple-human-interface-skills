# Nearby interactions

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/nearby-interactions) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

NearbyInteraction uses Ultra Wideband on compatible devices, with permission while the app is used. Session-scoped random identifiers protect privacy. Build on meaningful real-world proximity rather than proximity as a novelty.

<a id="Best-practices"></a>
## Best practices
Use distance, direction, and task context together, such as nearby intended recipients or an audio handoff. Let detail/feedback become more precise as people approach an object. Keep feedback continuous as people move. Blend visual, sound, and haptic guidance according to whether attention is on the display or surroundings. Always provide another way to complete the task.

<a id="Device-usage"></a>
## Device usage
Portrait usually improves direction/distance availability; prefer implicit visual guidance for holding the device. The sensor’s directional field resembles an iPhone 11-or-newer Ultra Wide camera: outside it, distance may be available without direction. Teach how intervening people, animals, or large objects can reduce accuracy and availability.

<a id="Platform-considerations"></a>
## Platform considerations
No extra iPadOS rules are listed; macOS/tvOS/visionOS are marked unsupported.

<a id="iOS"></a>
### iOS
iPhone APIs supply peer distance and direction.

<a id="watchOS"></a>
### watchOS
Watch APIs supply distance only, and every participating watch app must remain in the foreground.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/nearby-interactions) for linked Apple design assets and implementation resources.

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
