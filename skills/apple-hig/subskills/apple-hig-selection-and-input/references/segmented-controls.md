# Segmented controls

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/segmented-controls)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A segmented control groups two or more related buttons, usually at equal widths. It can represent a single choice; macOS also supports multiple simultaneous choices. A momentary control can instead perform related actions without retaining selection.

<a id="Best-practices"></a>
## Best practices

Use segments for related object attributes, state, views, or actions when visible grouping or selection matters. Keep the interaction model consistent: all segments represent selection or all perform momentary actions. Aim for about 5–7 segments in a wide interface and no more than about 5 on iPhone. Equal widths and similarly sized titles or glyphs make the group easier to parse.

<a id="Content"></a>
## Content

Use text throughout a control or images throughout it rather than mixing those representations. Keep content footprints similar. Use title-case nouns or short noun phrases for textual choices; text-labeled controls generally need no introduction.

<a id="Platform-considerations"></a>
## Platform considerations

Segmented controls are unsupported in watchOS.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Use segments to switch closely related subviews, such as two creation modes. Use a tab bar for separate top-level app sections.

<a id="macOS"></a>
### macOS

Add introductory text when context is unclear, per-segment captions for unfamiliar glyphs, and individual tooltips when the app offers them. Prefer a tab view for switching panes in the main window body; segments can suit view switches in a toolbar or inspector. Consider spring loading: dragging over a segment and force-clicking with a Magic Trackpad can activate it while retaining the drag.

<a id="tvOS"></a>
### tvOS

A split view can make filtering easier to reach than a segmented control. Segments select as focus moves onto them, so keep other focusable elements far enough away to reduce accidental transitions.

<a id="visionOS"></a>
### visionOS

For icon segments, supply descriptive text for the tooltip the system presents when someone looks at the control.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Split views](https://developer.apple.com/design/human-interface-guidelines/split-views)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/PickerStyle/segmented> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UISegmentedControl> — UIKit
<https://developer.apple.com/documentation/AppKit/NSSegmentedControl> — AppKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 21, 2023.
