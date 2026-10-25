# Tap to Pay on iPhone

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Tap to Pay turns a merchant’s iPhone into a contactless reader alongside existing hardware. Integration needs a supported payment service provider, entitlement, and ProximityReader directly or through its SDK. Follow PSP-supplied UI guidance where the SDK owns the experience.

<a id="Enabling-Tap-to-Pay-on-iPhone"></a>
## Enabling Tap to Pay on iPhone
Use API status to show terms only when needed and complete acceptance before initial device configuration, ideally before customer checkout. Only an administrator may accept; explain this to other staff and support administrator acceptance via an appropriate web/other-device/app route through the PSP. If the PSP needs a newer iOS, update before showing acceptance.

<a id="Educating-merchants"></a>
## Educating merchants
Provide a findable tutorial through onboarding, post-acceptance, Learn More, and persistent help/settings. Prefer current localized ProximityReaderDiscovery education or approved assets. Cover each payment type’s launch, card/wallet positioning, PIN entry including accessibility mode, and a final terms-acceptance opportunity where still needed.

<a id="Checking-out"></a>
## Checking out
Offer the option even before enablement or while configuration runs; selection can open necessary acceptance then proceed automatically once ready. Prepare at app start and every foreground entry to reduce wait. Show indeterminate progress unless the configuration API provides ongoing measurable progress. Keep the option visible without scrolling, or launch automatically when it is the sole method. Let merchants switch between reader hardware/payment methods during checkout without visiting settings, and consider coordinated setup.

For payment buttons use Tap to Pay on iPhone or the shorter Tap to Pay; if this is the only method, existing Charge/Checkout is acceptable. With multiple icon-labeled methods, use `wave.3.right.circle` or its filled variant, never the Apple logo. Match app button styling. Resolve tips, payment types, and other total-changing choices before showing the read screen so the final amount is clear.

<a id="Displaying-results"></a>
## Displaying results
A successful tap/PIN checkmark confirms reading, not final transaction approval. Send encrypted read data promptly to the PSP, optionally requesting it before the completion animation ends. After that animation, show authorization progress until a clear approved/declined result. Offer digital receipts where possible. On unreadable/unsupported/amount/PIN-limited cards, allow another card, cash, external hardware, or payment link. Consult PSP guidance for post-read Strong Customer Authentication PIN or offline-PIN fallback requirements in relevant markets. Give actionable system-error explanations, such as updating iOS, and direct support access for unresolved failures.

<a id="Additional-interactions"></a>
## Additional interactions
For reading without a transaction amount—lookup, stored card, verification, refund—use a generic action label rather than Tap to Pay. NFC Wallet loyalty/discount/points passes can be read with payment or separately; independent loyalty reading needs its own clearly labeled nonpayment action to avoid confusion.

<a id="Platform-considerations"></a>
## Platform considerations
The source lists iOS only and marks other platforms unsupported.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Change-log"></a>
## Change log
Source revision dates: January 17, 2024, May 7, 2024, March 3, 2023, September 14, 2022.
