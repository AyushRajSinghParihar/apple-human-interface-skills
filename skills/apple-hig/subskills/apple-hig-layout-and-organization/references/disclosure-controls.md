# Disclosure controls

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Disclosure controls progressively reveal information or functionality associated with a view or control.

<a id="Best-practices"></a>
## Best practices

Keep common information and actions visible at the top level. Hide advanced or occasional details until needed, reducing the amount people must initially interpret.

<a id="Disclosure-triangles"></a>
## Disclosure triangles

A triangle reveals a view's details or a hierarchy's children. Its collapsed direction is inward from the leading edge; its expanded direction is down. Activation switches state and resizes the view to fit. Supply an informative label that predicts the revealed content, such as advanced configuration options.

<a id="Disclosure-buttons"></a>
## Disclosure buttons

A button expands functionality associated with a particular control, as in the location-navigation expansion of a macOS Save sheet. Unlike a disclosure triangle, this control points down when collapsed and up when expanded. Put it beside the content it controls and use at most one such button in a view; several independent expansion buttons make the relationship harder to understand.

<a id="Platform-considerations"></a>
## Platform considerations

No additional macOS rules are specified. Disclosure controls are unsupported in tvOS and watchOS.

<a id="iOS-iPadOS-visionOS"></a>
### iOS, iPadOS, visionOS

SwiftUI DisclosureGroup supplies the platform's disclosure-control behavior.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Outline views](https://developer.apple.com/design/human-interface-guidelines/outline-views)
[Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)
[Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/DisclosureGroup> — SwiftUI
<https://developer.apple.com/documentation/AppKit/NSButton/BezelStyle-swift.enum/disclosure> — AppKit
<https://developer.apple.com/documentation/AppKit/NSButton/BezelStyle-swift.enum/pushDisclosure> — AppKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2020/10031>
