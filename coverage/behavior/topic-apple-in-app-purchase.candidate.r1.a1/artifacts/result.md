# Premium recipe purchase flow review

Decision: revise before implementation. The iOS brief establishes five defects at specification level. Rankings below reflect expected harm, not measured frequency. This is a framework-agnostic contract; no Apple SDK is assumed.

## Ranked verified findings

| Rank | Evidence in interface.md | Effect and decision | Guidance |
| --- | --- | --- | --- |
| 1 — Critical | “Dismissing the paywall removes saved free recipes.” | Exiting a sales task destroys unrelated saved work. Remove all recipe mutation from purchase dismissal. Every exit returns to the prior recipe/context with saved free recipes intact. Do not add a discard confirmation to justify this deletion. | [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices): protect created content across button and gesture exits. Preserving existing free recipes outright is the product correction. |
| 2 — Critical | Locked recipe button “looks like a one-time purchase yet starts an annual subscription.” | The apparent transaction differs from its recurring consequence. Label entry “View Premium Subscription”; it opens offer details without committing a purchase. Use an explicitly annual subscription action only after disclosure. | [Buttons — Content and Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Content), [Writing — Best practices](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices), [In-App Purchase — Auto-renewable subscriptions](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Auto-renewable-subscriptions). Exact current label/style is unavailable. |
| 3 — High | Paywall says “Free Trial” but omits renewal price and period. | People cannot assess the paid commitment. Show trial duration, full localized annual billing total, annual period, automatic renewal, included content, and subsequent price before the purchase action. Do not substitute a monthly equivalent for the annual total. | [In-App Purchase — Making signup effortless](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Making-signup-effortless). |
| 4 — High | “Restore purchases is absent.” | Returning purchasers lack a recovery path. Add Restore Purchases and an existing-customer sign-in route where account-linked purchases are supported; recognize existing entitlement before offering repurchase. | [In-App Purchase — Making signup effortless](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Making-signup-effortless). Absence of this control does not prove the entitlement backend is broken. |
| 5 — High | “Signup has no Terms or Privacy links.” | Subscription signup lacks access to its governing terms and privacy explanation. Add separately labeled, working Terms of Use and Privacy Policy links at subscription signup, preserving entered state when returning. | [In-App Purchase — Making signup effortless](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Making-signup-effortless). [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices) supports clear data-use communication; links alone do not establish compliant data handling. |

## Corrected behavior and decisions

The product is digital recipe access with an annual subscription. Model the intended trial-to-automatic-renewal offer as auto-renewing; verify the actual configured product before release. Price, trial duration, eligibility, precise included recipes, legal destinations, and supported account methods are unknown. Never invent them in production copy. Keep useful free access and saved recipes available after declining.

Offer content, in reading order:

1. “Premium Recipes — Annual Subscription” and an accurate summary of included content.
2. For confirmed trial eligibility: “{trial duration} free, then {localized full annual price} per year. Automatically renews annually unless canceled.” For confirmed ineligibility: “{localized full annual price} per year. Automatically renews annually unless canceled.”
3. Primary action: “Start Free Trial” only for the confirmed eligible offer; otherwise “Subscribe Annually.” Keep the annual total and transition explanation adjacent and prominent. Loading or unknown eligibility must not promise a trial.
4. Restore Purchases; supported existing-customer sign-in; Terms of Use; Privacy Policy; an obvious Close action.

Do not enable purchase while required offer details are missing. Show “Subscription details unavailable. Try again.” with Retry and Close. Do not imitate or modify the payment provider's system confirmation. Provide subscription summary and an easily reached Manage Subscription route in account/settings; cancellation remains easy to identify. These management and failure-state additions are proposed completeness decisions, not further observed defects. See [In-App Purchase — Best practices](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Best-practices) and [Managing subscriptions](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Helping-people-manage-their-subscriptions).

