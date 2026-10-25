# Apple Pay

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/apple-pay) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

## Contents

- [Offering Apple Pay](#Offering-Apple-Pay)
- [Streamlining checkout](#Streamlining-checkout)
- [Displaying a website icon](#Displaying-a-website-icon)
- [Handling problems](#Handling-problems)
- [Supporting subscriptions](#Supporting-subscriptions)
- [Supporting donations](#Supporting-donations)
- [Using Apple Pay buttons](#Using-Apple-Pay-buttons)
- [Referring to Apple Pay](#Referring-to-Apple-Pay)
- [Platform considerations](#Platform-considerations)
- [Resources](#Resources)
- [Change log](#Change-log)

Apple Pay serves physical goods, services, eligible subscriptions, and donations through an authorized payment sheet, distinct from In-App Purchase for digital content. People authenticate with device-supported biometrics, Watch double click, nearby devices, or supported browser code flows.

<a id="Offering-Apple-Pay"></a>
## Offering Apple Pay
Offer it wherever supported, hiding the option on unsupported hardware/browsers. If checking for an active Wallet card, make Apple Pay primary wherever that API is used, without requiring a separate checkout path. System Apple Pay buttons initiate payment or appropriate setup only. A custom generic purchase button must omit Apple Pay text/logo; indicate acceptance separately with the mark or prose on the same page. The mark is noninteractive. Do not disable/hide a button merely because required product selections are missing; explain and focus the missing field after activation. Include accepted-payment semantic markup for search engines. Websites require privacy statements and compliance with Apple’s web acceptable-use rules.

<a id="Streamlining-checkout"></a>
## Streamlining checkout
Keep checkout cohesive with the app/site rather than new windows. Give Apple Pay prominent placement. Product-page express purchase covers one item only, excluding the cart; remove that item from the cart after purchase if necessary. Cart express checkout buys all items with one shipping method/address. Support coupon entry in the sheet. Collect necessary product options before checkout, and collect optional messages/instructions, split shipping, and pickup location outside the sheet. Use the current Apple Pay contact/shipping data. Prefer guest purchase with optional account creation afterward using already-provided fields. Show transaction results in the sheet, then a confirmation with shipping/status details. If mentioning payment afterward, place Apple Pay beside the final four account digits or a separate payment note.

<a id="Customizing-the-payment-sheet"></a>
### Customizing the payment sheet
Request only essential fields; a digital gift card does not need shipping. Show applied promotions and permit code entry where useful. Describe shipping methods with price and optional delivery/pickup date/range, respecting calendar/time zone; pickup slots can use the shipping-method range. Use short line items for fees, discounts, pending totals, donations, recurring/future payments, not an item-by-item cart. Label the total with the statement-recognizable business name; intermediaries should identify end merchant and intermediary together. Disclose later costs, pending amounts, or preauthorizations accurately where allowed. Use the sheet’s progress rather than duplicate spinners.

<a id="Displaying-a-website-icon"></a>
## Displaying a website icon
Provide a recognizable site icon for Handoff authorization and subscription Wallet contexts: 60 × 60 pt, supplied as 120 × 120 px @2x and 180 × 180 px @3x.

<a id="Handling-problems"></a>
## Handling problems
<a id="Data-validation-errors"></a>
### Data validation errors
Validate whenever available data allows, before and after authorization. Before authorization the app only receives card type and redacted shipping information. Use correct status/error codes and customized field-detail explanations. Accept reasonable variants and infer irrelevant formatting, such as ignoring ZIP+4 suffixes when only five digits matter and allowing different phone punctuation. Name the specific issue and remedy, using sentence-case noun phrases without final punctuation, ideally at most 128 characters.

<a id="Payment-processing-problems"></a>
### Payment processing problems
On timeout/cancellation that dismisses the sheet, cancel any in-flight payment. Let people retry with the Apple Pay button.

<a id="Supporting-subscriptions"></a>
## Supporting subscriptions
Recurring authorization can cover a fixed amount, such as a monthly membership, or a variable amount, such as a changing grocery order, only where local regulations permit variable recurring payments. The initial authorization can include discounts and extra fees. Explain recurring frequency and terms before authorization. Repeat frequency, discounts, and upfront charges in line items, including when first billing occurs. For trials show trial price, including zero, regular amount, and start date; the total must reflect what is charged now. Request a fresh sheet for changes only if fees increase. Billing agreement text is an optional concise plain-language summary, not formal terms or duplicated detail; leave it blank when unnecessary.

<a id="Supporting-donations"></a>
## Supporting donations
Only approved nonprofits may accept donations. Identify the donation in a line item and offer suggested amounts plus a custom-amount choice.

<a id="Using-Apple-Pay-buttons"></a>
## Using Apple Pay buttons
Always generate Apple Pay buttons through Apple APIs for approved appearance, localization, proportions, VoiceOver, and configurable corners; do not reproduce them as artwork/custom designs.

<a id="Button-types"></a>
### Button types
<a id="Apple-Pay-button"></a>
#### Apple Pay button
Choose the generated button type using the payment context and the words already used in the app or website. The system can display the default card on the button when Apple Pay is ready.

| Type | Selection criteria |
| --- | --- |
| Buy | General purchases from a product page or cart. |
| Pay | Paying a bill or invoice, including utilities and service work. |
| Check Out | A cart or purchase flow whose other payment buttons begin with “Check Out.” |
| Continue | A cart or purchase flow whose other payment buttons begin with “Continue.” |
| Book | Reserving flights, trips, or other experiences. |
| Donate | Donations to an approved nonprofit. |
| Subscribe | Buying an eligible recurring service, such as a gym membership or meal-kit plan. |
| Reload | Adding funds to a card, account, or service payment system when the app calls this action Reload. |
| Add Money | The same funding context when the app calls the action Add Money. |
| Top Up | The same funding context when the app calls the action Top Up. |
| Order | Placing an order, such as meals or flowers. |
| Rent | Renting a vehicle or another item, such as a car or scooter. |
| Support | Giving money to a cause, project, organization, or similar entity when the app uses Support. |
| Contribute | The same giving context when the app uses Contribute. |
| Tip | Gratuities for goods or services. |
| Plain Apple Pay | A neutral call to action or a design needing the smaller minimum width. The system may substitute it when the selected type is unavailable on the current OS version. |

<a id="Set-Up-Apple-Pay-button"></a>
#### Set Up Apple Pay button
On supported but unconfigured devices, offer explicit setup in settings, profile, or an interstitial.

<a id="Button-styles"></a>
### Button styles
Automatic follows system appearance.

<a id="Black"></a>
#### Black
Use against a sufficiently light contrasting background.

<a id="White-with-outline"></a>
#### White with outline
Use on light backgrounds where a white fill alone lacks definition; avoid dark/saturated surfaces.

<a id="White"></a>
#### White
Use against sufficiently dark backgrounds.

<a id="Button-size-and-position"></a>
### Button size and position
Make Apple Pay at least as large/prominent as other payment options without scrolling. Beside Add to Cart, put Apple Pay to its right; stacked, put Apple Pay above. Match corner radius to adjacent buttons. Minimum plain width is 100 pt, other listed captioned buttons 140 pt; all minimum heights are 30 pt and outside margins one tenth of height. At @1x/@2x, these are 100/200 px or 140/280 px wide and 30/60 px tall. Localized titles may force fallback to the plain button; Set Up has no such automatic replacement.

<a id="Apple-Pay-mark"></a>
### Apple Pay mark
Use only the supplied acceptance mark. Change its displayed height proportionally, keeping it no smaller than neighboring payment marks; do not independently change width, corners, border, aspect ratio, add marks/effects, reflect, rotate, or animate it. Leave at least one tenth of its height clear around it, without sharing borders with another control/graphic.

<a id="Referring-to-Apple-Pay"></a>
## Referring to Apple Pay
Keep two-word capitalization, no plural/possessive or translation, except all caps matching an all-caps design. Do not replace Apple with the Apple logo. In US body copy, add the registered mark on first reference, excluding checkout-option labels. Use the surrounding font rather than mimicking Apple typography. Text-only payment selection is allowed only when every payment choice is text-only; otherwise use the mark. Follow App Store marketing guidance for promotion.

<a id="Platform-considerations"></a>
## Platform considerations
No extra iOS/iPadOS/macOS/visionOS/watchOS rules; tvOS is unsupported.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/apple-pay) for linked Apple design assets and implementation resources.

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
Source revision dates: June 8, 2026, December 16, 2025, June 10, 2024, September 12, 2023, May 2, 2023.
