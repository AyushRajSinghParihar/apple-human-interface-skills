# NFC

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/nfc) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

NFC exchanges data across a few centimeters. On supported iOS hardware, scanning physical objects can connect content, redeem offers, or track stock.

<a id="In-app-tag-reading"></a>
## In-app tag reading
Provide a scanning sheet for one or several objects while the app is active. In product copy, describe the actual object and say scan or hold near, without implying contact. Avoid developer terms such as tag, Core NFC, or near-field communication. Sheet instructions should be short complete sentences in sentence case with punctuation, changing appropriately for later scans.

<a id="Background-tag-reading"></a>
## Background tag reading
Compatible devices search for suitable tags while the display is lit and show a notification that opens the matching app with data. Background reading is unavailable during an active NFC sheet, Wallet/Apple Pay, camera use, Airplane Mode, or the locked state after restart. Still provide in-app scanning for devices without background support.

<a id="Platform-considerations"></a>
## Platform considerations
No additional iOS/iPadOS rules are listed; macOS/tvOS/visionOS/watchOS are marked unsupported.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/nfc) for linked Apple design assets and implementation resources.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.
