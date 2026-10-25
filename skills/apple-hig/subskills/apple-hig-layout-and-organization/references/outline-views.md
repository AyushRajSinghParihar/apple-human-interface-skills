# Outline views

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/outline-views)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

An outline is a macOS scrolling table for hierarchical data. Its primary column exposes parents and children through disclosure triangles; additional columns hold related attributes. It often serves as navigation beside a detail pane.

<a id="Best-practices"></a>
## Best practices

- Use an ordinary table for nonhierarchical data. Confine hierarchy to the first column and keep other columns as attributes of those items.
- Give every column in a multicolumn outline a descriptive title-case noun phrase with no terminal punctuation or colon. A single-column outline can instead use an external label for context.
- Where useful, sort through clickable headings; repeat activation reverses order. Sorting the primary column should sort separately at each hierarchy level, preserving parent/child relationships. Secondary sort criteria can resolve ties.
- Allow columns to resize and consider alternating row backgrounds for tracking values across a wide outline.
- Make both local and recursive expansion convenient; Finder's click versus Option-click disclosure behavior illustrates these two scopes. Restore expansion state so returning does not require retraversing a branch.
- Support editing when the task calls for it. A single click can edit a cell while a double click performs another expected action, such as opening a file. Add insertion, deletion, and reorder where useful.
- Consider middle ellipses rather than clipping to retain identifying prefixes and suffixes. A toolbar search field can help locate values in long outlines.

<a id="Platform-considerations"></a>
## Platform considerations

Outline views are for macOS; the source marks them unsupported in iOS, iPadOS, tvOS, visionOS, and watchOS.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Column views](https://developer.apple.com/design/human-interface-guidelines/column-views)
[Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)
[Split views](https://developer.apple.com/design/human-interface-guidelines/split-views)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/OutlineGroup> — SwiftUI
<https://developer.apple.com/documentation/AppKit/NSOutlineView> — AppKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2020/10031>
