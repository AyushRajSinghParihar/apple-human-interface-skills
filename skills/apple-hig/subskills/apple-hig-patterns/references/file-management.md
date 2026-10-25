# File management

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/file-management)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Document apps should work with the filesystem people already use: Finder on Mac and Files on iPhone, iPad, and Apple Vision Pro. tvOS/watchOS do not normally provide document browsing.

<a id="Creating-and-opening-files"></a>
## Creating and opening files

Provide standard New/Open commands and keyboard shortcuts on Mac/iPad. Expose a discoverable Add action; Mac creation also belongs in File. A custom browser may initially emphasize a relevant folder or recent location but should still let people browse the wider filesystem.

<a id="Saving-work"></a>
## Saving work

Autosave periodically and when closing or leaving the app so work survives unless explicitly canceled or deleted. Hide extensions initially, let people show them, and honor that choice consistently across Open/Save UI.

<a id="Quick-Look-previews"></a>
## Quick Look previews

Preview unsupported attachments without forcing a context switch through a Quick Look viewer. If producing a custom type, supply a generator so Finder, Files, Spotlight, and other apps can preview it. Depending on file type, previews may support audio, markup, or 3D inspection.

<a id="Platform-considerations"></a>
## Platform considerations

No additional tvOS, visionOS, or watchOS rules are specified.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

<a id="Document-launcher"></a>
#### Document launcher

From iOS/iPadOS 18, a system launcher combines a title card with two app actions, a customizable background/accessories, and a file-browser sheet with optional app tools. Assign primary/secondary actions to important work, usually creation plus a template or additional choice. Keep backgrounds distinct and quiet. Accessories may layer around the title for depth but must not obscure name/actions; test all sizes and orientations. Animate sparingly with gentle motion that supports content.

<a id="File-provider-app-extension"></a>
#### File provider app extension

An extension can expose import/export/open/move access to other apps. Filter open/import results to the host's accepted types and show useful metadata or local/remote status. Allow a destination choice for export/move unless there is only one directory; new subdirectories can help. Avoid a second top toolbar because the host modal already supplies one. Apps can also browse other providers through standard document-browser support.

<a id="macOS"></a>
### macOS

<a id="Custom-file-management"></a>
#### Custom file management

Prefer the standard browser. A justified custom opener should support useful recents, filters, and multiselection; adapt Open to the task, such as Insert. Let people change name, format, and location during saving, with logical initial folders and an initially Untitled document. Add a Save accessory view only for useful related options.

<a id="Finder-Sync-extensions"></a>
#### Finder Sync extensions

For local/remote synchronization, Finder Sync can add item status badges, contextual management commands, and global toolbar actions. Respect disabled autosaving: identify unsaved content and request saving on close, quit, logout, or restart. Show dirty dots on the close control and Window-menu name only when autosave is off. An Edited title suffix can apply in either mode but must disappear after an automatic or explicit save.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars)
[File menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#File-menu)
[Printing](https://developer.apple.com/design/human-interface-guidelines/printing)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/Documents> — SwiftUI

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2020/10039>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 10, 2024, June 21, 2023.
