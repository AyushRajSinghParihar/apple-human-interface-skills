# Lists and tables

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Lists and tables organize rows into one or more columns, with optional groups, hierarchy, selection, insertion, deletion, and reordering. A navigation list can express an app's structure; a multicolumn table can compare attributes and support sorting.

<a id="Best-practices"></a>
## Best practices

Use rows for text that people need to scan. Consider a collection for many images or highly variable item sizes. Support appropriate editing, including reorder even when addition and removal are unavailable. In iOS and iPadOS, table item selection for editing uses an edit mode. Distinguish selection feedback by purpose: keep a navigation row highlighted to show the current path; for a chosen option, brief row highlighting followed by a persistent checkmark may be more appropriate.

<a id="Content"></a>
## Content

Keep row wording short enough to avoid excessive wrapping or truncation. When items contain lengthy prose, show titles and reveal content in a detail view. Preserve recognizability at narrow widths; middle truncation can retain both ends of an identifying string. Give multicolumn tables descriptive noun or noun-phrase headings in title case without punctuation. If a single-column table has no heading, add context with a label or header.

<a id="Style"></a>
## Style

Choose grouping and row styles that fit the platform and data. iOS and iPadOS grouped lists use headers, footers, and spacing; watchOS elliptical lists visually roll content over a curved surface; macOS bordered tables can use alternating row backgrounds. Use row configurations appropriate to images, text, headers, and footers rather than rebuilding familiar arrangements unnecessarily.

<a id="Platform-considerations"></a>
## Platform considerations

<a id="iOS-iPadOS-visionOS"></a>
### iOS, iPadOS, visionOS

An info/detail-disclosure button reveals additional information about a row; a disclosure indicator navigates into the row's hierarchy. Keep these meanings distinct. Avoid placing a section index beside trailing row controls because their targets can interfere with one another.

<a id="macOS"></a>
### macOS

Support click-to-sort headings when useful, with another click reversing the sort. Allow column resizing. Alternate row backgrounds can help people track values across wide tables. Use an outline view when the data is hierarchical.

<a id="tvOS"></a>
### tvOS

Test nearby imagery against the focused row's expansion and rounded corners. Prepare images for those system effects and avoid adding a second corner mask.

<a id="watchOS"></a>
### watchOS

Favor shorter lists, but preserve access to the full expected dataset. Present relevant items first and offer more rather than silently dropping subscribed or owned items. Vertical page-based movement among row details works only with short detail views; a scrolling detail view prevents swiping directly between detail pages.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Collections](https://developer.apple.com/design/human-interface-guidelines/collections)
[Outline views](https://developer.apple.com/design/human-interface-guidelines/outline-views)
[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/List> — SwiftUI
<https://developer.apple.com/documentation/SwiftUI/Tables> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UITableView> — UIKit
<https://developer.apple.com/documentation/AppKit/NSTableView> — AppKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2020/10031>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 21, 2023, June 5, 2023.
