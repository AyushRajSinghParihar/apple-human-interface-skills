# Pop-up buttons

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A pop-up button offers one choice from a flat list, then closes its menu and can display the selection.

<a id="Best-practices"></a>
## Best practices

Use it for mutually exclusive states or options. Use a pull-down when the list contains actions, multiple selections, or submenus. Start with a useful default, usually a likely choice. Let a button or introductory label explain the hidden list's purpose. This is efficient where space is limited and options need not remain visible. An occasional Custom option can open less-common choices without crowding the default interface; explanatory text can clarify the list if needed.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, macOS, or visionOS rules are specified. Pop-up buttons are unsupported in tvOS and watchOS.

<a id="iPadOS"></a>
### iPadOS

Inside a modal or popover, a pop-up can replace navigation through a row disclosure when a small well-defined option set fits a menu, avoiding a needless detail view.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Pull-down buttons](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons)
[Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)
[Menus](https://developer.apple.com/design/human-interface-guidelines/menus)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/MenuPickerStyle>  — SwiftUI
<https://developer.apple.com/documentation/UIKit/UIButton/changesSelectionAsPrimaryAction> — UIKit
<https://developer.apple.com/documentation/AppKit/NSPopUpButton> — AppKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: October 24, 2023, September 14, 2022.
