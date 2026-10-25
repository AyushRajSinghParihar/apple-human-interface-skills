# Privacy

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/privacy) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Communicate collection and usage clearly and protect granted data. Keep App Store privacy disclosures accurate for new releases and updates; people rely on them before downloading.

<a id="Best-practices"></a>
## Best practices
Collect only what the specific feature requires and make access as precise as possible. Respect Hide My Email, Mail Privacy Protection, and tracking choices. Prefer on-device processing, including Create ML/Neural Engine where useful, to avoid unnecessary server transfers. Use system encryption, key management, and established security protections, including CloudKit’s additional encrypted data types where available.

<a id="Requesting-permission"></a>
## Requesting permission
Protected categories include personal/location/health/financial/contact information, user-created content, messages/calendar/music/gameplay/HomeKit data, media, Bluetooth/Wi-Fi/local network resources, camera/microphone, the advertising identifier, and permission-gated ARKit data in a visionOS Full Space. The system displays the app’s purpose string and stores choices/descriptions in privacy settings.

Ask when the person invokes the relevant feature. Request at launch only when access is essential and obviously necessary, such as location for navigation or room information for a spatial game that needs walls. Write a short, specific, active, complete sentence in sentence case with a period, explaining both use and reason. Vague promises of a better experience and commands to enable access do not explain the need.

<a id="Pre-alert-screens-windows-or-views"></a>
### Pre-alert screens, windows, or views
Usually context explains the request. If extra explanation is essential, use one button clearly leading to the system alert, such as Continue/Next; do not label it Allow or mimic the actual consent choice. Do not add cancellation, close, or other actions except those needed for legal consent. These restrictions apply to pre-permission custom explanations, not ordinary unrelated onboarding screens.

<a id="Tracking-requests"></a>
### Tracking requests
Show the AppTrackingTransparency alert before collecting tracking information, including if tracking begins at launch. Do not offer incentives, imitate a permission prompt, display an image of the alert, annotate behind it, or otherwise manipulate rushed choices. Such patterns can cause App Review rejection. A legally required consent view before/after the system alert is permitted by the source’s stated review guidance.

<a id="Location-button"></a>
## Location button
On iOS/iPadOS/watchOS, the system location button provides one-time access at the task’s moment of need. The first tap teaches and confirms its behavior through a system alert; later taps grant access without repeating that education. Authorization expires when app use ends. With no prior status it resembles Allow Once; an existing While Using status is unchanged.

Use it for individual tasks such as attaching a location or finding a nearby item/store. Customize only the supplied title, filled/outline glyph, foreground/background colors, and corner radius. Keep all localized and accessibility-size text untruncated and maintain contrast/transparency limits. Persistent customization violations can prevent location access even though the button still triggers other app actions.

<a id="Protecting-data"></a>
## Protecting data
Prefer passkeys; if passwords remain, add two-factor verification. Use Face ID, Optic ID, or Touch ID to protect continued signed-in access where appropriate. Store secrets in the encrypted keychain, never plaintext files even with restrictive permissions. Prefer established authentication, Sign in with Apple, and Password AutoFill over invented schemes.

<a id="Platform-considerations"></a>
## Platform considerations
No extra iOS/iPadOS/tvOS/watchOS rules are listed.

<a id="macOS"></a>
### macOS
Sign externally distributed apps with a valid Developer ID. Use sandboxing to limit resource/data access; Mac App Store apps require it. Account for fast user switching rather than assuming the current person is the only signed-in account.

<a id="visionOS"></a>
### visionOS
System ARKit algorithms support lighting, mapping, persistence, segmentation, and related rendering in Shared Space without exposing raw data to apps. ARKit API access requires Full Space, and plane estimation, scene reconstruction, image anchoring, and hand tracking require permission. Gaze remains private: system hover feedback can respond before a tap without disclosing where someone looks. Compatibility back-camera input is blank; front-camera input represents spatial Personas with permission. Adapt imported phone/tablet camera-dependent features by removal or content import instead of assuming conventional camera capture.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/privacy) for linked Apple design assets and implementation resources.

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
Source revision dates: June 21, 2023.
