# Ornaments

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/ornaments)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A visionOS ornament presents persistent contextual tools without covering the window's content. It sits parallel and slightly forward of its window, follows window movement, and remains stable when the window's content scrolls. It can attach to any edge; system toolbars, tabs, and playback controls already use ornaments.

<a id="Best-practices"></a>
## Best practices

Use an ornament for frequently needed controls or information in a predictable location. Usually keep it visible, allowing temporary hiding for focused photo/video viewing. Balance multiple ornaments and reduce their number when they add too much visual weight; relocate lower-priority tools into the window. Keep ornament width at or below the window width to avoid side controls. Borderless buttons can work against its glass background and inherit standard hover feedback. Use system toolbars and tabs for those standard components rather than rebuilding them inside custom ornaments.

<a id="Platform-considerations"></a>
## Platform considerations

Ornaments are unsupported in iOS, iPadOS, macOS, tvOS, and watchOS.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
[Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/View/ornament(visibility:attachmentAnchor:contentAlignment:ornament:)> — SwiftUI

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2023/10076>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: February 2, 2024, December 5, 2023, June 21, 2023.
