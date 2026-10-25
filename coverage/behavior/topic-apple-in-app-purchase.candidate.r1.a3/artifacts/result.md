# Premium recipe purchase flow review

Decision: revise before implementation. Target: iOS; specification is framework agnostic. The sole interface evidence is the brief in `interface.md`. “Verified” below means explicitly stated in that brief, not reproduced in an application. Severity is this review’s product judgment.

## Ranked verified findings

| Rank | Evidence and consequence | Decision and source |
| --- | --- | --- |
| 1 — Critical | “Dismissing the paywall removes saved free recipes.” Declining a purchase destroys unrelated saved work. | Every exit preserves saved recipes, free access, and return context. Dismissal has no library mutation. Do not add a discard confirmation to legitimize this deletion. HIG protects created content across button and gesture exits; preserving it outright is the product correction. [Modality: Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices). |
| 2 — High | Locked recipe button looks like a one-time purchase but starts an annual subscription. The apparent transaction differs from its recurring consequence. Exact label and styling are unavailable. | Label entry “View Premium Plans”; activation opens terms and never starts a transaction. Label the commitment with the actual subscription/trial action and show the full annual total before it. [Buttons: Content and Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Content), [Writing: Best practices](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices). |
| 3 — High | “Free Trial” omits renewal price and period. People cannot assess future billing. | Present subscription name, included content, trial duration, localized full annual charge, annual period, and automatic billing after trial. Make the full billed total more prominent than any monthly equivalent. Show trial copy only for confirmed eligibility. [In-App Purchase: Making signup effortless](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Making-signup-effortless). |
| 4 — High | Restore purchases is absent. Existing purchasers lack this recovery route and may attempt to pay again. | Add discoverable “Restore Purchases” and existing-customer sign-in where applicable. Check existing access before offering purchase; route entitled people directly to content. Restore must not initiate a new purchase. [In-App Purchase: Auto-renewable subscriptions](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Auto-renewable-subscriptions). |
| 5 — High | Signup has no Terms or Privacy links. Subscription signup lacks access to material information. | Include distinct “Terms of Use” and “Privacy Policy” links before commitment; preserve the signup state on return. Destinations must contain the actual applicable documents. This is a subscription-signup HIG finding, not a legal compliance determination. [In-App Purchase: Making signup effortless](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Making-signup-effortless), [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy). |

## Corrected behavior and control contract

Keep the annual subscription model described by the brief; do not silently convert it into a one-time product. Confirm the catalog’s actual renewal model, price, trial, eligibility, included recipes, and policy URLs before finalizing copy. Missing values are release blockers, not permission to invent them.

| Control/surface | Candidate procedure | Proposed contract |
| --- | --- | --- |
| Locked recipe entry | Buttons | “View Premium Plans”, normal navigation action; opens offer details retaining recipe ID and library position. No charge. |
| Paywall purchase action | Buttons + Apple In-App Purchase | One prominent action: “Start Free Trial” only when eligible, otherwise “Subscribe Annually”. Adjacent complete terms identify the annual subscription. Activating requests the purchase provider’s unmodified confirmation; it does not itself prove success. |
| Paywall dismissal | Buttons + Modality | Visible “Close”, cancel semantics; every supported dismissal returns to prior context without deleting recipes or granting access. Existing presentation type and gesture support are unknown; no specific sheet implementation is assumed. |
| Restore Purchases (new) | Buttons + Apple In-App Purchase | Secondary action; shows in-button progress on iOS, prevents duplicate requests, then reports restored access, no purchases found, or a recoverable error. |
| Signup / existing-customer sign-in | Managing accounts | Keep signup task state. Provide applicable sign-in recovery without forcing an existing subscriber to buy again. Account necessity and authentication methods are not supplied. |
| Terms of Use / Privacy Policy (new) | Writing + Privacy + Apple In-App Purchase | Clearly named destinations; returning retains offer and signup state. No unsupported claim about consent or data handling. |

Use perceivable press feedback and distinct pending/enabled states. For iOS, specify selectable regions of at least 44 × 44 pt with adequate separation; no dimensions were supplied to audit. Prefer system control behavior where the eventual stack provides it; custom controls must retain equivalent action semantics. [Buttons: Best practices and iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices).

## Worked before/after

**Before, from the brief:** A person with saved free recipes activates a locked recipe control that appears to sell a single recipe. It starts an annual subscription flow headed “Free Trial”, without renewal price/period or Restore Purchases. Signup lacks policy links. Closing the paywall removes saved free recipes.

**After, proposed:** The same person activates “View Premium Plans”. The offer shows:

```text
Recipe Premium — Annual Subscription
Includes: {verified premium content description}
{trial duration} free, then {localized full annual price} per year.
Automatically renews annually until canceled.
[Start Free Trial]       // eligible only
[Restore Purchases]  [Sign In]  // sign-in when applicable
[Terms of Use]  [Privacy Policy]
[Close]
```

