# Apple In-App Purchase

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Use In-App Purchase for digital goods, premium features, and digital subscriptions. Apple Pay serves physical goods/services and donations. Consumables deplete and can be rebought; nonconsumables do not expire; auto-renewables continue until canceled; nonrenewing subscriptions require a new purchase to extend time. Advanced Commerce API serves qualifying complex, frequently updated/multicreator catalogs and bundled subscription add-ons; consult eligibility and review rules.

<a id="Best-practices"></a>
## Best practices
Let people experience value before purchase, keeping shopping integrated with app styling. Use short clear names/descriptions and always show the complete billed price. Show a usable store only where payments are allowed, explaining parental/payment restrictions if needed. Use the system confirmation sheet without imitation or modification.

<a id="Supporting-Family-Sharing"></a>
### Supporting Family Sharing
Eligible nonconsumables/auto-renewables can be shared with up to five additional family members across devices. Highlight sharing in product names/signup information, explain benefits and the system’s notifications/settings, and tailor copy for both the purchaser and family recipients.

<a id="Providing-help"></a>
### Providing help
Offer missing-purchase help, FAQs, support/feedback, contextual product/date information, and alternatives such as immediate fulfillment, while keeping a clearly labeled refund request readily visible without extra scrolling/screens. Hand off to the system refund flow; do not speculate about Apple’s approval or refund policies. A help link to Apple’s refund explanation is appropriate.

<a id="Auto-renewable-subscriptions"></a>
## Auto-renewable subscriptions
Explain benefits and terms during onboarding with a clear action. Offer suitable content tiers/durations and sampling via freemium access, metering, or trials. Prompt at meaningful moments and make subscribing generally findable. Do not advertise a new subscription to an existing subscriber; let cross-app/web customers sign in instead of paying again.

<a id="Making-signup-effortless"></a>
### Making signup effortless
Give distinct short option names, price/duration, introductory price and period, and subsequent standard price. Ask only essential initial data. On tvOS, use another device/code for entry/authentication. Signup must include subscription name, period, included service/content, localized complete billing amount, sign-in/restore for existing purchasers, and Terms/Privacy links. Put full billing totals above equivalent-period price breakdowns. Clearly state trial length and automatic billing after it. Include signup in settings.

<a id="Supporting-offer-codes"></a>
### Supporting offer codes
One-time codes from App Store Connect work through redemption links, supported in-app UI, or App Store entry; choose these for restricted/small distributions. Custom reusable codes fit mass campaigns and redeem by URL or supported in-app UI, not App Store account settings. Custom codes use ASCII letters/numbers only. Explain offer terms and redemption clearly. A Redeem Code action should open the system flow; it can appear in paywalls, onboarding, or settings. Optional promotional art replaces the default app icon. Apply unlocked entitlements immediately and welcome people appropriately, including those who redeemed before first launch.

<a id="Helping-people-manage-their-subscriptions"></a>
### Helping people manage their subscriptions
Show subscription summaries and upcoming renewal near account/settings management. Prefer system subscription UI for upgrade/downgrade/cancel. Relevant alternative plans, discounts, or later win-back offers can help, but cancellation must remain easy to identify and reach.

<a id="Platform-considerations"></a>
## Platform considerations
No extra iOS/iPadOS/macOS/tvOS/visionOS rules.

<a id="watchOS"></a>
### watchOS
Include the same required subscription information while explicitly describing device-specific content/function differences. A modal sheet can present the complete details with a convenient Close; custom flows also need Close/Cancel to free content. Make duration/discount comparisons compact, either separate purchase buttons locked to descriptions or a list plus a clearly labeled purchase button reflecting the chosen option.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase) for linked Apple design assets and implementation resources.

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
Source revision dates: September 17, 2026, September 12, 2023, November 3, 2022.
