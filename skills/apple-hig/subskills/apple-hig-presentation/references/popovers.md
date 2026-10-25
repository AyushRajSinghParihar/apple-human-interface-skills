# Popovers

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/popovers)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A popover transiently exposes a small related set of information or tasks above content after a control or interactive region is activated.

<a id="Best-practices"></a>
## Best practices

Use it for temporary functionality instead of a persistent space-consuming panel or sidebar. Point its arrow closely at its source while keeping that source and essential reference content visible. Supply Close, Done, or Cancel only when the choice clarifies confirmation or saving; ordinary dismissal can happen outside the bounds or after a choice. Keep multi-selection popovers open until explicitly dismissed. Automatic nonmodal dismissal must save work; discard changes only through explicit Cancel.

Show one popover at a time without cascading another from it. Close the current one before opening a replacement, ideally in a single activation. Only an alert may appear above a popover. Keep dimensions limited to the content, and animate size changes to preserve the impression of one continuing view. Describe tasks rather than using popover terminology in help. Use an alert for warnings because popovers are easy to miss or dismiss accidentally.

<a id="Platform-considerations"></a>
## Platform considerations

No additional visionOS rules are specified. Popovers are unsupported in tvOS and watchOS.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Reserve popovers for wide layouts. Adapt compact layouts to use the available screen with a modal sheet or other suitable full-screen presentation.

<a id="macOS"></a>
### macOS

Consider detachable popovers when people may need to keep information visible while doing other work. Dragging can turn the popover into a panel; change its appearance minimally so the relationship remains clear.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets)
[Action sheets](https://developer.apple.com/design/human-interface-guidelines/action-sheets)
[Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts)
[Modality](https://developer.apple.com/design/human-interface-guidelines/modality)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/View/popover(isPresented:attachmentAnchor:arrowEdge:content:)> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UIPopoverPresentationController> — UIKit
<https://developer.apple.com/documentation/AppKit/NSPopover> — AppKit
