# Alerts

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/alerts)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

An alert interrupts to communicate urgent, critical information and useful actions, including problems, unexpected data loss, or important confirmations.

<a id="Best-practices"></a>
## Best practices

Reserve alerts for situations that warrant immediate attention. Put informational status in context when no action is required. Common undoable deletions generally need no confirmation; uncommon irreversible destruction does. Avoid startup alerts: cached or placeholder content with a discreet problem explanation is often a better response to an unavailable network.

<a id="Anatomy"></a>
## Anatomy

Alerts are modal and adapt their appearance to iOS, iPadOS, macOS, tvOS, visionOS, and watchOS rather than using one universal layout.

<a id="Content"></a>
## Content

Use a title, optional message, and up to three buttons. iOS, iPadOS, macOS, and visionOS can include text fields; macOS and visionOS can include an icon and accessory view. macOS additionally supports a suppression checkbox and Help button.

Use direct, neutral, approachable wording without blaming the person or concealing severity. The title should explain what happened, its context, and cause as concisely as possible, generally within two lines. Avoid a bare error label or code. Complete-sentence titles use sentence case and punctuation; fragments use title case without punctuation. Additional text should add information in brief complete sentences. Clear action labels should make button explanations unnecessary; if instructions are unavoidable, use device-neutral language such as choose and the exact title without quotation marks. Include an input field only when resolving the situation requires it, with secure entry for passwords.

<a id="Buttons"></a>
## Buttons

Use short, usually one- or two-word, title-case action labels without punctuation. Prefer specific outcomes over Yes/No or ambiguous OK; reserve OK for purely informational acknowledgment. A cancellation action is always Cancel. Place the expected/default action at the trailing end of a row or top of a stack, with cancellation generally leading or at the bottom.

Apply destructive styling to destructive consequences the person did not deliberately request. A confirmation of an explicitly chosen destruction, such as Empty Trash, can retain a normal default action so Return confirms intent. Always provide Cancel alongside destructive actions, but do not make Cancel the default. To force a deliberate reading, consider no default. A single default acknowledgment button should be Done rather than Cancel.

Support familiar alternate cancellation where appropriate: Home Screen exit on iOS/iPadOS; Escape or Command-Period on attached keyboards in iOS/iPadOS/macOS/visionOS; Menu on the tvOS remote.

<a id="Platform-considerations"></a>
## Platform considerations

No additional tvOS or watchOS rules are specified.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Use action sheets for multiple choices following an intentional action. Keep titles and optional messages short to minimize scrolling, while accommodating enlarged accessibility text.

<a id="macOS"></a>
### macOS

The app icon appears automatically but can be replaced. Repeating alerts can offer suppression; necessary details can use an accessory view, and Help can open documentation. Reserve a caution symbol for situations needing extra attention, particularly unexpected loss, rather than routine overwrite, save, or empty-trash tasks.

<a id="visionOS"></a>
### visionOS

In Shared Space, an alert sits slightly in front of its parent window and stays attached when the window moves. In Full Space, it centers in the wearer's field of view. An accessory view must be no taller than 154 pt and use a 16-pt corner radius.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Modality](https://developer.apple.com/design/human-interface-guidelines/modality)
[Action sheets](https://developer.apple.com/design/human-interface-guidelines/action-sheets)
[Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/View/alert(_:isPresented:actions:)-1bkka> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UIAlertController> — UIKit
<https://developer.apple.com/documentation/AppKit/NSAlert> — AppKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: February 2, 2024, September 12, 2023, June 21, 2023.
