# Premium recipe purchase flow — preimplementation audit

## Decision and scope

Do not implement the described flow unchanged. Resolve the five findings below before release. Target: iOS; task: opening a locked recipe and deciding whether to purchase an annual premium subscription. This is a review of the supplied textual interface specification, not an executed application.

“Verified” below means explicitly stated in [interface.md](interface.md). Severity and implementation decisions are this audit’s judgments. P0 means potential loss of existing user data; P1 means material purchase-consent, disclosure, or recovery failure. Within P1, rank reflects proximity to an unintended charge.

## Ranked findings and decisions

| Rank | Verified evidence | Effect and source-backed guidance | Corrected behavior / decision |
| --- | --- | --- | --- |
| 1 · P0 | “Dismissing the paywall removes saved free recipes.” | Leaving a purchase decision destroys unrelated saved work. HIG Modality calls for a familiar exit and explanation/save-discard choices before losing created content. | Dismissal must preserve all saved recipes and return to the prior context. Remove any deletion or save-list mutation from purchase navigation. A destructive confirmation is not an appropriate fix for this unrelated side effect. This preservation invariant is a product decision applying the guidance. |
| 2 · P1 | “The locked recipe button looks like a one-time purchase yet starts an annual subscription.” | The action misrepresents the commitment. HIG calls for clear subscription actions, benefits, terms, price, and duration. | Recipe action: **View Premium subscription**. It opens plan details; it does not start a transaction. The final action explicitly identifies the annual subscription or eligible trial. Use the genuine system purchase confirmation, without imitation or modification. |
| 3 · P1 | “Paywall says Free Trial but omits renewal price and period.” | People cannot assess the recurring cost. HIG says to always show the complete billed price and disclose introductory period, subsequent standard price, trial length, and automatic billing. | Show subscription name, included content, annual billing period, full localized annual amount, trial duration when eligible, and automatic billing after the trial. Full annual total takes visual priority over any optional monthly equivalent. Do not advertise a trial whose eligibility is unknown. |
| 4 · P1 | “Restore purchases is absent.” | Existing purchasers lack an explicit recovery route and may think they must buy again. HIG subscription signup includes sign-in/restore for existing purchasers and advises against advertising a new subscription to existing subscribers. | Add visible **Restore Purchases** on the paywall, plus **Sign In** where a supported account entitlement route exists. Resolve known entitlements before presenting a new-purchase action. Restore must never initiate a new purchase. |
| 5 · P1 | “Signup has no Terms or Privacy links.” | People cannot inspect the subscription’s terms and privacy information at commitment. HIG explicitly includes Terms/Privacy links in subscription signup. | Put independently operable **Terms of Use** and **Privacy Policy** links in subscription signup before commitment. If account signup is a separate screen, include the relevant links there too; this second placement is a product decision. Preserve entered state and purchase context when returning from a link. |

Source sections: [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices) supports finding 1; [Apple In-App Purchase — Best practices](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Best-practices) and [Making signup effortless](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Making-signup-effortless) support findings 2–5. [Auto-renewable subscriptions](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Auto-renewable-subscriptions) supports avoiding repeat purchase prompts for subscribers. These are official source links recorded in the local package; no linked page was fetched.

## Worked before / after

Scenario: a person has three saved free recipes and opens a fourth, locked recipe.

**Before, as supplied:** The recipe control resembles a one-time purchase, but starts an annual subscription. The paywall says “Free Trial” without renewal amount or period. It offers no restore route; signup lacks Terms/Privacy links. Dismissal removes saved free recipes. Exact original button text, layout, trial length, and price were not supplied.

**After, proposed:** The locked recipe shows **View Premium subscription**. Selecting it presents:

```text
Close
Premium Recipes
[Accurate description of included premium content]
Annual subscription
[Localized full annual billing amount] per year

If verified eligible:
  [Trial duration] free, then [full annual amount] per year.
  Automatically renews annually until canceled.
  Primary: Start [trial duration] free trial
Otherwise:
  Automatically renews annually until canceled.
  Primary: Subscribe for [full annual amount] per year

Restore Purchases    [Sign In, if supported]
Terms of Use        Privacy Policy
```

Bracketed values are required product data, not literal shipping copy or invented commercial terms. Specify actual trial duration, price/currency, included content, and functioning policy destinations before implementation approval. If accurate product terms cannot load, show an explanation and Retry/Close; keep purchase unavailable. Never substitute a guessed price or trial promise.

The primary action requests system purchase confirmation. Cancellation returns to the paywall without changing saved content; Close returns to the prior recipe and navigation position. All three saved free recipes remain saved and available. A confirmed entitlement unlocks the intended recipe and returns the person to it. An existing subscriber instead sees **Open Recipe** once their entitlement is resolved.

