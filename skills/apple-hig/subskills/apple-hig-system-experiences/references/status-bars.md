# Status bars

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/status-bars)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

The status bar reports device context such as time, network carrier, connectivity, and battery at the display's upper edge.

<a id="Best-practices"></a>
## Best practices

Keep status readable over underlying content and avoid implying that obscured controls can be activated. A scroll-edge blur is preferred for separation. Fullscreen media can temporarily hide status for immersion, with a simple discoverable restoration gesture such as a tap. Do not permanently remove access to time and connectivity information.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS or iPadOS rules are specified. This status-bar component is unsupported in macOS, tvOS, visionOS, and watchOS.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/UIKit/UIStatusBarStyle> — UIKit
<https://developer.apple.com/documentation/UIKit/UIViewController/preferredStatusBarStyle> — UIKit
