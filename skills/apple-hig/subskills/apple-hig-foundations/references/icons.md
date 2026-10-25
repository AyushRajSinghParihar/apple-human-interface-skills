# Icons

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/icons) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Interface glyphs communicate one concept through simplified shapes; app icons have a different branding role. Use SF Symbols or custom black-and-transparent template art that the system can tint.

<a id="Best-practices"></a>
## Best practices
Choose recognizable action/content metaphors with minimal detail. Keep size, perspective, stroke weight, and complexity consistent, including custom/system mixtures. Match adjacent text weight unless deliberate emphasis is needed. Adjust asymmetric art optically using small asset padding rather than assuming geometric centering looks balanced. Standard controls generally create selection appearances automatically.

Use inclusive, culturally recognizable figures. Include actual characters only when necessary for meaning and localize them; abstract text-line icons need RTL variants. Prefer PDF/SVG or a custom SF Symbol so artwork scales without multiple raster assets. Give custom glyphs accessible text descriptions. Avoid recreating Apple hardware; use authorized design-resource art or supplied product symbols if needed.

<a id="Standard-icons"></a>
## Standard icons
The following mappings retain the source’s recommended SF Symbol names.

<a id="Editing"></a>
### Editing
Cut → `scissors`; Copy → `document.on.document`; Paste → `document.on.clipboard`; Done/Save → `checkmark`; Cancel/Close → `xmark`; Delete → `trash`; Undo → `arrow.uturn.backward`; Redo → `arrow.uturn.forward`; Compose → `square.and.pencil`; Duplicate → `plus.square.on.square`; Rename → `pencil`; Move to/Folder → `folder`; Attach → `paperclip`; Add → `plus`; More → `ellipsis`.

<a id="Selection"></a>
### Selection
Select → `checkmark.circle`; Deselect/Close → `xmark`; Delete → `trash`.

<a id="Text-formatting"></a>
### Text formatting
Superscript/Subscript → `textformat.superscript` / `textformat.subscript`; Bold/Italic/Underline → `bold` / `italic` / `underline`; left/center/justified/right alignment → `text.alignleft` / `text.aligncenter` / `text.justify` / `text.alignright`.

<a id="Search"></a>
### Search
Search → `magnifyingglass`; Find, replacement, next/previous match, and using selection for find → `text.page.badge.magnifyingglass`; Filter → `line.3.horizontal.decrease`.

<a id="Sharing-and-exporting"></a>
### Sharing and exporting
Share/Export → `square.and.arrow.up`; Print → `printer`.

<a id="Users-and-accounts"></a>
### Users and accounts
Account/User/Profile → `person.crop.circle`.

<a id="Ratings"></a>
### Ratings
Dislike → `hand.thumbsdown`; Like → `hand.thumbsup`.

<a id="Layer-ordering"></a>
### Layer ordering
Front/back of three-layer stacks → `square.3.layers.3d.top.filled` / `square.3.layers.3d.bottom.filled`; one level forward/backward → `square.2.layers.3d.top.filled` / `square.2.layers.3d.bottom.filled`.

<a id="Other"></a>
### Other
Alarm → `alarm`; Archive → `archivebox`; Calendar → `calendar`.

<a id="Platform-considerations"></a>
## Platform considerations
No additional rules are given for iOS, iPadOS, tvOS, visionOS, or watchOS.

<a id="macOS"></a>
### macOS
<a id="Document-icons"></a>
#### Document icons
The folded-paper document shape distinguishes documents from apps. Without custom art, macOS combines the app icon and extension. Custom background, center artwork, and text can distinguish a family of document types; the system positions, layers, and masks these elements.

Make designs readable down to 16 × 16 px with a simple palette. A single background illustration can be enough. Reduce detail and thicken/align lines in small variants; remove fine grids at the smallest size. Keep essential background imagery away from the masked top-right fold.

Background canvases: 512, 256, 128, 32, and 16 px square at @1x, with matching @2x sizes of 1024, 512, 256, 64, and 32 px. Center artwork measures half the overall document canvas; supplied @1x center sizes are 256, 128, 32, and 16 px square, with @2x sizes 512, 256, 64, and 32 px. Keep most center art inside an approximately 10% margin on each side, occupying about 80% of its canvas: approximately 205 × 205 px inside 256 × 256 px. Small optical extensions can enter the margin. Replace an opaque extension with a short descriptive term if useful; the system scales it and normally displays uppercase.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/icons) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Videos"></a>
#### Videos
Apple’s linked design sessions provide demonstrations and additional implementation context; no video review is implied here.

<a id="Change-log"></a>
## Change log
Source revision dates: June 9, 2025, June 21, 2023.
