# Express checkout repair

Patched `interface.md` in place, replacing the original single-paragraph flow with an implementable iPhone cart checkout specification. This is specification work; no app or payment backend was supplied.

## Decisions and changes

| Supplied behavior | Revised contract and reason |
| --- | --- |
| Custom Apple Pay lookalike with modified logo | Apple's generated localized Buy-type button opens the system sheet. Explicit placement, dimensions, contrast, setup, and unsupported-device fallback replace imitation branding. |
| Card details required first | Guest Apple Pay uses sheet payment/contact data directly; card checkout is a separate secondary action. Required bicycle choices remain part of the cart. |
| Shipping/tax hidden until after authorization | Sheet shows subtotal, discount, shipping, tax, merchant total and delivery method before approval. Address/method/coupon changes refresh the quote; unresolved pricing blocks authorization and changed final pricing requires fresh approval. |
| Cancellation treated as failed order | Return to intact cart, stop processing, and permit retry after resolving the attempt. Cancellation, timeout, confirmed failure, unknown outcome, and success have distinct transitions. |

The cart buys all its bicycles with one shipping address/method. Concise sheet summaries, optional post-purchase account creation, essential data requests, and confirmation details follow the local [Apple Pay guidance](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Streamlining-checkout). Generated branding and availability follow [Using Apple Pay buttons](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Using-Apple-Pay-buttons). Cancellation and validation follow [Handling problems](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Handling-problems).

The specified 44 pt control height/hit region applies the general [Buttons guidance](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices) while exceeding the Apple Pay visual minimum of 30 pt. Minimal contact collection follows [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices). Quote locking, attempt idempotency, reconciliation, and conditional carrier/processor fields are product decisions; the HIG snapshot does not establish processor APIs or transaction guarantees.

## Worked before/after

Illustrative numbers only, in USD: a bicycle costs $800, discount is $50, shipping is $30, and assumed tax is $62.40. Total: $800 − $50 + $30 + $62.40 = **$842.40**. This is not a tax calculation rule or actual shop quote.

**Before:** A shopper taps the altered logo, types card details, and authorizes without seeing shipping or tax. The flow reveals $842.40 afterward. If the shopper cancels, it reports a failed order.

**After:** The shopper chooses the bicycle's size/color and taps the generated Buy with Apple Pay button. Without manual card entry, the system sheet uses their selected shipping address and shows subtotal $800, discount −$50, shipping $30, tax $62.40, and “Example Cycle Shop” total $842.40 (placeholder merchant name, to be replaced with the statement name). Choosing another address recalculates the quote before authorization. Cancel returns to the unchanged cart without a failed order. Retrying opens a new sheet after the prior attempt resolves. Authorization and confirmed payment produce one order and a delivery confirmation; an unknown network outcome enters reconciliation rather than another charge.

## Acceptance checks and observed status

**Passed — static specification inspection:**

- `interface.md` now replaces all four supplied defective behaviors with explicit required behavior.
- The written flow distinguishes cart scope, required selections, supported/configured/setup/unsupported states, and separate card checkout.
- The written sheet contract includes all cost components before approval, price refresh, validation, pending-price treatment, and fresh authorization for changed totals.
- Outcome rows distinguish cancellation, timeout, actual processing failure, unknown outcome, and confirmed success. Cart preservation and duplicate prevention are specified.
- Arithmetic in the worked example reconciles to $842.40.

**Failed:** No remaining failure was identified in the static contract checks above. The original four behaviors fail the revised contract. This is not a runtime pass.

**Not executed — implementation acceptance checks:**

1. On an iPhone, inspect generated/localized button appearance, 140 pt captioned minimum width, 44 pt chosen target/height, clear space, contrasting styles, and small-screen/large-text layout. Verify actual hit geometry and VoiceOver names/order; reading this specification cannot prove them.
2. Exercise configured, supported-unconfigured, and unsupported capability states. Confirm setup returns to the cart and card checkout remains available without gating Apple Pay.
3. In payment sandbox, buy a multi-item cart as a guest. Verify sheet fields, coupon entry, redacted-address quoting, address/method changes, full total, merchant name, system authentication/progress, and one confirmed order.
4. Exercise missing bicycle choices, unsupported destination, malformed contact data, unresolved quote, and a final-address price change. Verify focused remedies and no charge without approval of the complete current quote.
5. Cancel before submission and during processing; simulate sheet timeout, declined payment, delayed callback, duplicate callback, and lost network response. Verify cancellation/void requests, provider reconciliation, preserved cart, safe retry, and no duplicate charges/orders.
6. Verify success confirmation, receipt/delivery details, removal of only purchased items, absence of unnecessary fields/permissions, and actual data storage/logging/disclosures.

## Evidence limits and reading route

Used only supplied `interface.md` and installed local instructions/references; no web browsing. Official links above are source attribution from the local snapshot, not live verification. No device, SDK build, GUI, VoiceOver, payment sandbox, server integration, security, or accessibility execution occurred. Provider capabilities, deployment target, actual merchant identity, supported markets, carrier requirements, and real tax/shipping rules remain implementation inputs.

Auditable installed-package route, with each file read separately: `apple-hig/SKILL.md`; search of `references/topic-index.md`; technologies family → `.topics/apple-hig-apple-pay/SKILL.md` → `references/apple-pay.md`; menus-and-actions family → `.topics/apple-hig-buttons/SKILL.md` → `references/buttons.md`; foundations family → `.topics/apple-hig-privacy/SKILL.md` → `references/privacy.md`. All these paths resolve under `.agents/skills/apple-hig/`, with topic/reference paths beneath their respective `subskills/apple-hig-…/` family directories. Each family and procedure was consumed before its source guide. The selected route repairs an existing iOS purchase flow; it does not establish new platform support or choose a replacement payment framework.
