# Action sheets

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/action-sheets)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

An action sheet presents modal choices arising from an action the person deliberately started. SwiftUI confirmation dialogs offer this functionality; UIKit uses an action-sheet alert-controller style on supported platforms.

<a id="Best-practices"></a>
## Best practices

Use it for clarifying choices such as saving or discarding a canceled draft. An alert instead handles critical situations and confirmations without a set of related alternatives. Interrupt sparingly. Keep the title to one line where possible and add a message only when context and title cannot explain the decision. Supply Cancel when needed to safely reject data loss; it normally sits at the bottom, while watchOS places cancellation at the upper leading corner. SwiftUI dialogs include Cancel by default. Mark destructive options with the destructive role and place them prominently at the top.

<a id="Platform-considerations"></a>
## Platform considerations

No additional macOS or tvOS rules are specified. Action sheets are unsupported in visionOS in this component guidance.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Present related post-action choices as an action sheet. Menus are expected when the person explicitly asks to reveal a menu. Keep the action list short enough to avoid scrolling, which is slow and risks accidental selection.

<a id="watchOS"></a>
### watchOS

Use the standard title, optional message, mandatory Cancel, and action buttons. Default buttons carry no special meaning; destructive buttons remove data or perform another destructive action; Cancel exits without action. Limit the sheet to four total buttons, leaving at most three choices besides Cancel.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Modality](https://developer.apple.com/design/human-interface-guidelines/modality)
[Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets)
[Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/View/confirmationDialog(_:isPresented:titleVisibility:actions:)-46zbb> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UIAlertController/Style/actionSheet> — UIKit
