# Going full screen

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/going-full-screen)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Fullscreen mode supports concentration, games, and immersive media on iPhone, iPad, and Mac. TV and watch already fill their displays; visionOS instead lets people resize windows or use the Digital Crown to hide passthrough and enter a more immersive experience.

<a id="Best-practices"></a>
## Best practices

Offer fullscreen when it serves the task. Adapt layout subtly for extra room without programmatically resizing the window or replacing the interface. Preserve essential controls, either visible or easily revealed. Keep Dock access on iPad/Mac except games that need protection against accidental gestures. Pause time-sensitive content when the person leaves and restore their position on return. Let the person choose when to exit rather than leaving fullscreen automatically after playback or app switching. Hidden chrome should return through a familiar tap, swipe, or top-edge pointer action, while necessary task/navigation controls remain available.

<a id="Platform-considerations"></a>
## Platform considerations

Fullscreen mode is unsupported as a distinct mode in tvOS, visionOS, and watchOS.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Retain ordinary Home-indicator behavior where possible: it fades, reappears near the bottom, and allows one swipe to leave. If accidental exits disrupt play, defer the first system gesture so a second swipe exits.

<a id="macOS"></a>
### macOS

Use standard fullscreen support, including accommodation for camera housings. Games must not change display modes automatically; doing so does not improve performance. Let people enter with standard window controls, View commands, or Control-Command-F, with an optional game toggle instead of a custom mode menu.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
[Multitasking](https://developer.apple.com/design/human-interface-guidelines/multitasking)
[Windows](https://developer.apple.com/design/human-interface-guidelines/windows)
[The menu bar](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/View/fullScreenCover(item:onDismiss:content:)> — SwiftUI
<https://developer.apple.com/documentation/AppKit/NSScreen> — AppKit
<https://developer.apple.com/documentation/AppKit/NSWindow/CollectionBehavior-swift.struct> — AppKit
<https://developer.apple.com/documentation/Metal/managing-your-game-window-for-metal-in-macos> — Swift, Objective-C

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2025/208>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 9, 2025, June 10, 2024.
