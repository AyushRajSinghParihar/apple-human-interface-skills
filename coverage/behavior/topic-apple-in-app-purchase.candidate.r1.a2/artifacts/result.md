# Premium recipe purchase flow review

Decision: revise the flow before implementation. Target: iOS; framework-agnostic contract. The five findings below are verified against the explicit statements in `interface.md`, not reproduced in a running app. Priority reflects this review's judgment of user harm, not an Apple severity classification.

## Ranked findings and decisions

| Rank | Evidence in supplied brief | Effect | Corrected behavior and guidance |
| --- | --- | --- | --- |
| 1 — Critical | Dismissing the paywall removes saved free recipes. | An ordinary exit destroys existing user work and penalizes declining a purchase. | Every paywall exit preserves saved recipes and returns to the originating context. Remove deletion from dismissal entirely; a discard confirmation is not a suitable repair for unrelated saved data. HIG protects created content across button and gesture exits: [Modality, Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices). |
| 2 — High | The locked recipe button looks like a one-time purchase yet starts an annual subscription. | People cannot predict the recurring financial consequence. Exact label and appearance were not supplied. | Recipe entry becomes **View Premium Plans**, opening offer details without starting a transaction. Identify the annual subscription before the separate purchase action; use **Subscribe Annually** for a paid offer or **Start Free Trial** only for a verified eligible trial with adjacent full terms. [Buttons, Content](https://developer.apple.com/design/human-interface-guidelines/buttons#Content), [Writing, Best practices](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices), and [subscription signup](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Making-signup-effortless). |
| 3 — High | Paywall says “Free Trial” but omits renewal price and period. | The offer conceals the trial-to-recurring-charge commitment. | Before activation, show subscription name, included content, trial duration, complete localized annual billing total, annual period, and automatic renewal after the trial. Lead with the full annual total rather than a monthly equivalent. Do not invent a price, duration, or eligibility. [Making signup effortless](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Making-signup-effortless). |
| 4 — High | Restore purchases is absent. | Existing purchasers lack the stated recovery route and may attempt to buy again. | Expose **Restore Purchases** on the paywall and in purchase settings. Check existing access before offering a new subscription; offer sign-in for supported account-linked purchases. Report restored access, no eligible purchase found, or a recoverable error distinctly. Absence of the control does not prove backend restoration is impossible. [Auto-renewable subscriptions and signup](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Auto-renewable-subscriptions). |
| 5 — High | Signup has no Terms or Privacy links. | People cannot inspect those documents at commitment. | Include clearly labeled **Terms of Use** and **Privacy Policy** links in subscription signup and the offer view; opening and returning preserves context. Verify real destinations and accurate content before release. The specific link requirement comes from [purchase signup](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Making-signup-effortless); [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices) additionally supports clear collection/use and minimization. Missing links alone do not prove undisclosed collection or unlawful processing. |

## Corrected interaction contract

Premium recipes are digital content. Preserve the supplied annual subscription model and treat it as auto-renewing for this specification; confirm the actual product configuration before implementation. Use the In-App Purchase experience model, not a physical-commerce Apple Pay checkout. No SDK or API is prescribed.

All supplied controls remain in scope: locked recipe entry → Buttons and In-App Purchase; “Free Trial” purchase action → Buttons and In-App Purchase; paywall dismissal → Buttons and Modality; signup → Managing accounts, Privacy, and In-App Purchase. Restore and document links are proposed additions. No signup fields or presentation geometry were supplied, so no text-field defect or sheet-specific defect is asserted. Paywall modality is unknown; apply the same exit/data contract whether it blocks its parent or uses ordinary navigation.

| Surface/action | Contract |
| --- | --- |
| Locked recipe: View Premium Plans | Normal navigation action; opens details for the annual plan, preserving recipe identity, scroll position, and saved data. Does not purchase. Existing entitled people open the recipe instead. |
| Offer primary action | One prominent purchase action matching the actual eligible offer. It invokes the unmodified system purchase confirmation through an implementation adapter. No entitlement from a tap alone. |
| Close | Visible, secondary, nondestructive exit to origin. All supported gesture/navigation exits use the same policy. Closing an offer does not cancel an existing subscription. |
| Restore Purchases | Secondary recovery action, never a new sale. Show progress and a meaningful result; no automatic repurchase when nothing is found. |
| Terms of Use / Privacy Policy | Open the named real document, then return to the same signup/offer state without purchase or data loss. |
| Signup | Explain actual account needs and request only essential initial data. Allow useful unregistered access when accounts are not essential; necessity is unknown here. Deletion support is an inspection question, not a verified missing feature. [Managing accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Best-practices). |

Prefer platform controls where available. Otherwise preserve meaningful labels, enabled/pending states, and press feedback. For iOS, specify at least 44 × 44 pt selectable regions with separation; the supplied brief provides no measurements. For delayed purchase/restore initiation, show activity within the initiating button and guard duplicate activation. These are implementation acceptance requirements, not observed defects. [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices) and [iOS behavior](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS).

```text
persistent savedFreeRecipes is independent of purchaseUI and entitlement

openLockedRecipe(recipe, origin):
  if verifiedCurrentAccess(recipe): open(recipe)
  else:
    remember(origin, recipe)
    load product terms and trial eligibility
    show offer; if unavailable, show retry + Close; disable purchase

renderOffer(product, eligibility):
  show name, included content, localized full annual total, annual period
  if eligibility confirms trial:
    show trial length + subsequent total/period + automatic billing
    primary = "Start Free Trial"
  else:
    show annual total/period + automatic renewal
    primary = "Subscribe Annually"
  show Restore Purchases, Terms of Use, Privacy Policy, Close

purchase():
  require complete current terms and explicit activation
  guard against duplicate requests; show pending state
  request system confirmation through purchase adapter
  canceled -> return to offer, no entitlement or saved-data change
  failed -> offer retry/help, preserve context and saved data
  awaitingApproval -> explain pending, do not unlock or start another request
  verifiedSuccess -> apply access; open originating recipe

restore():
  guard duplicate requests; show progress
  verifiedAccess -> apply access; open originating recipe
  noPurchase -> explain no eligible purchase found; offer supported sign-in/help
  error -> explain recovery and offer retry

exitOffer(any supported exit):
  close purchase UI; return to remembered origin
  never mutate savedFreeRecipes or revoke existing access

verifiedTransactionArrivesAfterExit():
  update entitlement independently of offer visibility
  retain current navigation; make purchased access available without rebuying
```

The separation of persistent saved data, transaction processing, and offer visibility is a proposed engineering decision. It prevents dismissal from becoming a destructive operation. Pending work must reconcile after interruption rather than treating a closed view as a failed transaction.

Provide a discoverable **Manage Subscription** route in settings/account with renewal summary and cancellation access; prefer system management UI when available. This is a source-backed completion recommendation, not a verified missing feature. [Helping people manage subscriptions](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Helping-people-manage-their-subscriptions).

## Worked before/after

Before, per the brief: a person with saved free recipes selects a locked recipe through an entry that implies one-time purchase. They see “Free Trial” without renewal price or period; the purchase action starts an annual subscription. There is no restore control or Terms/Privacy link at signup. Dismissing deletes saved free recipes. These statements do not establish whether a system confirmation is present or absent.

After, proposed trace: with saved set `{A, B}`, selecting locked recipe C opens **Premium Recipes — Annual** via **View Premium Plans**. The offer reads:

> Includes: {verified premium content description}. {localized full annual price} per year. {trial duration} free, then {localized full annual price} per year. Automatically renews annually until canceled.

The braces are required product data, not shippable copy. Trial wording appears only when eligibility is confirmed; otherwise show paid annual terms and **Subscribe Annually**. Place **Restore Purchases**, **Terms of Use**, **Privacy Policy**, and **Close** visibly in the flow. Full annual price takes precedence over any equivalent monthly figure.

Trace 1: Close → return to C's origin; saved set remains `{A, B}`. Reopen and cancel system confirmation → offer remains available; saved set remains `{A, B}`, no new access granted. Trace 2: explicit confirmation and verified success → C opens with premium access; `{A, B}` remains saved. Trace 3: an existing purchaser restores → verified access opens C without creating another subscription. These are specification walkthroughs, not executed transactions.

## Acceptance checks and current results

**Passed — local review only:** read `interface.md`; explicitly read the installed root skill; searched the topic index; read the Technologies, Patterns, Menus and actions, and Foundations families, then selected topic procedures before their supporting source guides. The proposed contract separates offer entry from purchase and defines successful, canceled, failed, pending, restore, and dismissal outcomes. No runtime pass is implied.

**Failed — supplied design evidence:** all five ranked checks fail in the brief: preservation of saved free recipes on dismissal; truthful annual-subscription entry; complete trial renewal terms; visible restore route; Terms/Privacy links at signup.

**Not executed — implementation acceptance:**

1. Seed saved recipes `{A, B}`. Enter the offer from C, exit with Close and every supported gesture/navigation route, reopen, interrupt and relaunch. Assert `{A, B}` and originating context are retained; existing access is never revoked by dismissal.
2. For trial-eligible, ineligible, unknown-eligibility, and unavailable-product states, verify the matching label and complete localized terms before purchase. Annual totals remain primary; unknown data never becomes invented trial copy. Confirm price/period match the actual product and system confirmation.
3. Enter through the locked recipe button. Assert no transaction request until the separate correctly labeled purchase action is activated. Repeated activation issues at most one request. Exercise success, cancellation, failure, pending approval, delayed verification, and completion after exit; only verified access unlocks premium content.
4. Restore an eligible prior purchase, try a no-purchase account, and simulate failure. Assert distinct results and retry/help; no new sale. Existing entitled people bypass subscription advertising. Test account-linked sign-in only if supported.
5. Open both policy links from signup and the offer; verify real documents, usable return navigation, retained state, and accurate product/data descriptions. No placeholder links ship.
6. Verify management/cancellation is easy to reach. Inspect account necessity and, if creation exists, deletion support; neither is established by this brief. Do not imply account deletion cancels recurring billing.
7. Measure iOS hit regions and separation. Exercise pending feedback, enlarged/localized labels, accessible names, reading/focus order, focus restoration, and supported input paths in a suitable runtime. Native rendering and assistive-technology results remain unknown.

## Evidence limits and source record

Only the five-sentence `interface.md` supplies interface evidence. There are no supplied screenshots, source implementation, transaction logs, product catalog, actual price/trial duration, account schema, or device results. “Verified” means explicitly reported by that local brief. No SDK compilation, payment sandbox, GUI, iOS-device, VoiceOver, accessibility, network, or security/legal test was performed. The recommendations are a review specification, not implemented fixes or commercial-policy certification.

Guidance was consumed from `/tmp/hig-eval-oh5tdkia/.agents/skills/apple-hig/`: root `SKILL.md`; `references/topic-index.md`; the four named family `SKILL.md` files; topic procedures for Apple In-App Purchase, Managing accounts, Modality, Privacy, Buttons, and Writing; and each corresponding family reference article. Each file read used its own command. The installed articles identify a 2026-10-25 snapshot and are independent application guidance derived from HIG. Official links above identify the material sections; no website was accessed or current SDK/policy availability independently verified. No screenshot-specific media route was needed.
