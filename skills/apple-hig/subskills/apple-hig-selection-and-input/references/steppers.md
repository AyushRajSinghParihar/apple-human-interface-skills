# Steppers

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/steppers)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A stepper has separate increase and decrease segments and requires a nearby display of its value.

<a id="Best-practices"></a>
## Best practices

Make the affected value unmistakable. Steppers suit small adjustments; add an editable field when someone may need to jump across a large range, such as changing the number of printed copies substantially.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, iPadOS, or visionOS rules are specified. Steppers are unsupported in tvOS and watchOS.

<a id="macOS"></a>
### macOS

For large ranges, consider accelerated Shift-click changes, such as increments ten times the normal step.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Pickers](https://developer.apple.com/design/human-interface-guidelines/pickers)
[Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/UIKit/UIStepper> — UIKit
<https://developer.apple.com/documentation/AppKit/NSStepper> — AppKit
