# Digital Crown

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/digital-crown) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

The Digital Crown provides system interaction on Vision Pro and Watch, and app interaction on Watch.

<a id="Apple-Vision-Pro"></a>
## Apple Vision Pro
The system uses the Crown for volume, immersion amount in portals/Environments/Full Space, recentering, Accessibility settings, and exiting to Home View. Do not assume these are arbitrary app inputs.

<a id="Apple-Watch"></a>
## Apple Watch
Since watchOS 10, Crown rotation is the main navigation mechanism: Smart Stack on the face, vertical app browsing on Home, vertical paginated tabs, lists, and variable-height pages in apps. Provide equivalent touch navigation. Use rotation for data inspection or control adjustment where it is not needed for navigation. Crown presses are reserved by the system.

Always show a corresponding visual response. Match the rate of UI change to rotation speed while preserving precise selection. Use default haptic detents where they fit; disable them if animation and taps conflict. Tables can use row-based or linear detents; varying row heights can favor consistent linear feedback.

<a id="Platform-considerations"></a>
## Platform considerations
The source marks it unsupported on iOS, iPadOS, macOS, and tvOS.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/digital-crown) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Change-log"></a>
## Change log
Source revision dates: December 5, 2023, June 21, 2023, June 5, 2023.
