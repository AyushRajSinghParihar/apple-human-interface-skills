# Widgets

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/widgets)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

## Contents

- [Anatomy](#Anatomy)
- [Best practices](#Best-practices)
- [Rendering modes](#Rendering-modes)
- [Previews and placeholders](#Previews-and-placeholders)
- [Platform considerations](#Platform-considerations)
- [Specifications](#Specifications)

Widgets provide timely information and focused actions outside the app. Contexts include phone/tablet Home and Lock Screens, Mac desktop/Notification Center, watch Smart Stack, spatial surfaces, and Apple HomeView. Choose size, location, and rendering behavior together.

<a id="Anatomy"></a>
## Anatomy

WidgetKit supplies contextual treatment, but tailor the layout when a context needs a better information hierarchy.

<a id="System-family-widgets"></a>
### System family widgets

Small commonly focuses on one fact, medium/large on more information/actions, extra large adds room where supported, and extra-large portrait is spatial-only. The supported-context matrix is factual source data:

|Widget size                |iPhone                                                       |iPad                                    |Mac                            |Apple Vision Pro                |
|---------------------------|-------------------------------------------------------------|----------------------------------------|-------------------------------|--------------------------------|
|System small               |Home Screen, Today View, StandBy, CarPlay, and Apple HomeView|Home Screen, Today View, and Lock Screen|Desktop and Notification Center|Horizontal and vertical surfaces|
|System medium              |Home Screen and Today View                                   |Home Screen and Today View              |Desktop and Notification Center|Horizontal and vertical surfaces|
|System large               |Home Screen and Today View                                   |Home Screen and Today View              |Desktop and Notification Center|Horizontal and vertical surfaces|
|System extra large         |Not supported                                                |Home Screen and Today View              |Desktop and Notification Center|Horizontal and vertical surfaces|
|System extra large portrait|Not supported                                                |Not supported                           |Not supported                  |Horizontal and vertical surfaces|

<a id="Accessory-widgets"></a>
### Accessory widgets

These compact families provide very limited information. Corner is watch-only; inline, circular, and rectangular also support phone/tablet Lock Screens as listed.

|Widget size          |iPhone       |iPad         |Apple Watch                               |
|---------------------|-------------|-------------|------------------------------------------|
|Accessory circular   |Lock Screen  |Lock Screen  |Watch complications and in the Smart Stack|
|Accessory corner     |Not supported|Not supported|Watch complications                       |
|Accessory inline     |Lock Screen  |Lock Screen  |Watch complications                       |
|Accessory rectangular|Lock Screen  |Lock Screen  |Watch complications and in the Smart Stack|

<a id="Appearances"></a>
### Appearances

Widgets can be full color, tinted monochrome, or clear/translucent. Home Screens can use light/dark, desaturated tint, or clear Liquid Glass. visionOS adds physical framing and glass/paper treatment, with palette tint choices. Lock Screen accessories desaturate; StandBy and HomeView Modular remove backgrounds and scale content, using red monochrome in low light. A watch rectangular accessory can be full color/tinted on a face or live in Smart Stack. Rendering mode varies by context rather than following one universal rule.

|Platform        |Full-color                                                                |Accented                                               |Vibrant                           |
|----------------|--------------------------------------------------------------------------|-------------------------------------------------------|----------------------------------|
|iPhone          |Home Screen, Today view, StandBy and CarPlay (with the background removed)|Home Screen and Today view                             |Lock Screen, StandBy in Night Mode|
|iPad            |Home Screen and Today view                                                |Home Screen and Today view                             |Lock Screen                       |
|Apple Watch     |Smart Stack, complications                                                |Smart Stack, complications                             |Not supported                     |
|Mac             |Desktop and Notification Center                                           |Not supported                                          |Desktop                           |
|Apple Vision Pro|Horizontal and vertical surfaces                                          |Horizontal and vertical surfaces                       |Not supported                     |
|Apple HomeView  |Home Screen, Modular face (with the background removed)                   |Home Screen, Modular face (with the background removed)|Modular face in Night Mode        |

<a id="Best-practices"></a>
## Best practices

Choose a simple purpose central to the app and useful changing information. A static app-icon replica offers little benefit. Use multiple sizes only when they add layers of useful information, not stretched copies. Balance immediate clarity with secondary details available on longer inspection. Keep larger variants on the same core purpose. Brand through restrained color/type/glyphs; if source attribution needs a logo, a small upper-trailing mark suffices. Offer configuration when people must choose their content; otherwise useful automatic recents can remove setup. Avoid lookalike widget elements inside the app that behave differently. Explain any signed-in functionality when logged out. A subtle occasion-specific visual treatment can add delight without losing utility.

<a id="Updating-widget-content"></a>
### Updating widget content

Widgets refresh periodically under system limits rather than continuously. Match updates to meaningful changes and expected viewing, adding freshness text when data can age between checks. Use system date/time views to preserve reload budget. Show available data promptly instead of replacing it with placeholders while refreshing. Standard/custom transitions of up to 2 seconds can reveal new data.

<a id="Adding-interactivity"></a>
### Adding interactivity

Ordinary widget activation opens the app; native buttons/toggles can do simple relevant work in place. Deep-link precisely to the selected content. Keep targets clear and glanceable instead of recreating a miniature app. Inline accessories have one tap target.

<a id="Choosing-margins-and-padding"></a>
### Choosing margins and padding

Supply adaptable content and let system sizing handle device scale; iPad can render a larger canvas before downscaling. Most widgets use 16-pt margins; 11 pt can suit tighter grouped graphics/buttons/background shapes. Mac desktop and Lock Screen/StandBy use smaller contextual margins. Use container-relative rounding so inset shapes align with the outer corners.

<a id="Displaying-text-in-widgets"></a>
### Displaying text in widgets

Prefer system text styles and aligned SF Symbols. Custom type should be sparse and readable, often limited to large text with SF Pro for small labels. Generally keep type at least 11 pt. Render actual text rather than rasterizing so scaling and VoiceOver work. In iOS, iPadOS, and visionOS, SwiftUI system/custom fonts support Dynamic Type Large through AX5.

<a id="Using-color"></a>
### Using color

Use color to support content rather than compete with it, and provide noncolor meaning because tinting, grayscale, and watch-face inversion can change the result. Widget editing colors can come from the asset catalog. Preserving full-color images in clear/tinted modes can overpower system customization; reserve it for meaningful media such as artwork and keep images smaller than the whole widget where appropriate.

<a id="Rendering-modes"></a>
## Rendering modes

<a id="Full-color"></a>
### Full-color

Support light/dark through semantic colors or asset variants, normally matching light backgrounds to light appearance and dark to dark.

<a id="Accented"></a>
### Accented

Separate primary and accent groups. The system applies context-dependent solid colors; watch uses white for primary and the selected watch-face color for accent. Preserve hierarchy across all tint/clear options. The source's platform table excludes accented Mac mode while one prose sentence mentions Mac group tinting; do not infer Mac support from that conflicting sentence.

<a id="Vibrant"></a>
### Vibrant

Pixel opacity controls how much background material passes through, while grayscale brightness determines visual emphasis. Use opaque white/light gray for prominent information and darker opaque grays for supporting details. Check grayscale contrast; varying white opacity is not a substitute for optimized grayscale values.

<a id="Previews-and-placeholders"></a>
## Previews and placeholders

Gallery previews should show realistic real or simulated data promptly and accurately represent each variant. Loading placeholders can preserve static framing and use semitransparent blocks for dynamic text or images. Describe the widget with an approachable sentence-case action verb, omitting filler about adding/using a widget. Group its sizes under one description. The gallery Add button can use an appropriate brand color.

<a id="Platform-considerations"></a>
## Platform considerations

No additional macOS rules are specified. Widgets are unsupported in tvOS.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Treat Lock Screen widgets like complications: useful data first, with inline above the clock and circular/rectangular below. Verify reduced-luminance Always On grayscale. For frequent real-time bounded updates, design a Live Activity, reusing appropriate components rather than expecting widget refreshes to behave continuously.

<a id="StandBy-and-CarPlay"></a>
#### StandBy and CarPlay

StandBy shows two scaled small-family widgets; CarPlay also scales that family with removable backgrounds. Use large readable information and restrained rich imagery, especially for across-room or driving glances. Mark backgrounds removable. Test red monochrome in low-light StandBy.

<a id="Apple-HomeView"></a>
#### Apple HomeView

Small-family widgets can appear on a shared Modular face and personalized Home Screens, sourced locally or from connected household iPhones/iPads. The household has one Modular face with up to four widgets, potentially exposing one person's calendar to others. Each enrolled member has their own Home Screen; consider the privacy difference.

<a id="visionOS"></a>
### visionOS

Widgets persist on horizontal/vertical surfaces through device restarts at consistent real-world scale. Full color is default; selected palette tints use accented mode. Elevated frames have customizable widths, and widget-specific themes can exist despite no global light/dark appearance. Design as room objects, from desk information to wall posters, and test all palettes and lighting, including elements excluded from tinting.

<a id="Thresholds-and-sizes"></a>
#### Thresholds and sizes

Design nearby/default and distant/simplified versions. At a distance, enlarge type, reduce detail, and remove controls; retain common elements across thresholds for continuity. Match family size to the likely surface. People can scale to 75–125%, so use clear hierarchy and high-resolution assets readable across distances.

<a id="Mounting-styles"></a>
#### Mounting styles

Elevated is default and works on walls and horizontal surfaces, tilting back on desks and casting a grounding shadow. Recessed sets content into vertical surfaces only, suitable for ambient/windowlike content. Opt out of unsuitable styles; recessed-only widgets cannot be placed horizontally. Mounting support applies per configuration, so separate configurations when variants need different support. Test every elevated frame width because layout cannot adapt to the selected frame.

<a id="Treatment-styles"></a>
#### Treatment styles

Paper provides a solid print-like object whose whole appearance follows ambient brightness. Glass separates foreground and background: important foreground stays bright/full color while supporting material adapts to lighting. Choose paper for artwork/posters and glass for information needing reliable contrast.

<a id="watchOS"></a>
### watchOS

Smart Stack backgrounds default black; a meaningful custom color can communicate state. Supply relevance based on location or current system activity to encourage timely display/placement.

<a id="Specifications"></a>
## Specifications

Use these factual dimensions as design guidance and keep production layouts flexible. Dimensions in pt are distinct from real-world millimeters; iPad canvas and displayed device sizes are distinct rows.

<a id="iOS-dimensions"></a>
### iOS dimensions

|Screen size (portrait, pt)|Small (pt)|Medium (pt)|Large (pt)|Circular (pt)|Rectangular (pt)|Inline (pt)|
|--------------------------|----------|-----------|----------|-------------|----------------|-----------|
|430×932                   |170x170   |364x170    |364x382   |76x76        |172x76          |257x26     |
|428x926                   |170x170   |364x170    |364x382   |76x76        |172x76          |257x26     |
|414x896                   |169x169   |360x169    |360x379   |76x76        |160x72          |248x26     |
|414x736                   |159x159   |348x157    |348x357   |76x76        |170x76          |248x26     |
|393x852                   |158x158   |338x158    |338x354   |72x72        |160x72          |234x26     |
|390x844                   |158x158   |338x158    |338x354   |72x72        |160x72          |234x26     |
|375x812                   |155x155   |329x155    |329x345   |72x72        |157x72          |225x26     |
|375x667                   |148x148   |321x148    |321x324   |68x68        |153x68          |225x26     |
|360x780                   |155x155   |329x155    |329x345   |72x72        |157x72          |225x26     |
|320x568                   |141x141   |292x141    |292x311   |N/A          |N/A             |N/A        |

<a id="iPadOS-dimensions"></a>
### iPadOS dimensions

|Screen size (portrait, pt)|Target|Small (pt)|Medium (pt)|Large (pt) |Extra large (pt)|
|--------------------------|------|----------|-----------|-----------|----------------|
|768x1024                  |Canvas|141x141   |305.5x141  |305.5x305.5|634.5x305.5     |
|^                         |Device|120x120   |260x120    |260x260    |540x260         |
|744x1133                  |Canvas|141x141   |305.5x141  |305.5x305.5|634.5x305.5     |
|^                         |Device|120x120   |260x120    |260x260    |540x260         |
|810x1080                  |Canvas|146x146   |320.5x146  |320.5x320.5|669x320.5       |
|^                         |Device|124x124   |272x124    |272x272    |568x272         |
|820x1180                  |Canvas|155x155   |342x155    |342x342    |715.5x342       |
|^                         |Device|136x136   |300x136    |300x300    |628x300         |
|834x1112                  |Canvas|150x150   |327.5x150  |327.5x327.5|682x327.5       |
|^                         |Device|132x132   |288x132    |288x288    |600x288         |
|834x1194                  |Canvas|155x155   |342x155    |342x342    |715.5x342       |
|^                         |Device|136x136   |300x136    |300x300    |628x300         |
|954x1373 *                |Canvas|162x162   |350x162    |350x350    |726x350         |
|^                         |Device|162x162   |350x162    |350x350    |726x350         |
|970x1389 *                |Canvas|162x162   |350x162    |350x350    |726x350         |
|^                         |Device|162x162   |350x162    |350x350    |726x350         |
|1024x1366                 |Canvas|170x170   |378.5x170  |378.5x378.5|795x378.5       |
|^                         |Device|160x160   |356x160    |356x356    |748x356         |
|1192x1590 *               |Canvas|188x188   |412x188    |412x412    |860x412         |
|^                         |Device|188x188   |412x188    |412x412    |860x412         |

<a id="visionOS-dimensions"></a>
### visionOS dimensions

|Widget              |Size in pt|Size in mm (scaled to 100%)|
|--------------------|----------|---------------------------|
|Small               |158x158   |268x268                    |
|Medium              |338x158   |574x268                    |
|Large               |338x354   |574x600                    |
|Extra large         |450x338   |763x574                    |
|Extra large portrait|338x450   |574x763                    |

<a id="watchOS-dimensions"></a>
### watchOS dimensions

|Apple Watch size |Size of a widget in the Smart Stack (pt)|
|-----------------|----------------------------------------|
|40mm             |152x69.5                                |
|41mm             |165x72.5                                |
|42mm             |176x72.5                                |
|44mm             |173x76.5                                |
|45mm             |184x80.5                                |
|46mm             |194x80.5                                |
|49mm (Ultra 3, 4)|198x81.5                                |
|49mm (Ultra 1, 2)|191x81.5                                |

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/WidgetKit>
<https://developer.apple.com/documentation/WidgetKit/Developing-a-WidgetKit-strategy> — WidgetKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2026/277>
  <https://developer.apple.com/videos/play/wwdc2025/278>
  <https://developer.apple.com/videos/play/wwdc2025/255>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: October 13, 2026, December 16, 2025, January 17, 2025, June 10, 2024, June 5, 2023, November 3, 2022.
