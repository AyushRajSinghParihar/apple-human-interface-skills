# Text fields

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/text-fields)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Use a text field for a short, specific value such as a name or email address. A text view is the better primitive for extended text.

<a id="Best-practices"></a>
## Best practices

- Explain purpose with a placeholder, and add a persistent external label where losing the placeholder during entry would make the field ambiguous.
- Use secure entry for sensitive content. Size fields to suggest expected input length; stack groups with even spacing and consistent widths where possible so labels remain clearly associated.
- Keep Tab traversal in the expected logical order, using system behavior unless a correction is needed.
- Validate at a useful moment. Email validation often belongs when leaving the field; username/password creation feedback should occur before leaving it. Reject values incompatible with the required format with understandable feedback.
- Use number formatters for numeric constraints and representations such as decimal precision, percentages, and currency, retaining locale-sensitive formatting.
- Choose overflow behavior intentionally: system defaults clip, but character/word wrapping or beginning/middle/end ellipses may better fit the task. An expansion tooltip can reveal full clipped content to a pointer user.
- Select the appropriate virtual keyboard for iOS, iPadOS, tvOS, and visionOS. Minimize both field count and lengthy entry on tvOS and watchOS; choices or buttons can gather information more efficiently.

<a id="Platform-considerations"></a>
## Platform considerations

No additional tvOS or visionOS rules are specified.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Offer a trailing Clear control to erase the current value in one action. Leading imagery can explain purpose; trailing buttons can offer extra functionality, such as bookmarking.

<a id="macOS"></a>
### macOS

A combo box is useful when free typing should coexist with a predefined set of likely choices.

<a id="watchOS"></a>
### watchOS

Request typed text only when necessary; prefer selecting an existing option.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Text views](https://developer.apple.com/design/human-interface-guidelines/text-views)
[Combo boxes](https://developer.apple.com/design/human-interface-guidelines/combo-boxes)
[Entering data](https://developer.apple.com/design/human-interface-guidelines/entering-data)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/TextField> — SwiftUI
<https://developer.apple.com/documentation/SwiftUI/SecureField> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UITextField> — UIKit
<https://developer.apple.com/documentation/AppKit/NSTextField> — AppKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 5, 2023.
