# Revised entrance age-verification interaction

## Scope and decisions

The supplied `interface.md` proposes indefinite identity-image storage, unnecessary address/birth details for staff, and approval before a response. It also says iOS verification support is unconfirmed and verification can be declined or fail. This specification replaces those behaviors; no implementation or SDK is assumed.

Assume a staff-operated iPhone at the entrance. The event configures its required age threshold `T` before the queue opens; staff cannot change it per attendee. Example below uses 18 only as an illustration, not a legal age recommendation. Age verification establishes one entrance condition; tickets and other admission decisions remain separate.

1. **Minimum request:** ask whether the attendee meets `T`, rather than requesting birth date, current age, address, or full identity images. Choose **Display Only** for visual verification; the supplied purpose gives no need to store/process identity details. Data Transfer is excluded unless a separately established legal need and additional entitlement justify a new specification. Display Only details/photo belong solely to system UI; the app must not expect to receive them. These distinctions come from [ID Verifier, Best practices and mode descriptions](https://developer.apple.com/design/human-interface-guidelines/id-verifier#Best-practices).
2. **Capability gate:** treat ID Verifier as a conditional integration. The local guide describes iOS 17+ iPhone reading compatible ISO 18013-5 mobile IDs; that is not proof this installation, organization, credential, or device is eligible. Before enabling the digital action, an integration must confirm supported hardware/software, credentials/certificates, eligibility and entitlements, and a compatible verification method. Unknown or unavailable capability opens the manual route. Eligible organizations should register to display their verified business identity; do not invent a verified badge. [ID Verifier](https://developer.apple.com/design/human-interface-guidelines/id-verifier)
3. **Truthful outcomes:** initiating, reading, and waiting never mean approved. A completed system interaction and a staff visual decision are separate facts. No app-side automated portrait-match claim is made.
4. **No retained identity record:** remove indefinite storage. Do not capture, upload, cache, log, or put identity images, address, birth date, age, or system-view contents into analytics/crash reports. Keep only an opaque attempt identifier and transient workflow state while this attendee is being checked; clear them on completion/reset, backgrounding, or abandonment. No persistent per-attendee result history is required by this brief. This retention rule is a product decision applying [Privacy, Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices), not an Apple-defined retention period. If a deployed predecessor has stored images, stopping collection does not delete them: inventory and execute an authorized deletion/migration separately; do not claim it happened here.

## Screen and action contract

Use a single brief-check screen: event name and “Age requirement: T+” above the current status, with frequent actions in the middle/lower reachable area. Keep the same task hierarchy in portrait and landscape; allow vertical scrolling/reflow at enlarged text sizes. No custom swipe-back gesture. These choices apply [Designing for iOS, Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices).

Ready copy: “Check whether this guest meets the T+ age requirement. Identity details are shown only in the verification interface and are not saved by this app.” Show this as ordinary task context, not a fake permission alert. The actual supported system interaction owns disclosure/consent; do not request unrelated camera, photo-library, location, or tracking access. [Privacy, Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission)

| Control | Availability and outcome | Role and placement |
| --- | --- | --- |
| Verify Age | Ready and confirmed capability only; starts one minimal Display Only attempt | Primary, prominent lower-body button; no Apple logo, NFC glyph, or QR artwork |
| Use Manual Check | Ready, unavailable, declined, failed, or inconclusive; abandons digital attempt and opens manual instructions | Secondary normal action |
| Cancel Check | App-owned waiting state; invalidates attempt and returns to ready; system UI uses its supported cancellation controls | Cancel role; never means verification completed |
| Confirm Age and Match | Only after successful system presentation, where supported outcome reporting permits staff confirmation; records that staff observed both threshold met and portrait match | Explicit deliberate action; no automatic Return/default commitment |
| Does Not Match | Same visual-review context; records a human nonmatch, never an automated mismatch | Normal action, equal target size to confirmation |
| Cannot Confirm | Review context; records inconclusive, with manual route | Normal action |
| Finish Manual Check | Manual instructions; completes that workflow without creating a digital-verification success | Normal action; result explicitly labeled manual |
| Next Guest | Terminal result only; clears current result and starts a fresh ready/capability check | Primary; never starts verification automatically |

Use text labels as control names. Prefer available system button behavior, but framework-independent controls must specify pressed feedback, focus, and disabled states. Hit regions are at least 44 × 44 pt with nonoverlapping separation; this is a design requirement, not a measured result. While waiting in app UI, the initiating button shows an activity indicator and “Checking…” and rejects repeat activation; a nearby status explains “Waiting for verification. Age is not yet confirmed.” System-owned UI is not overlaid or restyled. [Buttons, Best practices, Style, and iOS](https://developer.apple.com/design/human-interface-guidelines/buttons)

## State and integration contract

An adapter may open supported system UI and signal lifecycle completion/cancel/failure. It must document what is actually observable. Display Only does **not** imply an app-readable threshold, portrait, or identity-data payload. Staff review occurs in the supported system flow; map supported requester outcome actions to the semantic events below. If that mapping cannot be established, disable the digital path rather than fabricating a success callback or copying data into custom UI.

| State | Display and allowed transition |
| --- | --- |
| Capability unknown/unavailable | “Digital age check unavailable. Use the event’s manual check.” No digital approval action. Manual or re-evaluate capability. |
| Ready | Requirement and explanation; Verify Age or Use Manual Check. |
| Pending | Checking status; no result or admission cue. Completion enters visual review only when the adapter confirms presentation is complete. Cancel/decline/failure take distinct paths below. |
| Visual review | System-owned minimal identity presentation; staff compares portrait to the person and checks the threshold outcome. Do not re-render details in app UI. Threshold not met → requirement-not-met. Threshold met plus explicit staff match → age-confirmed. Nonmatch → mismatch. Missing/uncertain evidence → inconclusive. |
| Age-confirmed | “Age requirement met — staff confirmed portrait match.” This is not “Admission approved.” Next Guest. |
| Requirement-not-met | “Age requirement not met.” Do not offer a bypass that turns this into digital success. Next Guest or follow event supervisor policy outside this digital result. |
| Mismatch | “Portrait does not match — age check not confirmed.” Manual route or Next Guest. |
| Declined/canceled | “Digital check not completed.” No implication of underage status. Retry by explicit action, manual route, or Next Guest. |
| Failed/inconclusive | “Couldn’t confirm age.” Brief actionable reason if known, without identity details; Retry, manual route, or Next Guest. A configured adapter timeout is failure/inconclusive, never approval. |
| Manual | “Check accepted physical ID using the event’s approved staff procedure. Do not photograph or enter identity details.” Completion says “Manual check completed,” with no claim of digital verification. The venue must supply the approved procedure before operational use. |

Framework-agnostic invariants:

```text
start(): require ready && capabilityConfirmed
         attempt = newOpaqueToken(); state = pending
         openDisplayOnlyRequest(threshold=T, token=attempt)

handle(event, token):
  ignore if token != activeAttempt or attempt invalidated
  accept only events legal for current state
  presentationCompleted -> visualReview       // never approval
  staffConfirmed -> ageConfirmed ONLY IF supported review establishes
                    thresholdMet AND explicit human portraitMatch
  thresholdNotMet -> requirementNotMet
  staffNonmatch -> mismatch
  cancel/decline/error/timeout -> corresponding non-success state

cancel/background/manual/reset():
  invalidate activeAttempt before dismissing/canceling integration
  clear transient result and review eligibility
  on resume show "Check interrupted — start again"; require a fresh attempt
```

Do not persist review eligibility across app switching or locking. Late callbacks from abandoned attempts cannot change the next guest’s screen. Orientation/text-size changes while active preserve the attempt and state without launching another request. These interruption rules deliberately prioritize avoiding a stale attendee result; they are product decisions, not claimed system API behavior.

## Worked before/after

**Before (from the brief):** Staff starts verification for an event guest. The app shows approval while the response is pending. It exposes address/birth details and retains full identity images forever. A later decline or failure can leave staff acting on premature approval.

**After (18+ example):** Ready shows “Age requirement: 18+” and Verify Age. Staff taps once; Pending says age is not yet confirmed. A supported Display Only interaction requests the age-threshold fact and provides its system visual check. Staff sees that the threshold is met and compares the portrait in system UI, then explicitly confirms both using the supported outcome action. Only then does the app say “Age requirement met — staff confirmed portrait match.” No identity image/address/birth date enters app storage. Next Guest clears the result. If the guest declines instead, the screen says “Digital check not completed” and offers the manual route; it never labels that guest underage or approved.

## Acceptance checks and audit status

**Passed — document inspection only:** The revised contract requests a threshold, chooses Display Only, separates system completion from human observation, forbids premature success, covers decline/failure/nonmatch/manual recovery, and contains no SDK dependency. Root skill, topic-index search, selected families, topic procedures, and source guides were read locally in that order per route, with one file per read command. Routes: Getting started → Designing for iOS; Technologies → ID Verifier; Foundations → Privacy; Menus and actions → Buttons.

**Failed — supplied proposal as written:** Minimization (unnecessary address/birth details), retention (images forever), and result timing (approval before response). These are findings about `interface.md`, not observed runtime defects. No executed runtime test failed because none was run.

**Not executed — implementation acceptance scenarios:**

- With capability unknown, unsupported, or unavailable, Verify Age cannot launch; the manual route remains usable. Confirm eligibility/certificates/entitlements and real credential interoperability separately.
- Hold the response pending, double-tap, then simulate failure: exactly one attempt, no success text, and an actionable non-success result.
- Complete presentation without a staff decision: no age-confirmed state. Test threshold false, human nonmatch, and uncertain evidence independently; none produces digital success. Confirm system outcome mapping with the real integration.
- Decline or cancel, then deliver a late success callback: no approval. Repeat after Next Guest, manual handoff, lock/background, and fresh attempt; old callbacks never affect the current guest.
- Confirm a valid threshold and explicit match: only this path yields age-confirmed. It does not approve admission. Next Guest removes the result and review eligibility.
- Inspect requests, app storage, caches, logs, network traffic, analytics, and crash reporting: no prohibited identity data or persistent per-attendee record. Validate consent behavior and disclosure accuracy against the eventual integration.
- On iPhone, check portrait/landscape, enlarged text, Dark Mode, interruptions, reachability, actual 44 × 44 pt hit regions, control separation, press/wait feedback, names/focus/default activation, and system cancellation. Labels must remain readable and actions reachable without losing the active task. Device and assistive-technology checks require execution; this document proves none of them.

## Evidence limits

Only `interface.md` and installed local instructions/guides informed this specification. Official links above identify source sections; they were not fetched. The installed guides are derivative snapshots dated 2026-10-25; the ID Verifier reference records a 2023-09-12 source revision. They describe design expectations, not verified current API contracts. No device, SDK, GUI, accessibility, security, entitlement, certificate, credential, or legal-compliance execution occurred. No screens or implementation were supplied, so geometry, rendering and behavior remain unverified. The event’s threshold, manual policy, organizational eligibility, supported deployment devices and actual adapter outcome semantics remain operational prerequisites. HIG cannot establish legal necessity or authorize retention.
