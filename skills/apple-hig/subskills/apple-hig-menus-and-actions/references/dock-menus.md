# Dock menus

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/dock-menus)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Secondary-clicking a running or closed Mac app's Dock icon reveals system and custom commands appropriate to its state. iOS and iPadOS offer Home Screen quick actions instead of Dock menus.

<a id="Best-practices"></a>
## Best practices

Use brief labels and a logical order. Make custom commands available in main menus or visible interface too. Favor a few valuable actions that help when the app is not frontmost or has no windows, such as composing an item, refreshing data, or choosing a current/recent window.

<a id="Platform-considerations"></a>
## Platform considerations

Dock menus are unsupported in iOS, iPadOS, tvOS, visionOS, and watchOS.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Menus](https://developer.apple.com/design/human-interface-guidelines/menus)
[Home Screen quick actions](https://developer.apple.com/design/human-interface-guidelines/home-screen-quick-actions)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/AppKit/NSApplicationDelegate/applicationDockMenu(_:)> — AppKit
