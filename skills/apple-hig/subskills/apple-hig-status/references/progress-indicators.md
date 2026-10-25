# Progress indicators

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/progress-indicators)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Progress UI is temporary feedback during work, disappearing when it finishes. Determinate indicators represent measurable completion with a leading-to-trailing bar or clockwise circular fill. Indeterminate indicators communicate ongoing activity without a completion estimate; every platform has a spinner, and macOS also has an indeterminate bar.

<a id="Best-practices"></a>
## Best practices

Prefer measurable progress when possible and report it honestly. Estimate the whole operation so an early sprint to 90% does not conceal a much longer final stage. Keep activity visibly ongoing, and explain stalls with a useful recovery route. When duration becomes known, an indeterminate bar can become determinate; avoid changing a spinner into a differently shaped bar midtask because that disrupts layout and interpretation.

Add a short, specific task description only when it supplies real context. Choose a consistent place for status. Allow cancellation where it is safe; offer pause as well when cancel would discard useful partial work. Explain consequential cancellation and let the person either confirm it or resume.

<a id="Platform-considerations"></a>
## Platform considerations

No additional tvOS or visionOS rules are specified.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

<a id="Refresh-content-controls"></a>
#### Refresh content controls

Pull-to-refresh reveals an activity indicator when people drag down a content view. It supplements periodic automatic refreshes rather than making users responsible for every update. An optional title should convey useful content context, such as the previous update time, rather than explaining the pull gesture or merely restating that loading is occurring.

<a id="macOS"></a>
### macOS

Both animated bars and spinners can represent indeterminate work. Prefer a small spinner for asynchronous background operations or tight spaces, such as beside a control or within a field. Usually omit spinner labels when the initiating action already explains the activity.

<a id="watchOS"></a>
### watchOS

Progress bars, circular fills, and spinners default to white against the scene background. Tint can customize their color.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/ProgressView> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UIProgressView> — UIKit
<https://developer.apple.com/documentation/UIKit/UIActivityIndicatorView> — UIKit
<https://developer.apple.com/documentation/UIKit/UIRefreshControl> — UIKit
<https://developer.apple.com/documentation/AppKit/NSProgressIndicator> — AppKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: September 12, 2023, June 5, 2023.
