# Revised merchant checkout: Tap to Pay on iPhone

## Scope and evidence

Design specification, framework agnostic. The only product evidence is `interface.md`: support is unverified; the flow exposes a customer PIN, says “Paid” before processor confirmation, lacks cancel/retry after decline, and permits amount changes after presentation. No screens, code, provider contract, or runtime were supplied. Examples below are proposed behavior, not observed screens.

The installed apple-hig root was read, followed by the Getting started → Designing for iOS and Technologies → Tap to Pay on iPhone procedures and their local source guides. Foundations → Privacy, Writing, and Accessibility, and Menus and actions → Buttons were also read, each family and topic before its guide. The topic index was searched for payment, iPhone, privacy, accessibility, writing, and buttons. Official links below identify the local snapshot’s sources; no web access was used.

## Decisions and ownership

1. **Gate execution on verified capability, not a presumed iPhone entitlement.** Tap to Pay stays discoverable in checkout, including before setup. Query a supported provider integration for device, OS, region, merchant/account, entitlement and readiness status. Unknown status is not eligible. Show “Checking availability…” with indeterminate progress, then readiness, setup, or a specific unavailable reason and another payment method. This specification supplies no reader implementation and assumes no Apple SDK. Actual contactless collection requires a supported integration; a custom web NFC/PIN screen is not a substitute. [Tap to Pay: enabling and checkout](https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone#Enabling-Tap-to-Pay-on-iPhone).
2. **Separate administrator setup from staff checkout.** Prepare at launch and foreground entry. Use provider status to show terms only when needed; required OS readiness precedes acceptance. Administrators accept before configuration. Staff see “An administrator needs to enable Tap to Pay” and an approved administrator handoff, plus “Choose Another Method.” Preserve the order and continue automatically after setup if the merchant is still in checkout; reconfirm the total if it changed. Keep current provider/system-approved education findable in onboarding and persistent Help: positioning, supported payment types, PIN/accessibility mode, and terms where needed. [Enabling and education](https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone#Educating-merchants).
3. **Freeze the amount before presentation.** Review shows currency, items, tax, tip and final total; resolve all total-changing choices here. Selecting “Tap to Pay on iPhone” creates an immutable amount/currency/order-version snapshot. Read, authorization and receipt must use that snapshot. No total editor appears on the read surface. A requested change requires ending the reader safely, confirming no unresolved payment, returning to review, and creating a fresh attempt. This extends the source’s pre-read final-total guidance into an explicit product invariant. [Checkout](https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone#Checking-out).
4. **Keep PIN entry outside merchant UI and app data.** Remove plaintext PIN display entirely; do not replace it with a merchant-owned masked keypad. Hand off any required PIN interaction to the supported system/provider secure customer surface, including its accessibility mode. Merchant UI may say “Customer verification in progress”; it receives only permitted status/outcome metadata. Never collect, store, log, announce, put on receipts, or send a PIN to analytics. This is a proposed security boundary based on data minimization and provider ownership, not a claim that HIG specifies a complete PIN security protocol. If secure PIN handling is unsupported, follow provider fallback guidance or offer another method. [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices), [Tap to Pay results](https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone#Displaying-results).
5. **A successful read is not payment approval.** Let the owned reader animation finish; promptly forward its encrypted payment payload through the supported provider path. App-owned UI then says “Authorizing payment…” until a verified processor result. Only an explicit approval for this attempt and exact amount/currency may produce “Payment Approved.” Offer a digital receipt. Timeout, lost connectivity and cancellation requests never imply decline or approval. [Results](https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone#Displaying-results).
6. **Recover within checkout.** Confirmed decline says “Payment Declined. Try another card or choose another payment method.” Unreadable/unsupported cards and amount/PIN limits receive the provider-safe specific explanation and available alternatives: another card, cash, external reader or payment link. Offer only configured alternatives. System errors explain an actionable remedy, such as an OS update when actually required, and unresolved errors expose support. Follow provider guidance for post-read authentication and offline-PIN fallback; invent no offline approval. [Results](https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone#Displaying-results), [Writing](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices).

## Screen and transition contract

App screens show order reference, final total/currency and explicit status above actions. Put frequent actions toward the middle/lower display with safe-area clearance. Keep Tap to Pay discoverable without scrolling at ordinary sizes; enlarged text may reflow into a usable scroll layout. Retain order and status across orientation changes, backgrounding and navigation. Preserve normal system navigation; Back during an active attempt follows the same safe exit rules as Cancel. [iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices).

| State | Content and actions | Transition |
| --- | --- | --- |
| Review | Editable order, final total; primary “Tap to Pay on iPhone”; secondary “Choose Another Method”; “Cancel Checkout” preserves order draft | Check readiness/setup; freeze snapshot immediately before reader launch |
| Preparing | “Preparing Tap to Pay…”; activity indication in initiating button, no duplicate activation; “Choose Another Method” and “Cancel Checkout” | Ready → reader; error → actionable recovery. Cancel preparation and invalidate late callbacks before leaving |
| Reading / secure verification | System/provider-owned read/PIN surface displays frozen total and supported positioning guidance. Use its supported cancellation and accessibility affordances | Read success → authorizing; confirmed cancellation → review; read error → recovery |
| Authorizing | Frozen total; “Authorizing payment…”; no success receipt or second payment action | Explicit verified approval → approved; confirmed decline → declined; ambiguous result → checking |
| Checking | “Payment status unknown. Check this payment before trying again.” Primary “Check Payment Status”; secondary “Contact Support” | Reconcile same attempt until authoritative result. Preserve unresolved order; no new charge or method switch |
| Declined / failed with confirmed no payment | Persistent explanation; primary “Try Another Card”; secondary “Choose Another Method”; “Cancel Checkout” | Retry creates fresh attempt with same reviewed total; method choice returns to checkout methods; cancel preserves unpaid order |
| Approved | “Payment Approved”, exact total/currency, order reference; primary “Send Receipt”; secondary “Done” | Receipt delivery never reauthorizes; Done returns to sales with paid order |

Cancellation is available before an authorization is committed, through the supported integration. Show “Cancelling…” until acknowledged. A cancellation request racing with read/submission does not make the order unpaid: reconcile it. If authorization is already underway, explain “Payment is processing. Its result must be checked before another payment.” Leaving the page retains the unresolved transaction and exposes “Resume Payment Status” on return. A refund after approval is a separate workflow, not Cancel Checkout. These concurrency and duplicate-payment safeguards are product decisions; provider semantics must validate them.

Buttons use app styling and at most one primary action per screen in this design. Use text “Tap to Pay on iPhone” (or “Tap to Pay”); no Apple logo. An optional supported wave glyph must come from approved assets; use text alone if unavailable. App-owned buttons have at least 44 × 44 pt activation regions with separation, visible press/focus feedback, names matching labels, and explicit disabled reasons when unclear. No payment starts merely from restoring focus or returning to the app. [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), [Tap to Pay checkout](https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone#Checking-out).

Use text plus symbols for pending, declined and approved states; color or sound alone carries no outcome. Keep outcomes until explicit dismissal. At 200% text enlargement, retain amount, status, explanations and all actions without overlap or truncation. Reading order is heading → amount → explanation → actions; controls expose names, roles and availability. Test assistive navigation through the app and supported reader/PIN handoff. Customer PIN digits never enter merchant-facing accessibility content. Actual contrast, semantics, handoff and physical reach remain unmeasured. [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility).

## Framework-agnostic transaction model

The operations below are abstract contracts, not SDK methods. A supported provider must supply equivalent capabilities; otherwise that path is unavailable.

```text
startPayment(order):
  require verifiedReadiness && noUnresolvedAttempt(order.id)
  snapshot = freeze(order.id, order.version, totalInMinorUnits, currency)
  attempt = persistNewAttempt(snapshot, uniqueAttemptKey)
  disableDuplicateStart()
  openSupportedReader(snapshot, attempt.id)

onReaderEvent(attemptId, event):
  require event belongs to current persisted attempt
  if event is encryptedReadCompleted:
    persist submission intent before sending
    submitOnceToProvider(attempt.uniqueAttemptKey, encryptedPayload, snapshot)
    # Prefer early submission; do not overlay the owned completion animation.
    afterOwnedAnimation: showAuthorizingUnlessAlreadyResolved()
  if event is cancelAcknowledged and provider guarantees no submission/payment:
    markCancelled(); returnToReview()
  if event is ambiguous or cancellation raced with submission:
    enterChecking(); reconcileSameAttempt()

onProviderResult(attemptId, result):
  authenticateAndCorrelate(result, attemptId, snapshot)
  reject/quarantine mismatched amount, currency, order or stale attempt events
  apply idempotently; never let a late read event overwrite a final result
  if confirmedApproved: persistPaidOrder(); showApproved()
  if confirmedDeclinedOrNoPayment: persistResolvedFailure(); showRecovery()
  otherwise: persistUnresolved(); showChecking()

onResume:
  restore order and persisted attempt
  if unresolved: reconcileSameAttempt()  # Never automatically start a new read.
```

Idempotency, durable state, callback authenticity and cancellation guarantees require provider/backend implementation review. Retry a submission only under its documented idempotency contract; never resend by creating a new charge because of a timeout. Keep encrypted payload handling minimal and within the provider’s supported lifecycle.

| Data | Purpose and boundary |
| --- | --- |
| Order, amount, currency, attempt key and provider reference/status | Correlation, authorization and reconciliation; retain under the merchant’s defined access/retention policy |
| Customer PIN | Secure system/provider input only; absent from app models, backend, logs, analytics, receipts and merchant UI |
| Encrypted payment payload | Transient supported payment path to PSP; never general logs or analytics |
| Receipt destination | Optional, requested only when sending receipt; do not request unrelated contacts/location access or make receipt delivery a condition of payment |

## Worked before/after

Illustrative order: items plus tax and tip total USD 27.50.

| Moment | Before, based on the brief | Revised behavior |
| --- | --- | --- |
| Present phone | Amount can change after presentation | Review USD 27.50, then freeze it before opening reader. A later tip edit requires safe exit and new review |
| Customer verification | Customer PIN displayed in plaintext | Secure owned PIN surface; merchant sees only verification status, never digits |
| Read checkmark | “Paid” before processor confirmation | Reader completes; merchant sees “Authorizing payment…” for USD 27.50 |
| Processor declines | No cancel/retry | “Payment Declined” with Try Another Card, Choose Another Method and Cancel Checkout; order remains unpaid |
| Retry succeeds | Outcome handling otherwise unspecified | New correlated attempt for USD 27.50; only processor approval yields Payment Approved and receipt option |
| Network result missing | Not specified | Payment Status Unknown; reconcile existing attempt and block a second charge until resolved |

## Acceptance checks and status

**Passed — specification inspection only:** all four supplied problems have concrete replacements; read and approval are distinct; final amount is immutable; PIN ownership excludes merchant/app plaintext; decline includes retry, alternative method and cancel; administrator/setup, interruption, unknown-result and duplicate-activation paths are specified. Source routes and local guides were consumed in order. No framework or API availability is assumed.

**Failed — supplied behavior as described:** PIN privacy boundary; approval timing; amount integrity after presentation; decline recovery. These are brief-level findings, not independently reproduced runtime failures.

**Not executed — implementation acceptance gates:**

| Scenario | Required observable result |
| --- | --- |
| Eligibility unknown/unsupported; OS update needed; unconfigured device | No reader launch until readiness verified; accurate reason/setup route; other methods remain accessible |
| Staff encounters terms; administrator completes setup | Staff cannot accept; approved administrator route works; setup resumes checkout without losing order |
| Attempt to edit amount/tip during read or authorization | Snapshot cannot change; safe exit/review required; processor and receipt match exact amount and currency |
| PIN-required payment, including supported accessibility mode | Only secure supported surface handles digits; inspect UI, accessibility output, app/backend logs, analytics and receipt for absence of PIN |
| Read succeeds; processor approval delayed | No Paid/Approved app state before authoritative approval; owned completion animation is respected |
| Decline, unreadable card, PIN/amount limit, unsupported card | Accurate provider-safe explanation; actionable retry and configured alternatives; cancellation preserves unpaid order |
| Double tap, duplicate/stale callbacks and mismatched results | At most one live charge; final state not overwritten; mismatches do not mark order paid |
| Timeout, cancellation/submission race, background/termination and resume | Persisted unresolved attempt restores and reconciles; no automatic new charge; cancel is not confused with refund |
| Approved payment, receipt delivery failure | Paid state remains accurate; receipt retry sends only receipt, without another authorization |
| Portrait/landscape, 200% text, light/dark and Increase Contrast | Essential content/actions remain usable; measure actual contrast and target geometry; no clipping or overlapping targets |
| VoiceOver, Switch Control, Full Keyboard Access and reader handoff | Named controls reachable/activatable in task order; status understandable without color/sound; supported secure PIN accessibility mode works |
| Physical iPhone handling and interruption | Primary actions comfortably reachable; system navigation preserved; context and status survive interruption |

## Evidence limits

Only local text was inspected and this specification was written. No device, SDK, GUI, payment, backend, accessibility, contrast measurement, build or test execution occurred. No support matrix, specific iPhone/OS/market eligibility, entitlement, provider API, PIN behavior, cancellation guarantee, settlement or security/compliance certification is established. Approval denotes the confirmed processor outcome required by the configured merchant payment flow; authorization/capture/settlement semantics must be resolved with that provider before shipping.

The installed guides are dated local HIG-derived guidance, not SDK documentation or proof of independently reviewed Apple media. Official links are attribution, not newly verified sources. Current approved assets, education, integration contracts and feasibility remain implementation prerequisites. General privacy guidance supports minimization but does not establish a payment-security protocol. Idempotency, immutable snapshots and unknown-result blocking are explicit product safeguards added here, not claims of universal Apple HIG mandates.
