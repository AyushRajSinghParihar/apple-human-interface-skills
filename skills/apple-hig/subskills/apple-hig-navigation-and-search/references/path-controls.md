# Path controls

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/path-controls)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A macOS path control exposes the filesystem location of a file or folder. A standard path shows root, parents, and item as icon/name segments and hides intermediate names when space is tight. An editable standard control accepts a dropped item as its selected path. A pop-up version shows only the selected item until opened; its menu lists the full hierarchy, and editable mode adds Choose as well as accepting drops.

<a id="Best-practices"></a>
## Best practices

Place the control in the window body. Neither the toolbar nor the status bar is its intended location; Finder's bottom path bar is still part of its window body.

<a id="Platform-considerations"></a>
## Platform considerations

Path controls are unsupported in iOS, iPadOS, tvOS, visionOS, and watchOS.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[File management](https://developer.apple.com/design/human-interface-guidelines/file-management)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/AppKit/NSPathControl> — AppKit
