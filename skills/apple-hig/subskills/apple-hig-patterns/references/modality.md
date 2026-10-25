# Modality

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/modality)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A modal mode blocks its parent until explicitly dismissed. It can deliver critical information, clarify a recent action, support a narrow task, or focus attention on an immersive/complex activity. Alerts are available across platforms, while activity views, sheets, and confirmation dialogs or action sheets provide context-specific options. For a distinct task, iOS, iPadOS, and macOS commonly use a sheet or popover; iPadOS, macOS, and visionOS can also use a separate window. Fullscreen experiences can also be nonmodal.

<a id="Best-practices"></a>
## Best practices

Use modality only for a clear focus/decision benefit. Keep tasks brief and direct so the suspended context remains memorable. Avoid a miniature app inside the modal; if subviews are essential, offer one understandable route and distinguish back-navigation from dismissal. A fullscreen modal can suit substantial editing, camera, or media; in visionOS Shared Space it fills a window, while Full Space can create immersion.

Provide an obvious familiar exit: often a top control or downward swipe on iOS/iPadOS/watch, or a body control on Mac/tvOS. Before losing created content through either gesture or button, explain consequences and offer appropriate save/discard choices. Identify the task with a clear title and necessary guidance. Dismiss one modal before showing another, keeping only the necessary context; an alert can appear over other modal content, but never stack multiple alerts.

<a id="Platform-considerations"></a>
## Platform considerations

The source adds no separate rules for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets)
[Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts)
[Popovers](https://developer.apple.com/design/human-interface-guidelines/popovers)
[Action sheets](https://developer.apple.com/design/human-interface-guidelines/action-sheets)
[Activity views](https://developer.apple.com/design/human-interface-guidelines/activity-views)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/View-Presentation> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UIModalPresentationStyle> — UIKit
<https://developer.apple.com/documentation/AppKit/modal-windows-and-panels> — AppKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2025/356>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: December 5, 2023, June 21, 2023.
