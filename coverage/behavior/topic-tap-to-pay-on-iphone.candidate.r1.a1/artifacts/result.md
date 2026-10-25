# Revised merchant Tap to Pay checkout

## Scope and evidence

Design contract for a merchant-operated iPhone accepting a customer's contactless payment. `interface.md` supplies only a behavioral brief: eligibility is unverified; PIN is displayed in plaintext; “Paid” precedes processor confirmation; decline has no cancel/retry; and the amount can change after presentation. No screens, implementation, processor contract, or runtime evidence were supplied. Examples below use an illustrative USD transaction.

This specification assumes a payment service provider (PSP) adapter can expose supported capability, setup, reader, cancellation, and authoritative payment-status operations. These are conceptual operations, not Apple API names. A framework-agnostic specification cannot itself implement a secure contactless reader. Production requires a supported integration; do not substitute a custom NFC/PIN screen when one is unavailable.

## Decisions and source basis

1. **Gate execution, retain discovery.** Keep “Tap to Pay on iPhone” visible on the checkout payment-choice screen without scrolling at ordinary text size, alongside “Other Payment Methods.” Query capability and prepare at launch/foreground. Unknown readiness shows “Checking availability…” with indeterminate progress; it does not imply eligibility. Verified unavailability explains the returned reason and offers another method. Verify eligible device, iOS, region, entitlement, merchant account and PSP support before offering a working reader. This is a release prerequisite, not a claim that this phone qualifies. [Tap to Pay: Checking out](https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone#Checking-out).
2. **Finish setup before customer checkout where possible.** Only an authenticated administrator can accept required terms through the supported flow, after any required OS update. Staff see “An administrator needs to set up Tap to Pay” with “Contact Administrator” opening the approved administrator route and “Other Payment Methods.” Never give staff an acceptance action. A pending checkout may continue automatically after readiness, using its unchanged reviewed total; if the draft changed, return to review. Provide persistent “Tap to Pay Help” and approved localized education covering card/wallet positioning, payment types, PIN accessibility mode and terms. [Enabling](https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone#Enabling-Tap-to-Pay-on-iPhone), [Educating merchants](https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone#Educating-merchants).
3. **Freeze the customer-visible price.** Resolve tips, tax, discounts, currency and other total changes on Review before presentation. Freeze an immutable order revision and total when starting the read session, earlier than the source's prohibition on post-read changes. Edits require a confirmed stopped/unsubmitted attempt, return to Review, and a fresh customer presentation. Approved sales are not edited through this flow. [Checking out](https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone#Checking-out). The earlier freeze is a product safety decision.
4. **Keep PIN handling in the supported secure surface.** Remove merchant PIN text, reveal controls and custom PIN fields. The customer enters a PIN only through the provider/system-owned secure interaction, with its supported accessibility mode. App code receives outcomes and opaque encrypted read material, never PIN digits; do not put digits in state, logs, analytics, receipts, screenshots or accessibility descriptions. A masked merchant PIN field is not a substitute. HIG supports minimizing/protecting private data and using supported PIN education; this stricter data boundary is an application security requirement, not a claim that HIG certifies it. [Privacy: Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices), [Tap to Pay: Displaying results](https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone#Displaying-results).
5. **A read is not approval.** Keep the provider's read/PIN checkmark meaning intact. Send encrypted data promptly to the PSP; after the provider animation, show “Authorizing payment…” until an authoritative result. Show “Payment Approved” only for a confirmed successful payment matching this attempt, order revision, amount and currency. Offer a digital receipt after approval. Never treat local tap completion, timeout or cancellation request as payment success. [Displaying results](https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone#Displaying-results).
6. **Make recovery explicit.** Declines and reader errors retain the order and amount, explain the known outcome and offer a new attempt or another method in checkout. Follow PSP guidance for authentication, PIN limits, offline-PIN and market-specific requirements. Never invent an offline approval. Uncertain outcomes block a second collection until reconciled. Retry locking, idempotency and reconciliation below are product engineering decisions supporting the source's result distinction. [Displaying results](https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone#Displaying-results), [Writing: Best practices](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices).

Use app-styled text “Tap to Pay on iPhone”; no Apple logo. If using a payment-method glyph, use the source's supported wave glyph only where available and approved; a text button works without a symbol library. This is merchant acceptance, so do not substitute a customer Apple Pay purchase button. [Checking out](https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone#Checking-out).

## Screen and action contract

App-owned screens show order reference, localized total and currency, then the current status, with frequent actions toward the middle/lower display. Keep secondary help discoverable. On large text or landscape, reflow into a vertical scrollable layout; retain total and all actions without clipping, overlap or a new navigation hierarchy. Preserve draft and attempt identity across interruptions. [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices).

All app buttons have labeled button semantics, enabled/busy states and visible press feedback. Use at least 44 × 44 pt activation regions with separation; related actions share size and differ in emphasis. The buttons source recommends 44 pt general regions; the accessibility source also lists a smaller 28 pt iOS minimum. This design conservatively uses 44 pt throughout. One prominent action per state is sufficient. No automatic keyboard/default action initiates a charge on screen entry. [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices).

| State | Content and actions | Transition/ownership |
|---|---|---|
| Review | Item/tip/tax breakdown; “Total $24.00 USD”; primary “Tap to Pay on iPhone”; secondary “Other Payment Methods”, “Edit Order”, “Tap to Pay Help” | Edit affects draft only. Tap checks readiness, then freezes revision and opens supported reader. Other methods opens checkout choices; Help opens education and returns with draft intact. |
| Preparing/setup | “Preparing Tap to Pay…”; activity indication in initiating button; secondary “Other Payment Methods” | Necessary approved setup may continue automatically. Switching cancels continuation; late readiness cannot open a reader. No fabricated percentage. |
| Present/read | Frozen total, provider-owned positioning/read instructions and secure PIN interaction | Provider owns protected layout and controls. Use its supported Cancel; do not overlay custom controls over it. On confirmed pre-submission stop, return to Review with draft intact. |
| Stopping | “Stopping payment attempt…” | A cancellation request disables duplicate commands. If read/submission won the race, proceed to authorization/reconciliation instead of claiming cancellation. |
| Authorizing | “Authorizing payment…” and frozen total; indeterminate progress | No Retry, amount edit or alternate collection. Leaving the view does not cancel payment; order list retains “Payment Pending” and reopens status. |
| Declined | “Payment Declined”; “Try another card or choose another payment method.” | Primary “Try Another Card” starts a fresh read after terminal decline. “Other Payment Methods” returns to checkout choices. “Cancel Checkout” leaves order unpaid, retains draft and returns to orders. |
| Read failed | “Card Couldn’t Be Read” or truthful provider-specific reason; appropriate remedy | “Try Again” only when supported and no submission is outstanding; “Other Payment Methods”; “Cancel Checkout”. Unsupported/PIN/amount-limit cases favor an appropriate alternative over a futile retry. |
| Unknown | “Payment Status Unknown”; “Check the payment status before collecting again.” | Primary “Check Payment Status” queries existing attempt; secondary “Contact Support” opens support with safe attempt reference; leaving preserves pending status. No new collection, receipt or “unpaid” assertion. |
| Approved | “Payment Approved”; confirmed amount/reference | Primary “Send Receipt” opens optional receipt delivery; “Done” returns to orders marked paid. Receipt failure says “Payment approved. Receipt couldn’t be sent” with receipt retry; it never retries payment. |
| Confirmed canceled before submission | “Payment Canceled” | Return to Review; order remains unpaid and editable. This does not imply a refund or reversal. |

During authorization, generic Back can leave the status screen but must preserve the unresolved attempt. During reading, Back requests supported cancellation rather than silently destroying state. A decline-screen Cancel abandons checkout; it does not reverse a transaction. Copy for unknown outcomes never claims “You weren’t charged.”

## State and adapter pseudocode

```text
order = {id, draftRevision, items, tip, tax, amountMinor, currency}
attempt = {id, orderId, frozenRevision, amountMinor, currency,
           providerReference, state, submissionKey}

startTapToPay():
  require readyCapabilityVerified && noUnresolvedAttempt(order.id)
  atomically freeze reviewed order revision; create durable unique attempt
  disable repeat start; presentSupportedReader(attempt.amountMinor, currency)

onReadComplete(opaqueEncryptedPayload):
  persist read/submission intent for this attempt
  submitPromptlyToPSP(payload, sameAttemptSubmissionKey)
  after provider completion animation: show Authorizing
  # Never inspect PIN or convert reader checkmark to Paid.

onCancelRequested():
  request provider stop; show Stopping
  if confirmed stopped with no submission: mark Canceled; unlock review
  else: retain lock; reconcile same attempt

onAuthoritativeResult(result):
  validate provenance and attempt identity/reference, revision, amount, currency
  if mismatch: retain unresolved state; reconcile/support
  else if confirmed successful payment: mark Approved exactly once
  else if terminal decline: mark Declined; allow explicit new attempt
  else: keep Pending/Unknown; query authoritative status

onTimeoutOrDisconnectOrAppResume():
  restore order and attempt; query existing attempt before enabling collection
  no result != decline; never auto-retry a charge

onEditRequested():
  if attempt active: stop and confirm no submission, or resolve it first
  only then return to Review; edits create a new revision
```

Persist safe attempt identifiers/status before external operations. Duplicate events are idempotent; stale events update their original attempt and cannot overwrite a newer screen. Repeating a submission after transport uncertainty reuses the same provider-supported idempotency key, never creates a fresh payment. If the PSP lacks equivalent guarantees, block automatic resubmission and require reconciliation. Only a terminal non-success with no outstanding collection permits another method. Refunds/reversals are a separate workflow, outside this specification.

## Data-purpose boundary

| Data | Purpose and permitted handling |
|---|---|
| PIN | Customer authentication; secure provider/system input only. No merchant-app collection, transfer, persistence or disclosure. |
| Encrypted read payload | Payment submission to PSP only through supported integration; no analytics/logs; lifecycle follows verified provider requirements. |
| Order revision, amount, currency, attempt reference/status | Price integrity, reconciliation and safe recovery; persist minimum necessary data with access controls. Never contain PIN. |
| Optional receipt destination | Ask only when Send Receipt is chosen; explain delivery use; offer Done without providing it. Retention/disclosures require implementation review. |

Do not invent permission prompts or request unrelated contacts/location access. Supported setup/permission UI belongs to its documented owner. Exact processor data retention and privacy disclosures remain to be established.

## Worked before → after

**Before (brief instantiated with $24.00):** Merchant presents $24.00; a late tip changes the total to $27.00; customer's PIN appears on the merchant screen. The reader checkmark triggers “Paid” while the processor is pending. The processor declines and the merchant has no recovery action.

**After:** Merchant finalizes a $3.00 tip in Review, sees $27.00 USD and selects Tap to Pay. Revision 8 is frozen at 2700 minor units. Further tip/amount changes are blocked during this attempt. The supported reader presents that total and privately handles any required PIN. Read completion submits encrypted data and transitions to “Authorizing payment…” after the reader animation. PSP returns terminal decline for the matching $27.00 attempt: show “Payment Declined,” “Try Another Card,” “Other Payment Methods,” and “Cancel Checkout.” Merchant chooses another card; a new attempt retains revision 8 and $27.00. Only its authoritative success shows “Payment Approved” and receipt actions. If either request times out instead, show unknown/pending and reconcile before allowing another collection.

## Acceptance checks and audit status

**Passed — static specification review only:** The revised contract separates read and approval, removes app PIN access, freezes the total before presentation, defines decline/cancel/retry/unknown states, restricts terms to administrators, retains payment alternatives, and distinguishes provider-owned UI from app UI. Installed root → family → topic → source reading was completed for iOS, Tap to Pay, privacy, writing, buttons and accessibility; the topic index was searched. These passes establish document coverage, not working software.

**Failed — supplied baseline, from the brief:** PIN confidentiality, truthful approval timing, decline recovery, and amount stability. No code or screen inspection independently reproduced these failures.

**Not executed — required implementation/integration acceptance:**

| Scenario | Required observable result |
|---|---|
| Unverified/unsupported device, region or PSP | No operational reader launch; clear reason when known; another checkout method remains reachable. Verify actual eligibility and entitlements independently. |
| Staff encounters missing terms | No staff acceptance; administrator route works; return preserves draft. Required update occurs before terms acceptance. |
| Ready, preparing and switched-away setup | Option is discoverable; indeterminate wait; repeated taps create one attempt; late setup completion cannot launch after switching methods. |
| Total edited during presentation | Reader/session total cannot mutate. Edit proceeds only after confirmed safe stop, then new review/presentation. |
| Read/PIN succeeds but authorization delays/declines | Never Paid at checkmark; progress then explicit result; alternatives available after terminal decline. |
| Cancel/read race, timeout, restart, duplicate/stale callbacks | Existing attempt reconciled; no second collection while unresolved; no false canceled/unpaid/approved state. |
| Read failure, unsupported card, PIN/amount limits | Appropriate retry or alternative reachable in checkout; PSP-required authentication/fallback respected. |
| PIN lifecycle | Secure provider input verified; inspect app state, logs, analytics, receipts and assistive descriptions for absence of PIN data. Requires supported integration/security review. |
| Approved sale and receipt failure | Exactly one paid outcome; receipt retry never issues another payment. |
| Portrait, landscape, interruption, 200% text | Draft/attempt survives; total, status and actions reflow without clipping or overlap. Measure 44 pt targets and separation; assess real hand reach. |
| Assistive access and sensory feedback | Complete app flow operable with VoiceOver, Switch Control and Full Keyboard Access; controls expose names/roles/states in task order; approval/decline conveyed in persistent text, not just color/sound. Verify provider's accessible PIN mode separately. |
| Appearance/preferences | Measure actual light/dark and Increase Contrast rendering; preserve status meaning without color. Reduced-motion presentation retains state and progress meaning. |

Accessibility requirements are design targets, supported by [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision) and [Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility); no assistive-technology execution is claimed. App status changes should be exposed as accessible status updates without repeatedly stealing focus; exact integration requires runtime testing. Provider-owned surfaces must use supported behavior rather than custom replacements.

## Evidence limits

All work used local files and the installed guidance; no web browsing occurred. Official links above identify the articles represented by local snapshots, not live verification. Local references identify retrieval/snapshot date 2026-10-25 and are original guidance derived from HIG; their existence does not establish independent source/media review. No device, SDK, GUI, payment, settlement, accessibility, security or legal-compliance execution occurred. No API availability, eligible hardware/region, PSP cancellation guarantee, offline behavior or entitlement was verified. Those are release blockers for a real payment implementation, not reasons to invent SDK behavior. This deliverable is an implementable interaction contract pending adapter feasibility and runtime validation.
