# Designing for games

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/designing-for-games) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Preserve the game’s identity while adopting each Apple platform’s device, input, and system conventions.

<a id="Jump-into-gameplay"></a>
## Jump into gameplay
Include playable material in the initial install and target an initial download of 30 minutes or less; retrieve later content in the background. Choose strong automatic defaults from display resolution, connected controllers/accessories, and accessibility settings. Teach controls in playable context; make written instructions a reference rather than a gate. Ask for sensor or personal-data permissions at the moment gameplay explains the need, and request ratings only after meaningful play.

<a id="Look-stunning-on-every-display"></a>
## Look stunning on every display
Keep text readable with adequate background contrast. Source default/minimum text sizes are:

|Platform|Default|Minimum|
|---|---:|---:|
|iOS and iPadOS|17 pt|11 pt|
|macOS|13 pt|10 pt|
|tvOS|29 pt|23 pt|
|visionOS|17 pt|12 pt|
|watchOS|16 pt|12 pt|

Keep buttons separated and easy to activate. The source button table gives these default/minimum dimensions:

|Platform|Default|Minimum|
|---|---:|---:|
|iOS and iPadOS|44 × 44 pt|28 × 28 pt|
|macOS|28 × 28 pt|20 × 20 pt|
|tvOS|66 × 66 pt|56 × 56 pt|
|visionOS|60 × 60 pt|28 × 28 pt|
|watchOS|44 × 44 pt|28 × 28 pt|

The same source’s prose describes 44 × 44 pt as the iOS touch minimum; treat 44 pt as the conservative touch target and consult the component guidance before using the smaller table exception.

Prefer resolution-independent art, particularly vectors that remain crisp under visionOS dynamic scaling. Otherwise match the rendering resolution to the device. Respect safe areas, rounded corners, and camera housings. Use relative layouts for menus that accommodate 16:10, 19.5:9, and 4:3 aspect ratios and supported phone/tablet orientations; custom device layouts should be exceptional. Support distraction-free full screen on phone, tablet, and Mac, and Full Space where suitable on visionOS.

<a id="Enable-intuitive-interactions"></a>
## Enable intuitive interactions
Provide the platform’s normal input first and adapt control sizes and menus when moving from pointer input to touch.

|Platform|Default input|Additional inputs identified by source|
|---|---|---|
|iOS|Touch|Game controller|
|iPadOS|Touch|Controller, keyboard, mouse, trackpad, Pencil|
|macOS|Keyboard, mouse, trackpad|Controller|
|tvOS|Remote|Controller, keyboard, mouse, trackpad|
|visionOS|Touch, including eye-targeted hand interactions|Controller, keyboard, mouse, trackpad, spatial controller|
|watchOS|Touch|None listed|

Physical controllers are supported on all these platforms except watchOS, but offer alternative interaction for players who lack or cannot use one. On phone and tablet, combine direct interaction with suitable onscreen controls rather than treating a touchscreen solely as a controller replacement.

<a id="Welcome-everyone"></a>
## Welcome everyone
Make essential information perceivable through more than color, sound, or motion alone. Provide descriptive subtitles or another readable form for cutscene information. Allow personalization of text size, input mapping, motion strength, and audio balance; use built-in accessibility APIs or Apple’s Unity plug-ins where relevant. Support varied names, descriptions, avatars, and human characteristics. Review stories and enemies for racial, cultural, and gender stereotypes and treat real cultures and languages respectfully.

<a id="Adopt-Apple-technologies"></a>
## Adopt Apple technologies
Use Game Center for discovery, friends, progress, achievements, leaderboards, challenges, and multiplayer. Use GameSave with iCloud identity to resume on another device. Core Haptics supports custom tactile patterns with optional audio on iOS, iPadOS, tvOS, visionOS, and many controllers. Supply multichannel audio to enable adaptive Spatial Audio. Consider AR, machine learning, HealthKit, camera, microphone, and location only where gameplay benefits and required permissions are obtained. Use In-App Purchase for relevant digital goods.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/designing-for-games) for linked Apple design assets and implementation resources.

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
Source revision dates: June 9, 2025, June 10, 2024.
