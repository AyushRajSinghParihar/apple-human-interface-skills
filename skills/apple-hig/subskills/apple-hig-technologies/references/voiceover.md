# VoiceOver

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/voiceover) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

VoiceOver makes interface and content usable without visual access, including Apple-platform games and Unity experiences using Apple’s plug-ins.

<a id="Descriptions"></a>
## Descriptions
Label every important element, improving generic system labels to describe actual function and labeling custom controls. Keep descriptions synchronized with changing content. Describe meaningful images only for information they themselves convey, avoiding redundant surrounding captions. Give charts/infographics a concise purpose description and accessible equivalents of every interaction. Hide purely decorative imagery from accessibility navigation to reduce irrelevant speech.

<a id="Navigation"></a>
## Navigation
Give each page a short unique title and meaningful section headings. Express grouping, order, links, and relationships otherwise conveyed only through proximity/alignment. Use the current locale’s reading sequence and group images with their own captions. Notify assistive technologies when visible content or layout changes. Identify headings, links, and other content for rotor navigation; the rotor can also offer braille keyboard access.

<a id="Platform-considerations"></a>
## Platform considerations
No extra iOS/iPadOS/macOS/tvOS/watchOS rules are listed.

<a id="visionOS"></a>
### visionOS
With VoiceOver enabled, custom-gesture apps do not receive hand input by default, preventing accidental app actions during accessible exploration. A person may enable Direct Gesture mode, which turns off standard VoiceOver gestures and lets the app receive hand input directly. Application advice: do not make custom gestures the only route through the experience.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/voiceover) for linked Apple design assets and implementation resources.

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
Source revision dates: March 7, 2025.
