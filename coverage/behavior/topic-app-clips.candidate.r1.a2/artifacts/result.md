# Parking-meter App Clip interaction specification

## Scope and decisions

Target: iOS, a person standing at a meter after scanning its QR code. The finite task is to identify that meter, choose a permitted parking duration, pay, and see whether parking is active. This is a framework-agnostic design contract; no Apple SDK is assumed available here.

The supplied `interface.md` states that the current flow opens onboarding, requires an account before showing the meter, and requires full-app installation before payment. It also supplies a meter identifier in the invocation URL and warns of poor connectivity. No screens, implementation, tariff model, payment service, or backend contract were supplied.

| Decision | Revised behavior | Basis |
| --- | --- | --- |
| Direct contextual entry | Remove the carousel. Resolve the invocation meter immediately; show its identifier while loading authoritative details. | [App Clips — Designing your App Clip](https://developer.apple.com/design/human-interface-guidelines/app-clips#Designing-your-App-Clip) |
| Complete without gates | Guest parking purchase requires neither account creation nor full-app installation. | Same App Clips section; [Apple Pay — Streamlining checkout](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Streamlining-checkout) |
| Short, linear purchase | One meter/duration review, payment authorization, then explicit completion. Keep unrelated settings and promotions out of the purchase. | App Clips — Designing your App Clip |
| Minimal startup | Bundle essential text and layout; fetch only meter rules, quote, and transaction state. Avoid decorative downloads. | Same App Clips section, especially poor-bandwidth startup guidance |
| Appropriate checkout | Prefer Apple Pay for this physical service where supported. Use a generated, localized payment button in an eventual integration, never an imitation. | [Apple Pay — Offering Apple Pay](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Offering-Apple-Pay), [Using Apple Pay buttons](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Using-Apple-Pay-buttons) |
| Recoverable task | Store authoritative session and payment state on the server; temporary Clip storage is insufficient. No background Clip work is required for completion. | [App Clips — Preserving privacy](https://developer.apple.com/design/human-interface-guidelines/app-clips#Preserving-privacy) |
| Optional continuation | Completion stands alone. If useful, offer the platform installation overlay only after success; full-app entry preserves the meter/session destination. | [App Clips — Showcasing your app](https://developer.apple.com/design/human-interface-guidelines/app-clips#Showcasing-your-app) |

Specific error copy, transaction consistency rules, and recovery mechanisms below are proposed product/engineering decisions, rather than claims that HIG prescribes a particular backend.

## Entry and screen contract

1. **Invocation/card:** Configure the QR destination for the relevant App Clip experience. Proposed card title: “Pay for parking”; subtitle: “Choose your time and pay at this meter”; action: **Open**. Use task-explaining opaque meter imagery, without embedded text; header asset 1800 × 1200 px PNG/JPEG. The title/subtitle fit the local guide’s 30/56-character limits. Card configuration and invocation association still require implementation verification. Do not treat an ordinary QR code as an Apple-generated App Clip Code or apply its production dimensions to this QR. Suggested adjacent sign copy: “Scan to pay for parking.” [Card guidance](https://developer.apple.com/design/human-interface-guidelines/app-clips#Creating-content-for-an-App-Clip-card)
2. **Resolving:** Show “Parking” and “Checking meter 042…” with visible progress and a way to leave. The URL identifier is untrusted input: validate its format and resolve it through the service. Do not infer location from GPS or request location permission merely to rediscover the supplied meter. If lookup is unavailable, show “Can’t load this meter. Check your connection and try again.” **Try again** repeats lookup. Never show a cached tariff as a currently payable quote.
3. **Ready:** Show operator branding first, then “Meter 042,” authoritative street/zone, parking restrictions, duration choices allowed by those rules, end time with date/time zone where needed, parking charge, fees, and total. Initial duration is visibly selected only after valid rules arrive; no silent purchase. Ask the person to check the displayed identifier against the meter. If incorrect, offer “Scan the correct meter” guidance and leave the current purchase unsubmitted. Do not silently substitute a nearby meter.
4. **Review and pay:** Keep the meter, chosen duration, end time, and total together with the primary payment action toward the middle/lower screen. Let content scroll as needed without hiding required details. Changing duration requests a new quote; show updating state and prevent payment against stale pricing. If the server quote expires, refresh and require review of any changed total or end time before authorization. [iOS best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices)
5. **Payment sheet:** Use the generated **Pay** Apple Pay button where available. Purchase scope is exactly the displayed meter and duration, with no recurring charge or automatic extension. Sheet line items show parking and any fee; the total uses the statement-recognizable merchant name. Request no shipping address or unrelated contact fields. Show system payment progress in the sheet. A missing required choice produces an explanation and focus on that choice after activation, rather than an unexplained disabled Apple Pay button. [Sheet guidance](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Customizing-the-payment-sheet)
6. **Completion:** Only confirmed activation shows “Parking active.” Show meter/location, session identifier, paid total, and “Expires today at 11:15 AM” (include date when not today), plus **Done**. Do not equate payment authorization with parking activation. Done leaves a readable receipt view; it does not assume the Clip can terminate itself. Optional secondary full-app promotion: “Get the app to manage future parking,” through an appropriate system overlay, after this receipt is visible. No automatic redirect or installation requirement. No notification permission prompt in this baseline flow.

If Apple Pay is unsupported, show only a genuinely supported guest payment alternative; if none exists, explain that payment is unavailable here and direct the person to the meter’s existing payment instructions. On supported but unconfigured devices, offer appropriate Apple Pay setup. This specification does not assert an alternative payment provider exists. Installation must never be the payment fallback.

A vehicle identifier is not assumed necessary by the brief. If the actual enforcement system requires one, add only that necessary choice before authorization, with its validation and clear explanation; this is a discovery dependency, not permission to add an account gate.

## State, failure, and recovery contract

```text
invoke(url):
  validate meter identifier -> resolving OR invalid_invocation
  fetch authoritative meter and rules -> ready OR lookup_error

ready + duration_change:
  request current quote -> ready(new quote) OR quote_error

ready + pay:
  validate required choices and quote
  freeze purchase snapshot; create/reuse server attempt identifier
  open payment sheet -> authorizing

authorizing + cancel/timeout:
  request cancellation of in-flight processing
  reconcile attempt -> cancelled | failed | active | outcome_unknown

authorizing + authorization:
  submit once using attempt identifier
  server coordinates payment and parking activation
  -> active only after authoritative session confirmation
  -> failed only when no charge/activation can still occur
  -> outcome_unknown otherwise

outcome_unknown + check_status:
  query same attempt; never create a second charge
  -> active | failed | cancelled | outcome_unknown
```

- **Invalid invocation:** “This parking link is invalid. Scan the code on the meter again.” No generic home page or payment action.
- **Known decline/failure:** Explain the specific remedy; retain meter and duration. Re-enable payment only after the earlier attempt is terminal and a valid quote is available. [Handling problems](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Handling-problems)
- **Cancelled sheet:** Keep selections. Stop processing where still cancellable. If the server has already committed, reconcile and show the real result instead of asserting cancellation. Retry cannot create duplicate processing.
- **Unknown result:** “We haven’t confirmed your parking. Check status before trying another payment.” Show **Check status** and the available support reference/contact. Do not say “Parking active,” “Not charged,” or “Pay again” while uncertain. If charged but activation fails, show “Parking not active” and the actual refund/support status; never promise an unconfirmed refund.
- **Interruption:** Preserve meter, duration, and nonterminal attempt reference where possible. On resume, reconcile before allowing payment. Do not rely on background execution to finish or display success.
- **Clip eviction:** Require a secure server-backed recovery mechanism independent of Clip-local data. Proposed integration requirement: merchant/payment infrastructure must provide a recoverable receipt reference and a secure way to retrieve the session after local data loss. A QR meter identifier alone is public and must not expose other drivers’ receipts. The exact guest recovery credential/channel remains unresolved; do not claim eviction recovery is implemented until this contract is designed and tested. No email or account gate is silently introduced to solve it.
- **Full app installed:** Subsequent invocation resolves the same meter; any authorized transferred session context opens that session, without repeated login or redundant onboarding. Public meter context alone conveys no private session access.

Server requirements: idempotent attempt submission; authoritative status lookup; quote validation; expiry and duplicate protection; payment/activation reconciliation and compensation policy. These must run server-side, including when the Clip is no longer running. Do not queue an offline purchase or indicate parking is valid without confirmation.

## Worked before/after

Illustrative fixture only: meter 042, Market Street, 60 minutes, $3 parking + $0.20 fee, $3.20 total; server confirms expiry at 11:15 AM. These are not supplied real tariffs.

**Before, as supplied:** scan QR → onboarding carousel → account creation → meter → required full-app download → payment. The immediate parking task is blocked by identity and installation, especially on a poor network. The brief does not describe the old completion behavior.

**After:** scan QR → task card / Open → “Checking meter 042…” → “Meter 042 · Market Street,” choose 60 minutes, review 11:15 AM expiry and $3.20 → generated Apple Pay action → authorize → confirmed receipt: “Parking active · Meter 042 · Expires today at 11:15 AM · Paid $3.20 · Session P123.” Done is available immediately; installation is optional afterward.

**Poor-network branch:** authorization returns but confirmation is lost → “We haven’t confirmed your parking” → Check status queries the original attempt → server returns session P123 → same receipt. Repeated taps or reopening must not submit a second purchase. If lookup fails before a quote arrives, the flow stops at recoverable lookup error without claiming an offline payment.

## Acceptance checks and current evidence

**Passed — static specification inspection only:** supplied brief read; root → family → topic → source route read for iOS, App Clips, and Apple Pay; before/after explicitly removes all three gates; invocation context, checkout, cancellation, completion, and unknown outcome are specified. Card copy fits supplied length limits. No framework-specific API implementation is claimed.

**Failed — supplied design against the local App Clips procedure:** installation is necessary to finish the task; onboarding and account creation precede the invoked meter. This is a finding about the written brief, not an executed app. No runtime checks have a pass/fail result.

**Not executed — acceptance scenarios for implementation:**

| Scenario | Required observable outcome |
| --- | --- |
| Scan two distinct meter URLs | Each opens its own correct meter; invalid/unknown identifiers never fall through to another meter. |
| First-time guest | Can complete authorized parking without onboarding, account creation, or full-app installation. |
| Poor bandwidth / offline lookup | Essential layout appears without decorative downloads; actionable error; no stale payable tariff or false activation. |
| Duration or tariff changes | Total/end time refresh; changed purchase is reviewed before authorization. |
| Cancel, decline, timeout, repeated tap | Correct remedy, retained choices, no duplicate charge; cancellation reconciliation handles commit races. |
| Authorization succeeds but response is lost | Unknown state blocks a second purchase; status lookup resolves the original attempt. |
| Payment succeeds but activation fails | No active-parking claim; accurate payment/refund/support state. |
| App switch, rotation, enlarged text | Same meter/draft survives; required totals and primary action remain readable/reachable; no alternate navigation hierarchy. |
| Clip data deleted | Secure recovery retrieves only the rightful guest’s session; public meter URL reveals no private receipt. Pending recovery-design dependency. |
| Full app replaces Clip | Invocation opens the correct focused context without redundant login or steps. |
| Completion | Receipt appears only after confirmed activation; Done works without installing; promotion is secondary and post-task. |
| Real device and payment integration | Scan association, cold start, localized generated button, sheet setup/cancel/timeout, server idempotency, touch reach, and assistive-technology order verified independently. |

## Evidence limits

Only `interface.md` and installed local guidance were used. No web browsing occurred. Official links above are source pointers from the installed snapshot, not live verification. Local references identify retrieval as 2026-10-25 and are derivative guidance, not SDK documentation or proof of current API availability.

No device, SDK, GUI, payment sandbox, network simulation, backend, accessibility, print, or physical scan execution occurred. No startup latency measurement is available. Actual invocation configuration, service eligibility, enforcement inputs, tariff rules, guest recovery security, payment fallback, and payment/activation compensation remain implementation dependencies. This artifact specifies behavior; it does not establish runtime conformance. Physical App Clip Code production is outside this existing-QR flow.
