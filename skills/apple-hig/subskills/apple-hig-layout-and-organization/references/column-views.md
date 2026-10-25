# Column views

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/column-views)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A macOS column browser displays one hierarchy level per vertical column. A parent row has a triangle; selecting it reveals its children in the next column, supporting movement into a branch and back to earlier levels. For hierarchical presentation on iPadOS or visionOS, evaluate a split view instead.

<a id="Best-practices"></a>
## Best practices

Use columns for deep hierarchies that people frequently traverse in both directions when table-style sorting is unnecessary. Put the root at the first column so returning to the beginning is predictable. At a leaf, consider using the next area for a preview and useful metadata, such as creation or modification date, type, or size. Allow column resizing so long names remain available.

<a id="Platform-considerations"></a>
## Platform considerations

This component is for macOS; it is unsupported in iOS, iPadOS, tvOS, visionOS, and watchOS.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)
[Outline views](https://developer.apple.com/design/human-interface-guidelines/outline-views)
[Split views](https://developer.apple.com/design/human-interface-guidelines/split-views)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/AppKit/NSBrowser> — AppKit
