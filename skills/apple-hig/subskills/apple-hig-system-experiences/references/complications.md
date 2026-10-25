# Complications

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/complications)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

## Contents

- [Best practices](#Best-practices)
- [Visual design](#Visual-design)
- [Circular](#Circular)
- [Corner](#Corner)
- [Inline](#Inline)
- [Rectangular](#Rectangular)
- [Legacy templates](#Legacy-templates)
- [Platform considerations](#Platform-considerations)

Complications expose timely watch-face information without opening the app. WidgetKit families are preferred from watchOS 9 onward; support older watchOS with ClockKit data sources and legacy templates. Watch faces choose supported families for their slots.

<a id="Best-practices"></a>
## Best practices

Prioritize useful changing information over a static app launcher. Support every family where possible, falling back to a recognizable launch image when useful data cannot fit. Several distinct complications per family can create a curated shareable face; each should deep-link to its own relevant area. Protect sensitive information on Always On displays. Schedule timeline entries when they become useful, accounting for limited daily reloads and stored entries rather than assuming unlimited updates.

<a id="Visual-design"></a>
## Visual design

Use closed rings for percentages, open gauges for arbitrary bounded ranges, and segmented gauges for ranges with rapid changes. Tinted mode desaturates full-color content and applies the selected watch color; retain meaning without color alone and provide alternate tinted images if needed. Legacy tinting applies to graphic templates only. Generally use lines at least 2 pt thick for glanceability in motion. Supply static placeholders for every supported complication; their required dimensions may differ from content images and they can appear during initial load or in the selection carousel.

<a id="Circular"></a>
## Circular

Circular families show text, gauges, or color images on faces such as Infograph and include extra-large layouts for X-Large. Bezel text can occupy nearly 180° before truncation. Regular circular images are masked to a circle; extra-large circular/open/closed gauge images also receive circular masks. Standard rounded medium-weight text sizes are 12/12.5/13/14.5 pt across 40/41/44/45-or-49 mm watches; extra-large uses 34.5/36.5/36.5/41 pt. The factual source image and placeholder dimensions follow.

|Image           |40mm                   |41mm                       |44mm                   |45mm/49mm                  |
|----------------|-----------------------|---------------------------|-----------------------|---------------------------|
|Image           |42x42 pt (84x84 px @2x)|44.5x44.5 pt (89x89 px @2x)|47x47 pt (94x94 px @2x)|50x50 pt (100x100 px @2x)  |
|Closed gauge    |27x27 pt (54x54 px @2x)|28.5x28.5 pt (57x57 px @2x)|31x31 pt (62x62 px @2x)|32x32 pt (64x64 px @2x)    |
|Open gauge      |11x11 pt (22x22 px @2x)|11.5x11.5 pt (23x23 px @2x)|12x12 pt (24x24 px @2x)|13x13 pt (26x26 px @2x)    |
|Stack (not text)|28x14 pt (56x28 px @2x)|29.5x15 pt (59X30 px @2x)  |31x16 pt (62x32px @ 2x)|33.5x16.5 pt (67x33 px @2x)|

|Image       |40mm                       |41mm                       |44mm                       |45mm/49mm                  |
|------------|---------------------------|---------------------------|---------------------------|---------------------------|
|Image       |120x120 pt (240x240 px @2x)|127x127 pt (254x254 px @2x)|132x132 pt (264x264 px @2x)|143x143 pt (286x286 px @2x)|
|Open gauge  |31x31 pt (62x62 px @2x)    |33x33 pt (66x66 px @2x)    |33x33 pt (66x66 px @2x)    |37x37 pt (74x74 px @2x)    |
|Closed gauge|77x77 pt (154x154 px @2x)  |81.5x81.5 (163x163 px @2x) |87x87 pt (174x174 px @2x)  |91.5x91.5 (183x183 px @2x) |
|Stack       |80x40 pt (160x80 px @2x)   |85x42 (170x84 px @2x)      |87x44 pt (174x88 px @2x)   |95x48 pt (190x96 px @2x )  |

|Layout     |38mm|40mm/42mm                  |41mm                       |44mm                       |45mm/49mm                  |
|-----------|----|---------------------------|---------------------------|---------------------------|---------------------------|
|Circular   |–   |42x42 pt (84x84 px @2x)    |44.5x44.5 pt (89x89 px @2x)|47x47 pt (94x94 px @2x)    |50x50 pt (100x100 px @2x)  |
|Bezel      |–   |42x42 pt (84x84 px @2x)    |44.5x44.5 pt (89x89 px @2x)|47x47 pt (94x94 px @2x)    |50x50 pt (100x100 px @2x)  |
|Extra Large|–   |120x120 pt (240x240 px @2x)|127x127 pt (254x254 px @2x)|132x132 pt (264x264 px @2x)|143x143 pt (286x286 px @2x)|

<a id="Corner"></a>
## Corner

Corner layouts support text, gauges, and full-color imagery, with some multicolor text. Images receive circular masks. Default text is rounded semibold at 10/10.5/11/12 pt across 40/41/44/45-or-49 mm sizes.

|Image   |40mm                   |41mm                   |44mm                   |45mm/49mm               |
|--------|-----------------------|-----------------------|-----------------------|------------------------|
|Circular|32x32 pt (64x64 px @2x)|34x34 pt (68x68 px @2x)|36x36 pt (72x72 px @2x)|38x38 pt (76x76 px @2x )|
|Gauge   |20x20 pt (40x40 px @2x)|21x21 pt (42x42 px @2x)|22x22 pt (44x44 px @2x)|24x24 pt (48x48 px @2x) |
|Text    |20x20 pt (40x40 px @2x)|21x21 pt (42x42 px @2x)|22x22 pt (44x44 px @2x)|24x24 pt (48x48 px @2x) |

|38mm|40mm/42mm              |41mm                   |44mm                   |45mm/49mm              |
|----|-----------------------|-----------------------|-----------------------|-----------------------|
|–   |20x20 pt (40x40 px @2x)|21x21 pt (42x42 px @2x)|22x22 pt (44x44 px @2x)|24x24 pt (48x48 px @2x)|

<a id="Inline"></a>
## Inline

Small utilitarian layouts occupy a rectangular corner region for a glyph, image, or circular graph. Large utilitarian layouts are mainly text, optionally preceded by a glyph, along the bottom of faces such as Utility or Motion. Use the source's specific device dimensions; N/A denotes unavailable combinations. The small 41-mm Flat cell lists 21 pt height but a 21-pixel height at 2×; those conflict. The large version lists 10.5 pt. Treat this as an unresolved source typo and verify the target template before sizing production art. The legacy circular placeholder also prints 18×18× pt; its matching 36×36-pixel entry suggests a typographical extra ×.

|Content|38mm                       |40mm/42mm                    |41mm                          |44mm                   |45mm/49mm                    |
|-------|---------------------------|-----------------------------|------------------------------|-----------------------|-----------------------------|
|Flat   |9-21x9 pt (18-42x18 px @2x)|10-22x10 pt (20-44x20 px @2x)|10.5-23.5x21 pt (21-47x21 @2x)|N/A                    |12-26x12 pt (24-52x24 px @2x)|
|Ring   |14x14 pt (28x28 px @2x)    |14x14 pt (28x28 px @2x)      |15x15 pt (30x30 px @2x)       |16x16 pt (32x32 px @2x)|16.5x16.5 pt (33x33 px @2x)  |
|Square |20x20 pt (40x40 px @2x)    |22x22 pt (44x44 px @2x)      |23.5x23.5 pt (47x47 px @2x)   |25x25 pt (50x50 px @2x)|26x26 pt (52x52 px @2x)      |

|Content|38mm                       |40mm/42mm                    |41mm                               |44mm|45mm/49mm                    |
|-------|---------------------------|-----------------------------|-----------------------------------|----|-----------------------------|
|Flat   |9-21x9 pt (18-42x18 px @2x)|10-22x10 pt (20-44x20 px @2x)|10.5-23.5x10.5 pt (21-47x21 px @2x)|N/A |12-26x12 pt (24-52x24 px @2x)|

<a id="Rectangular"></a>
## Rectangular

This region can show color imagery, text, gauges, and an optional title. Use the space for informative changing charts with prominent data and quieter axes/labels. Since watchOS 10, rectangular content may also appear in Smart Stack; add meaningful backgrounds, relevant intent data, or a layout tailored to that context. Both large-image forms receive a 4-pt corner radius. Default text is rounded medium at 16.5/17.5/18/19.5 pt for 40/41/44/45-or-49 mm watches.

|Content                    |40mm                      |41mm                        |44mm                       |45mm/49mm                   |
|---------------------------|--------------------------|----------------------------|---------------------------|----------------------------|
|Large image with title *   |150x47 pt (300x94 px @2x) |159x50 pt (318x100 px @2x)  |171x54 pt (342x108 px @2x) |178.5x56 pt (357x112 px @2x)|
|Large image without title *|162x69 pt (324x138 px @2x)|171.5x73 pt (343x146 px @2x)|184x78 pt (368x156 px @2x) |193x82 pt (386x164 px @2x)  |
|Standard body              |12x12 pt (24x24 px @2x)   |12.5x12.5 pt (25x25 px @2x) |13.5x13.5 pt (27x27 px @2x)|14.5x14.5 pt (29x29 px @2x) |
|Text gauge                 |12x12 pt (24x24 px @2x)   |12.5x12.5 pt (25x25 px @2x) |13.5x13.5 pt (27x27 px @2x)|14.5x14.5 pt (29x29 px @2x) |

<a id="Legacy-templates"></a>
## Legacy templates

These preserve support for older watchOS and specific nongraphic appearances. Follow each template's size rather than substituting dimensions from newer families.

<a id="Circular-small"></a>
### Circular small

Use a few characters or a small image in a corner slot, as on Color. Stack width measurements are maxima.

|Image      |38mm                   |40mm/42mm               |41mm                       |44mm                   |45mm/49mm                  |
|-----------|-----------------------|------------------------|---------------------------|-----------------------|---------------------------|
|Ring       |20x20 pt (40x40 px @2x)|22x22 pt (44x44 px @2x) |23.5x23.5 pt (47x47 px @2x)|24x24 pt (48x48 px @2x)|26x26 pt (52x52 px @2x)    |
|Simple     |16x16 pt (32x32 px @2x)|18x18 pt (36x36 px @2x) |19x19 pt (38x38 px @2x)    |20x20 pt (40x40 px @2x)|21.5x21.5 pt (43x43 px @2x)|
|Stack      |16x7 pt (32x14 px @2x) |17x8 pt (34x16 px @2x)  |18x8.5 pt (36x17 px @2x)   |19x9 pt (38x18 px @2x) |19x9.5 pt (38x19 px @2x)   |
|Placeholder|16x16 pt (32x32 px @2x)|18x18x pt (36x36 px @2x)|19x19 pt (38x38 px @2x)    |20x20 pt (40x40 px @2x)|21.5x21.5 pt (43x43 px @2x)|

<a id="Modular-small"></a>
### Modular small

Supports two stacked icon/content rows, a ring graph, or one larger item in a Modular slot. Stack widths are maxima.

|Image      |38mm                   |40mm/42mm              |41mm                       |44mm                   |45mm/49mm                  |
|-----------|-----------------------|-----------------------|---------------------------|-----------------------|---------------------------|
|Ring       |18x18 pt (36x36 px @2x)|19x19 pt (38x38 px @2x)|20x20 pt (40x40 px @2x)    |21x21 pt (42x42 px @2x)|22.5x22.5 pt (45x45 px @2x)|
|Simple     |26x26 pt (52x52 px @2x)|29x29 pt (58x58 px @2x)|30.5x30.5 pt (61x61 px @2x)|32x32 pt (64x64 px @2x)|34.5x34.5 pt (69x69 px @2x)|
|Stack      |26x14 pt (52x28 px @2x)|29x15 pt (58x30 px @2x)|30.5x16 pt (61x32 px @2x)  |32x17 pt (64x34 px @2x)|34.5x18 pt (69x36 px @2x)  |
|Placeholder|26x26 pt (52x52 px @2x)|29x29 pt (58x58 px @2x)|30.5x30.5 pt (61x61 px @2x)|32x32 pt (64x64 px @2x)|34.5x34.5 pt (69x69 px @2x)|

<a id="Modular-large"></a>
### Modular large

A broader central canvas supports up to three rows, arranged as columns, standard body content, or a table.

|Content      |38mm                         |40mm/42mm                    |41mm                             |44mm                         |45mm/49mm                        |
|-------------|-----------------------------|-----------------------------|---------------------------------|-----------------------------|---------------------------------|
|Columns      |11-32x11 pt (22-64x22 px @2x)|12-37x12 pt (24-74x24 px @2x)|12.5-39x12.5 pt (25-78x25 px @2x)|14-42x14 pt (28-84x28 px @2x)|14.5-44x14.5 pt (29-88x29 px @2x)|
|Standard body|11-32x11 pt (22-64x22 px @2x)|12-37x12 pt (24-74x24 px @2x)|12.5-39x12.5 pt (25-78x25 px @2x)|14-42x14 pt (28-84x28 px @2x)|14.5-44x14.5 pt (29-88x29 px @2x)|
|Table        |11-32x11 pt (22-64x22 px @2x)|12-37x12 pt (24-74x24 px @2x)|12.5-39x12.5 pt (25-78x25 px @2x)|14-42x14 pt (28-84x28 px @2x)|14.5-44x14.5 pt (29-88x29 px @2x)|

<a id="Extra-large"></a>
### Extra large

Use larger text/images for X-Large faces. Stack widths are maxima.

|Image      |38mm                     |40mm/42mm                      |41mm                           |44mm                       |45mm/49mm                     |
|-----------|-------------------------|-------------------------------|-------------------------------|---------------------------|------------------------------|
|Ring       |63x63 pt (126x126 px @2x)|66.5x66.5 pt (133x133 px @2x)  |70.5x70.5 pt (141x141 px @2x)  |73x73 pt (146x146 px @2x)  |79x79 pt (158x158 px @2x)     |
|Simple     |91x91 pt (182x182 px @2x)|101.5x101.5 pt (203x203 px @2x)|107.5x107.5 pt (215x215 px @2x)|112x112 pt (224x224 px @2x)|121x121 pt (242x242 px @2x )  |
|Stack      |78x42 pt (156x84 px @2x) |87x45 pt (174x90 px @2x)       |92x47.5 pt (184x95 px @2x)     |96x51 pt (192x102 px @2x)  |103.5x53.5 pt (207x107 px @2x)|
|Placeholder|91x91 pt (182x182 px @2x)|101.5x101.5 pt (203x203 px @2x)|107.5x107.5 pt (215x215 px @2x)|112x112 pt (224x224 px @2x)|121x121 pt (242x242 px @2x)   |

<a id="Platform-considerations"></a>
## Platform considerations

Complications are watchOS experiences, unsupported in iOS, iPadOS, macOS, tvOS, and visionOS. Lock Screen accessories on other platforms share design concepts but are widgets.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Watch faces](https://developer.apple.com/design/human-interface-guidelines/watch-faces)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/WidgetKit>

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2023/10309>
  <https://developer.apple.com/videos/play/wwdc2022/10051>
  <https://developer.apple.com/videos/play/wwdc2022/10050>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: October 24, 2023, June 5, 2023, September 14, 2022.
