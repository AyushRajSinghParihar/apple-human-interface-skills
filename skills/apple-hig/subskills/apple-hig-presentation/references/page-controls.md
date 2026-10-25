# Page controls

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/page-controls)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A page control locates the current page among flat, ordered peers. Equally spaced dots are standard, with the current one filled; long sets can clip or scroll.

<a id="Best-practices"></a>
## Best practices

Use it for sequential peers rather than hierarchy or unrelated destinations. Center it horizontally near the view's bottom. Beyond about 10 pages, dots become difficult to count; evaluate a grid or other direct-access layout.

<a id="Customizing-indicators"></a>
## Customizing indicators

A special page can use a simple symbol, such as current location, instead of a dot. A changed default symbol should clarify the whole set's meaning. Keep at most two image types so users need not memorize many codes. Avoid fine inner lines, text, negative space, and complicated shapes that fail at small sizes. Let the system color indicators to preserve current-page contrast across backgrounds.

<a id="Platform-considerations"></a>
## Platform considerations

Page controls are unsupported in macOS.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

The control can shrink edge dots to signal hidden pages. Tapping beside the active indicator advances a page; iPad pointers can choose a particular indicator. Scrubbing traverses pages continuously, with dragging beyond an edge accelerating toward the first or last page. Animate discrete taps, but avoid animated page scrolling during rapid scrubbing because it causes flashes and lag.

Background styles are automatic (visible during interaction, for secondary navigation), prominent (always visible, for primary navigation), and minimal (never visible, for position-only feedback). Avoid enabling scrubbing with minimal styling because it lacks scrubbing feedback.

<a id="tvOS"></a>
### tvOS

Use page controls for full-screen peer pages. Extra controls can interfere with focus during page movement.

<a id="visionOS"></a>
### visionOS

Page controls communicate availability and position; they are not directly interactive.

<a id="watchOS"></a>
### watchOS

Horizontal pagination places indicators below; vertical tab views place them beside the Digital Crown and transition between within-page scrolling and between-page movement. Prefer purposeful vertical pages navigated by the crown over horizontal paging or deep hierarchies. Aim for one screen height per page; use taller pages sparingly and preferably after fixed-height ones.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Scroll views](https://developer.apple.com/design/human-interface-guidelines/scroll-views)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/PageTabViewStyle> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UIPageControl> — UIKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 21, 2023, June 5, 2023.
