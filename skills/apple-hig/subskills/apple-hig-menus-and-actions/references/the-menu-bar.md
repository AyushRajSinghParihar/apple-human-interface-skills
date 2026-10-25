# The menu bar

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

## Contents

- [Anatomy](#Anatomy)
- [Best practices](#Best-practices)
- [App menu](#App-menu)
- [File menu](#File-menu)
- [Edit menu](#Edit-menu)
- [Format menu](#Format-menu)
- [View menu](#View-menu)
- [App-specific menus](#App-specific-menus)
- [Window menu](#Window-menu)
- [Help menu](#Help-menu)
- [Dynamic menu items](#Dynamic-menu-items)
- [Platform considerations](#Platform-considerations)

The menu bar exposes an app's full command structure on Mac and iPad. Familiar ordering and keyboard equivalents let people discover capabilities and work with a hardware keyboard.

<a id="Anatomy"></a>
## Anatomy

Order supported menus as app name, File, Edit, Format, View, app-specific menus, Window, Help. Mac additionally places Apple at the leading end and menu-bar extras at the trailing end.

<a id="Best-practices"></a>
## Best practices

Preserve standard menus, order, and shortcuts. Keep unavailable commands visible but disabled. Use familiar action glyphs and brief, preferably one-word menu titles; multiword titles use title case. Standard controls often provide command enablement automatically.

<a id="App-menu"></a>
## App menu

This menu holds app-wide rather than document/window tasks. Use the short app name, preferably 16 characters or fewer, without a version. Standard order is About (alone before a separator), Settings…, custom configuration items in the same group, Services, Hide App, Hide Others, Show All, and Quit App. Services and hide/show commands are Mac-only, and iPad has further differences below. Settings is for app-level configuration; document-specific settings belong in File. Hide App activates the previous app; Show All restores others behind it. Option can change Quit to Quit and Keep Windows.

<a id="File-menu"></a>
## File menu

Omit or rename File when the app handles no files. Preserve the following functional order where relevant:

| Command | Behavior and qualification |
| --- | --- |
| New Item | Create a document/file/window; name the actual kind of item |
| Open / Open… | Open selection directly or request a selection, adding ellipsis for the latter |
| Open Recent | Recognizable names, newest first, usually with Clear Menu; avoid full paths |
| Close | Close current window/document; Option offers Close All |
| Close Tab | Replaces Close in tabbed windows; Option offers Close Other Tabs; consider separate Close Window |
| Close File | Close all views of one file when several views can coexist |
| Save | Save current content; autosave periodically; ask a new file's name/location and offer formats in the Save sheet |
| Save All | Save every open document |
| Duplicate | Keep original and copy open; Option offers Save As; clearer than ambiguous copy/save-to commands |
| Rename… / Move To… | Change current name or request another location |
| Export As… | Choose name, location, and atypical format; retain the original open and do not open the export |
| Revert To | With autosave, expose recent versions and version browser; selected version replaces current content |
| Page Setup… | Document-specific paper size/orientation; retain parameters with the document |
| Print… | Standard printer/fax/PDF output; printer choice and frequently changed copy counts belong here rather than Page Setup |

<a id="Edit-menu"></a>
## Edit menu

Keep Edit useful for any editable content, including nondocument apps. File/object search may belong in File rather than Edit. Order Undo and Redo, Cut/Copy/Paste/Paste and Match Style/Delete/Select All, then Find, Spelling and Grammar, Substitutions, Transformations, Speech, Start Dictation, Emoji & Symbols.

Name undo/redo targets, such as Typing or the command reversed. Cut removes to Clipboard; Copy duplicates there; Paste leaves Clipboard reusable; Paste and Match Style adopts surrounding formatting; Delete removes without copying and should be named Delete rather than Erase/Clear. Select All covers the current document/text container.

Find normally includes Find, Find and Replace, next/previous, use selection, and jump to selection. Spelling/grammar includes its panel, immediate check, while-typing spelling, grammar, and autocorrection. Substitutions includes its panel plus smart copy/paste, quotes, dashes, links, data detection, and replacement. Transformations offers uppercase/lowercase/capitalization. Speech starts/stops spoken selected text. The system adds dictation and the character viewer at the bottom.

<a id="Format-menu"></a>
## Format menu

Omit Format when rich-text editing is absent. Font comes before Text. Font includes the font panel, bold/italic/underline, bigger/smaller, colors, and copy/paste style. Text includes left/center/justified/right alignment, writing direction, ruler, and copy/paste ruler.

<a id="View-menu"></a>
## View menu

View controls appearance rather than managing individual windows. Include it even for only a supported subset, such as fullscreen. Show/hide labels must reflect the next action. Standard order covers tab bar visibility, tab overview, toolbar visibility, toolbar customization, sidebar visibility, then Enter/Exit Full Screen.

<a id="App-specific-menus"></a>
## App-specific menus

Put custom menus between View and Window and expose custom commands there even when advanced or available elsewhere. This supports discovery, keyboard shortcuts, and Full Keyboard Access. Order around the app's hierarchy and common usage; for example, containers precede objects and object formatting. The source's wording about general versus specialized ordering is internally inconsistent, so use the concrete hierarchy and frequency criteria rather than inventing an absolute rule.

<a id="Window-menu"></a>
## Window menu

Provide it even for a single-window app so Minimize and Zoom remain keyboard-accessible. It manages windows; View customizes appearance and File closes them. Panel show/hide commands can live here, except font/color panels already in Format. Standard order:

| Command | Behavior |
| --- | --- |
| Minimize | Active window to Dock; Option offers Minimize All |
| Zoom | Toggle content-appropriate size and user size; Option offers Zoom All; distinct from fullscreen |
| Show Previous/Next Tab | Navigate document tabs |
| Move Tab to New Window | Detach current tab |
| Merge All Windows | Combine into one tabbed window |
| Enter/Exit Full Screen | Include here only without a View menu; retain Minimize and Zoom separately |
| Bring All to Front | Preserve positions, sizes, and layering; Option offers neatly tiled Arrange in Front |
| Open window names | Alphabetical window list; omit panels and modal views |

<a id="Help-menu"></a>
## Help menu

Keep Help at the trailing end. Help Book content adds system search and opens in Help Viewer. Standard entries can include feedback to Apple and App Help. Separate additional items such as registration or release notes from primary documentation, and keep their number low or link them from the documentation instead.

<a id="Dynamic-menu-items"></a>
## Dynamic menu items

Modifier-dependent alternates can accelerate advanced actions, such as Option-Minimize All. They must have discoverable alternatives because they are hidden by default. Prefer menu-bar use over Dock/context menus, require only one modifier, and let system menu sizing account for the widest alternate.

<a id="Platform-considerations"></a>
## Platform considerations

The menu bar is unsupported in iOS, tvOS, visionOS, and watchOS.

<a id="iPadOS"></a>
### iPadOS

The bar is hidden until a top-edge pointer movement or downward swipe and occupies the status-bar area. It centers horizontally; Mac aligns leading and is visible by default. iPad has no Apple menu or extras, and fullscreen window controls appear within the bar. About, Services, and app-visibility items are unavailable on iPad.

Every function must also be reachable through app UI because the bar is often hidden; dynamic commands additionally require a hardware keyboard. Reserve App > Settings for the app's page in system Settings; link in-app preferences and other custom app-wide configuration beneath it in that group. Consider listing navigation tabs in View with shortcuts. Taller touch-friendly rows may justify submenus more often than on Mac.

<a id="macOS"></a>
### macOS

The system Apple menu stays first and cannot be changed. Extras occupy trailing space when available. Space pressure can reduce intermenu spacing and truncate titles. Fullscreen generally hides the bar until the pointer reaches the top.

<a id="Menu-bar-extras"></a>
#### Menu bar extras

An extra remains available while the app runs even when it is not frontmost, but the system can hide it to protect menu space. Use a black/transparent template icon or SF Symbol so system tint adapts to background and selection; menu-bar height is 24 pt. Prefer a menu over a popover unless the feature is too complex for one. Let people choose whether to add the extra, optionally offering that choice during setup. Never rely on its visibility or fixed position; provide another route such as a Dock menu.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Menus](https://developer.apple.com/design/human-interface-guidelines/menus)
[Dock menus](https://developer.apple.com/design/human-interface-guidelines/dock-menus)
[Standard keyboard shortcuts](https://developer.apple.com/design/human-interface-guidelines/keyboards#Standard-keyboard-shortcuts)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/CommandMenu> — SwiftUI
<https://developer.apple.com/documentation/UIKit/adding-menus-and-shortcuts-to-the-menu-bar-and-user-interface> — UIKit
<https://developer.apple.com/documentation/AppKit/NSStatusBar> — AppKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2025/208>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 9, 2025.
