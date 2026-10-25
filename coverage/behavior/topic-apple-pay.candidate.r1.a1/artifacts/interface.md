# iPhone bicycle shop — cart express checkout

## Scope and entry

Platform: iOS on iPhone. This checkout purchases physical bicycles, so use Apple Pay rather than digital-content In-App Purchase. Preserve the existing app stack and payment provider; this is a behavior specification, not an SDK implementation.

Cart express checkout buys all cart items using one shipping address and one shipping method. Show bicycle model, size, color, quantity, prices, and stock in the cart. Resolve required bicycle choices before opening payment. If a choice is missing when Apple Pay is activated, explain it and focus the relevant choice; do not silently disable the button. Split shipments are outside this express flow and must be resolved before entering it.

## Cart payment controls

- Remove the custom Apple Pay lookalike and modified logo. Generate the localized **Buy with Apple Pay** button through Apple's system APIs; never draw the button or alter its branding. Use the generated Buy type for this general cart purchase.
- Place it prominently above the secondary **Check out with another payment method** action, at least as large and prominent, visible without scrolling in the default cart layout. Keep the primary action near the middle/lower display without covering cart information or system navigation.
- Use automatic system appearance with sufficient background contrast. Project layout: at least 140 pt wide and 44 pt high, expanding for available width/localization, with at least 4.4 pt outside clearance at that height. The local Apple Pay guide's captioned-button minimum is 140 × 30 pt with clearance of one tenth of height; 44 pt height is this project's choice, not that guide's minimum.
- On unsupported devices, omit Apple Pay and retain ordinary checkout. On supported devices without configured Apple Pay, offer the generated Set Up Apple Pay action in a clearly identified setup interstitial; setup does not place an order. Recheck readiness on return. Capability/API details require implementation verification.
- Do not request typed card details, sign-in, or account creation before Apple Pay. Guest purchase is the default. Manual card entry belongs only to the separately selected ordinary checkout path. Optional account creation may follow success.

## Payment sheet and pricing contract

Activating the ready button opens the system Apple Pay sheet in the existing purchase context. Use its payment selection, authentication, validation, and progress presentation; do not imitate these in custom UI.

Request the current shipping recipient/address for bicycle delivery and email for the order receipt/status. Request billing details only if the payment provider requires them, documenting that requirement. Do not request phone, contacts access, location access, or raw card entry for this flow. Use the sheet's current address rather than overwriting it with a stale saved address. Send fulfillment/contact data only to services needed to process and deliver the order; keep payment credentials within the established payment integration. Explain: “We use your delivery address to ship your bicycle and your email to send your receipt and order updates.” Review privacy disclosures when implementing these data flows.

The cart shows subtotal, any known shipping/tax, and the current total. If destination is unknown, label shipping/tax as awaiting address; do not imply the subtotal is the final price. In the sheet:

1. Validate the available destination and offer shipping methods with price and estimated delivery date/range. Use redacted address data available before authorization for quotes; never assume the full address is available then.
2. On address, method, or promotion change, recalculate shipping, tax, discount, and total. Discard stale quote responses. A quote in progress or invalid destination cannot authorize a stale total. If available address data cannot establish the final amount, stop express checkout with a clear remedy rather than concealing later costs.
3. Show concise summary lines: bicycle subtotal, discount if applicable, shipping, tax, and final total. Keep detailed cart contents in the cart, not duplicated item by item in the sheet. Label the total with the shop's actual statement-recognizable merchant name; confirm that name with the payment provider before release.
4. Allow promotion-code entry in the sheet using supported integration facilities. A rejected code explains the issue without discarding cart/address state. Any pricing change must be visible in the sheet before authorization. No shipping/tax surcharge is added after authorization without a fresh review and authorization.

## Outcomes and recovery

| State/event | Required behavior |
| --- | --- |
| Address or shipping validation error | Keep the sheet open when supported. Identify the field and remedy, such as “Delivery unavailable for this address”. Accept reasonable address formatting variants. Validate again when full data becomes available. |
| Authorization submitted | Use system progress. Freeze the authorized cart/quote for this attempt and submit once. Guard repeated callbacks with an attempt identifier and server idempotency. |
| Payment and order confirmed by server | Report success in the sheet, then show order number, purchased bicycles, final amount, shipping address/method, delivery estimate, and status access. Remove only the purchased cart contents. Authorization alone is not order success. |
| User cancels or sheet times out/dismisses | Cancel in-flight processing for that attempt. Return to the preserved cart without “failed order” messaging or a failed-order record. No order is created solely for opening/canceling the sheet. The Apple Pay button permits a fresh attempt after cancellation is resolved. |
| Recoverable payment rejection | Give a specific available remedy in the sheet, such as choosing another payment method. Retain cart and fulfillment selections. |
| Network/processor outcome unknown | Show “Checking payment status” and reconcile the attempt with the server before allowing another charge. Never call an unknown result a confirmed failure or invite an immediate duplicate payment. |
| Confirmed processing failure | Explain the failure and offer retry with the Apple Pay button or ordinary checkout. Preserve cart and valid selections; a retry uses a fresh attempt identifier. |

Cancellation after processing has begun requires a server/provider cancellation and reconciliation path. Suppress late callbacks from advancing a canceled attempt. If a charge already completed despite dismissal, reconcile it, show the true order/payment status, and resolve any unwanted payment through the provider's reversal/refund process. Do not promise that dismissing UI alone reverses a completed charge. Idempotency and reconciliation are project reliability requirements supporting the HIG cancellation behavior.

On app interruption, retain cart, choices, and attempt identifier. On resume, reconcile any submitted attempt before presenting retry. Rotation and enlarged text preserve checkout context and keep totals/actions readable and reachable through reflow/scrolling. Preserve standard Back/swipe-back behavior outside the system sheet.

## Acceptance contract

- Ready cart opens the real system sheet directly without card typing or account gates; unsupported/setup states follow the specified alternatives.
- Inspect generated branding, localization, contrast, dimensions, and prominence on the target iPhone layout. No custom Apple Pay artwork remains.
- Changing address or shipping method updates all costs and the merchant total before authorization; stale quotes cannot be authorized. Unsupported destinations have a field-specific remedy.
- Cancellation before submission returns an unchanged cart with no failed-order record. Cancellation/timeout during processing cancels/reconciles the attempt; late callbacks and repeated taps cannot create duplicate charges/orders.
- Successful payment yields a server-confirmed receipt and shipping details. Rejection, offline/unknown outcome, and retry each follow the table above.
- Verify interruption/resumption, portrait/landscape, enlarged text, generated-button VoiceOver behavior, and focus to missing choices on real implementation. These are required future checks, not executed results.

## Guidance basis

Decisions use the installed local HIG snapshot. Official links identify the source sections; no web verification was performed:

- [Apple Pay — offering and streamlining checkout](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Offering-Apple-Pay): physical-goods scope, availability, cart scope, guest purchase, current shipping data, essential fields, sheet totals, and confirmation.
- [Apple Pay — buttons](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Using-Apple-Pay-buttons): generated branding, type, appearance, size, and placement.
- [Apple Pay — handling problems](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Handling-problems): validation, cancellation, timeout, and retry.
- [Privacy — best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices): minimum necessary collection and accurate disclosures.
- [Designing for iOS — best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices): reachable actions, system navigation, adaptation, and continuity.
