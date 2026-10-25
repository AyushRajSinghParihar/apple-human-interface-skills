# Context menus

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/context-menus)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Context menus expose a few likely actions for a specific item. They are hidden conveniences, revealed through familiar touch/pinch-and-hold, Control-click, or secondary-click interactions appropriate to the platform.

<a id="Best-practices"></a>
## Best practices

Prioritize likely current tasks rather than advanced unrelated commands. Keep menus short and apply them consistently to comparable objects. Every command must also be available through the visible interface or, on Mac, main menus. Use at most one submenu level with predictive titles, and generally no more than three separated groups. Hide unavailable contextual actions; macOS Cut, Copy, and Paste may remain dimmed exceptions. Put frequent actions nearest the point where scanning begins, potentially reversing order when a menu opens above versus below its source. Show keyboard equivalents in main menus rather than here. On iOS, iPadOS, and visionOS, put destructive commands at the end and mark their destructive role.

<a id="Content"></a>
## Content

Use short action labels and standard familiar glyphs consistently. A menu usually needs no title; add one only to clarify scope, such as the number of selected objects affected.

<a id="Platform-considerations"></a>
## Platform considerations

No additional tvOS rules are specified. Context menus are unsupported in watchOS.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Give an object either a context menu or an edit menu to avoid ambiguous gestures. On iPad, an empty-area context menu can create a new object. A graphical preview should confirm the target; it can sometimes open or be dragged elsewhere. Match its clipping path to its actual shape so corners and contours remain stable through the system emergence animation.

<a id="macOS"></a>
### macOS

The platform also uses the term contextual menu. Keep commands available through the menu bar.

<a id="visionOS"></a>
### visionOS

Context menus can replace frequently used inspector/panel tools to reduce separate windows. Generally keep menu height within the parent window height so system controls above and below remain accessible. Specialist apps may justify more contextual commands than simple-task experiences, but still balance access and scan time.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Menus](https://developer.apple.com/design/human-interface-guidelines/menus)
[Edit menus](https://developer.apple.com/design/human-interface-guidelines/edit-menus)
[Pop-up buttons](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons)
[Pull-down buttons](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/View/contextMenu(menuItems:)> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UIContextMenuInteraction> — UIKit
<https://developer.apple.com/documentation/AppKit/NSMenu/popUpContextMenu(_:with:for:)> — AppKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: December 5, 2023, June 21, 2023, September 14, 2022.
