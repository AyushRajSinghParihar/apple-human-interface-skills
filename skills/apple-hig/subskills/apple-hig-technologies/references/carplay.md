# CarPlay

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/carplay) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

CarPlay presents the connected iPhone app through vehicle displays and controls. Use the appropriate system templates for the app category so the system handles display variation and hardware input. Focus the driving experience on quick, minimal interactions. The source notes audio/video CarPlay apps also work on Apple HomeView unchanged.

<a id="iPhone-interactions"></a>
## iPhone interactions
Complete phone-dependent setup before driving. Work with iPhone locked and inaccessible; never block CarPlay awaiting a phone action. Defer necessary phone-side problem resolution until the vehicle stops.

<a id="Audio"></a>
### Audio
Start playback through deliberate selection except for a single-source app or resuming interrupted audio. Do not start the audio session early because it silences other sources. Play as soon as buffered sufficiently and show Now Playing, loading descriptive metadata afterward. The system retains selection/spinner until readiness is signaled. Resume only a resumable interruption, such as a call, and only if previously playing; a new Siri playlist is a permanent/nonresumable interruption. Adjust relative mix levels if needed without overriding overall user volume.

<a id="Layout"></a>
## Layout
Use high-value, scannable content with consistent functions/appearances. Put prominent, tappable primary content/controls generally in the upper half. The system scales template UI across densities/aspect ratios. Source sample displays: 800 × 480 px (5:3), 960 × 540 and 1280 × 720 px (16:9), and 1920 × 720 px (8:3).

<a id="Color"></a>
## Color
Favor a restrained logo-related palette, distinguish interactive from inert content, and test inside a real car across sunlight, weather/tint, and night lighting. Support both automatic light/dark appearances and accessible/inclusive color interpretation.

<a id="Icons-and-images"></a>
## Icons and images
Supply @2x and @3x art for landscape and portrait displays. Reuse the phone app icon’s design; lighten a black background or add a separating border. Required icon canvases are 120 × 120 px @2x and 180 × 180 px @3x.

<a id="Error-handling"></a>
## Error handling
Handle failures quietly where possible. Necessary errors belong in CarPlay itself; never direct a driver to pick up the phone.

<a id="Platform-considerations"></a>
## Platform considerations
The source lists iOS only and marks the other platforms unsupported.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/carplay) for linked Apple design assets and implementation resources.

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
Source revision dates: May 2, 2023.
