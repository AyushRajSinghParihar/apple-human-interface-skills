# Watch faces

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/watch-faces)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

People choose system watch faces and configure complications, colors, and images for everyday or activity-specific wrist viewing. Since watchOS 7, configurations can be shared through apps, websites, messages, mail, and other channels; this shares a configured face rather than creating an unrestricted new face type.

<a id="Best-practices"></a>
## Best practices

Share useful curated configurations featuring several of your complications where appropriate. The system can prompt installation when a recipient lacks the app. Provide an honest preview: emailing a face through the iPhone Watch app supplies a framed preview; an official high-fidelity bezel can replace its illustrated frame.

Account for device compatibility. The source identifies California, Chronograph Pro, Gradient, Infograph, Infograph Modular, Meridian, Modular Compact, and Solar Dial as Series 4-and-later examples, and Explorer as Series 3 cellular-and-later. Offer comparable configurations for older watches and label supported devices. When an incompatible face returns an error for Series 3 or earlier, prefer an immediate compatible alternative over a dead-end error, and explain the possible substitution in advance.

<a id="Platform-considerations"></a>
## Platform considerations

Watch faces are watchOS experiences, unsupported as a native face component in iOS, iPadOS, macOS, tvOS, and visionOS; iPhone can still help share/configure them.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Apple Design Resources — Product Bezels](https://developer.apple.com/design/resources/#product-bezels)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/ClockKit/sharing-an-apple-watch-face> — ClockKit
