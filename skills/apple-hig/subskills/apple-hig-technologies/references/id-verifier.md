# ID Verifier

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/id-verifier) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

From iOS 17, ID Verifier supports in-person reading of ISO 18013-5 mobile IDs on iPhone without external readers. Apple manages important certificate issuance/validation components.

Display Only requests show identity data/photo solely in system UI for visual checking, without transmitting it to the app. Data Transfer requests require a legal verification need to store/process details and an additional entitlement.

<a id="Best-practices"></a>
## Best practices
Request only necessary attributes; use an age-threshold test instead of date of birth or current age when that answers the question. Eligible organizations should register in Apple Business Register so customers see a verified name/logo. Start verification with a clear age/identity button, avoiding NFC/QR-specific symbols and any Apple logo. For Display Only, provide an outcome choice such as a portrait match/nonmatch so the requester can report the visual decision.

<a id="Platform-considerations"></a>
## Platform considerations
The source is iOS-only and marks all other platforms unsupported.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/id-verifier) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Videos"></a>
#### Videos
Apple’s linked design sessions provide demonstrations and additional implementation context; no video review is implied here.

<a id="Change-log"></a>
## Change log
Source revision dates: September 12, 2023.
