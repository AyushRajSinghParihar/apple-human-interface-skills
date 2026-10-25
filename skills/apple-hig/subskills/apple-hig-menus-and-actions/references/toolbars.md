# Toolbars

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/toolbars)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Toolbars group frequent actions, current-view titles, navigation, and search along a view edge. A tab bar instead changes top-level destinations.

<a id="Best-practices"></a>
## Best practices

Choose controls deliberately and define overflow priority as width shrinks. Mac/iPad add system overflow automatically; do not add a second manual overflow or overflow by default. More is for genuinely secondary actions after trying to fit important ones. Allow customization on Mac/iPad when extensive tools and long sessions make personal workflows valuable. Retain system backgrounds and restrained tint; use content beneath and scroll-edge effects to establish separation. Prefer standard components with concentric corner radii. Contextual hiding can support focused viewing, provided reliable restoration is available.

<a id="Titles"></a>
## Titles

Name the content or location to orient navigation and distinguish windows. Omit a redundant title where content itself suffices, but name separate windows for identification. Avoid the app name as a title. Aim for a short word/phrase under 15 characters to preserve room for controls.

<a id="Navigation"></a>
## Navigation

Put hierarchical navigation at the top. Use standard symbol-only Back and Close controls for returning within hierarchy versus dismissing a modal. Custom controls must preserve their recognizable appearance and behavior consistently.

<a id="Actions"></a>
## Actions

Prioritize main tasks and meaningful objects. Prefer recognizable, borderless system symbols; use words where a glyph cannot explain an action such as Edit. The enclosing group already supplies a boundary and system interaction states. Use one prominent primary action, such as Done/Submit, at the trailing side.

<a id="Item-groupings"></a>
## Item groupings

Leading items contain Back/sidebar controls, the title, and an optional document-wide menu such as Rename/Move/Export; these navigation essentials are not customizable. The center contains common tools and possibly the title, supports customization on Mac/iPad, and collapses into system overflow. Trailing items contain persistent essentials, nearby-inspector controls, optional search, More/customization, and a primary action.

Pin items to their intended region and group by function/frequency. Keep navigation and critical completion/dismissal controls in distinct familiar sections. Maintain comparable placement across platforms and generally no more than three groups. Separate textual actions from adjacent glyph actions and from other text buttons with fixed spacing so they do not read as one combined control.

<a id="Platform-considerations"></a>
## Platform considerations

No additional tvOS rules are specified.

<a id="iOS"></a>
### iOS

Include essential actions first and place secondary ones in More. Large titles can collapse while scrolling and expand at the top to reinforce location.

<a id="iPadOS"></a>
### iPadOS

A toolbar and tab bar can share the top horizontal region, preserving full content width while retaining actions and section switching.

<a id="macOS"></a>
### macOS

Toolbars sit in the top window frame below or integrated with the title area; items are bezel-free. Every toolbar action must also exist in the menu bar because the toolbar can hide or be customized. Menu commands need not all become toolbar items.

<a id="visionOS"></a>
### visionOS

The standard toolbar sits at the bottom, above window-management controls and slightly forward of the window, using variable blur for legibility. Glyph items reveal labels on look. Prefer this system placement and eye/hand behavior. Avoid vertical bars because tabs already occupy that form. Prevent shrinking below essential toolbar width since no app menu bar provides a fallback. Modal editing can use contextual tools, restoring normal tools on exit. Avoid toolbar pull-downs because they are hard to discover and can cover window controls below.

<a id="watchOS"></a>
### watchOS

Top-corner and bottom toolbar controls stay visible above scrolling content. A scrolling primaryAction toolbar button instead appears when scrolling upward to the top. Use that location for an important related action that is not the view's main purpose, such as Compose above an inbox.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Sidebars](https://developer.apple.com/design/human-interface-guidelines/sidebars)
[Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars)
[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
[Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)
[Search fields](https://developer.apple.com/design/human-interface-guidelines/search-fields)
[Apple Design Resources](https://developer.apple.com/design/resources/)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/Toolbars> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UIToolbar> — UIKit
<https://developer.apple.com/documentation/AppKit/NSToolbar> — AppKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2025/356>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: December 16, 2025, June 9, 2025, June 21, 2023, June 5, 2023.
