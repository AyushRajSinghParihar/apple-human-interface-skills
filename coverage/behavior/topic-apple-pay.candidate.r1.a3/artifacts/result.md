# Express checkout repair

Patched `interface.md` in place, replacing the original one-paragraph flow with a concrete iPhone checkout specification.

## Decisions and changes

- Replace the modified-logo lookalike with Apple's generated localized Check Out button and system sheet. Specify prominence, geometry, setup and unsupported-device fallback.
- Purchase the whole cart with one address/method, preserve bicycle selections, and offer guest checkout without manual card entry.
- Use current sheet delivery information and receipt email. Show shipping, tax, discounts and the merchant-labeled final total before authorization; recalculate on changes and block stale quotes.
- Separate cancellation, timeout, decline, uncertain outcome and success. Preserve the cart on cancellation/failure and define safe retry, reconciliation and duplicate prevention.
- Confirm the purchased items and delivery details; preserve items added after payment began.

The supplied text explicitly establishes the four defects: custom branding, card-entry gating, hidden shipping/tax and cancellation classified as failure. These corrections follow the locally installed [Apple Pay guidance](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Streamlining-checkout), its [button guidance](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Using-Apple-Pay-buttons) and [problem handling](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Handling-problems). The design's 44 pt target follows general [Buttons guidance](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), exceeding the Apple Pay-specific 30 pt minimum. Essential data collection follows [Privacy guidance](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices). Links cite the local snapshot's official sources; no browsing occurred.

Server idempotency, quote binding, uncertain-outcome reconciliation and preservation of later cart additions are product engineering decisions supporting the flow, not backend algorithms prescribed by HIG. Email is a proposed receipt/status requirement. The shop must confirm provider dependencies, merchant identity, delivery policies and privacy disclosures before release.

## Worked before/after

Illustrative fixture, not supplied shop pricing: one selected bicycle costs USD 800.00, shipping to address A costs USD 30.00, and fixture tax is USD 66.40. Total: USD 896.40. Actual tax calculation remains a merchant/provider responsibility.

Before: the buyer taps a modified-logo lookalike, types card details, then authorizes without shipping or tax disclosed. Cancellation is treated as a failed order. The supplied brief establishes no actual charged amount or transaction outcome.

After: the buyer sees the selected bicycle in the cart and activates the generated Check Out Apple Pay button without typing a card or creating an account. The sheet uses address A and shows Merchandise subtotal USD 800.00, Shipping USD 30.00, Tax USD 66.40 and the configured merchant total USD 896.40. Changing the address refreshes shipping, tax and total before authorization. Cancellation returns to the intact cart without a failed-order message. Once cancellation resolves, retry opens a fresh sheet. Successful processing confirms one order for USD 896.40 with delivery details; duplicate callbacks create no additional charge/order.

## Acceptance checks and status

Passed — static specification review:

- All four original defects have explicit replacement requirements; iOS, physical bicycles and address-based shipping are preserved.
- Scope, generated controls, guest path, data purposes, complete cost disclosure and shipping updates are specified.
- Cancellation, timeout, failure, unknown outcome, retry and success have distinct transitions; unresolved attempts cannot simply be charged again.
- Worked arithmetic is consistent: 800.00 + 30.00 + 66.40 = 896.40.

Failed — revised specification review: none identified. This does not establish working implementation behavior.

Not executed — required implementation acceptance checks:

1. On an eligible iPhone, activate Apple Pay: exactly one native sheet opens without card-entry/login gates. Verify unsupported-device fallback and unconfigured-device setup without unintended purchase.
2. Change destination, shipping method and coupon: options and all costs refresh; stale totals cannot be authorized. Invalid destinations receive a specific remedy. Missing bicycle choices receive focused correction.
3. Cancel before authorization and during processing; simulate sheet timeout. Verify cart preservation, cancellation classification, cancellation of pending work, reconciliation and safe retry.
4. Simulate decline, lost network response, late settlement, repeated taps and duplicate callbacks. Verify no duplicate charge/order and no false confirmation/failure while status is unknown.
5. Complete sandbox payment: verify the exact reviewed cart scope, currency and amount; sheet result; confirmation and delivery details; purchased-item removal with later additions retained.
6. Verify on device the generated localization, appearance contrast, target geometry/spacing, unclipped labels, native states and VoiceOver identification/operation. These checks are pending, not accessibility results.

## Evidence limits and route audit

Explicitly read the installed `.agents/skills/apple-hig/SKILL.md`, inspected the supplied `interface.md`, and searched relevant rows of `references/topic-index.md`. Read each owning family, then topic procedure, then supporting source guide: Technologies → Apple Pay; Menus and actions → Buttons; Foundations → Privacy. All paths resolved under the installed apple-hig package. Each file was consumed through its own command. No web access was used.

Only a specification was supplied. No app/backend implementation, SDK documentation, build, payment sandbox, device, GUI or accessibility execution was available or performed. Local references are a dated, independent HIG-derived snapshot, not an SDK reference or proof of current provider capabilities. Native rendering, API availability, data storage, authorization correctness, cancellation races, physical comfort and accessibility behavior remain unverified. This work repairs the specification and does not certify a payment integration.
