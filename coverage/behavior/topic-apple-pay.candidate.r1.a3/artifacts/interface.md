# Bicycle shop: iPhone express checkout

Platform: iOS. Physical bicycles ship to a selected address. Replace the custom Apple Pay lookalike flow with this contract; preserve the existing app stack and payment provider.

## Cart and entry

Express checkout purchases the entire cart, including selected bicycle size, color and quantity, with one shipping address and one shipping method. Display those selections and the merchandise subtotal in the cart. Collect necessary product choices before payment. If a choice is missing when Apple Pay is activated, explain the omission and focus the choice instead of silently disabling payment. Split shipping requires ordinary checkout before payment.

Use guest checkout. Do not require an account, login or manual card entry before Apple Pay. Optional account creation may follow purchase. Retain a separate “Check Out” action for ordinary checkout.

Replace the modified logo and custom button with Apple's API-generated, localized Check Out Apple Pay button. It opens the system payment sheet; tapping it does not charge immediately. Never redraw, distort or overlay its artwork. A separate acceptance mark uses the supplied Apple asset and is noninteractive.

Place Apple Pay above ordinary checkout, visible without scrolling in the cart payment area and at least as prominent as other payment options. Use automatic system appearance and a corner radius matching adjacent controls. Use full available content width, at least 140 pt width and 44 pt height, at least 4.4 pt clear outer margins, and nonoverlapping targets. Increase width for localization and retain system-supported fallback behavior. This design's 44 pt height follows general button targeting guidance and exceeds the Apple Pay-specific 30 pt minimum.

On unsupported devices, omit Apple Pay and retain ordinary checkout. On supported but unconfigured devices, offer the generated Set Up Apple Pay action in a labeled setup interstitial, with return to cart and ordinary checkout. Setup returns to the preserved cart without placing an order. Prevent repeated taps from opening multiple sheets.

## Payment sheet and data

Request current sheet shipping name/address for fulfillment and email for receipts and shipping updates. Do not request phone or billing contact without an established fulfillment/payment dependency. Do not collect raw card details or request address-book access. Use current sheet selections rather than silently substituting an old profile address. Send delivery information to order/fulfillment services and email to receipt/status services; do not enroll the buyer in marketing. Confirm actual provider needs, storage policies and privacy disclosures before release.

Offer shipping methods with price and delivery range. Recalculate availability, shipping, discounts, tax and total whenever the address, method or coupon changes. Support coupon entry in the sheet. Validate as soon as available data permits; preauthorization address information can be redacted, so finish validation when full information becomes available.

Show concise summary lines: Merchandise subtotal, Discount when applied, Shipping, Tax, and a final total labeled with the shop's actual statement-recognizable merchant name. Configure that name before release. Use consistent currency. Do not reproduce the whole cart inside the sheet. Resolve and display all costs for the selected address/method before authorization; never add hidden charges afterward. During calculation use system progress and prevent authorization of a stale quote. This purchase has no recurring or later charges.

For an undeliverable destination, provide a specific field-level remedy such as “Choose an address within our delivery area”. Preserve other valid selections and the cart. If stock or price changes, explain the change and require review of the refreshed amount before a new authorization. Use the sheet's progress and result feedback without duplicate app spinners.

## State and recovery contract

| Event | Required result |
| --- | --- |
| Activate Apple Pay | Validate product selections, snapshot the cart revision and open one system sheet for that cart. |
| Edit sheet selections | Update delivery options and all costs; prevent stale-quote authorization. |
| Authorize | Submit one payment attempt for the reviewed cart revision and amount. Block duplicate submission. Authorization alone is not order confirmation. |
| User cancels | Dismiss normally, cancel in-flight processing and preserve cart/selections. Record cancellation separately from failure; never show “Failed order” for cancellation. Restore Apple Pay retry after resolving the prior attempt. |
| Timeout dismisses sheet | Cancel in-flight processing and preserve the cart. Resolve the prior attempt before allowing another charge. |
| Definitive decline or processing failure | Explain the recoverable issue in the system sheet when available. Permit correction or retry after the previous attempt resolves; retain the cart. |
| Unknown payment outcome | Show “Checking payment status” and reconcile with the server/provider using the same attempt identifier. Do not announce success/failure or start another charge until resolved. |
| Confirmed success | Show the result in the sheet, then order confirmation with order number, purchased items, final amount/currency, address, shipping method/delivery range and order-status access. Remove only purchased items; preserve later additions. |

Product reliability requirements: enforce idempotency on the server, bind payment to the reviewed cart revision and quote, and deduplicate callbacks. Cancellation requests stop pending processing. If settlement wins a cancellation race, reconcile and show the confirmed outcome rather than permit duplicate purchase; do not claim cancellation reversed a completed charge. A new attempt is allowed only after the previous attempt has a definitive outcome. These engineering mechanisms require implementation verification.

## Source basis

Design basis: installed local HIG snapshot, [Apple Pay — streamlining checkout](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Streamlining-checkout), [Apple Pay buttons](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Using-Apple-Pay-buttons), [handling problems](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Handling-problems), [Buttons — best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), and [Privacy — best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices). Official links identify sources; they were not fetched for this work.
