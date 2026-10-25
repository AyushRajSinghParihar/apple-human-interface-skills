# Game Center

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/game-center) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Game Center enables discovery, friends, progress, invitations, and activity across the system, App Store, notifications, and Apple Games app. GameKit offers complete system UI or data for custom presentation.

<a id="Accessing-Game-Center"></a>
## Accessing Game Center
Check sign-in at game launch and initialize Game Center when needed to support a smooth start and system/social discovery.

<a id="Integrating-the-access-point"></a>
### Integrating the access point
Use Apple’s access point in main/settings menus, not gameplay, transient splash/cinematics, or pre-menu tutorials. It opens Game Overlay on iOS/iPadOS/macOS and a full-screen dashboard on visionOS/tvOS. Account for collapsed/expanded size at any selected corner; visionOS placement depends on immersive/volume game type. Keep nearby controls clear and consider pausing behind the overlay/dashboard.

<a id="Using-custom-UI"></a>
### Using custom UI
Custom links may deep-link to profiles or leaderboards. Use official artwork without dimension/effect changes. Use Game Center, Game Center Profile, Achievements, Leaderboards, Challenges, and Add Friends rather than invented equivalents or developer terms. Use the system’s localized Game Center term and localize Profile/other labels appropriately.

<a id="Achievements"></a>
## Achievements
<a id="Integrating-achievements-into-your-game"></a>
### Integrating achievements into your game
Map locked, in-progress, hidden, and completed states correctly; the system groups completed separately from all locked/incomplete states. Upload order determines display order, so plan progression before upload. Titles and descriptions each allow two displayed lines before truncation; use title case for titles and sentence case for descriptions. Report progressive achievement data so system progress/encouragement remains useful.

<a id="Creating-achievement-images"></a>
### Creating achievement images
Create distinct high-quality rewards rather than reusing art or leaving placeholder images. Center primary art for circular masks. All source specs require at least 72 DPI, PNG/TIF/JPG, sRGB or P3. On iOS/iPadOS/macOS/visionOS: 512 × 512 pt canvas and 512 pt circular mask, or 1024 × 1024 px / 1024 px mask @2x. On tvOS: 320 × 320 pt canvas (640 px square @2x) with a 200 pt mask (400 px @2x).

<a id="Leaderboards"></a>
## Leaderboards
Classic boards retain all-time best scores indefinitely; recurring boards reset on a chosen daily/weekly/seasonal interval, giving renewed chances to lead. Group numerous boards into sets by difficulty, activity, or theme. Supply distinctive gameplay-related art and preserve content inside source crop/focus-safe areas.

|Platform|Format/profile|Canvas|Crop/focus dimensions|
|---|---|---|---|
|iOS/iPadOS/macOS|JPEG/JPG/PNG; sRGB/P3; ≥72 DPI|512 × 512 pt / 1024 × 1024 px @2x|Set crop 512 × 312 pt / 1024 × 624 px|
|tvOS|PNG/TIF/JPG; sRGB/P3; ≥72 DPI|659 × 371 pt / 1318 × 742 px @2x|Focused 618 × 348 pt / 1236 × 696 px; unfocused 548 × 309 pt / 1096 × 618 px|

Use one image for phone/tablet/Mac and focus-responsive layers for TV; account for edge cropping.

<a id="Challenges"></a>
## Challenges
Build time-limited friend competitions on leaderboards using individual skill attempts lasting around 1–5 minutes. Use the latest attempt rather than lifetime progress/best scores that unfairly favor regular players. Deep-link invitations, Game Overlay, and Games-app entries to the precise mode/level; complete necessary first-time tutorials first with a clear promise to continue into the challenge. Use attractive art avoiding title/description overlays; localize any embedded text. Specs: JPEG/JPG/PNG, sRGB/P3, ≥72 DPI, 1920 × 1080 pt / 3840 × 2160 px @2x, with crop 1465 × 767 pt / 2930 × 1534 px @2x.

<a id="Multiplayer-activities"></a>
## Multiplayer activities
Support real-time or turn-based play through system or custom matchmaking UI. Party codes, usually eight alphanumeric characters, can coordinate sessions even with custom networking. Keep the current code visible/findable and allow manual entry, late joining, leaving, and rejoining. Default invitation UI can find nearby/recent players, friends, and contacts. Activity artwork uses the same 1920 × 1080 pt / 3840 × 2160 px canvas and 1465 × 767 pt / 2930 × 1534 px crop, JPEG/JPG/PNG, sRGB/P3, at least 72 DPI.

<a id="Platform-considerations"></a>
## Platform considerations
No extra iOS/iPadOS/macOS/visionOS rules.

<a id="tvOS"></a>
### tvOS
Optional dashboard header art can use a recognizable logo/wordmark, not the app icon. Use 600 × 180 pt / 1200 × 360 px @2x, PNG/TIF/JPG, sRGB/P3, at least 72 DPI.

<a id="watchOS"></a>
### watchOS
GameKit APIs exist, but no system Game Center UI can be invoked on Watch; its Game Center content appears on the connected iPhone.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/game-center) for linked Apple design assets and implementation resources.

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
Source revision dates: June 9, 2025, February 2, 2024, September 12, 2023, May 2, 2023.
