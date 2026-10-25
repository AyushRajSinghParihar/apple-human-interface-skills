# Activity views

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/activity-views)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

The system share sheet offers contextual sharing, common actions, and frequently used apps. It appears as a sheet or popover according to device and orientation. App-specific activities normally precede general system actions; people can customize the action list. Extensions can expose share/action functionality in other apps, including on macOS even though Mac has no activity-view component.

<a id="Best-practices"></a>
## Best practices

Use the standard Share button to reveal it. Exclude irrelevant tasks and show only currently appropriate custom tasks; system task order is not app-controlled. Avoid duplicating existing actions such as Print. Give a specialized variation a clearly distinct name. Use a short verb phrase for custom actions without product/company branding; share destinations can use the company name beneath their icon. Prefer SF Symbols; center a custom glyph in an approximately 70×70-pixel area.

<a id="Share-and-action-extensions"></a>
## Share and action extensions

Share extensions transfer contextual information to another app or service; action extensions operate on content without leaving context. iOS/iPadOS expose both through the share sheet. On Mac, sharing comes from toolbar or context-menu Share; actions may come from embedded-content controls, a toolbar, or Finder quick actions.

Prefer the familiar system composition view for sharing. Include the app name for an action extension and use related app interface elements when a custom UI is necessary. Keep the task to few steps. Avoid stacking another modal over the already modal extension, except a necessary alert. Share extensions inherit the app icon; actions should use a meaningful symbol or glyph. Continue long work in the background after dismissal and show status in the main app. Notify only about a problem rather than routine completion.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, iPadOS, or visionOS rules are specified. Activity views themselves are unsupported in macOS, tvOS, and watchOS; Mac share/action extensions remain supported as described above.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets)
[Popovers](https://developer.apple.com/design/human-interface-guidelines/popovers)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/UIKit/UIActivityViewController> — UIKit
<https://developer.apple.com/documentation/UIKit/UIActivity> — UIKit
<https://developer.apple.com/documentation/Foundation/app-extension-support> — Foundation

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2022/10015>
