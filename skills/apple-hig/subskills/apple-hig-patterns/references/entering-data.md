# Entering data

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/entering-data)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Reduce effort and mistakes by gathering known information and supporting the input methods available to the person.

<a id="Best-practices"></a>
## Best practices

Get existing system/settings data automatically or request permission for relevant private data. Clearly label requested information and prefill reasonable nonsecret defaults. Securely obscure sensitive text or TV digit entry; visionOS secure fields keep input private from AirPlay viewers. Never prepopulate passwords: use explicit entry, biometrics, or keychain authentication. Prefer meaningful choices to typing, and accept paste and drag/drop where appropriate. Validate early enough to fix mistakes in context, with locale-aware number formatting for numeric constraints/presentation. Make required-data gating understandable, enabling Next/Continue only when necessary information is supplied.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, iPadOS, tvOS, visionOS, or watchOS rules are specified.

<a id="macOS"></a>
### macOS

An expansion tooltip can expose complete clipped/truncated field content on pointer dwell, including for iOS/iPadOS apps running on Mac.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields)
[Virtual keyboards](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards)
[Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/Input-events> — SwiftUI

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2021/10059>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 21, 2023.
