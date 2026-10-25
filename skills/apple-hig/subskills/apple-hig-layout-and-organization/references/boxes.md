# Boxes

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/boxes)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A box visually groups related information and controls with a border or contrasting background; a title can explain the relationship.

<a id="Best-practices"></a>
## Best practices

Keep a box meaningfully smaller than its containing window or screen so the boundary communicates a group without crowding surrounding content. For subgroups, use alignment and spacing before adding nested borders; nested boxes can make the interface feel cramped.

<a id="Content"></a>
## Content

Add a short introductory title when the relationship is not obvious or when it helps VoiceOver users anticipate the contents. Use a brief sentence-case phrase. Omit terminal punctuation except for a box title in a settings pane, which takes a colon.

<a id="Platform-considerations"></a>
## Platform considerations

visionOS has no additional guidance. Boxes are unsupported in tvOS and watchOS.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

System boxes normally use secondary and tertiary background colors.

<a id="macOS"></a>
### macOS

The default placement puts the title above the box.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/GroupBox> — SwiftUI
<https://developer.apple.com/documentation/AppKit/NSBox> — AppKit
