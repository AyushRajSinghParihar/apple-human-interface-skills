# Split views

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/split-views)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A split view coordinates adjacent content panes. Selection in a primary pane can reveal children in a secondary pane, and another selection can reveal detail in a tertiary pane. It can also position supporting tools around a main canvas.

<a id="Best-practices"></a>
## Best practices

Persist the selected appearance in each navigation pane so the relationship to detail remains clear. Consider cross-pane drag and drop for moving content between visible levels or collections.

<a id="Platform-considerations"></a>
## Platform considerations

<a id="iOS"></a>
### iOS

Prefer multiple simultaneous panes in regular-width environments. Compact portrait layouts otherwise risk clipped, wrapped, and hard-to-operate content.

<a id="iPadOS"></a>
### iPadOS

Two- and three-pane vertical arrangements are available. Design the transitions across narrow, compact, and intermediate window sizes, preserving a logical route among panes as windows resize fluidly.

<a id="macOS"></a>
### macOS

Panes can stack vertically, sit side by side, or combine both arrangements. Dividers can resize panes. Choose useful minimum and maximum sizes that keep dividers visible and operable. Allow supporting panes to hide when that helps editing, and provide several restoration routes, such as a toolbar control plus a menu command and shortcut. Prefer the 1-point thin divider for space efficiency; a stronger divider can be appropriate when adjacent table rules would obscure it.

<a id="tvOS"></a>
### tvOS

Use a primary filter pane and secondary results pane where helpful. Standard proportions are one-third/two-thirds, with an equal split also available; choose visual balance. Use one overall title rather than separate instructional titles for each pane. Center the title in the window for a secondary content collection; when a single important secondary view needs space, consider placing the title above the primary pane.

<a id="visionOS"></a>
### visionOS

Prefer a split view for supplementary information that belongs to the current context. A separate window adds positioning and relationship-management demands. For a small required input or self-contained task that must precede continuation, use a sheet.

<a id="watchOS"></a>
### watchOS

The list and detail each occupy the full screen rather than appearing adjacent. Launch directly into the most relevant detail based on factors such as location, time, or recent activity. Put multiple detail pages into a vertical tab view so the Digital Crown can move between them; the system page indicator beside the crown shows count and current position.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Sidebars](https://developer.apple.com/design/human-interface-guidelines/sidebars)
[Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars)
[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/NavigationSplitView> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UISplitViewController> — UIKit
<https://developer.apple.com/documentation/AppKit/NSSplitViewController> — AppKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2025/282>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 9, 2025, December 5, 2023, June 5, 2023.
