# Virtual keyboards

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

The system virtual keyboard optimizes keys for the current input task and does not provide keyboard shortcuts. App-specific input views and installable keyboard extensions serve different scopes.

<a id="Best-practices"></a>
## Best practices

Choose keyboard type and semantic content type together so appropriate characters and corrections are available. The source illustrates default and ASCII letter layouts; ASCII-capable, ordinary, decimal, and telephone number pads; a name/phone layout; email with @ and period; URL with slash and domain entry; social entry with @ and #; numbers/punctuation; and web search. Use the task's semantics rather than a visually similar arbitrary layout. Customize the Return/submit label when it clarifies the result, such as Search instead of Return.

<a id="Custom-input-views"></a>
## Custom input views

An app-specific input view replaces the keyboard only inside the app, for example a spreadsheet's numerical entry controls. It should clearly improve the current task and remain understandable to someone expecting the system keyboard. Use standard input-click sounds and honor the person's system keyboard-sound setting.

<a id="Custom-keyboards"></a>
## Custom keyboards

Keyboard extensions in iOS, iPadOS, and tvOS let people select your keyboard in Settings and use it across apps, except in secure and phone-number fields. People can install several and switch at any time. Use an extension for unique systemwide entry or an otherwise unsupported language; use an input view for functionality limited to one app.

Provide an obvious keyboard-switching control equivalent in clarity to the system Globe key. Do not duplicate Emoji/Globe or Dictation keys that the device already places below the keyboard and that your extension cannot change. Put tutorials in the containing app, covering selection, activation, use, and switching back; do not consume keyboard space with help content.

<a id="Platform-considerations"></a>
## Platform considerations

Virtual keyboards are unsupported in macOS in this component guidance.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Use the keyboard layout guide to keep fields and actions visible as the keyboard appears or moves. The source's correct/incorrect examples demonstrate that both the active field and its action need clearance. Add only task-relevant accessory controls, using standard padding and layout guides. A standard toolbar automatically receives Liquid Glass; a custom accessory container can adopt it when needed to fit the surrounding interface.

<a id="tvOS"></a>
### tvOS

The Siri Remote invokes a linear keyboard for text fields; other input devices can invoke a grid layout, with content adapting automatically. Digit-entry views invoke a numeric-specific keyboard.

<a id="visionOS"></a>
### visionOS

The keyboard is a separate movable window supporting direct and indirect gestures. App layout need not reserve space for its position.

<a id="watchOS"></a>
### watchOS

A sufficiently large display can show a keyboard; otherwise the system offers dictation or Scribble. Keyboard type is not configurable, but content type can improve suggestions. A nearby paired iPhone provides another entry route.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Entering data](https://developer.apple.com/design/human-interface-guidelines/entering-data)
[Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards)
[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/View/keyboardType(_:)> — SwiftUI
<https://developer.apple.com/documentation/SwiftUI/View/textContentType(_:)> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UIKeyboardType> — UIKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 9, 2025, February 2, 2024, December 5, 2023, June 21, 2023.
