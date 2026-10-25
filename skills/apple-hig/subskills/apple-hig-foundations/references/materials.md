# Materials

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/materials) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Materials separate layers by letting underlying color influence foreground surfaces. Use Liquid Glass for the functional navigation/control layer and standard materials to organize content beneath it.

<a id="Liquid-Glass"></a>
## Liquid Glass
Standard controls adopt responsive glass automatically. Apply custom glass only to important functional elements. Keep it out of content backgrounds; a transient interactive part of a content-layer slider or toggle may temporarily take on glass to emphasize activation.

`regular` glass blurs and adjusts background luminosity for legible text, supplemented by scroll-edge effects. Use it for uncertain or complex backgrounds and substantial text such as alerts, sidebars, and popovers. `clear` glass is highly translucent and belongs over rich photos/video. For bright media consider a dark 35%-opacity dimming layer behind clear controls; skip extra dimming for already-dark content or AVKit controls that supply their own. Both variants adapt to appearance, contrast, and transparency settings.

<a id="Standard-materials"></a>
## Standard materials
Choose by semantic purpose rather than a sampled color. Use system vibrant foreground colors so text, symbols, fills, and dividers retain contrast. Thick/opaque materials favor fine detail and text; thin/translucent ones preserve background context. Combine blur and vibrancy according to the needed separation.

<a id="Platform-considerations"></a>
## Platform considerations
<a id="iOS-iPadOS"></a>
### iOS, iPadOS
Content-layer materials are ultra-thin, thin, regular/default, and thick. Vibrant labels offer `label`, `secondaryLabel`, `tertiaryLabel`, and `quaternaryLabel`, decreasing in contrast. Avoid quaternary labels on thin/ultra-thin backgrounds. Fills provide `fill`, `secondaryFill`, and `tertiaryFill` on all materials; separators have one default vibrancy level.

<a id="macOS"></a>
### macOS
Use purpose-specific materials and vibrant system colors. Test whether custom views/controls should allow vibrancy under different configurations. Choose behind-window or within-window background blending according to the interface context.

<a id="tvOS"></a>
### tvOS
Liquid Glass appears in navigation, Top Shelf, Control Center, and focus states of items such as images/buttons. Standard material recommendations are: ultra-thin for light full-screen views; thin for light partial overlays; regular for partial overlays generally; thick for dark partial overlays.

<a id="visionOS"></a>
### visionOS
Windows normally use unmodifiable adaptive glass that limits incoming background colors while showing light, the Environment, virtual content, and real surroundings. There is no separate Dark Mode. Prefer translucency over opaque window fills that block awareness. For custom components, thin emphasizes buttons/selection, regular separates sections such as sidebars/grouped tables, and thick makes a dark element distinct above regular material. Vibrancy brings surrounding light/color forward: `label` for ordinary text, `secondaryLabel` for explanatory text such as subtitles/footnotes, and `tertiaryLabel` for inactive low-priority content that does not demand strong readability.

<a id="watchOS"></a>
### watchOS
Preserve default material backgrounds in full-screen modal sheets so layering explains context and distinguishes controls/system UI from content.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/materials) for linked Apple design assets and implementation resources.

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
Source revision dates: September 9, 2025, June 9, 2025, August 6, 2024, December 5, 2023, June 21, 2023, June 5, 2023.
