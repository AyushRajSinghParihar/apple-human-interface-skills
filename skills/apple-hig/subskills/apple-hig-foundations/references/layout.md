# Layout

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/layout) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Use predictable relationships among content and controls while adapting to the actual available space.

<a id="Visual-hierarchy"></a>
## Visual hierarchy
Prioritize important content toward the top and leading edge in reading order. Use system components for RTL adaptation. Align related items, indent subordinate items, and group relationships with space, containers, or separators. Reveal secondary choices progressively through disclosure, menus, nested views, or scrollable media sections. Distinguish navigation/controls with Liquid Glass and scroll-edge treatments; extend full-window backgrounds under bars and sidebars. A background extension effect can mirror and blur imagery under adjacent components instead of hiding essential original art.

<a id="Adaptability"></a>
## Adaptability
Handle size classes, display sizes, orientation/aspect ratio, Dynamic Island, external displays, Display Zoom, resizable windows, text changes, localized length/direction/fonts, and date/number formats. Use SwiftUI or Auto Layout, safe areas, margins, and layout modifiers. Orientation-locked games must still resize. With large text, stack horizontal content, increase row height, and allow wrapping. Apple’s Unity accessibility plug-in can supply Dynamic Type in games. Preview smallest/largest layouts first, then multiple devices, localizations, sizes, iPad resizing, and iPhone Mirroring. Scale backgrounds to fill without distorting aspect ratio; extreme wide/short or narrow/tall windows may crop much more than standard displays.

<a id="Size-classes"></a>
### Size classes
Each axis is compact or regular, describing available width or height rather than device type or orientation. All four combinations can occur as apps resize, multitask, or mirror. Base layout on these environmental values, not idiom/orientation guesses. Preserve functionality across classes while changing how much is exposed, such as sidebar versus tabs or visible actions versus overflow. The platform idiom remains the same during resizing, so preserve its familiar character.

<a id="Guides-and-safe-areas"></a>
## Guides and safe areas
Layout guides supply rectangular regions for alignment, spacing, margins, and readable text widths; custom guides can add app-specific structure. Safe areas exclude edge obstructions such as camera hardware, status bars, tab bars, and toolbars. Keep important content and controls within the appropriate safe regions.

<a id="Platform-considerations"></a>
## Platform considerations
No extra iOS/iPadOS rules are listed.

<a id="macOS"></a>
### macOS
Do not rely on the bottom of a window for essential controls because it may sit below the physical display. Avoid placing content behind the top camera housing.

<a id="tvOS"></a>
### tvOS
Inset primary content 60 pt vertically and 80 pt horizontally to withstand TV overscan/settings. Leave enough focus padding for system enlargement so focused items do not obscure important information.

<a id="Grids"></a>
#### Grids
Use consistent row/column spacing, sufficient room for enlargement, and symmetrical partial items at both horizontal edges. Add extra separation above and below row titles. UIKit collection flow layout derives the column count from item width and spacing. Source grid measurements follow; all use 40 pt horizontal gaps and a minimum 100 pt vertical gap between unfocused rows.

<a id="Two-column-grid"></a>
#### Two-column grid
Unfocused item width: 860 pt. Horizontal gap: 40 pt. Minimum vertical gap: 100 pt.

<a id="Three-column-grid"></a>
#### Three-column grid
Unfocused item width: 560 pt. Horizontal gap: 40 pt. Minimum vertical gap: 100 pt.

<a id="Four-column-grid"></a>
#### Four-column grid
Unfocused item width: 410 pt. Horizontal gap: 40 pt. Minimum vertical gap: 100 pt.

<a id="Five-column-grid"></a>
#### Five-column grid
Unfocused item width: 320 pt. Horizontal gap: 40 pt. Minimum vertical gap: 100 pt.

<a id="Six-column-grid"></a>
#### Six-column grid
Unfocused item width: 260 pt. Horizontal gap: 40 pt. Minimum vertical gap: 100 pt.

<a id="Seven-column-grid"></a>
#### Seven-column grid
Unfocused item width: 217 pt. Horizontal gap: 40 pt. Minimum vertical gap: 100 pt.

<a id="Eight-column-grid"></a>
#### Eight-column grid
Unfocused item width: 184 pt. Horizontal gap: 40 pt. Minimum vertical gap: 100 pt.

<a id="Nine-column-grid"></a>
#### Nine-column grid
Unfocused item width: 160 pt. Horizontal gap: 40 pt. Minimum vertical gap: 100 pt.

<a id="visionOS"></a>
### visionOS
Support resizing in windows and volumes; center content horizontally at very large sizes. Set minimum/maximum bounds only to avoid overlaps or unwieldy layouts, not to disable resizing. Use inline 3D content sparingly for meaningful additions; inset it so it avoids controls and window edges. Prefer volumes or immersive spaces for large/model-centric content. Open supplemental content in an adjacent window, reserving ornaments for interactive app controls. Space controls so hover feedback remains distinct; regular buttons should have centers at least 60 pt apart.

<a id="watchOS"></a>
### watchOS
Normally use no more than three glyph buttons or two text buttons side by side. Full-width text controls usually work best; two short labels can fit on a non-scrolling screen. Support autorotation when people may show content, such as a photo or QR code, to another person or reader instead of always sleeping on wrist-away movement.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/layout) for linked Apple design assets and implementation resources.

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
Source revision dates: September 9, 2026, September 9, 2025, June 9, 2025, March 7, 2025, September 9, 2024, June 10, 2024, February 2, 2024, December 5, 2023, September 15, 2023, June 21, 2023, September 14, 2022.
