# Home Screen quick actions

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/home-screen-quick-actions)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Holding an iOS/iPadOS app icon on Home Screen or Dock reveals app actions alongside system remove/edit-home commands. On devices with 3D Touch, pressing the icon with increased pressure also reveals these actions. Each action has a title, an icon whose side follows placement, and an optional subtitle. Text remains leading-aligned in left-to-right languages. Actions can update dynamically, such as recent conversations.

<a id="Best-practices"></a>
## Best practices

Offer at least one useful high-value shortcut where possible and no more than four. Update predictably from context such as recent activity, location, time, or settings. Use concise outcome-oriented titles and optional clarifying subtitles without the app name or filler, allowing localization room. Use familiar SF Symbols or a glyph built from the official Quick Action template. Do not substitute emoji: quick-action symbols are monochrome and adapt for Dark Mode.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS or iPadOS rules are specified. Quick actions are unsupported in macOS, tvOS, visionOS, and watchOS.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Menus](https://developer.apple.com/design/human-interface-guidelines/menus)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/UIKit/add-home-screen-quick-actions> — UIKit
