# Panels

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/panels)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A macOS panel floats above app windows to supply controls or information for the active window or current selection, usually with less prominence than the main window. Other platforms normally use an appropriate modal or supplementary presentation.

<a id="Best-practices"></a>
## Best practices

Use panels for quickly accessible contextual tools. An inspector updates as selection changes; an Info window preserves the same object's information and should be a regular window instead. A split-view inspector can be another option. Favor direct adjustments such as sliders and steppers over multi-step text entry or object selection.

Provide a movable title bar and a short, title-case noun phrase identifying purpose. Bring all open panels forward when the app activates and hide them when it deactivates. Show/hide commands may appear in Window, but panels do not belong in its document list. Generally disable minimization. In interface copy refer to the title, such as Show Inspector; in help use the title or a clear phrase such as Fonts window rather than introducing panel terminology.

<a id="HUD-style-panels"></a>
## HUD-style panels

Prefer standard panels. A dark translucent HUD fits media or immersive content only when a normal panel would obscure important content and controls are unnecessary; most standard controls except disclosure triangles do not match HUD styling. Keep its style consistent when entering/leaving full screen. Use restrained high-contrast color and keep the HUD small enough not to obstruct or compete with its subject.

<a id="Platform-considerations"></a>
## Platform considerations

Panels are unsupported in iOS, iPadOS, tvOS, visionOS, and watchOS.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Windows](https://developer.apple.com/design/human-interface-guidelines/windows)
[Modality](https://developer.apple.com/design/human-interface-guidelines/modality)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/AppKit/NSPanel> — AppKit
<https://developer.apple.com/documentation/AppKit/NSWindow/StyleMask-swift.struct/hudWindow> — AppKit
