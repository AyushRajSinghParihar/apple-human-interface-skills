Change the paywall so the actual charge and trial terms are clear before someone subscribes.

| Issue | What to change |
|---|---|
| **Annual price is visually misleading** | Make **“$59.88/year”** the primary price. Show “Equivalent to $4.99/month, billed annually” as secondary text. Keep billing terms legible and high contrast. |
| **“Start free” omits key terms** | State the trial duration and renewal terms prominently near the button: **“7 days free, then $59.88/year. Automatically renews unless canceled.”** Use your actual trial duration. A button such as **“Start 7-day free trial”** is clearer. Show a paid-subscription CTA to users who aren’t eligible for the trial. |
| **No access path for existing subscribers** | Add a visible **Restore Purchases** action. If subscriptions are associated with your own accounts, also add **Sign In**. Make both accessible without starting a purchase. |
| **Subscribers see the paywall after updates** | Check current StoreKit entitlements before presenting the paywall and unlock subscribed features automatically. An app update should not require a subscriber to buy again or manually restore. Handle loading and verification failures without treating users as unsubscribed. |
| **Custom code `SUMMER-25!`** | Change it to an alphanumeric code, such as **`SUMMER25`**; custom subscription offer codes don’t accept hyphens or punctuation. Configure eligibility, discount, duration, redemption limits, and expiration in App Store Connect. Redemption through App Store account settings is supported; also consider Apple’s redemption link or in-app redemption sheet. Explain the offer and subsequent renewal price wherever you promote it. |
| **Refund link is buried** | Put **Request a Refund** directly in subscription settings or a clearly visible billing-help section. Use Apple’s in-app refund request flow where supported, or link to **reportaproblem.apple.com**. Explain that Apple reviews refund requests. |

Also place **Terms of Use**, **Privacy Policy**, and a **Manage Subscription** route somewhere readily accessible. Before purchase, clearly explain automatic renewal and how to cancel.

Prioritize the price hierarchy, trial disclosure, and existing-subscriber access before shipping. The refund-link placement is a usability improvement; being three screens deep alone doesn’t establish an App Store violation.