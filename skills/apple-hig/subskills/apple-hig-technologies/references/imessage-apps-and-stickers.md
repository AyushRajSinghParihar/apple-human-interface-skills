# iMessage apps and stickers

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/imessage-apps-and-stickers) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Messages apps/packs support sharing, collaboration, and games inside conversations and effects in Messages/FaceTime. They can be standalone or extensions of an iOS/iPadOS app.

<a id="Best-practices"></a>
## Best practices
Focus each app on one quickly understood experience, considering separate apps for distinct collections/functions. Surface useful host-app content or lightweight collaborative decisions. Put frequent functions in compact view; reserve extras and generally text editing for expanded view so the keyboard does not obscure the app. Make stickers expressive, inclusive, legible over varied backgrounds, and resilient to scaling/rotation; transparency can integrate with conversation content. Provide a localized VoiceOver description for each sticker.

<a id="Specifications"></a>
## Specifications
<a id="Icon-sizes"></a>
### Icon sizes
Provide square-cornered source canvases and let the system round-mask them. Source pixel sizes are:

|Context|@2x|@3x|
|---|---|---|
|Messages/notifications|148 × 110; 143 × 100|Not listed|
|Messages/notifications|120 × 90|180 × 135|
|Messages/notifications|64 × 48|96 × 72|
|Messages/notifications|54 × 40|81 × 60|
|Settings|58 × 58|87 × 87|
|App Store|1024 × 1024|1024 × 1024|

<a id="Sticker-sizes"></a>
### Sticker sizes
Choose one pack-wide size: small 300 × 300 px, regular 408 × 408 px, or large 618 × 618 px, all at @3x; the system downsamples as needed. Maximum file size is 500 KB. PNG supports 8-bit transparency without animation; APNG adds animation; GIF supports animation and single-color transparency; JPEG has neither transparency nor animation.

<a id="Platform-considerations"></a>
## Platform considerations
No extra iOS/iPadOS rules; macOS/tvOS/visionOS/watchOS are unsupported.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/imessage-apps-and-stickers) for linked Apple design assets and implementation resources.

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
