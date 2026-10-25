# Pull-down buttons

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A pull-down presents commands or items directly related to the button's purpose and closes after selection. Examples include choosing what to add, the sort attribute, or an earlier navigation destination.

<a id="Best-practices"></a>
## Best practices

Use a pop-up instead for a flat mutually exclusive noncommand choice. Keep primary actions directly discoverable rather than hiding the entire view's functionality in one button. Aim for at least three menu items to justify the reveal step; one or two often work better as separate buttons or toggles. Avoid excessively long menus. Add a title only when button and item labels fail to explain the list. Mark destructive choices and confirm intent: iOS uses an action sheet and iPadOS a popover for this confirmation. Add familiar symbols where they clarify meaning and preserve text alignment across scales.

<a id="Platform-considerations"></a>
## Platform considerations

No additional macOS or visionOS rules are specified. Pull-down buttons are unsupported in tvOS and watchOS.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

A familiar button can additionally reveal related actions through touch-and-hold, as Safari does for tabs. A More/ellipsis button can collect secondary actions in limited space, but its contents are hard to predict, so balance compactness against discovery.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Pop-up buttons](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons)
[Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)
[Menus](https://developer.apple.com/design/human-interface-guidelines/menus)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/MenuPickerStyle> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UIControl/showsMenuAsPrimaryAction> — UIKit
<https://developer.apple.com/documentation/AppKit/NSPopUpButton/pullsDown> — AppKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: September 14, 2022.
