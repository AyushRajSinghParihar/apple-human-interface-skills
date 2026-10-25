# Images

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/images) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Treat points as logical measurements. On 2D displays the pixel-to-point mapping depends on density; in visionOS points are angular and scale with viewing distance.

<a id="Resolution"></a>
## Resolution
Provide bitmap assets for every supported density: @1x means one pixel per point, @2x two, @3x three. Supply @2x for iPadOS/watchOS, @2x and @3x for iOS, @1x and @2x for macOS/tvOS, and at least @2x for visionOS according to viewing needs. Mark scale in filenames and asset catalogs. Start vector artwork at a logical low-resolution grid with whole-number control points so scaled 2x/3x rasterizations remain aligned.

<a id="Formats"></a>
## Formats
Use de-interlaced PNG for raster artwork, an 8-bit palette where 24-bit color is unnecessary, optimized JPEG or HEIC for photos, stereo HEIC for spatial/stereo photos, and PDF or SVG for scalable icons and flat art.

<a id="Best-practices"></a>
## Best practices
Embed a color profile in every image. Inspect assets on actual supported devices to catch stretching, pixelation, and compression that design previews can miss.

<a id="Platform-considerations"></a>
## Platform considerations
No additional iOS/iPadOS/macOS rules are listed.

<a id="tvOS"></a>
### tvOS
Use layers, transparency, scaling, and motion to reinforce focus and depth.

<a id="Parallax-effect"></a>
#### Parallax effect
The system raises, lights, and gently moves a focused item; after inactivity the focused item expands and other content dims. Layered artwork is required for this treatment.

<a id="Layered-images"></a>
#### Layered images
Use 2–5 layers. Layering is mandatory for the app icon and encouraged for other focusable artwork, including Top Shelf. Standard views and focus APIs apply the effect automatically. Place key objects and text in front, supporting content/shadows in the middle, and an opaque background behind. A transparent background causes an error. Keep depth subtle, leave a crop-safe margin especially on foreground layers, and preview through design tools plus an actual TV.

Artwork can be bundled or downloaded. For server-delivered layers, generate `.lcr` runtime images from LSR/Photoshop with Xcode’s `layerutil`; these download-oriented files should not be embedded in the app. Apple’s Parallax Previewer/Exporter can help check clipping and scaling.

<a id="visionOS"></a>
### visionOS
Prefer vectors for 2D art because size and angle vary broadly and image pixels need not align to display pixels. App icons use 2–3 layers. A @2x raster can work at ordinary distance but may blur close up; higher resolutions increase file size and runtime cost, especially beyond @6x. Apply high-quality filtering when exceeding @2x, balancing clarity and performance.

<a id="Spatial-photos-and-spatial-scenes"></a>
#### Spatial photos and spatial scenes
A spatial photo is stereo imagery plus spatial metadata, captured on devices such as iPhone 15 Pro or newer, Vision Pro, or another compatible camera. A spatial scene derives a head-responsive 3D/parallax presentation from 2D imagery. RealityKit supports both.

Use stereo HEIC with spatial metadata so visionOS recognizes photos and supplies comfort treatments. Prefer feathered glass behind overlaid text to add contrast and soften stereo detail. Tune disparity and metadata carefully because comfortable depth depends on viewing position. Present photos/scenes in a separate window or sheet; if stereo art must be inline, provide generous space from neighboring content to ease depth adjustment.

Scene generation can take several seconds. Prefer a deliberate creation action for a specific moment, as in a single-photo viewer. Avoid many scenes at once; use pagination, scrolling, or explicit navigation with a simple hierarchy. Immersive viewing should have minimal UI. Center a reasonably large scene in the field of view to make lateral head-motion parallax effective.

<a id="watchOS"></a>
### watchOS
Flatten art onto its known solid background to reduce size, except template imagery such as complication/menu/interface icons that needs alpha for system tinting. An autoscaling PDF designed for 40/42 mm at @2x can cover all screen sizes.

|Watch screen|Automatic image scale|
|---|---:|
|38 mm|90%|
|40 mm|100%|
|41 mm|106%|
|42 mm|100%|
|44 mm|110%|
|45 mm|119%|
|49 mm|119%|

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/images) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Change-log"></a>
## Change log
Source revision dates: December 16, 2025, December 5, 2023, June 21, 2023, September 14, 2022.
