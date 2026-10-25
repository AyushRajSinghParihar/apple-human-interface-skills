# Printing

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/printing)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Use system printing on iOS, iPadOS, macOS, and visionOS when the content benefits, adding only necessary document/printer options.

<a id="Best-practices"></a>
## Best practices

Put Print where expected: Mac File, optionally a customizable toolbar item, and an iOS/iPadOS toolbar action that opens the relevant action sheet. When nothing can print or no printer is available, dim the Mac menu command, remove the mobile sheet action, and dim/hide a custom control. Present only relevant supported options such as page range, copies, and duplex through the system view.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, iPadOS, or visionOS rules are specified. Printing is unsupported in tvOS and watchOS.

<a id="macOS"></a>
### macOS

Put genuinely custom settings in a clearly named print-panel category. A document-specific Page Setup can contain infrequently changed size/orientation/scaling without duplicating system features. Make incompatible choices clear, such as transparency versus duplex. Put rare advanced settings behind an Advanced Options disclosure. Preview the effect of adjustments when useful and retain changed settings with the document, at least until it closes.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[File management](https://developer.apple.com/design/human-interface-guidelines/file-management)
[File menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#File-menu)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/UIKit/UIPrintInteractionController> — UIKit
<https://developer.apple.com/documentation/AppKit/NSDocument> — AppKit
