# Collections

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/collections)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A collection presents ordered content in a flexible visual layout, particularly well suited to imagery.

<a id="Best-practices"></a>
## Best practices

Prefer the familiar horizontal row or grid before inventing a layout. Text-heavy content usually scans more efficiently in a table or list. Make items easy to reach and choose, leaving enough space around images for focus and hover effects to remain visible without overlap. Preserve standard selection, editing, and scrolling interactions; add custom gestures only where the task needs them. Standard insertion, deletion, and reorder animations can explain changes, with custom animation available when appropriate.

<a id="Platform-considerations"></a>
## Platform considerations

No additional macOS, tvOS, or visionOS rules are specified. Collections are unsupported in watchOS.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Treat dynamic layout changes cautiously. Keep changes understandable and easy to follow, and prefer an explicit user action as their trigger while someone is viewing or manipulating content.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)
[Image views](https://developer.apple.com/design/human-interface-guidelines/image-views)
[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/UIKit/UICollectionView> — UIKit
<https://developer.apple.com/documentation/AppKit/NSCollectionView> — AppKit
