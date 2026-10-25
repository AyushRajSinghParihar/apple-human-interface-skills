# Tab bars

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/tab-bars)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A tab bar exposes top-level destinations while preserving each section's navigation state.

<a id="Best-practices"></a>
## Best practices

Use tabs for destinations and toolbars for actions on current content. Keep tabs available while navigating sections, except when a temporary modal covers them. Choose enough destinations for real needs while keeping navigation manageable; evaluate a convertible sidebar for complex structures. Avoid overflow/More destinations because they hide content and slow access. Keep empty destinations present and explain their unavailable content instead of hiding or disabling tabs.

Supply short, preferably single-word labels and scalable icons, usually filled SF Symbols. Compact layouts put the glyph above text; regular layouts can place them side by side. Custom dimensions are specified in Apple Design Resources. Reserve red badges with a number or exclamation point for information that truly needs attention. Ensure tab labels separate visually from colorful content below; monochrome or a differentiated accent can preserve that distinction.

<a id="Platform-considerations"></a>
## Platform considerations

macOS has no additional rules. Tab bars are unsupported in watchOS; watch tab views use a different page-based presentation.

<a id="iOS"></a>
### iOS

The bar floats at the bottom on Liquid Glass. With an attached accessory such as a mini-player, scrolling can minimize tabs and place the accessory inline. Tapping a tab or returning to the top restores expansion. A dedicated search tab can sit at the trailing end.

<a id="iPadOS"></a>
### iPadOS

Tabs appear near the top and may stay fixed or convert into a sidebar through a button. A sidebar-only design uses a navigation split view. Prefer tabs for common sections and allow sidebar conversion for a broader hierarchy. When customization is useful, let people add frequent destinations and remove less useful ones; begin with five or fewer default tabs to retain continuity across compact and regular widths.

<a id="tvOS"></a>
### tvOS

Backgrounds, fonts, selected/unselected tints, and glyphs such as search/settings can be customized. The default bar is translucent except for the selected tab, which gains a focus shadow. Its height is fixed at 68 points and its top edge at 46 points from screen top. Overflow fades the rightmost content; a scrolling bar also gains a left-side fade.

A tab with one main view normally allows scrolling the bar away. Split-view tabs keep it pinned while panes scroll. Pressing Menu returns focus to the top tab bar. Live-viewing apps should order tabs as live content, recorded/cloud-DVR content, then other content.

<a id="visionOS"></a>
### visionOS

Tabs form a vertical floating bar fixed relative to the window's leading edge. Looking expands it; looking at a destination and tapping activates it. Expansion may temporarily obscure underlying content. Supply both a symbol and a short text label: symbols stay visible, labels appear during expansion. A sidebar can handle secondary hierarchy inside a tab, with selection confined to that tab.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Tab views](https://developer.apple.com/design/human-interface-guidelines/tab-views)
[Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars)
[Sidebars](https://developer.apple.com/design/human-interface-guidelines/sidebars)
[Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/TabView> — SwiftUI
<https://developer.apple.com/documentation/SwiftUI/TabViewBottomAccessoryPlacement> — SwiftUI
<https://developer.apple.com/documentation/SwiftUI/Enhancing-your-app-content-with-tab-navigation> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UITabBar> — UIKit
<https://developer.apple.com/documentation/UIKit/elevating-your-ipad-app-with-a-tab-bar-and-sidebar> — UIKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2025/356>
  <https://developer.apple.com/videos/play/wwdc2025/208>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 8, 2026, December 16, 2025, July 28, 2025, September 9, 2024, August 6, 2024, June 21, 2023.
