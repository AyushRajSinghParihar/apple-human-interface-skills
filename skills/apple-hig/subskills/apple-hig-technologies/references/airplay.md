# AirPlay

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/airplay) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

AirPlay sends media from supported Apple devices to receivers such as Apple TV, HomePod, and compatible televisions/speakers.

<a id="Best-practices"></a>
## Best practices
Prefer the standard player with familiar controls, chapters, subtitles/captions, and AirPlay. Supply all available HLS resolutions so AVFoundation can choose for the destination; a 720p phone rendition alone is inadequate on a 4K television. Support streaming and mirroring, but send only intended media, not incidental loops or short app-local clips. Handle remote play/pause/seek commands from Lock Screen, Siri, and HomePod. Continue streaming when backgrounded or locked without automatically mirroring unrelated private activity. Do not interrupt another app’s playback for launch/inline clips; use local ambient playback unless the person starts immersive media. Keep other app areas usable and prevent their videos from replacing the stream.

If a custom player is necessary, match system controls and their starting/playing/unavailable states. Use Apple-provided AirPlay symbols and, on iOS/iPadOS 16+, place the player’s AirPlay control at lower right.

<a id="Using-AirPlay-icons"></a>
## Using AirPlay icons
The noninteractive compatibility artwork has separate branding rules from the system-style player control above.

<a id="Black-AirPlay-icon"></a>
### Black AirPlay icon
Use black on a light surface when neighboring technology icons are black.

<a id="White-AirPlay-icon"></a>
### White AirPlay icon
Use white on a dark surface when neighboring technology icons are white.

<a id="Custom-color-AirPlay-icon"></a>
### Custom color AirPlay icon
Match neighboring technology-icon colors and containers. Use the downloaded compatibility icon/name noninteractively, not as a custom button. If other technology names accompany icons, put AirPlay beside/below its icon in the layout’s normal font; do not substitute the graphic within prose. Keep the app’s own identity more prominent.

<a id="Referring-to-AirPlay"></a>
## Referring to AirPlay
Spell AirPlay as one word with capital A/P; all caps is acceptable only to match an all-caps layout. Treat it as a noun, using wording such as support, compatibility, enabled, or use rather than a verb or ownership claim. Apple AirPlay is acceptable. Mention it when useful for capability-specific explanation or technical specifications.

<a id="Platform-considerations"></a>
## Platform considerations
No additional rules are listed for iOS/iPadOS/macOS/tvOS/visionOS; watchOS is marked unsupported.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/airplay) for linked Apple design assets and implementation resources.

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
