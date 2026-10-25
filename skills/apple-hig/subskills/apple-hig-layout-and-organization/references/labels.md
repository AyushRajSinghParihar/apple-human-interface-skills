# Labels

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/labels)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A label presents short, uneditable text, including an action name, list-item description, or context for nearby controls. SwiftUI provides both Text and Label; component-specific guidance may further constrain the wording.

<a id="Best-practices"></a>
## Best practices

Use a text field for a short editable value and a text view for longer or richly formatted content. Prefer system typography and retain Dynamic Type support where available; check readability whenever introducing custom fonts or styling. Permit selection and copying when the text conveys useful portable information such as an error, address, or location.

Use semantic label colors to express hierarchy rather than hard-coded tones:

| Role | Typical use | UIKit name | AppKit name |
| --- | --- | --- | --- |
| Primary | Main information | label | labelColor |
| Secondary | Supporting text or subheading | secondaryLabel | secondaryLabelColor |
| Tertiary | Description of unavailable behavior | tertiaryLabel | tertiaryLabelColor |
| Quaternary | Watermark | quaternaryLabel | quaternaryLabelColor |

The UIKit column applies to iOS, iPadOS, tvOS, and visionOS.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, iPadOS, tvOS, or visionOS rules are specified.

<a id="macOS"></a>
### macOS

An NSTextField configured as noneditable can display label text.

<a id="watchOS"></a>
### watchOS

Use system date/time and timer text components for changing temporal information. Date text supports formats, calendars, and time zones; timer text supports count-up and countdown formats. The system adapts presentation to available space and updates values without further app work. These components are also useful in complications.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields)
[Text views](https://developer.apple.com/design/human-interface-guidelines/text-views)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/Label> — SwiftUI
<https://developer.apple.com/documentation/SwiftUI/Text> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UILabel> — UIKit
<https://developer.apple.com/documentation/AppKit/NSTextField> — AppKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 5, 2023.
