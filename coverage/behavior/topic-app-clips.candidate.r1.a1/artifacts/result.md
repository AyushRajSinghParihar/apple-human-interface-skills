# Parking-meter App Clip: revised interaction specification

Design contract for iOS; framework agnostic. Input evidence is the short flow in `interface.md`, not a running application. The finite task is to buy parking at the invoked meter and receive an authoritative end time and receipt without an account or full-app installation.

## Decisions and source basis

1. Remove the onboarding carousel, account gate, and installation gate. Open the meter supplied by the invocation URL, then offer duration selection and guest payment. Keep required interface assets bundled and defer promotional assets. This applies [App Clips — Designing your App Clip](https://developer.apple.com/design/human-interface-guidelines/app-clips#Designing-your-App-Clip): a short, focused task that can finish without installation, including under poor bandwidth.
2. Use Apple Pay as the preferred checkout where supported, with an eventual system-generated localized **Pay** button. Parking is a physical service. A guest alternative must remain available where Apple Pay is unavailable; processor and method are unresolved implementation dependencies. Do not draw an imitation button in a prototype. Collect choices before authorization, request no shipping/contact fields without a demonstrated need, and show the merchant, fees, and total consistently. See [Apple Pay — Streamlining checkout](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Streamlining-checkout) and [Using Apple Pay buttons](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Using-Apple-Pay-buttons).
3. Keep the meter, price, and primary action together, with frequent controls toward the middle/lower display. Use a single scrolling task page rather than tabs. Preserve context through interruption, rotation, and enlarged text. See [Designing for iOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices).
4. Store authoritative payment/session state on the service; never depend on Clip storage or background work. Secure recovery must survive removal of local Clip data. See [App Clips — Preserving privacy](https://developer.apple.com/design/human-interface-guidelines/app-clips#Preserving-privacy). The recovery protocol below is a proposed engineering contract, not an Apple API guarantee.
5. Offer full-app installation only after confirmed completion, optionally through the appropriate system overlay. Keep the receipt visible and promotion dismissible; do not repeat it during retries. Future invocations with the full app installed should preserve the meter/session destination. See [App Clips — Showcasing your app](https://developer.apple.com/design/human-interface-guidelines/app-clips#Showcasing-your-app).
6. No launch permission requests, location lookup, account, or marketing consent is needed: the URL already supplies context. No notification feature is included in this scope. If expiry reminders are later added, design them as explicit task-related opt-in, respecting the Clip's limited notification window rather than promising indefinite delivery. See [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices) and [App Clips — Limiting notifications](https://developer.apple.com/design/human-interface-guidelines/app-clips#Limiting-notifications).

## Entry surface and state contract

Existing physical QR placement remains in scope as an entry point, not a new App Clip Code production project. Sign copy: **“Scan to pay for parking · Meter {printed ID}.”** Verify that the deployed QR invokes that exact meter. Do not apply App Clip Code geometry rules to an ordinary QR code. No NFC is assumed.

Where an App Clip card is configured: title **“Pay for parking”**, subtitle **“Choose your time and pay at this meter.”**, action **Open**. Use opaque, task-explaining meter/location art without embedded copy, PNG/JPEG at 1800 × 1200 px. Title/subtitle are within the source's 30/56-character limits; localized variants must be checked separately. Operator branding leads provider branding. These requirements come from [Creating content for an App Clip card](https://developer.apple.com/design/human-interface-guidelines/app-clips#Creating-content-for-an-App-Clip-card).

| State | Visible content and actions | Transition contract |
| --- | --- | --- |
| Resolve meter | Operator identity; “Meter {ID}” from validated URL, labeled “Checking meter”; compact progress text | Validate URL host/path and identifier syntax, then fetch authoritative meter identity, location, availability, tariff, time zone, limits, and quote version. Never trust URL price or availability. No splash/carousel. |
| Ready | “Meter {ID}”; street/zone; “Check this matches your meter”; duration choices from service; end time with local date/time zone when needed; itemized fees and total; payment action; “Wrong meter?” | Default to a clearly selected valid duration supplied by tariff policy. Changing duration refreshes quote/end time. Wrong meter explains rescanning the correct meter; never silently substitutes a nearby meter. |
| Checkout | Selected meter, duration, end time, and total remain the purchase scope | Open payment only against a current quote. If a selection is missing, explain and focus it after activation rather than silently disabling Apple Pay. If tariff changed, show the revised amount/end time and require review before fresh authorization. |
| Processing | System payment progress while sheet owns checkout; afterward, if necessary, “Checking payment — don’t pay again yet” and Check status | One attempt per purchase intent. Authorize and commit against the frozen quote. Do not label parking active on client authorization alone. |
| Complete | **“Parking active”**; meter/location; authoritative start and “Paid until {time, date}”; duration, amount/fees, receipt ID; Save receipt; Done | Success requires service-confirmed payment and parking activation. Save receipt exports a minimal receipt through an implementation-appropriate mechanism. Optional installation appears below the result. Done ends the flow; do not claim it programmatically terminates the Clip. |

Duration choices and limits are tariff data, not invented universal increments. No plate, space, email, or telephone field is assumed. If the operator requires a plate/space for enforcement, add only that essential field before payment, explain its purpose, and validate against the real operator contract before launch.

## Failure, interruption, and recovery

- **Invalid/missing ID:** “We couldn’t identify this meter. Scan the code on your meter again.” No generic home page or payment action. Unsupported/inactive meter: show the verified ID and operator-provided alternative payment instructions.
- **Poor connection before quote:** retain the invoked ID and say “Can’t load parking rates. Check your connection and try again.” Offer Retry. No guessed tariff or offline authorization. Cached rates may be labeled informational only. If payment cannot be completed, explicitly say “Parking has not started” and show verified alternate instructions if available.
- **Payment cancellation/decline:** preserve meter and duration; show a specific remedy where available. Cancellation returns to review without claiming success. Request cancellation of in-flight processing when the payment sheet dismisses on cancellation/timeout, following [Apple Pay — Payment processing problems](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Payment-processing-problems). Reconcile with the processor before retrying; cancellation is not proof that a previously committed charge was undone.
- **Connection lost after submission:** outcome is unknown. Do not show “failed,” “active,” or allow a fresh charge until status reconciliation returns a terminal result. Foreground Check status retries the same attempt. On confirmed failure/cancellation, allow a new authorization; on confirmed success, show the receipt. If unresolved, give the reference and operator support route, and say parking is not yet confirmed.
- **Charged but activation failed:** show “Payment received; parking not confirmed,” reference, support, and the service's refund/remediation status. Never disguise partial completion as active parking.
- **Interruption:** preserve non-sensitive draft context when available; on foreground return, refresh quote or query existing attempt before exposing payment. No dependency on a background timer or background request completing.
- **Local data removed:** provide a secure receipt/status recovery link or opaque recovery credential outside temporary Clip storage before submitting payment. Copy: “Save this recovery link to check your payment if you lose connection.” Offer Save link, then Continue after successful handoff; no account/install gate. Server retains the attempt and result. Link must reveal only this transaction, resist guessing, and follow a defined retention/revocation policy. A rescan containing only a public meter ID must never expose another driver's receipt. If the delivery mechanism cannot provide durable recovery, this design is not ready to launch.

The extra recovery handoff is a deliberate product tradeoff for the stated poor-network condition, not a HIG-mandated screen. Its actual export, return behavior, security, and user comprehension require validation.

## Framework-agnostic orchestration

```text
onInvoke(url):
  context = validateAndResolveMeter(url)
  renderReview(context, fetchCurrentQuote(context))

onPay(selection):
  quote = validateCurrentQuote(selection)
  intent = service.createIntent(quote)       // stable idempotency key
  ensureRecoveryLinkSaved(intent)           // durable route outside Clip storage
  result = paymentAdapter.authorize(quote)  // system sheet where supported
  if result.dismissedOrTimedOut:
    service.requestCancellation(intent)
  else if result.authorized:
    service.commitPaymentAndActivate(intent, result)
  reconcile(intent)                         // query; never issue another charge

reconcile(intent):
  status = service.status(intent)
  confirmedActive -> renderReceipt(status)
  terminalUnpaid -> renderReviewWithRemedy()
  paidNotActive -> renderRemediation(status)
  pendingOrUnreachable -> renderUnknownWithCheckStatus(intent)
```

The service must deduplicate simultaneous taps, retries, and resumed calls by intent; maintain unique processor transaction references; and serialize commit/cancel reconciliation. A duplicate request returns the same result. A recovery link resolves only authorized transaction context. These are proposed backend requirements and have not been implemented or tested here.

## Data-purpose/access matrix

| Data | Purpose and access | Collection decision |
| --- | --- | --- |
| Meter ID, tariff, duration | Resolve context and buy the selected parking service | Use validated invocation and service data; no location permission |
| Payment authorization/reference | Process and reconcile this purchase | Payment provider handles sensitive payment inputs; no raw payment credentials in URL, receipt link, or logs |
| Receipt/recovery credential | Restore status after interruption or Clip eviction | Secure server record plus user-saved opaque link; redact from analytics; define expiry and retention before release |
| Account, address, contacts, location, marketing identifiers | No demonstrated task need | Omit; no startup prompts or account creation |

Update actual privacy disclosures when implementation data flows are known. This matrix does not certify security or legal compliance.

## Worked before/after

Illustrative test fixture only: meter M-042 at Oak Street; 30 minutes costs $2.00 plus $0.20 fee; service confirms a 14:00–14:30 session in the meter's time zone.

**Before (supplied):** scan M-042 → onboarding carousel → create account before seeing meter → download full app before paying. The supplied file does not establish that any payment or completion screen exists.

**After (specified):** scan M-042 → card/Open → review “Meter M-042 · Oak Street,” selected “30 minutes,” “Paid until 14:30,” fee $0.20 and total $2.20 → Pay → save recovery link on first attempt → authorize $2.20 for that meter → service confirms → “Parking active · Paid until 14:30,” receipt R-123 → Save receipt or Done, optional full-app offer below.

If connectivity drops immediately after authorization, the worked path changes to “Checking payment”; Check status uses the same intent. A later confirmed success shows R-123 without another charge. If the Clip is removed, the saved recovery link restores that same status securely. No offline success is fabricated.

## Acceptance checks and audit status

**Passed — specification inspection only:** supplied flow was read; root → family → topic → supporting reference reads were completed from the installed package. The revised path contains no carousel, account, or installation prerequisite. URL context, guest checkout, post-completion promotion, foreground recovery, and a local-data-loss path are specified. Card copy fits the English source limits. No SDK is assumed.

**Failed — supplied-flow design inspection:** the installation requirement prevents completing the task inside the Clip; onboarding/account requirements delay the invoked meter task. These findings describe `interface.md`, not a tested build.

**Not executed — implementation acceptance scenarios:**

1. Scan deployed QR for M-042: card and first task page resolve M-042, never a generic provider home. Wrong, malformed, inactive, or hostile URL fails safely before payment.
2. Complete the fixture as a guest without installing; sheet and receipt agree on meter, duration, merchant, fees, and $2.20 total. No unnecessary personal fields appear.
3. Simulate slow, unavailable, and restored network at invocation, quote refresh, authorization, commit, cancellation, and status lookup. Preserve input; never fabricate activation; repeated taps produce at most one charge/session.
4. Cancel/timeout checkout; verify cancellation and processor reconciliation before retry. Test charge-success/activation-failure separately.
5. Terminate the Clip and erase all local data after submission. Open the saved recovery link and recover the same transaction; another person scanning only the meter cannot retrieve it.
6. Rotate and enlarge text: meter, selection, total, remedies, and actions remain readable and reachable through scrolling without losing state. Return from another app and restore the correct context. Check real-device touch comfort, Dark Mode, and assistive-technology operation; none is established by this document.
7. Verify the eventual Apple Pay adapter uses the generated localized button and system sheet. Unsupported/unconfigured cases offer appropriate setup or the approved guest alternative without an install gate.
8. After confirmed success, dismiss installation promotion and still access the receipt. With the full app installed, invoke the same meter/recovery link and retain the focused destination without repeat account steps.
9. Test physical QR scanning and actual startup on constrained bandwidth. No print, camera, device, payment sandbox, SDK build, GUI, or accessibility execution occurred here.

## Evidence limits and unresolved release decisions

Only `interface.md` and the installed local HIG instructions/articles were used. Official links above identify source sections; no web pages were fetched. Local articles identify retrieval as 2026-10-25 and are summarized guidance, not SDK references or independently verified runtime evidence. No conflicting passages were found in the selected guidance.

Operator identity, tariffs, enforcement fields, supported payment alternative, payment/activation atomicity, receipt export, secure recovery mechanism, support route, and retention policy are not supplied. They require product/backend decisions and executable validation before release. The full-app/Clip routing and system-card deployment also remain unverified. This specification establishes intended behavior; it does not demonstrate platform availability, payment correctness, security, physical scan reliability, or accessibility conformance.
