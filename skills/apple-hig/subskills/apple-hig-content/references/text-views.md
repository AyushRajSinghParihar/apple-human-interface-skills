# Text views

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/text-views)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A text view handles multiple lines, rich styling, scrolling, and optional editing. Content normally starts at the leading edge and uses the system label color. Editing invokes a keyboard in iOS, iPadOS, and visionOS.

<a id="Best-practices"></a>
## Best practices

Choose a text view for lengthy, editable, or specially formatted content. Use a label for short static text and a text field for short editable input. Styling must preserve reading comfort: adopt Dynamic Type and check accessibility settings such as Bold Text. Allow selection and copying when the text contains information people may need elsewhere, including error details, identifiers, or network addresses.

<a id="Platform-considerations"></a>
## Platform considerations

The source adds no separate macOS, visionOS, or watchOS rules.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Match the virtual keyboard to the expected input so entry is efficient and relevant characters are easy to reach.

<a id="tvOS"></a>
### tvOS

Use text views to display content. Editable tvOS text belongs in text fields; the platform deliberately minimizes text entry.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Labels](https://developer.apple.com/design/human-interface-guidelines/labels)
[Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields)
[Combo boxes](https://developer.apple.com/design/human-interface-guidelines/combo-boxes)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/Text> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UITextView> — UIKit
<https://developer.apple.com/documentation/AppKit/NSTextView> — AppKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 5, 2023.