## Framework-agnostic behavior specification

The following state and recovery details are proposed implementation requirements, not additional observed defects. A platform adapter supplies product terms, eligibility, purchase confirmation, verified entitlements, and restoration; no SDK or API names are assumed.

```text
Persistent state:
  savedRecipes                      // independent of purchase UI state
  verifiedEntitlements
Transient purchase states:
  loading, offer, purchasing, pending, restoring, entitled, error

onLockedRecipe(recipe):
  remember origin and recipe
  resolve entitlement and authoritative product/eligibility data
  if entitled: open recipe
  else if complete terms available: show offer
  else: show error with Retry and Close; disable purchase

onPurchase:
  require complete displayed terms for selected annual product
  require no purchase/restore operation already active
  request genuine system confirmation through platform adapter
  canceled -> offer, no entitlement or saved-content mutation
  pending -> explain awaiting approval; do not unlock or resubmit
  failed -> show understandable error and retry route
  verified success -> update entitlement; open intended recipe
  unverified result -> keep locked; explain verification/retry route

onRestore:
  query existing purchases through adapter; do not create purchase
  verified active entitlement -> unlock and open intended recipe
  none found -> explain no active purchase found; offer supported sign-in/help
  failed -> explain failure; allow retry and dismissal

onCloseOrDismiss:
  return to origin with navigation and savedRecipes preserved
  do not treat closing as transaction cancellation
  reconcile any later transaction result independently of paywall visibility

Invariant:
  no purchase, restore, dismissal, failure, or entitlement-expiry handler
  deletes saved free recipes
```

For successful restoration or purchase, confirm the outcome accessibly and avoid duplicate submissions while an operation is active. Keep an exit available where the app controls presentation. System confirmation owns its own controls. These are proposed recovery and accessibility checks; the supplied description does not establish their current implementation.

## Acceptance checks

These are checks to execute against the eventual implementation, not test results.

1. Seed three saved free recipes. Open and dismiss the paywall through every supported exit. Confirm identical saved IDs/content and restored navigation context. Repeat after purchase cancellation, failure, pending status, restore failure, and relaunch.
2. Inspect the locked-recipe action and final purchase action: both communicate a subscription; only the final action requests system confirmation for the displayed annual product.
3. For trial-eligible, ineligible, and unknown eligibility states, verify correct copy and action. Eligible copy includes actual trial duration, subsequent full localized annual amount, annual period, and automatic renewal. Unknown terms cannot trigger purchase. Any equivalent monthly price is subordinate to the full annual bill.
4. Restore is discoverable without beginning a purchase. Active, absent, and failed restoration produce distinct outcomes. Known active subscribers can open premium recipes without being sold the same subscription again. Any offered sign-in route works.
5. Both policy links open the intended documents before commitment, and returning preserves signup/purchase state. Verify actual destinations; placeholders fail acceptance.
6. Exercise confirmed, canceled, failed, pending, and unverified purchase results, repeated taps, and a result arriving after dismissal. Unlock only on verified entitlement; preserve saved recipes in every branch.
7. On actual iOS hardware or an appropriate test environment, verify readable disclosures at supported text sizes, operable controls and links, logical focus/reading order, labeled dismissal, and accessible purchase/restore status. These are proposed validation targets, not verified accessibility findings.

## Evidence and limits

Read the installed root `apple-hig/SKILL.md` first. Routed to Technologies for digital subscriptions and Patterns for dismissal/account behavior, reading both family `SKILL.md` files before their articles. Also searched the installed topic index. The families route directly to article references; no additional topic procedure was specified along these routes.

Local articles read: `subskills/apple-hig-technologies/references/apple-in-app-purchase.md`; `subskills/apple-hig-patterns/references/managing-accounts.md`, `modality.md`, and `undo-and-redo.md`, all relative to `.agents/skills/apple-hig/`. Managing accounts and Undo and redo were contextual checks; neither establishes another verified defect. Each file was consumed with a separate single-file shell command. Source snapshots identify 2026-10-25 and are package-derived guidance, not independently verified current Apple policy or SDK documentation.

Only `interface.md` supplies interface evidence. No screenshot, code, product catalog, subscription configuration, account architecture, live policy documents, or runtime was supplied or inspected. The description does not prove whether recipe removal is permanent deletion or a display/filter bug; either way, the specified disappearance fails the preservation decision. There is no evidence that trial length is absent, only that renewal price and period are absent; trial duration is included as a required future check rather than an invented finding.

No browser, GUI, device, SDK, purchase sandbox, accessibility tool, or implementation test was run. No claim is made about App Store approval, legal compliance, exact visual hierarchy, contrast, touch target sizes, or screen-reader behavior. Official links are citations from local guidance only. Current commercial terms, platform API availability, and implementation behavior remain to be verified during implementation.