For an ineligible person, omit the trial claim, show “{localized full annual price} per year. Automatically renews annually until canceled.” and use “Subscribe Annually”. All braces are unresolved catalog values, not production strings. Provide easy-to-reach subscription management and cancellation from account/settings; this is a proposed completeness measure, not a verified missing feature. [In-App Purchase: Helping people manage their subscriptions](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Helping-people-manage-their-subscriptions).

Closing returns to the same recipe/list position with all saved free recipes intact. If the person instead confirms purchase, verified entitlement unlocks the selected recipe. Cancellation or failure keeps the library intact and returns to a usable offer/free experience.

## Framework-agnostic state specification

```text
persistent library is independent of transient offer and entitlement state

openPremium(recipe, origin):
    retain recipe and origin
    resolve existing entitlement
    if entitled: open recipe; return
    load authoritative offer and eligibility
    if unresolved: show retry + Close; no purchase action
    else: show complete terms + applicable purchase action + recovery links

closeOffer(anySupportedExit):
    return to retained origin
    never write library or change entitlement

purchase():
    require complete current offer and no operation in flight
    request provider confirmation using the displayed product
    while pending: prevent duplicate purchase; show pending status
    on verified entitlement: unlock recipe; return to retained task
    on canceled: leave library unchanged; return to offer/free experience
    on failed: leave library unchanged; explain retry or Close
    on deferred/unknown: show pending status; reconcile later; do not claim unlocked

restore():
    prevent duplicate restore; show progress
    reconcile purchases through purchase provider
    on verified entitlement: unlock access without another charge
    on no match: explain no purchases found; offer applicable sign-in/help
    on failed: show retry + Close; keep library and existing valid access intact

on interruption/relaunch or late provider result:
    reconcile entitlement independently of whether offer is visible
    never launch a second charge automatically or delete saved recipes
```

Trial eligibility, validation, reconciliation, and request deduplication are implementation contracts requiring a real purchase integration. Account creation is not proof of entitlement. Policy links do not by themselves establish consent, security, or compliant collection. The brief supplies no data categories, transfers, permissions, or retention details; those require a separate data-purpose inventory before implementation.

## Acceptance checks and present status

**Passed — static review only:** The brief establishes iOS and the five reported behaviors. The corrected specification names full billing disclosures, recovery controls, explicit exits, and a library-preservation invariant. Manual tracing of the proposed close/cancel/failure paths reveals no library write; this is a specification check only.

**Failed — supplied design contract:** Declining purchase preserves saved free recipes; entry accurately represents subscription intent; trial explains renewal price/period; restore is available; signup exposes Terms/Privacy. Each fails according to the explicit brief, not an executed test.

**Not executed — implementation acceptance:**

1. Seed multiple saved free recipes; exercise visible Close, every supported gesture/escape, purchase cancellation, provider failure, interruption, and relaunch. Assert IDs, saved state, free access, and return context are unchanged.
2. With eligible, ineligible, and unresolved trial states, assert displayed offer and confirmation refer to the same catalog product, currency, full annual total and period. No unresolved placeholder or false trial claim reaches production.
3. Restore with active, expired, absent, and other-account purchases; verify truthful outcomes, no new transaction, and no repurchase prompt for verified active access.
4. Complete, cancel, defer, interrupt, and repeat purchase requests. Assert verified access unlocks once, duplicate activation creates no duplicate request, and late success is reconciled after dismissal.
5. Open both policy links before commitment; verify correct documents and retained state on return. Verify subscription management/cancellation is reachable. Inspect account necessity and actual deletion support separately; absence is not established here. [Managing accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts).
6. Measure iOS hit regions/separation; check long localized prices, large text, press/pending feedback, and readable complete terms. Exercise accessible names, focus order/restoration, and actual purchase-provider confirmation on a suitable implementation/device. No such execution is claimed.

## Evidence and guidance limits

Read the installed root `apple-hig/SKILL.md`, searched `references/topic-index.md`, and followed family → topic procedure → supporting guide for Technologies/Apple In-App Purchase; Patterns/Managing accounts and Modality; Menus and actions/Buttons; Foundations/Privacy and Writing. Paths resolve under `.agents/skills/apple-hig/`. Each file read used its own command. Official links above identify guidance obtained from local snapshots; no web request was made.

No screenshot, markup, source implementation, catalog, policy document, device, GUI, SDK, payment sandbox, or accessibility execution was supplied or used. Visual emphasis, exact existing button text, hit areas, accessibility, account deletion, actual payment stack, and server behavior remain unknown. The installed references are derived guidance snapshots, not independent verification of current commerce policy or SDK availability. This review specifies behavior without assuming an Apple SDK and does not certify App Review, legal, security, or runtime compliance.
