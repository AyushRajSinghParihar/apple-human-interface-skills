# Designing for iPhone Duo

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Treat the two-display device as an iPhone whose existing experience resizes continuously. Standard resizable components supply much of the needed behavior; retain normal iOS conventions.

<a id="Anatomy"></a>
## Anatomy
The outer display is used while closed. A central hinge changes usable areas as the device folds. Toolbars and tab bars appear along the side on the outer display and stay there when the inner display opens in landscape. The outer corner camera remains visible and aligned with hardware-side controls; the inner camera is hidden behind the display until active.

<a id="Device-poses"></a>
### Device poses
Support handheld book-like, surface-supported, and edge-standing poses through layout adaptation, rather than inventing a separate design for each. Use compact width outside and regular width inside, expanding existing structure naturally. Preview varying poses through Xcode’s device hub.

<a id="Best-practices"></a>
## Best practices
Use size classes, safe-area insets, and layout margins rather than fixed widths or assumptions tied to one panel. Support Split View sizes. Preserve state, content, features, and information hierarchy across opening and closing; a larger display may expose an additional hierarchy level, as a list and detail together. Keep all controls available as content moves or items overflow. Preserve the system’s vertical placement of toolbars, tab bars, and navigation controls. Games may lock portrait or landscape but must fill every pose, keeping text and controls consistently sized. Change aspect ratio before adding letterbox/pillarbox padding; if padding is unavoidable, use suitable art.

<a id="Dynamic-layouts"></a>
## Dynamic layouts
Build on safe areas and layout margins in every configuration. The screen’s dimensions alone do not define the available content regions.

<a id="Reserved-regions"></a>
### Reserved regions
The outer camera region is permanent and can grow for Dynamic Island Live Activities. The inner camera region exists only while its camera operates; UI moves aside to reveal camera activity. A partially folded inner screen introduces a center folding region that separates usable areas. Standard alerts, menus, sheets, and split views adapt automatically; custom views can use SwiftUI or UIKit `ReservedRegion` APIs. Favor adaptable containers, even column counts in grids, and modest moves that retain control visibility and reachability. Avoid abrupt reorganization as the fold changes.

<a id="Split-views"></a>
### Split views
A standard split view shows columns in regular-width inner configurations and collapses to one pane on the outer display. Automatic width and margin adaptation keeps content clear of reserved regions and the fold.

<a id="Arrangement-views"></a>
### Arrangement views
An arrangement contains primary and secondary content views and responds to size, orientation, and reserved regions. A split arrangement lays them side by side when wider than tall, or vertically when taller than wide; axes can be restricted. An overlay stacks them normally and places them on opposite sides when partially folded; its secondary view can collapse. Choose an arrangement when an existing HStack/VStack or ZStack already has the matching relationship. Keep navigation split views and tab views outside the arrangement: this container arranges content but does not navigate.

<a id="Vertical-controls"></a>
## Vertical controls
Side placement preserves scarce height; the inner screen in portrait uses ordinary horizontal bars. Dynamic Island, status bar, navigation toolbar, and tabs align along the side. In Split View, each app uses its outer edge, so the left app’s controls appear on the left. Hardware alignment also means these side controls stay on the same physical side in right-to-left languages.

- Respect asymmetrical safe areas, including the opposite-side case in multitasking. Keep relative action locations stable between poses.
- Put Back/Close first along the top, then prominent completion actions such as Done. Keep original toolbar groups distinct; system spacing separates prior top and bottom groups.
- Overflow proceeds bottom upward by default. Set visibility priorities for groups, then individual items if needed; retain common actions and important badges longer.
- Preserve standard bar placement. A non-scrolling visual or immersive view may span the entire width when it avoids status/Dynamic Island interference; full-width backgrounds can coexist with inset scrolling content.
- Use toolbar groups for automatic spacing instead of manual fixed gaps. Keep a control near the pane it affects rather than relocating every control to the outer side.
- Supply both title and symbol unless text-only; the system needs the title for expanded representations and overflow. Prefer meaningful symbols because text labels remain in horizontal bars.
- In navigation-led views, allow toolbar actions to overflow so tabs remain available. For task-led views, minimize tabs to preserve task tools. Use the vertical-bar compression APIs to express this choice.
- Consolidate extra actions in the system overflow menu. Reserve the ellipsis for that menu and use distinct symbols for other menus.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) for linked Apple design assets and implementation resources.

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
Source revision dates: September 9, 2026.
