# Color

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/color) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

## Contents

- [Best practices](#Best-practices)
- [Inclusive color](#Inclusive-color)
- [System colors](#System-colors)
- [Liquid Glass color](#Liquid-Glass-color)
- [Color management](#Color-management)
- [Platform considerations](#Platform-considerations)
- [Specifications](#Specifications)
- [Resources](#Resources)
- [Change log](#Change-log)

Use color to clarify hierarchy, state, continuity, and identity. Prefer system colors when their semantics fit: they adapt to appearance, vibrancy, and accessibility preferences.

<a id="Best-practices"></a>
## Best practices
Keep each color’s meaning consistent; an interactive tint should not also decorate inert text. Provide light, dark, and increased-contrast variants for custom colors, including both appearances in a single-appearance app because Liquid Glass adapts locally. Test outdoors, in dim rooms, on different hardware and display profiles, and against visionOS physical backgrounds. True Tone changes white point on supported phones/tablets/Macs; media, reading, and game apps can specify white-point adaptivity. Test several HD/4K TV brands. Account for nearby artwork and translucent surfaces when choosing colors. Prefer a system color picker so people get familiar selection and shared saved colors.

<a id="Inclusive-color"></a>
## Inclusive color
Pair essential color signals with words, shapes, or glyphs. Check text/icon contrast and combinations that can be hard to distinguish. Consider cultural meanings rather than assuming colors convey universal emotions or warnings.

<a id="System-colors"></a>
## System colors
Use APIs rather than copying numeric system values, which can change by release and environment. Dynamic semantic colors describe purpose, such as label, separator, link, or hierarchical background. Preserve those meanings rather than borrowing separator colors for text or label colors for fills.

<a id="Liquid-Glass-color"></a>
## Liquid Glass color
Clear glass derives its appearance from the content behind it. Small bars can switch between light and dark with underlying content; labels and symbols normally remain monochrome. Larger surfaces such as sidebars become more opaque to preserve readability.

Use tinted glass sparingly for important status or a primary action. To emphasize a primary button, color its background rather than its text or symbol, and avoid coloring several control backgrounds. Over colorful content, prefer monochrome bars or an accent that contrasts clearly; a brand accent works more readily against monochrome content. Check resting and initial layouts for overlap between similarly colored content and controls, not only intermediate scroll states.

<a id="Color-management"></a>
## Color management
A color model describes components such as RGB/CMYK; a color space defines their gamut, and an embedded profile maps numeric values to actual colors. Embed profiles in images; sRGB is broadly reliable. On a wide-color display, Display P3 can improve photo/video fidelity and visual differentiation. The source recommends Display P3 PNG with 16 bits per channel where appropriate. P3 imagery usually converts well to sRGB, but close colors or gradients can merge or clip; provide color-space-specific asset variants when testing exposes problems.

<a id="Platform-considerations"></a>
## Platform considerations
<a id="iOS-iPadOS"></a>
### iOS, iPadOS
Use grouped backgrounds for grouped tables, otherwise the ordinary system background family. In each family, primary is the overall view, secondary groups within it, and tertiary groups within secondary content.

|Role|UIKit API|
|---|---|
|Primary through quaternary labels|`label`, `secondaryLabel`, `tertiaryLabel`, `quaternaryLabel`|
|Placeholder strings|`placeholderText`|
|Translucent divider|`separator`|
|Opaque divider|`opaqueSeparator`|
|Linked text|`link`|
|Ordinary backgrounds, levels 1–3|`systemBackground`, `secondarySystemBackground`, `tertiarySystemBackground`|
|Grouped backgrounds, levels 1–3|`systemGroupedBackground`, `secondarySystemGroupedBackground`, `tertiarySystemGroupedBackground`|

<a id="macOS"></a>
### macOS
Choose NSColor semantic APIs by the actual role, available in the standard Color panel’s Developer palette.

|Role|NSColor API|
|---|---|
|Text on selection in table/list|`alternateSelectedControlTextColor`|
|Alternating rows/columns|`alternatingContentBackgroundColors`|
|User accent|`controlAccentColor`|
|Browser/table background|`controlBackgroundColor`|
|Control surface / enabled text|`controlColor`, `controlTextColor`|
|System tint / disabled text|`currentControlTint`, `disabledControlTextColor`|
|Find indicator / grid lines|`findHighlightColor`, `gridColor`|
|Table header / virtual illumination|`headerTextColor`, `highlightColor`|
|Keyboard focus ring|`keyboardFocusIndicatorColor`|
|Primary through quaternary label|`labelColor`, `secondaryLabelColor`, `tertiaryLabelColor`, `quaternaryLabelColor`|
|Link / placeholder|`linkColor`, `placeholderTextColor`|
|Selected content in key view|`selectedContentBackgroundColor`|
|Selected control / its text|`selectedControlColor`, `selectedControlTextColor`|
|Selected menu text|`selectedMenuItemTextColor`|
|Text-selection fill / selected text|`selectedTextBackgroundColor`, `selectedTextColor`|
|Divider / raised-object shadow|`separatorColor`, `shadowColor`|
|Document background / document text|`textBackgroundColor`, `textColor`|
|Behind document|`underPageBackgroundColor`|
|Inactive selected content|`unemphasizedSelectedContentBackgroundColor`|
|Inactive text-selection fill / text|`unemphasizedSelectedTextBackgroundColor`, `unemphasizedSelectedTextColor`|
|Window surface / title-bar text|`windowBackgroundColor`, `windowFrameTextColor`|

<a id="App-accent-colors"></a>
#### App accent colors
Since macOS 11, an app accent can color buttons, selections, and sidebar icons when the user chooses multicolor. Another user-selected accent overrides it, except fixed-color sidebar icons whose specific colors carry meaning.

<a id="tvOS"></a>
### tvOS
Use a restrained palette related to the app logo while letting content lead. Show focus through scaling and responsive motion as well as color.

<a id="visionOS"></a>
### visionOS
Physical and virtual colors show through glass. Use color for important relationships or emphasis, preferably in bold text or large areas rather than thin text and tiny details. Balance brightness during immersion: avoid isolated bright, flashing, or moving objects against dark surroundings when eyes have adapted to darkness.

<a id="watchOS"></a>
### watchOS
Background color can convey context or supporting information, such as a ring’s category. Avoid long-lived full-screen colored backgrounds in workouts or playback. Graphic complications must also work in the wearer’s chosen single-color tinted mode.

<a id="Specifications"></a>
## Specifications
### System colors
The following dated design-reference values were recovered from the official JSON swatch descriptions in the 2026-10-25 snapshot. Each tuple is an 8-bit RGB triplet. Use the semantic APIs in production instead of hard-coding these values: system colors can change with releases and context. SwiftUI properties are shown below; visionOS uses default dark values.

|Color/API|Light RGB|Dark RGB|High-contrast light RGB|High-contrast dark RGB|
|---|---|---|---|---|
|Red / `red`|255,56,60|255,66,69|233,21,45|255,97,101|
|Orange / `orange`|255,141,40|255,146,48|197,83,0|255,160,86|
|Yellow / `yellow`|255,204,0|255,214,0|161,106,0|254,223,67|
|Green / `green`|52,199,89|48,209,88|0,137,50|74,217,104|
|Mint / `mint`|0,200,179|0,218,195|0,133,117|84,223,203|
|Teal / `teal`|0,195,208|0,210,224|0,129,152|59,221,236|
|Cyan / `cyan`|0,192,232|60,211,254|0,126,174|109,217,255|
|Blue / `blue`|0,136,255|0,145,255|30,110,244|92,184,255|
|Indigo / `indigo`|97,85,245|109,124,255|86,74,222|167,170,255|
|Purple / `purple`|203,48,224|219,52,242|176,47,194|234,141,255|
|Pink / `pink`|255,45,85|255,55,95|231,18,77|255,138,196|
|Brown / `brown`|172,127,94|183,138,102|149,109,81|219,166,121|


<a id="iOS-iPadOS-system-gray-colors"></a>
### iOS, iPadOS system gray colors
UIKit supplies the six gray variants below. These are dated 2026-10-25 design-reference RGB values, not production constants. SwiftUI `Color.gray` corresponds to `systemGray`.

|Color/API|Light RGB|Dark RGB|High-contrast light RGB|High-contrast dark RGB|
|---|---|---|---|---|
|Gray / `systemGray`|142,142,147|142,142,147|108,108,112|174,174,178|
|Gray (2) / `systemGray2`|174,174,178|99,99,102|142,142,147|124,124,128|
|Gray (3) / `systemGray3`|199,199,204|72,72,74|174,174,178|84,84,86|
|Gray (4) / `systemGray4`|209,209,214|58,58,60|188,188,192|68,68,70|
|Gray (5) / `systemGray5`|229,229,234|44,44,46|216,216,220|54,54,56|
|Gray (6) / `systemGray6`|242,242,247|28,28,30|235,235,240|36,36,38|


<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/color) for linked Apple design assets and implementation resources.

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
Source revision dates: December 16, 2025, June 9, 2025, February 2, 2024, September 12, 2023, June 21, 2023, June 5, 2023, December 19, 2022.
