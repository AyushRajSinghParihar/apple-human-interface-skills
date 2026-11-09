All six points need changes under Apple’s [In-App Purchase guidance](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase).

| Issue | What to change |
|---|---|
| **Annual price hierarchy is reversed.** The monthly equivalent obscures the actual charge. | Lead with **“$59.88/year.”** Put “Equivalent to $4.99/month” below it with less emphasis. Keep the full billed amount clearly readable and localize prices. |
| **“Start free” leaves the commitment unclear.** | Use **“Start [duration] Free Trial.”** Immediately beside it, state: “[Duration] free, then $59.88/year. Automatically renews until canceled.” Use the actual configured trial length and show this offer only to eligible people. Apple requires clear trial terms; this button wording is a suggested implementation. |
| **Existing customers cannot recover access.** | Add visible **Restore Purchases** and, if you support app accounts, **Sign In** actions on the paywall. Successful recovery should open subscribed content. |
| **Subscribers repeatedly receive a sales prompt.** | Check current entitlements before presenting the paywall after an update. Route active subscribers directly to their content, with subscription management available in settings. Don’t ask them to purchase access they already have. |
| **The custom code and redemption instructions are invalid.** | Custom codes use **ASCII letters and numbers only**: change `SUMMER-25!` to something like `SUMMER25`. Custom codes redeem through a **redemption URL or supported in-app system flow**, not App Store account settings. Add **Redeem Code**, explain the offer’s actual terms, and apply access promptly—including redemption before first launch. |
| **Refund help is buried.** | Put a clearly labeled **Request a Refund** action directly on the purchase-help screen, visible without additional screens or scrolling. Open the system refund flow and show relevant purchase context. Don’t promise approval. |

Also verify that the paywall names the subscription, explains included benefits, and provides **Terms of Use** and **Privacy Policy** links. Keep **Manage Subscription** and cancellation easy to reach from account/settings.

These are findings from your description; no runtime checks were performed. Before release, test trial eligibility, restore/sign-in, subscriber access after updates, both custom-code redemption routes, redemption before installation, and the refund handoff on an iPhone.