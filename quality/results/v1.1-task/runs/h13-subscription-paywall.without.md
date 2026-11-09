Change all six items. The pricing, trial disclosure, and subscriber access issues should block release.

| Issue | What to change |
|---|---|
| **Annual price hierarchy** | Make **“$59.88/year”** the most prominent price. Put “Equivalent to $4.99/month, billed annually” underneath in readable, accessible text. Apple’s guidance puts the actual billed amount ahead of a monthly equivalent. |
| **“Start free” button** | Use **“Start [actual duration] free trial.”** Immediately beside it, disclose: “Then $59.88/year. Automatically renews unless canceled.” Clearly explain how to cancel. Show trial messaging only to eligible customers; others should see their actual purchase terms. |
| **No restore or sign-in** | Add a visible **Restore Purchases** action to the paywall. If subscriptions are associated with your own accounts, also add **“Already subscribed? Sign in.”** Signing in should recover the relevant entitlement; it doesn’t replace restoring App Store purchases. |
| **Subscribers see the paywall after updates** | Check verified subscription entitlements before presenting it, and send active subscribers directly into the app. Refresh entitlement state across launches, updates, purchases, and restores. Don’t treat an update—or a temporary verification failure—as proof that someone has no subscription. |
| **`SUMMER-25!` offer code** | Change it to an alphanumeric code such as **`SUMMER25`**; custom codes don’t support the hyphen or exclamation mark. Custom offer codes **cannot be redeemed by typing them into App Store account settings**. Distribute Apple’s redemption URL or provide Apple’s in-app redemption sheet. Explain eligibility, offer duration, discounted price, and subsequent renewal terms. |
| **Buried refund link** | Move **Request a Refund** into an easily found subscription-management or support screen. Use Apple’s in-app refund request flow or link to [reportaproblem.apple.com](https://reportaproblem.apple.com/). Keep refund requests and subscription cancellation as distinct actions; Apple determines refund eligibility. Three screens deep is a usability problem, rather than a specific universal depth-rule violation. |

A suggested paywall, using your actual trial duration:

> **Annual subscription — $59.88/year**  
> Equivalent to $4.99/month, billed annually  
>  
> **Start [duration] free trial**  
> Free for [duration], then $59.88/year. Automatically renews unless canceled.  
>  
> Restore Purchases · Sign In  
> Terms of Use · Privacy Policy

Also state what the subscription unlocks and make cancellation instructions easy to find.

Apple references: [Subscription design guidance](https://developer.apple.com/design/human-interface-guidelines/subscriptions), [App Review Guidelines §3.1.2](https://developer.apple.com/app-store/review/guidelines/#subscriptions), and [Offer codes](https://developer.apple.com/help/app-store-connect/manage-subscriptions/set-up-offer-codes/). I couldn’t retrieve the live documentation in this session, so these are reference links rather than a live policy verification.