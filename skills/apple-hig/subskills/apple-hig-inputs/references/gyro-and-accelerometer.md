# Gyroscope and accelerometer

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Core Motion supplies real-time movement information for iOS/iPadOS/watchOS experiences; tvOS can use Siri Remote gyroscope data.

<a id="Best-practices"></a>
## Best practices
Collect motion only for a clear benefit, such as meaningful fitness feedback or gameplay. Supply a specific purpose explanation for the first system permission request. Outside active gameplay, avoid direct UI manipulation through accelerometer/gyroscope: motions can be hard to reproduce accurately, physically inaccessible, and battery-intensive.

<a id="Platform-considerations"></a>
## Platform considerations
The source lists no extra platform rules beyond the availability above.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Videos"></a>
#### Videos
Apple’s linked design sessions provide demonstrations and additional implementation context; no video review is implied here.
