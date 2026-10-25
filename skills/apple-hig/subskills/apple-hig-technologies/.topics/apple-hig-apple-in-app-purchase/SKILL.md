---
name: apple-hig-apple-in-app-purchase
description: Use when designing or reviewing digital purchases, paywalls, subscription terms, restore/sign-in paths, offer redemption, Family Sharing, or purchase help.
---

# Explain the entitlement before the purchase

Read [Apple In-App Purchase](../../references/apple-in-app-purchase.md). Inspect what is sold, entitlement duration, existing-customer paths, prices/offers, and requested design/review/adaptation. Preserve the payment stack; use current platform documentation for implementation/eligibility rather than treating this design snapshot as current commercial policy.

Classify the product first: digital goods/features/subscriptions use this model; physical goods/services and donations belong to Apple Pay guidance. Choose consumable, nonconsumable, auto-renewing, or nonrenewing behavior according to what access means. Advanced Commerce needs eligibility, not merely a large catalog.

Show usable value before prompting and keep purchase discovery integrated. Use clear short product names, complete localized billed amounts, and the unmodified system confirmation. For subscriptions, display included service, period, full billing total, any introductory/trial duration, subsequent price and automatic billing, Terms/Privacy, and sign-in/restore for existing purchasers. Keep full totals more prominent than equivalent-period breakdowns; never resell a new subscription to someone who already has access. TV should reduce entry through another device/code; Watch still needs complete terms and an easy close/cancel route.

Define what follows redemption/purchase and how people manage access. Apply entitlements promptly, support prelaunch redemption, explain eligible Family Sharing for purchaser/recipient, and make subscription management/cancellation easy to reach. Purchase help should show useful product/date context and an obvious system refund request; do not promise Apple's refund outcome.

**Worked transformation:** Before, a language app advertises “Only $2/month,” bills annually, hides restore, and shows the same offer to active subscribers. Decision: terms and existing access must be explicit. After, the paywall leads with the full annual charge and period, explains any trial-to-paid transition, exposes sign-in/restore, and routes existing subscribers to content/management instead of repurchase.

Deliver corrected offer/paywall/help states or implementation. Fail if the billed total is obscured, existing purchases cannot be recovered, trial billing is ambiguous, or cancellation/refund access is buried. Static copy review cannot establish StoreKit transactions, entitlement synchronization, eligibility, or refunds; identify sandbox/device checks still pending.

Use [Apple Pay](../apple-hig-apple-pay/SKILL.md) for physical commerce and [Writing](../../../apple-hig-foundations/.topics/apple-hig-writing/SKILL.md) for precise offer/help language.
