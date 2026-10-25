# Snippets

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/snippets)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A snippet responds to a Siri, Spotlight, or Shortcuts action with a compact result or confirmation. App Intents define its task. Confirmation can offer choices and cancel/confirm; a result provides the outcome without requiring further action. Every snippet intent shows a result, with confirmation optional.

<a id="Anatomy"></a>
## Anatomy

The intent supplies spoken dialogue, included as text above the custom view by default. The custom view conveys information and can include relevant actions. Confirmation adds system Cancel and a customizable primary button; result adds Done.

<a id="Best-practices"></a>
## Best practices

Keep contrast and margins clear in light/dark appearances. Custom content must not exceed 400 pt high, accounting for Dynamic Type. Deep-link to longer result details. Use a concrete primary label such as the actual action rather than OK/Proceed; Continue is the default when none is given. Keep spoken dialogue complete for eyes-away use, but generally omit its visible repetition and make the custom view communicate purpose independently.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, iPadOS, or macOS rules are specified. Snippets are unsupported in tvOS, visionOS, and watchOS.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Siri](https://developer.apple.com/design/human-interface-guidelines/siri)
[App Shortcuts](https://developer.apple.com/design/human-interface-guidelines/app-shortcuts)
[Live Activities](https://developer.apple.com/design/human-interface-guidelines/live-activities)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/AppIntents>

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2025/281>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 8, 2026.
