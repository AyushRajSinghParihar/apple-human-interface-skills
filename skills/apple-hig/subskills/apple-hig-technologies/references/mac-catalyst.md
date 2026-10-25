# Mac Catalyst

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/mac-catalyst) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

A Catalyst app should provide an intentional Mac experience while maintaining continuity with its iPad origin.

<a id="Before-you-start"></a>
## Before you start
Strong foundations are iPad drag/drop, keyboard navigation/shortcuts, multitasking/resizing, and multiple scenes. Device-specific essentials such as motion sensors/rear camera, HealthKit/ARKit, handwriting/marking, or navigation may make a port unsuitable. Catalyst supplies pointer/focus/window/toolbar/text-edit/file/menu/settings integration and Mac-like split views, browser, activity/form sheets, context actions, and color picker. Inspect UIKit Catalog’s Mac target to understand transformations.

<a id="Choose-an-idiom"></a>
## Choose an idiom
The default iPad idiom scales views/text to 77%, converting a 17 pt baseline to about 13 pt. Mac idiom renders at 100% with greater detail, more native appearance, and potential graphics/power improvements, but requires layout/text/image review. Consider separate Mac assets, semantic text styles rather than fixed sizes, and only supported shared/native appearance customizations. Unscaled metrics can require substantial revision.

<a id="Integrate-the-Mac-experience"></a>
## Integrate the Mac experience
<a id="Navigation"></a>
### Navigation
Replace an imported bottom tab bar where appropriate with a sidebar split view, generally preferred, or a segmented control for flat mutually exclusive categories. Sidebars can expose child hierarchy and share a structure across tablet/Mac. Keep top-level destinations in the View menu. Add Next/Previous controls alongside swipe gestures for keyboard/pointer users.

<a id="Inputs"></a>
### Inputs
Phone/tablet touch assumptions should yield to keyboard/mouse conventions. For a mouse, tap maps to either left or right click, touch-and-hold to click-and-hold, and pan to left-click-and-drag. On a trackpad, tap maps to click, touch-and-hold to click-and-hold, pan to click-and-drag, and pinch/rotation remain pinch/rotation. For the latter, both touches are delivered to the view under the pointer rather than individually targeted views.

<a id="App-icons"></a>
### App icons
Create a Mac-suitable icon that follows the current Mac visual language while preserving recognizable identity across platforms.

<a id="Layout"></a>
### Layout
Use larger space for columns, regular width/height, responsive side-by-side content, and an adjacent inspector instead of a popover. Put suitable main-view controls in the window toolbar and mirror their commands in menus. Favor a top-down hierarchy and reconsider bottom/side controls whose placement was motivated by touch reach.

<a id="Menus"></a>
### Menus
Expose app commands through the persistent menu bar. Use UIKeyCommand for shortcuts, UIMenuBuilder for custom menu structure, and UICommand for actions. Standard popup/pulldown menus adapt. Imported context menus work automatically; add relevant contextual actions to other objects where Mac users expect them.

<a id="Platform-considerations"></a>
## Platform considerations
The source lists iPadOS/macOS and marks iOS/tvOS/visionOS/watchOS unsupported.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/mac-catalyst) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Videos"></a>
#### Videos
Apple’s linked design sessions provide demonstrations and additional implementation context; no video review is implied here.

<a id="Change-log"></a>
## Change log
Source revision dates: May 2, 2023.
