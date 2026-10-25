# Sidebars

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/sidebars)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A leading sidebar navigates app areas or top-level collections. It consumes substantial space, so consider a tab bar or a tab bar that converts to a sidebar when that better serves content.

<a id="Best-practices"></a>
## Best practices

Extend rich content under floating Liquid Glass sidebars on iOS, iPadOS, and macOS, either through horizontal scrolling or the background extension effect that mirrors adjacent content. Let people customize important destinations and order where feasible. Use disclosure to contain large hierarchies; generally keep the sidebar to two levels and introduce a middle content-list pane for deeper structures. Name groups with short, descriptive labels.

Use familiar SF Symbols or a custom symbol rather than a bitmap where possible. Respect accent-color expectations, particularly the person's system accent on macOS. A rare fixed color can call out meaningful exceptions, such as an important category, but should have a reason.

Allow hiding when useful and support familiar restoration: edge swipe on iPad, a button and View-menu commands on Mac. Keep the sidebar initially discoverable. In visionOS the window typically expands for it, so hiding is rarely necessary.

<a id="Platform-considerations"></a>
## Platform considerations

No additional tvOS rules are specified. Sidebars are unsupported in watchOS.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

A sidebar-adaptable TabView can start as either tabs or a sidebar and includes a conversion button, adapting to platform, rotation, and width. For a sidebar without tab conversion, use NavigationSplitView or UISplitViewController. Evaluate tab navigation first for content space and frequent destinations; expose less-used areas through its convertible sidebar when needed. A UIKit collection-list sidebar should use the sidebar appearance.

<a id="macOS"></a>
### macOS

Sidebar row, text, and glyph dimensions follow small, medium, or large sizing; people can change sidebar icon size in settings. Automatically collapsing/revealing the sidebar as the window changes size can preserve content space. Keep critical actions and information away from the bottom because people may position the window with its bottom edge offscreen.

<a id="visionOS"></a>
### visionOS

A sidebar inside a tab can support a deep hierarchy. Its selections must stay within that tab rather than switching top-level tabs.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Split views](https://developer.apple.com/design/human-interface-guidelines/split-views)
[Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars)
[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/TabViewStyle/sidebarAdaptable> — SwiftUI
<https://developer.apple.com/documentation/SwiftUI/NavigationSplitView> — SwiftUI
<https://developer.apple.com/documentation/SwiftUI/ListStyle/sidebar> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UICollectionLayoutListConfiguration-swift.struct> — UIKit
<https://developer.apple.com/documentation/AppKit/NSSplitViewController> — AppKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2025/208>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 8, 2026, June 9, 2025, August 6, 2024, December 5, 2023, June 21, 2023.
