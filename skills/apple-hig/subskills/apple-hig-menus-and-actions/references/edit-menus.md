# Edit menus

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/edit-menus)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Edit menus operate on selected text, images, files, and other content with commands such as copy, translation, and lookup. Data detection can add contextual actions, such as directions for an address.

On iOS, selection gestures reveal a compact horizontal menu that can expand through a trailing chevron. iPad touch uses that layout; keyboard/pointer interactions open a vertical context-style menu. Mac offers contextual editing and the menu-bar Edit menu. visionOS offers pinch-and-hold horizontal or contextual editing. tvOS and watchOS do not provide this component.

<a id="Best-practices"></a>
## Best practices

Use the system edit menu and its expected activation gestures. Remove or dim irrelevant commands, including selection-dependent actions without a selection and Paste when no paste content exists. Put custom commands near related standard commands, such as custom formatting after system formatting, and avoid excessive additions. Allow useful static content to copy, while normally keeping control labels unselectable. Support undo/redo rather than confirmations before menu actions. Avoid redundant editing controls that crowd out unfamiliar functionality. Distinguish Delete, which removes content, from Cut, which first places it on the pasteboard.

<a id="Content"></a>
## Content

Name custom actions with concise verbs or verb phrases.

<a id="Platform-considerations"></a>
## Platform considerations

No additional visionOS rules are specified. Edit menus are unsupported in tvOS and watchOS.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Verify both horizontal touch and vertical keyboard/pointer presentations. The system chooses above/below-selection placement and its pointing indicator; adjust position when necessary to avoid essential content, without changing menu or pointer shape.

<a id="macOS"></a>
### macOS

Follow the standard menu-bar Edit ordering documented in The menu bar.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Menus](https://developer.apple.com/design/human-interface-guidelines/menus)
[Context menus](https://developer.apple.com/design/human-interface-guidelines/context-menus)
[The menu bar](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar)
[Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/UIKit/UIEditMenuInteraction> — UIKit
<https://developer.apple.com/documentation/AppKit/NSMenu> — AppKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 21, 2023, September 14, 2022.
