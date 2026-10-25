# Managing accounts

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/managing-accounts)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Require an account only for essential core functionality; otherwise permit useful access without one. A consistent trusted sign-in method can reduce credential burden.

<a id="Best-practices"></a>
## Best practices

Explain account benefits and signup requirements briefly and defer sign-in until commitment is needed, such as purchase after browsing. Consider Sign in with Apple; otherwise prefer passkeys on iOS, iPadOS, macOS, and visionOS. If retaining passwords, strengthen them with two-factor authentication. Name the actual available method, checking device capabilities instead of mentioning unsupported Face ID. Avoid a redundant app-specific biometric opt-in when the system already manages it. Reserve passcode terminology for device/Apple authentication rather than implying people should reuse it for an app account.

<a id="Deleting-accounts"></a>
## Deleting accounts

An app that supports account creation must also support deletion rather than only deactivation. Clearly disclose legally required retention or special processes; applicable legal requirements need separate verification. Provide a discoverable in-app deletion route or direct deletion-page link, not a buried policy link. Revoke Sign in with Apple tokens when deleting that account. Keep web and app flows comparably straightforward. If scheduling later deletion, retain immediate deletion too. State the expected completion time and notify when complete.

Explain that deleting an account does not itself cancel an Apple auto-renewable subscription: billing continues until canceled, and subscription/refund management may still be needed. Provide management instructions. Support deletion even for subscriptions purchased elsewhere.

<a id="TV-provider-accounts"></a>
## TV provider accounts

Use system TV Provider Authentication when available. Do not offer independent sign-out for a system-authenticated provider; if an option is necessary, direct to Settings > TV Provider. Privacy access controls are not a sign-out mechanism.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, iPadOS, macOS, or visionOS rules are specified.

<a id="tvOS"></a>
### tvOS

Minimize remote data entry and prefer signup/authentication through another device with associated-domain credential suggestions. Shared account credentials can coexist with separate current-user profiles from tvOS 16; restore the current profile without repeatedly asking. For longer input, use a companion website; email keyboards can offer recent addresses.

<a id="watchOS"></a>
### watchOS

Use iCloud/keychain synchronization for credential autofill and retained app settings.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding)
[Sign in with Apple](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/AuthenticationServices/supporting-passkeys> — Authentication Services

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2025/279>
  <https://developer.apple.com/videos/play/wwdc2024/10143>
