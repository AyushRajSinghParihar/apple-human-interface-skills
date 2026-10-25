# Color wells

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/color-wells)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A color well opens a system or custom picker for changing the color of text, shapes, guides, and other content.

<a id="Best-practices"></a>
## Best practices

Prefer evaluating the system picker first. It provides familiar behavior across iOS, iPadOS, and macOS, and gives people saved colors accessible across apps.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, iPadOS, or visionOS rules are specified. Color wells are unsupported in tvOS and watchOS.

<a id="macOS"></a>
### macOS

Activation highlights the well, opens the picker, and updates the displayed swatch after selection. Preserve color drag and drop between wells and from the picker to a well.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Color](https://developer.apple.com/design/human-interface-guidelines/color)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/UIKit/UIColorWell> — UIKit
<https://developer.apple.com/documentation/UIKit/UIColorPickerViewController> — UIKit
<https://developer.apple.com/documentation/AppKit/NSColorWell> — AppKit
[Color Programming Topics](https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/DrawColor/DrawColor.html)
