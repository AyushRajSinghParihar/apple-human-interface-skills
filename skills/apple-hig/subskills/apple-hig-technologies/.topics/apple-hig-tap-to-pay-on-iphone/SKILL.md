---
name: apple-hig-tap-to-pay-on-iphone
description: Use when designing or reviewing merchant Tap to Pay setup, administrator terms, payment-method choice, card reading versus authorization, and PSP recovery.
---

# Distinguish a successful read from an approved payment

Read [Tap to Pay on iPhone](../../references/tap-to-pay-on-iphone.md). Inspect merchant/staff roles, PSP-owned versus app-owned UI, enablement state, checkout totals, read/authorization results, and requested design/review/adaptation. Preserve the supported PSP/SDK integration and verify current entitlement/device/market conditions. The source is iOS-only.

Resolve setup before customer checkout where possible: use API status, required OS readiness, administrator-only terms acceptance, and an appropriate administrator route for other staff. Offer findable current system/approved education covering positioning, payment types, PIN/accessibility, and terms where still needed.

Keep checkout payment choices accessible even before enablement/configuration. Prepare at launch/foreground entry; use indeterminate progress unless real measured progress exists. Selection may complete necessary setup and continue automatically, and merchants should switch to hardware/another method without visiting settings. Resolve tips and other total changes before the read screen. Use appropriate app-styled Tap to Pay wording and supported wave glyphs, never an Apple logo.

After reading, do not label the tap/PIN checkmark “Payment approved.” Send encrypted data promptly to the PSP, then show authorization progress and an explicit approved/declined result after the animation. Provide actionable alternatives for unreadable/unsupported/PIN/amount limits and follow PSP guidance for authentication/offline fallback. Nonpayment card or independent loyalty reading needs a clearly nonpayment action label.

**Worked transformation:** Before, a merchant sees “Paid” at the reader checkmark and hands over goods while authorization is pending; unavailable cards send staff into Settings. Decision: read completion is not approval. After, the flow shows “Authorizing” until the PSP result, then a clear receipt/decline state, with another card/payment method accessible in checkout.

Deliver role/setup/checkout/read/authorization/recovery states or implementation. Fail if nonadministrators accept terms, a final amount changes after reading, or read success is mistaken for authorization. Actual PSP settlement, card/PIN behavior, device configuration, and accessibility modes need supported integration tests; UI inspection cannot prove payment success.

Use [Apple Pay](../apple-hig-apple-pay/SKILL.md) for customer-side authorization and [Writing](../../../apple-hig-foundations/.topics/apple-hig-writing/SKILL.md) for merchant results/remedies.
