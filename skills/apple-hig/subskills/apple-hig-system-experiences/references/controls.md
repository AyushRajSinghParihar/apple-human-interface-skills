# Controls

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/controls)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Controls expose an app button or binary toggle in Control Center, Lock Screen, or the Action button. Buttons can act, open a specific destination, or launch a locked-device camera. People add them through Control Center editing, Lock Screen customization, or Action button settings.

<a id="Anatomy"></a>
## Anatomy

Provide a meaningful SF/custom symbol, a title, and optional state value. Larger Control Center sizes show text; Lock Screen uses only the symbol; Action-button activation can show symbol and value in Dynamic Island. The symbol therefore must communicate purpose without labels.

<a id="Best-practices"></a>
## Best practices

Favor useful actions that avoid launching the app, such as starting a Live Activity. Update after interaction, completion, and remote changes so displayed state and progress remain accurate. Supply meaningful symbols for both toggle states, animate their transitions, and animate a duration-based button while its task remains active. Choose a branded tint for the on symbol and Action-button feedback. Prompt for required configuration when first added, with later reconfiguration available. Provide verb-based press-and-hold hints for Action button use, and illustrative placeholders for variable titles/values in galleries. Redact private title/value text when locked and, if needed, show the symbol's off state too. Require authentication for security-sensitive actions such as doors or vehicle starting.

<a id="Camera-experiences-on-a-locked-device"></a>
## Camera experiences on a locked device

From iOS 18, a control can open a capture experience while locked. Tasks beyond capture require unlocking and transition into the app. Reuse the app's camera UI for a familiar seamless transition, and explain how to add the camera control.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, iPadOS, or macOS rules are specified. Controls are unsupported in watchOS, tvOS, and visionOS.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Widgets](https://developer.apple.com/design/human-interface-guidelines/widgets)
[Action button](https://developer.apple.com/design/human-interface-guidelines/action-button)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/LockedCameraCapture>
<https://developer.apple.com/documentation/WidgetKit>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 10, 2024.
