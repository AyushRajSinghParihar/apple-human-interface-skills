# Menus

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/menus)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Menus reveal space-efficient commands, states, and options for the current selection or context. Familiar behavior matters for both native and custom menus; specialized menu components add their own rules.

<a id="Labels"></a>
## Labels

Write short, clear labels, normally title-case verbs for actions, with consistent product tone. Remove unnecessary articles. Show unavailable items dimmed in ordinary menus, and keep the menu openable even if all items are unavailable so its capabilities remain discoverable. Add an ellipsis when completion needs more information or a further choice. App menus can display keyboard equivalents; games often omit them because input devices and mappings vary.

<a id="Icons"></a>
## Icons

Use standard glyphs for common actions. Add icons only when meaningful: common features, locations/devices, visual transformations, or user content. Do not invent unrelated images merely to decorate labels. Within a logical group, give every item an icon or give none.

<a id="Organization"></a>
## Organization

Put frequent/important commands early, and separate logical groups with lines or gaps. Keep related commands together even when some are rarely used. Divide overly long menus or use a suitable submenu, but allow user-created/dynamic sets such as history or bookmarks to remain complete and scroll.

<a id="Submenus"></a>
## Submenus

Submenus can collapse repeated concepts, such as several Sort by commands under one Sort by label. Use them sparingly, normally at one level only. Beyond about five items in a submenu, evaluate a separate menu. Keep the parent openable even when all children are unavailable. Prefer real submenus over improvised indentation.

<a id="Toggled-items"></a>
## Toggled items

A changing action label can switch between Show and Hide. Use explicit verbs if labels such as HDR On could be mistaken for state descriptions. Showing both alternatives and disabling the inapplicable one can clarify some choices. Checkmarks communicate applied attributes; a reset command can clear several selected attributes at once.

<a id="In-game-menus"></a>
## In-game menus

Honor each platform's ordinary menu input, including touch and direct/indirect spatial gestures. Test typography and targets after adapting game rendering to other screens; scaling gameplay must not make menus unreadable or untappable.

<a id="Platform-considerations"></a>
## Platform considerations

No additional macOS, tvOS, or watchOS rules are specified.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Large/default menus list all items. Medium menus place three key actions in an icon-plus-short-label row above the rest. Small menus place four icon-only actions above the list; use them only for familiar tightly related commands such as text styles. Choose medium to accelerate three important actions, and ensure any unlabeled icons are recognizable.

<a id="visionOS"></a>
### visionOS

Menus support small and large layouts and can emerge from 3D content through SwiftUI. Keep them close to their target so people can see the effect after looking toward a command; window menus may extend beyond window bounds. A breakthrough effect can preserve access when 3D content occludes the menu. Prefer subtle, which automatic uses for overlapping 3D content. Prominent draws over the entire scene but can disrupt comfort; none preserves full occlusion for intentional scene mechanics while potentially reducing discoverability.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Pop-up buttons](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons)
[Pull-down buttons](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons)
[Context menus](https://developer.apple.com/design/human-interface-guidelines/context-menus)
[The menu bar](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/Menu> — SwiftUI
<https://developer.apple.com/documentation/UIKit/menus-and-shortcuts> — UIKit
<https://developer.apple.com/documentation/AppKit/menus> — AppKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 8, 2026, December 16, 2025, July 28, 2025, June 10, 2024, June 21, 2023, September 14, 2022.
