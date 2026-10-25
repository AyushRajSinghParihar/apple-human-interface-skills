# Wallet

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/wallet) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

## Contents

- [Passes](#Passes)
- [Pass anatomy](#Pass-anatomy)
- [Designing passes](#Designing-passes)
- [Pass styles](#Pass-styles)
- [Pass images](#Pass-images)
- [Order tracking](#Order-tracking)
- [Identity verification](#Identity-verification)
- [Platform considerations](#Platform-considerations)
- [Resources](#Resources)
- [Change log](#Change-log)

Wallet stores cards, IDs, passes, and keys on phone/Watch and supports payments, identity, and order tracking. Use PassKit/system interfaces to keep these exchanges familiar and trusted.

<a id="Passes"></a>
## Passes
Offer system one-tap addition after a relevant purchase/registration; for predictable repeat additions, request one-time background-add permission. The system notifies additions. A custom preview may include the Add to Apple Wallet button. Suggest externally created passes on the next app visit, but stop after refusal. Add related passes together and bundle web downloads. Keep an Add button available for absent/removed passes and a direct View in Wallet link for existing ones. Set expiry/relevance/voiding accurately, obtain deletion permission, and supply time/location metadata for Lock Screen or supported Live Activity suggestions. Update changing details, but reserve interruptive change messages for time-critical fields, never marketing or minor support-detail edits.

<a id="Pass-anatomy"></a>
## Pass anatomy
Fields specify visible information; semantic tags explain content to the system for suggestions and featured actions. Poster event and semantic boarding styles require tags and should also include fallback fields for older iOS. Supplemental sheets can link from the front; the back contains infrequently used legal/settings detail.

<a id="Pass-field-types"></a>
### Pass field types
Logo/name and header remain visible when collapsed. Primary fields convey the most important content, secondary/auxiliary fields useful supporting information, footer fields categories such as membership type, and back fields additional details. Exact arrangement depends on style.

<a id="Designing-passes"></a>
## Designing passes
Use Pass Designer templates or a blank canvas and create a clean digital pass rather than copying paper. Test phone/Watch variations and never put essential information solely in imagery/fields that disappear on another device. Keep fronts uncluttered, collapsed headers informative, brands recognizable, text well contrasted over art, and language device-independent. Do not pad image assets because Watch can crop whitespace.

<a id="Pass-styles"></a>
## Pass styles
<a id="Boarding-passes"></a>
### Boarding passes
Use for specific journeys/transit with origin/destination. Airlines use semantic tags; other transit types use fields.

<a id="Coupons"></a>
### Coupons
Use for offers and discounts.

<a id="Event-tickets"></a>
### Event tickets
Use for individual events or season access. Poster styles can use full-art backgrounds/semantics; nonposter styles use standard fields and can add background/thumbnail art.

<a id="Store-cards"></a>
### Store cards
Use for loyalty, points, discounts, and gift cards, showing a balance where relevant.

<a id="Poster-generic-passes"></a>
### Poster generic passes
Use a full-background layout for flexible cases outside other categories.

<a id="Generic-passes"></a>
### Generic passes
Use for remaining needs such as gym membership or coat-check claims.

<a id="Pass-images"></a>
## Pass images
Supply efficient PNG assets at @2x/@3x. Keep information as accessible fields/tags rather than embedded text, and add barcodes through APIs/Pass Designer instead of baking them into images. Always provide an icon.

<a id="Logo"></a>
### Logo
For nonsemantic airline/non-airline boarding, coupon, nonposter event, generic, and store passes: `logo.png`, 50–160 pt wide × 50 pt high, at top-leading. Avoid inner shadows that reduce readability.

<a id="Primary-logo"></a>
### Primary logo
For semantic airline, poster event, and poster generic passes: `primaryLogo.png`, 30–126 pt wide × 30 pt high, at top-leading.

<a id="Secondary-logo"></a>
### Secondary logo
For a poster event’s additional issuer/organizer: `secondaryLogo.png`, 12–135 pt wide × 12 pt high, at bottom-trailing.

<a id="Icon"></a>
### Icon
All pass styles use `icon.png`, 38 × 38 pt; supply square corners for system rounding.

<a id="Strip-image"></a>
### Strip image
Coupon/store `strip.png` is 375 × 144 pt. Keep text-background regions quiet and high contrast, put key art toward bottom/trailing, and do not embed text.

<a id="Thumbnail"></a>
### Thumbnail
Event/generic `thumbnail.png` is 60–90 pt wide × 90 pt high. Use rounded artwork and transparent PNG.

<a id="Background"></a>
### Background
Nonposter event `background.png` is 343 × 503 pt. Poster event/generic `artwork.png` is 358 × 448 pt. Keep content within safe areas, allowing for a material strip at the bottom and any barcode; preview in Pass Designer.

<a id="Footer"></a>
### Footer
Airline boarding `footer.png` is 268 × 15 pt.

<a id="Order-tracking"></a>
## Order tracking
Supply WalletOrders data immediately after purchase even while payment/fulfillment is pending, then keep status and shipping/pickup details current. Apple Pay can add order details automatically; from iOS 17, Track with Apple Wallet can appear on confirmation/status/tracking pages or email. Re-adding an existing order opens it. Provide opaque 300 × 300 px PNG/JPEG logo and distinct product images with simple solid backgrounds. Keep localized descriptions concise and the price equal to the confirmed final amount.

<a id="Displaying-order-and-fulfillment-details"></a>
### Displaying order and fulfillment details
Include a universal order-management link, clear per-item name/price/image data, all items at order level and only relevant ones per fulfillment, and optional transaction PDF receipts. Supply associated app IDs in priority order: link to the highest-priority app installed on the device, or to the first listed app when none are installed. Avoid duplicate app/Wallet notifications. Provide at least a merchant website plus useful phone/email/support/Messages contacts.

Support multiple shipping or pickup fulfillments with ETA, carrier tracking link/number, needed pickup barcode, and clear instructions. Keep fulfillment UI focused on tracking. Name the carrier only when known, otherwise retain the generic tracking label. Use detailed onTheWay/outForDelivery/delivered states only with supporting carrier data, otherwise shipped; provide a tracking link when available. Explain Issue/Canceled directly with cause and remedy.

<a id="Identity-verification"></a>
## Identity verification
From iOS 16 on iPhone, apps/Clips can request ID attributes from Wallet in context. Apple does not create/view the ID documents; the app receives encrypted data unreadable on-device. For in-person reader use, follow ID Verifier instead.

Offer verification only when supported and provide another method otherwise. Ask exactly when the transaction needs it, explain use through a concise active complete sentence with punctuation, and request only necessary fields such as an age threshold. For example, an account-opening identity check can explain that legally required identification helps prevent fraud; a rental driving-privilege check can explain that local law requires a valid right to drive. Specify retention intention/duration using system APIs so the sheet explains it. Choose Verify Age/Verify Identity when that finishes the transaction, Continue when more non-Wallet data is still required, or Verify with Apple Wallet when those labels do not fit and verification finishes the flow. Labels have automatic multiline variants. Use the system black button with white text, optional light outline against dark surfaces, and matching corner radius.

<a id="Platform-considerations"></a>
## Platform considerations
No extra iOS/iPadOS/macOS/visionOS rules; tvOS is unsupported.

<a id="watchOS"></a>
### watchOS
Passes appear in a scrolling carousel even without a Watch-specific app. Tapping reveals extra information in a scrollable details view, including overflow from the main layout. Every style can show different image/field subsets. Watch always crops strip art to the card’s aspect ratio and may remove whitespace from other images, so keep essential content out of vulnerable areas.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/wallet) for linked Apple design assets and implementation resources.

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
Source revision dates: June 8, 2026, January 17, 2025, December 18, 2024, September 12, 2023, February 20, 2023, November 30, 2022, September 14, 2022.
