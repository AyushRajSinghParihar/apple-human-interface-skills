Change all six items before release. Based on your description, the paywall obscures billing terms and fails existing subscribers.

| Issue | What to change |
|---|---|
| **Annual price hierarchy** | Make **“$59.88/year, billed annually”** the dominant price. Put “Equivalent to $4.99/month” below it with less emphasis. Apple says the total billed amount should be most prominent. |
| **Ambiguous trial** | Use **“Start [actual duration] Free Trial.”** Beside the button, clearly state: “Free for [duration], then $59.88/year. Automatically renews unless canceled.” Show trial wording only to eligible people. |
| **No purchase recovery** | Add a visible **Restore Purchases** action on the paywall. Include **Sign In** if an existing app account can recover subscription access. |
| **Subscribers see the paywall after updates** | Check existing entitlements before presenting a purchase offer. Route active subscribers directly to their content, with subscription management available in settings. An update should not trigger another subscription pitch. |

These corrections follow Apple’s [subscription signup guidance](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Making-signup-effortless).

Your **offer-code plan has two separate problems**:

- Change `SUMMER-25!` to an ASCII alphanumeric code such as **`SUMMER25`**; the punctuation is invalid.
- Custom subscription codes redeem through a **redemption URL or supported in-app StoreKit flow**. App Store account-settings entry is for **one-time-use codes**. Add a **Redeem Code** action that opens Apple’s redemption flow, explain the offer’s duration and subsequent price, and apply access promptly after redemption. See Apple’s [offer-code setup guidance](https://developer.apple.com/help/app-store-connect/manage-subscriptions/set-up-subscription-offer-codes/).

Move **Request a Refund** to a clearly visible purchase-help or subscription-details screen, without additional navigation or scrolling to discover it. Open Apple’s system refund flow and avoid promising approval. This follows Apple’s [purchase-help guidance](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Providing-help).

Also verify that signup includes the subscription name, included benefits, duration, localized billing amount, and Terms and Privacy links; your description doesn’t establish whether these are present.

**Review result:** all six described items need changes. Runtime checks remain unexecuted: restoration, entitlement persistence across updates, trial eligibility, redemption before first launch, and the refund handoff.