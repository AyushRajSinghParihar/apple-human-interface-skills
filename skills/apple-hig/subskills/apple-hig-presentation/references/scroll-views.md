# Scroll views

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/scroll-views)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A scroll view reveals content beyond its bounds through vertical or horizontal movement. The container is visually neutral; transient indicators communicate position and scrolling, with platform-specific behavior.

<a id="Best-practices"></a>
## Best practices

Keep system gestures, keyboard shortcuts, and elastic feedback. Suggest offscreen content with partial items at edges because indicators are not always visible. Avoid nested scrolling on the same axis; orthogonal nested scrolling is acceptable. Page-by-page movement can suit fixed chunks; retain a small overlap, such as a line or part of an image, to preserve context.

Automatically reveal hidden relevant content when locating a search result, typing at an offscreen insertion point, extending selection beyond an edge, or acting on a selection after scrolling away. Move only as far as needed; a partially visible selection need not be fully recentered. Bound zoom to useful minimum and maximum scales.

<a id="Scroll-edge-effects"></a>
## Scroll edge effects

In iOS, iPadOS, and macOS, edge effects separate floating UI from scrolling content beneath. Prefer automatic styling; it provides stronger separation for dense toolbars, uncontained text, or pinned headers. Thoroughly test legibility if choosing soft styling. The hard style gives a more defined opaque boundary; the soft style fades through a variable blur. Use an effect only where floating controls overlap a scroll view, not as decoration or a dark overlay. Apply one per view; split panes can each have one, with aligned heights.

<a id="Platform-considerations"></a>
## Platform considerations

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

A page control can show position in paged scrolling. Suppress the scroll indicator on that same axis to avoid redundant signals.

<a id="macOS"></a>
### macOS

Scroll indicators are also called scroll bars. Small or mini bars can suit tight panels; match other control sizes in that panel.

<a id="tvOS"></a>
### tvOS

Scrolling follows focus automatically to keep focused content visible, without distinct scroll-view objects and indicators.

<a id="visionOS"></a>
### visionOS

A small fixed-size indicator stays at the vertical center of the trailing edge or horizontal center of the bottom edge. Swiping reveals it; looking and dragging it enables a jog bar that adjusts scrolling speed rather than absolute position, with tick marks communicating acceleration. Allow adequate margin because this indicator is slightly thicker than on iOS.

<a id="Look-to-Scroll"></a>
#### Look to Scroll

Eye-only scrolling starts near a scroll boundary and coexists with gestures. Opt in separately for each reading or browsing scroll view; the behavior is not automatic. Avoid it for secondary controls or dense views needing precise quick movement. Apply it consistently across comparable content. Full-width or full-height regions give generous, understandable boundaries; inset regions need clear edges. Remove custom scroll-position effects such as parallax or animation before enabling it to prevent unpredictable behavior.

<a id="watchOS"></a>
### watchOS

Prefer vertical content that works with the Digital Crown. Use vertical tab views for page-based navigation, with an indicator beside the crown. Keep pages near one screen tall when possible; long pages can scroll and the page indicator expands into a scroll indicator. Use variable heights sparingly and preferably after short fixed pages.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Page controls](https://developer.apple.com/design/human-interface-guidelines/page-controls)
[Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures)
[Pointing devices](https://developer.apple.com/design/human-interface-guidelines/pointing-devices)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/ScrollView> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UIScrollView> — UIKit
<https://developer.apple.com/documentation/AppKit/NSScrollView> — AppKit
<https://developer.apple.com/documentation/WatchKit/WKPageOrientation> — WatchKit
<https://developer.apple.com/documentation/SwiftUI/ScrollInputKind/look> — SwiftUI

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 8, 2026, March 24, 2026, July 28, 2025, February 2, 2024, December 5, 2023, June 5, 2023.
