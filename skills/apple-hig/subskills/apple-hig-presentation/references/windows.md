# Windows

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/windows)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Primary windows host app navigation, content, and actions. Auxiliary windows focus on one task or area and typically close after that task. iPadOS, macOS, and visionOS windows establish content boundaries and enable multitasking with system movement, sizing, and closing controls.

<a id="Best-practices"></a>
## Best practices

Adapt smoothly to size changes. Open new windows when preserving context or working in parallel helps, without generating clutter by default. Offer Open in New Window in a context or File menu when useful. Retain system frames and controls instead of imitating them. Call the experience a window in user-facing copy; scene is an implementation term.

<a id="Platform-considerations"></a>
## Platform considerations

This multiwindow component guidance marks iOS, tvOS, and watchOS unsupported.

<a id="iPadOS"></a>
### iPadOS

People choose fullscreen or windowed behavior in Multitasking & Gestures settings. Fullscreen fills the display and uses app switching; windowed mode supports multiple resizable, movable windows with remembered placement. Move leading toolbar items inward when window controls appear so they do not overlap. Consider gestures to open content in a new window, such as expanding a collection item with a pinch. Quick Look can present a single file without a custom window if the app supports multiple windows.

<a id="macOS"></a>
### macOS

Support normal movement, resize, minimization, and frequent switching among multiple apps' windows. Games also need the appropriate system game-window configuration.

<a id="macOS-window-anatomy"></a>
#### macOS window anatomy

A frame above the body supplies movement, window controls, and optionally a toolbar. Edges normally resize. A rare bottom bar is also part of the frame.

<a id="macOS-window-states"></a>
#### macOS window states

An app has one main window; the system has one key/input window at a time. A floating panel can be key while its document stays main. Dock activation brings app windows forward but makes only the recently used one key. Other windows are inactive. Colored close/minimize/zoom controls identify key state; inactive and non-key main windows use gray, and inactive windows lose vibrancy. Some panels take key status only through the title bar or keyboard-input controls. Custom rendering must preserve these automatic state cues. Avoid critical controls at the bottom, which may be offscreen; reserve bottom bars for small contextual summaries, using an inspector for more detail.

<a id="visionOS"></a>
### visionOS

Windows and volumetric windows can each contain 2D/3D content and coexist in Shared or Full Space. Plain style omits the glass plane. The system positions the first opened surface, then people can move it.

<a id="visionOS-windows"></a>
#### visionOS windows

Default windows use an upright glass plane with close, move, and resize controls, and can add Share, tabs, toolbars, and ornaments. Dynamic scale preserves apparent size across distance. Prefer familiar windows for familiar tasks, reserving immersion for meaningful content. Retain the glass background: it adapts to surroundings and communicates scale and position; removing it weakens legibility and grouping, while an opaque replacement conceals surroundings.

Default initial size is 1280×720 pt, placed about 2 meters ahead with an apparent width of about 3 meters. Avoid excess empty space and choose a shape suited to content. Set minimum/maximum sizes and adapt layout throughout. Keep 3D depth shallow in a window because content too far from its surface is clipped; use a volume for deeper objects.

<a id="visionOS-volumes"></a>
#### visionOS volumes

Volumes show bounded content from multiple angles; close and move controls turn to face the viewer. Prefer them for rich 3D scenes over UI-centric interfaces. Pin 2D overlays to 3D content with attachments and test multiple viewpoints. Dynamic scaling usually improves distant legibility and interaction, but fixed scaling (the default) suits true-to-life products.

From visionOS 2, a baseplate border glow on look reveals bounds and resize controls when content does not fill them. Full-bleed content or a custom baseplate may not need it. Volumes can have an ornament alongside toolbar/tabs: use attachment anchors to keep its position viewer-relative, place it on another edge, and usually add only one. Choose a floor-parallel alignment for largely viewed objects, or a viewer-tilting alignment when interactive content should remain usable while reclining.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
[Split views](https://developer.apple.com/design/human-interface-guidelines/split-views)
[Multitasking](https://developer.apple.com/design/human-interface-guidelines/multitasking)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/Windows> — SwiftUI
<https://developer.apple.com/documentation/SwiftUI/WindowGroup> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UIWindow> — UIKit
<https://developer.apple.com/documentation/AppKit/NSWindow> — AppKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2025/208>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 9, 2025, June 10, 2024, June 21, 2023.
