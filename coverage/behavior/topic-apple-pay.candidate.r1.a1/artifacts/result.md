# Express checkout repair

Patched `interface.md` in place, replacing the original one-paragraph flow with an implementable iPhone cart checkout contract.

## Decisions

| Supplied behavior | Revised specification and reason |
| --- | --- |
| Custom Apple Pay lookalike with modified logo | Apple's generated localized Buy button opens the system sheet. Apple Pay's button guidance requires generated appearance; the acceptance mark is not a substitute interactive button. |
| Card typing before express checkout | Direct guest checkout with current sheet shipping/contact data; manual card entry is confined to ordinary checkout. This removes an unnecessary gate. |
| Shipping/tax hidden until after authorization | Address/method updates produce visible shipping, tax, discount, and merchant total before authorization. Unresolved or stale quotes cannot authorize. |
| Cancellation becomes a failed order | Return to the preserved cart, cancel/reconcile pending processing, and allow a safe retry. Unknown payment outcomes are reconciled before another charge. |

The patch also defines cart-wide scope with one destination/method, missing bicycle-choice correction, unsupported/unconfigured-device paths, validation copy, server-confirmed receipts, interruption recovery, and future layout checks. It retains the existing stack/provider because none was supplied to replace.

The 44 pt button height, receipt email choice, stale-quote protection, attempt identifiers, idempotency, and reconciliation details are concrete project decisions. They are not claimed as verbatim HIG requirements. Merchant name, actual delivery coverage/rates, tax calculation, provider-required billing fields, and API availability must be supplied/verified during implementation.

## Worked before/after

Illustrative USD fixture, not actual store pricing: one bicycle costs $1,000; standard shipping is $40; tax is $83.20; final amount is $1,123.20.

**Before:** The customer types card details, activates a modified Apple Pay lookalike, and authorizes without seeing shipping/tax. Those costs appear afterward. Canceling produces a failed order.

**After:** The customer confirms bicycle size/color in the cart and taps the generated Buy with Apple Pay button. The system sheet uses the selected address and displays bicycle subtotal $1,000, shipping $40 with a delivery estimate, tax $83.20, and merchant total $1,123.20 before authorization. Changing to $60 shipping triggers a new tax/total calculation before authorization; the prior quote cannot be charged. Canceling before submission returns to the cart with the same bicycle and no failed-order record. Reopening creates a fresh attempt. A confirmed purchase shows the server's order number and delivery details. If a submitted attempt's outcome is unknown, status reconciliation precedes another payment.

## Acceptance checks and results

**Passed — static specification inspection:** The revised file explicitly removes all four supplied defects, defines one-cart/one-address purchase scope, requests essential fulfillment data, separates cancellation/failure/unknown/success, and specifies costs before authorization. Required behavior and remedies are concrete enough to become implementation scenarios.

**Failed — original specification inspection:** Generated branding, direct express entry, preauthorization cost disclosure, and cancellation handling all failed against the supplied original text. These findings describe the original specification, not an observed running app.

**Not executed — implementation acceptance:**

1. On supported configured iPhone, open the genuine sheet with no card/account gate; test unsupported and setup paths separately.
2. Change destination, shipping, and promotions; verify exact totals, quote ordering, unsupported-address remedies, and inability to authorize pending/stale prices.
3. Cancel before authorization, dismiss/timeout during submission, inject a late success callback, and retry; verify provider cancellation/reconciliation and one charge/order at most per attempt.
4. Exercise processor rejection, offline/unknown outcome, successful order confirmation, and app interruption/resumption; verify preserved state and truthful status.
5. Check localization, Dark Mode, portrait/landscape, enlarged text, reachability, generated-button dimensions/contrast, VoiceOver behavior, and focus to missing options on the implementation.

## Evidence and limits

Read the installed root `.agents/skills/apple-hig/SKILL.md`, then the Technologies family and Apple Pay topic procedure before its article. Also read Getting started → Designing for iOS → its article, and Foundations → Privacy → its article. Each consumed file was read by its own `cat` command from the installed package. The source articles identify a local snapshot retrieved 2026-10-25; file presence does not establish independent source review.

Material source support: [Apple Pay: checkout](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Streamlining-checkout), [buttons](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Using-Apple-Pay-buttons), [problems](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Handling-problems), [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices), and [iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices). These links are attribution from local files, not browsed evidence.

Only the supplied text and installed guidance were used. No app code, SDK, device, GUI, accessibility session, payment sandbox, backend, or transaction execution was supplied or run. The patch establishes a design contract; it does not prove native rendering, availability, accessibility, tax correctness, payment correctness, security, or regulatory compliance. No current-web verification was performed, as requested.