Control inspection map: locked-recipe entry, trial/subscribe action, proposed Restore/Retry/Close/sign-in actions, and legal links use the Buttons action contract. Entry opens details; subscribe requests confirmation; Restore recovers entitlement without creating a purchase; Close abandons the offer; legal links open their named destination. Subscribe is the single prominent offer action. Secondary actions remain discoverable. On delayed purchase/restore, show activity in the activating button and prevent duplicate requests; custom controls need press feedback. Specify iOS selectable regions of at least 44 × 44 pt with separation. Current geometry, emphasis, names, focus, and feedback are unknown, so none are verified violations. [Buttons — Best practices, Style, iOS](https://developer.apple.com/design/human-interface-guidelines/buttons).

Account creation and authentication fields are unspecified. Inspect whether an account is essential, defer it when possible, and verify an account-deletion route if creation is supported. Do not infer missing deletion, forced signup, or unsupported authentication from this brief. Deletion must not falsely promise subscription cancellation. [Managing accounts — Best practices and Deleting accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts).

No presentation geometry is specified: this contract does not mandate a sheet or invent current modal blocking. Preserve the prior destination and apply the same exit policy to every dismissal mechanism actually supported.

## Framework-agnostic state contract

```text
Persistent: savedRecipeIDs, entitlement
Transient: offerState, originRecipeID, returnContext, operationID
Invariant: purchase-flow handlers never delete or replace savedRecipeIDs

openPremium(recipe, context):
  retain origin and return context
  resolve existing entitlement first
  if active: open recipe; do not advertise repurchase
  else: load validated offer and eligibility -> offerReady or offerUnavailable

subscribe (only offerReady, no operation in flight):
  freeze displayed product/offer identity
  request provider confirmation for that same product/offer -> purchasing
  canceled: return to offerReady; no access or saved-data mutation
  pending: explain pending approval; do not unlock or invite duplicate purchase
  failed: keep offer/context; explain failure and permit a deliberate retry
  verified success: reconcile entitlement; unlock recipe promptly -> recipe
  verification unresolved: show pending verification and recovery; do not claim success

restore:
  reconcile existing purchases -> restoring
  active entitlement: unlock and return to origin recipe
  none: explain “No purchases found”; offer supported sign-in/help; no auto-purchase
  failure: explain inability to restore; offer retry/help; retain free data

dismiss (Close, supported gesture/escape/navigation exit):
  close offer; restore returnContext; preserve all savedRecipeIDs
  dismissal does not cancel an already confirmed transaction or erase its result

late purchase/restore result:
  reconcile entitlement independently of whether offer is visible
  update access without reopening obsolete offer or deleting free data

legalLink:
  open actual destination; returning retains offer and signup state
```

Duplicate-operation prevention and late-result handling are engineering decisions supporting predictable outcomes, not claimed HIG API requirements. Entitlement changes affect premium access only; subscription expiration must not remove saved free recipes.

## Worked before/after

Illustrative fixture only: a 7-day eligible trial followed by $39.99 USD annually; these are not supplied commercial terms.

**Before:** A person has saved free recipes A and B. They activate a locked recipe control that implies a one-time purchase, encounter “Free Trial” without renewal information, and dismiss. A and B disappear. There is no Restore Purchases or Terms/Privacy path.

**After:** The same person activates “View Premium Subscription.” The offer says “Premium Recipes — Annual Subscription,” accurately describes its content, and shows “7 days free, then $39.99 per year. Automatically renews annually unless canceled.” “Start Free Trial” requests the matching provider confirmation. Restore Purchases, legal links, and Close are available. Closing returns to the same recipe/context with A and B still saved and no purchase initiated. On reopening and confirming, access unlocks only after verified entitlement; cancellation leaves A and B and the prior access unchanged. A returning entitled purchaser reaches the recipe through entitlement resolution/restore rather than another subscription offer.

## Acceptance checks and evidence status

**Passed — document inspection:** Read interface.md; identified iOS and all five stated problems. Read installed root, selected families, topic procedures, then their supporting guides. The proposed contract explicitly covers each defect and contains no framework-specific API dependency. These are document checks only.

**Failed — supplied specification:** saved-data preservation on dismissal; truthful recurring-purchase presentation; complete trial billing disclosure; restore availability; Terms/Privacy availability. Each failure is grounded in the corresponding explicit statement above, not in execution.

**Not executed — implementation acceptance:**

- Seed free saves A/B; open and close via every supported exit, reopen, relaunch, and check A/B and original navigation context remain intact. Repeat after failed, pending, canceled, restored, expired, and late-completing transactions.
- Test eligible, ineligible, and unknown trial states with localized offer fixtures. Confirm full annual total/period, trial duration, subsequent price, auto-renewal, and included service precede commitment; missing/stale details block purchase until refreshed. Confirm provider product and displayed offer match.
- Test successful purchase, provider cancellation, failure, pending approval, verification delay, repeated activation, and dismissal during an in-flight operation. Only verified entitlement grants access; retries do not create duplicate app requests.
- Test restore with active access, no purchases, failure, and supported account-linked customers. Active subscribers bypass repurchase; restoring never buys a new subscription.
- Open Terms and Privacy from signup and return without lost state. Verify real destinations and policy content. Confirm Manage Subscription reaches the supported management/cancellation flow.
- Once implemented, measure iOS hit regions and separation; inspect labels, roles, enabled states and custom press feedback. Exercise large/localized text, focus restoration, accessible names, reading order, and supported assistive technology on an appropriate runtime. No such results are claimed here.
- If account creation ships, verify useful guest access where accounts are nonessential, actual authentication capabilities, account deletion, and separate billing-management guidance.

## Evidence limits and source trail

Only the supplied one-paragraph interface.md and installed local instructions/guides informed this audit. “Verified” means explicitly stated in that brief. No screenshot, code, interactive prototype, transaction configuration, prices, trial metadata, policy content, or backend was supplied. Exact visual appearance, persistence mechanism, account necessity, accessibility, refund/help behavior, Family Sharing eligibility, and commercial/API availability remain unknown. No device, SDK, GUI, accessibility, purchase sandbox, build, or runtime test was executed. This is design guidance, not a legal or App Store compliance certification.

Installed package root: `.agents/skills/apple-hig/`. Explicitly read `SKILL.md`, followed each selected family under `subskills/`, then its `.topics/<topic>/SKILL.md`, then its `references/<topic>.md`:

| Family | Topic procedures and supporting guides read |
| --- | --- |
| apple-hig-technologies | apple-hig-apple-in-app-purchase → apple-in-app-purchase.md |
| apple-hig-patterns | apple-hig-managing-accounts → managing-accounts.md; apple-hig-modality → modality.md |
| apple-hig-menus-and-actions | apple-hig-buttons → buttons.md |
| apple-hig-foundations | apple-hig-privacy → privacy.md; apple-hig-writing → writing.md |

The installed guides identify a 2026-10-25 snapshot and are derived application guidance, not SDK references. Official links above are attribution copied from those local guides; they were not browsed or independently verified. No platform feasibility decision or new system integration is claimed.
