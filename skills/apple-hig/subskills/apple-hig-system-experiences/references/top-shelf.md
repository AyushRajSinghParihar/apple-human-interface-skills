# Top Shelf

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/top-shelf)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Top Shelf showcases a favorite Dock app's content on Apple TV Home Screen. Full-screen previews can play as the Dock recedes, and people can browse to Play or More Info.

<a id="Best-practices"></a>
## Best practices

Deep-link directly to content. Carousel templates provide playback and detail buttons. Feature fresh, relevant releases rather than already consumed/purchased items, and personalize recommendations, resume playback, or active games. Avoid ads and prominent prices; show purchase information when interest warrants it. Prefer dynamic content and layered imagery. Provide a static fallback when fullscreen content is unavailable: 2320×720 pt, with 2320×720 px at 1× and 4640×1440 px at 2×. The system flips/blurs it into a 1920-pixel-wide 16:9 context; it is not focusable, so do not imply interaction.

<a id="Dynamic-layouts"></a>
## Dynamic layouts

Choose a full-screen video/image carousel, a focusable content row, or scrolling banners according to the content.

<a id="Carousel-actions"></a>
### Carousel actions

Use for familiar shows, franchises, or personal media requiring little explanation. Provide a short content title and optional useful subtitle such as series name or date range.

<a id="Carousel-details"></a>
### Carousel details

Adds decision-supporting synopsis, cast, or other metadata. Identify current content near the top; a concise attribution can sit above it.

<a id="Sectioned-content-row"></a>
### Sectioned content row

Fill at least one full screen-width row and provide at least one contextual label. Focus reveals labels and remote motion animates imagery. Several labels can be supported. The source's per-state dimensions follow.

<a id="Poster-23"></a>
#### Poster (2:3)

|Aspect                |Image size                                  |
|----------------------|--------------------------------------------|
|Actual size           |404x608 pt (404x608 px @1x, 808x1216 px @2x)|
|Focused/Safe zone size|380x570 pt (380x570 px @1x, 760x1140 px @2x)|
|Unfocused size        |333x570 pt (333x570 px @1x, 666x1140 px @2x)|

<a id="Square-11"></a>
#### Square (1:1)

|Aspect                |Image size                                   |
|----------------------|---------------------------------------------|
|Actual size           |608x608 pt (608x608 px @1x, 1216x1216 px @2x)|
|Focused/Safe zone size|570x570 pt (570x570 px @1x, 1140x1140 px @2x)|
|Unfocused size        |500x500 pt (500x500 px @1x, 1000x1000 px @2x)|

<a id="169"></a>
#### 16:9

|Aspect                |Image size                                   |
|----------------------|---------------------------------------------|
|Actual size           |908x512 pt (908x512 px @1x, 1816x1024 px @2x)|
|Focused/Safe zone size|852x479 pt (852x479 px @1x, 1704x958 px @2x) |
|Unfocused size        |782x440 pt (782x440 px @1x, 1564x880 px @2x) |

Mixing image types can upscale shorter images to the tallest row height; a 16:9 image can scale to 500 pixels high beside posters/squares.

<a id="Scrolling-inset-banner"></a>
#### Scrolling inset banner

Timed automatic cycling stops when an item is focused and loops after the last image. Focus supports lighting/layered depth effects and swipes select adjacent banners. Supply 3–8 images. Put any text in the image because no external label is provided, optionally on its own image layer, and include it in accessibility text.

|Aspect                |Image size                                      |
|----------------------|------------------------------------------------|
|Actual size           |1940x692 pt (1940x692 px @1x, 3880x1384 px  @2x)|
|Focused/Safe zone size|1740x620 pt (1740x620 px @1x, 3480x1240 px @2x) |
|Unfocused size        |1740x560 pt (1740x560 px @1x, 3480x1120 px @2x) |

<a id="Platform-considerations"></a>
## Platform considerations

Top Shelf is tvOS-specific and unsupported in iOS, iPadOS, macOS, visionOS, and watchOS.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Apple Design Resources](https://developer.apple.com/design/resources/#tvos-apps)

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2019/211>
