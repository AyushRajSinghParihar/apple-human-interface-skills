# Tab views

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/tab-views)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A tab view swaps mutually exclusive, related panes within a shared content area. This article's pane-switching component is distinct from an app's top-level tab bar.

<a id="Best-practices"></a>
## Best practices

Keep panes closely related and self-contained: controls inside one pane affect that pane. Label tabs to predict their contents, generally with short nouns or noun phrases in title case; a short action phrase can suit some contexts. A visible tab control exposes choices and takes one activation, whereas a pop-up hides choices and takes two. Avoid exceeding six tabs; already at six or more, evaluate a different presentation such as a pop-up containing view choices.

<a id="Anatomy"></a>
## Anatomy

The tab control normally sits on the top edge of the content. Hide it only when the app switches panes programmatically. Without visible tabs, the content can have a bezel, a line border, or no border; borderless content can be opaque or transparent. Normally inset the whole view with window-body margins on every side, leaving room for unrelated controls. Extending it to the window edge is possible but unusual.

<a id="Platform-considerations"></a>
## Platform considerations

The conventional tab-view component is unsupported in iOS, iPadOS, tvOS, and visionOS; macOS supplies the pane-style control.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Evaluate a segmented control for a similar switch among related views.

<a id="watchOS"></a>
### watchOS

SwiftUI tab views use page controls. The indicator beside the Digital Crown identifies pages and can enlarge the active dot to show that its content can scroll as well as move between pages.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars)
[Segmented controls](https://developer.apple.com/design/human-interface-guidelines/segmented-controls)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/TabView> — SwiftUI
<https://developer.apple.com/documentation/AppKit/NSTabView> — AppKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 5, 2023.
