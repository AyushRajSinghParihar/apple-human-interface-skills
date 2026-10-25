---
name: apple-hig-apple-pay
description: Use when designing or reviewing Apple Pay checkout, payment-sheet fields, generated buttons, express purchase, recurring payment disclosures, or processing recovery.
---

# Keep payment scope and authorization unambiguous

Read [Apple Pay](../../references/apple-pay.md). Inspect goods/services, checkout scope, supported devices/browser, required fulfillment data, pricing, and requested design/review/adaptation. Preserve the existing payment integration. Digital-content purchases require the separate In-App Purchase decision; verify current service/regional eligibility when implementing.

Choose the purchase scope before the button: product-page express buys that one item, while cart express buys the cart with one address/method. Collect necessary product choices and out-of-sheet options such as split shipping or pickup location before payment. Prefer guest checkout and use current sheet contact/shipping information, requesting only essential fields.

Use Apple's generated localized button with the appropriate action type, prominence, contrast, and dimensions from the guide. The acceptance mark is noninteractive; a generic custom purchase button must not impersonate an Apple Pay button. On supported but unconfigured devices, offer appropriate setup. Missing product selections should produce a clear focused correction after activation rather than silently disabling payment.

In the sheet, use concise fees/discounts/pending or recurring-payment line items and a statement-recognizable merchant total, not the entire cart. Explain frequency, trial/current charge, future costs, and preauthorization accurately. Use system progress. Validate data when available with specific remedies; on cancellation/timeout that dismisses the sheet, cancel in-flight processing and permit a clear retry. Donations require approved nonprofit status.

**Before → decision → after:** A florist's product button charges the whole cart, asks for an account first, and continues charging after the sheet times out. Decision: express scope and cancellation must match expectations. After, product express purchases only the chosen bouquet, optional instructions are collected outside the sheet, guest checkout uses necessary delivery fields, and a dismissed timeout cancels pending processing before retry.

Deliver the checkout/sheet/error contract or corrected implementation. Fail if the charged scope differs from the button context, unnecessary fields gate payment, later charges are concealed, or cancellation can cause duplicate processing. Report actual payment sandbox/device/server evidence; a UI artifact cannot prove authorization or transaction correctness.

Use [Apple In-App Purchase](../apple-hig-apple-in-app-purchase/SKILL.md) for digital access, [Privacy](../../../apple-hig-foundations/.topics/apple-hig-privacy/SKILL.md) for minimal data, or [Wallet](../apple-hig-wallet/SKILL.md) for a resulting pass rather than payment authorization.
