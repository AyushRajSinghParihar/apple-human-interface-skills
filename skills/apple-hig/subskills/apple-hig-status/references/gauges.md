# Gauges

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/gauges)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A gauge shows a numerical position within a range, optionally providing endpoints and other contextual information.

<a id="Anatomy"></a>
## Anatomy

The path can be circular or linear. Standard styles use a position indicator; capacity styles fill the path to the current value. Accessory variants resemble watch complications and can fit Lock Screen widgets or related compact presentations. macOS additionally has level indicators, which are related but distinct controls.

<a id="Best-practices"></a>
## Best practices

Provide concise descriptions of the value and both endpoints. Visible labels also help VoiceOver communicate meaning, even though styles differ in which labels they show. A meaningful gradient can explain a range, such as a cold-to-hot temperature scale.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, iPadOS, visionOS, or watchOS rules are specified. Gauges are unsupported in tvOS.

<a id="macOS"></a>
### macOS

Level indicators support capacity, rating, and rarely relevance. Continuous capacity uses a filled horizontal track; discrete capacity uses equally sized rectangles, one per capacity unit, with each fully filled or empty. Use continuous presentation when a large range would make individual segments too small. Capacity fill defaults to green; meaningful thresholds can change the entire fill or use tiered colors in the same indicator. A relevance indicator uses a shaded bar for comparisons such as search-result relevance. Rating presentation is covered separately in Rating indicators.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Ratings and reviews](https://developer.apple.com/design/human-interface-guidelines/ratings-and-reviews)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/Gauge> — SwiftUI
<https://developer.apple.com/documentation/AppKit/NSLevelIndicator> — AppKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: September 23, 2022.
