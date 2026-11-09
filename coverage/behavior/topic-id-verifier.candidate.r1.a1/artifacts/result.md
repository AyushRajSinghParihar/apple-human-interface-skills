# Revised event-entrance age verification

This is a framework-agnostic interaction specification for a staff-operated iPhone. The supplied `interface.md` is a brief, not an implementation. It explicitly proposes indefinite identity-image storage, unnecessary staff-visible address/birth details, and approval before a response. Replace all three behaviors.

## Decisions and source basis

1. **Verify the minimum fact:** request “meets event age threshold T,” not date of birth, current age, address, or a full identity image. T comes from the event’s approved policy, is visible to staff, and cannot change during an attempt. No threshold was supplied; examples below assume 21 only for illustration. [ID Verifier — Best practices](https://developer.apple.com/design/human-interface-guidelines/id-verifier#Best-practices).
2. **Choose Display Only as the intended integration mode.** The local guide describes iPhone mobile-ID verification from iOS 17, but this does not establish support on the deployment device. Display Only presents identity data/photo exclusively in system UI; the app must not assume it receives attributes or a portrait. Staff record a visual outcome through the supported requester interaction. Data Transfer is excluded: no legal need to store/process identity details was supplied, and the guide identifies an additional entitlement requirement. [ID Verifier](https://developer.apple.com/design/human-interface-guidelines/id-verifier).
3. **Gate digital verification on proven capability.** Before enabling it, an adapter must establish supported hardware/OS, compatible credentials, required authorization/entitlements, and organizational eligibility. Unknown is unavailable. Eligible organizations should register for the verified business name/logo described by the guide; never invent a verification badge. Default to an event-approved alternative ID check until prerequisites are confirmed. These are release dependencies, not claims of available APIs.
4. **No identity retention in this design.** Do not capture, upload, cache, export, or log identity images, address, birth details, or raw provider payloads. Retain only transient attempt state and staff observation until the attempt is cleared; no person-linked verification history or analytics. This retention policy is a product decision applying minimization, not a HIG-mandated retention duration. Provider/system handling must be separately established before making an attendee-facing retention promise. Update applicable privacy disclosures before release. [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices).
5. **Pending never means approved.** Show a waiting state until the supported verification interaction completes. A declined request, failed check, unmet threshold, and portrait nonmatch are distinct outcomes. Neither a tap nor successful ID reading authorizes entry. Staff confirmation is explicitly a human observation, not an automated identity verdict.
6. **Use direct commands:** “Verify Age,” without Apple-logo, NFC, or QR artwork. Prefer familiar system controls where available; custom equivalents need semantic states and press feedback. Use at least 44 × 44 pt hit regions, separated so targets do not overlap, and one prominent likely action per screen. The accessibility source also lists a smaller minimum; this specification conservatively uses the buttons guide’s 44 pt general target. [Buttons — Best practices and iOS](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices).

## Screen and action contract

Use one task view with the event name and “Required age: T+” at the top, current status in the center, and frequent actions toward the middle/lower display. Result and next action remain adjacent. Portrait and landscape share the same state and hierarchy; enlarged content can scroll without hiding necessary actions. Preserve normal system Back navigation. [Designing for iOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices).

| State | Visible content and actions | Transition contract |
|---|---|---|
| Capability unknown/unavailable | “Digital age verification unavailable. Use the event’s alternative ID check.” “Use Alternative Check” | No digital launch or simulated success. Alternative opens concise venue instructions; it does not mark digital verification passed. |
| Ready | “Verify age T+ for this event.” “Ask the attendee if they want to use a supported mobile ID. An alternative ID check is available.” Primary “Verify Age”; secondary “Use Alternative Check” | Verify creates one fresh attempt and launches the supported system interaction. No custom imitation of the system consent screen. |
| Starting / awaiting | “Waiting for verification. Age has not been confirmed.” Initiating button becomes “Verifying…” with an in-button activity indicator; duplicate activation disabled. “Cancel Verification” available in app-owned UI when accessible | System owns attendee presentation/consent and sensitive display. While its UI is foregrounded, use its supported cancellation behavior. No app approval controls overlaid on system UI. |
| Staff observation | System-owned age/portrait display and supported requester outcome choices; where app-owned controls are required, label “Age requirement met and portrait matches,” “Requirement not met or portrait does not match,” and “Unable to Determine” | Positive choice requires staff to have observed both the threshold result and portrait match for the same completed interaction. No default/Return shortcut chooses a positive outcome. If system does not expose the needed supported outcome workflow, digital flow remains unavailable. |
| Age check complete | “Staff confirmed age requirement and portrait match. Continue the event’s other entry checks.” “Next Attendee” | Explicit staff confirmation only. This result is not ticket validation or permission to bypass other entrance policy. Result persists until cleared. |
| Requirement not met / nonmatch | “Age check not passed. Follow the event’s entry policy.” “Use Alternative Check”; “Next Attendee” | Do not accuse the attendee of fraud or reveal extra identity details. A negative threshold result is not a technical error to retry automatically. |
| Attendee declined / canceled | “Verification not completed. An alternative ID check is available.” “Use Alternative Check”; “Verify Age”; “Next Attendee” | No adverse age inference. Retry only after a fresh voluntary initiation. |
| Technical failure / timeout | “Couldn’t complete verification. Age has not been confirmed.” “Try Again”; “Use Alternative Check”; “Next Attendee” | Retry creates a new attempt. Surface only a safe actionable reason when known; never raw identity payloads. |
| Alternative check | “Follow the event’s approved alternative ID procedure. Digital verification has not been completed.” “Back to Age Check”; “Next Attendee” | This specification does not invent a manual policy, record a manual pass, or capture a document. Venue must supply approved instructions before operation. |

“Next Attendee” clears transient state and returns to Ready or Unavailable after rechecking capability. It is a normal completion/reset action, not Cancel. Retry supersedes prior attempts. Cancel, Back, reset, lock/background interruption, or loss of the current verification context invalidates a pending attempt; on return show “Verification interrupted. Start again or use an alternative check.” Preserve event and threshold, but do not restore sensitive identity display or an old positive result. This conservative interruption rule is a product decision to prevent one attendee’s result being applied to the next.

## Adapter and state rules

The following are conceptual events, not Apple SDK methods or promised Display Only return fields:

```text
start():
  require capability == confirmed_supported and state permits start
  clear prior transient outcome
  activeAttempt = new opaque token
  freeze event and threshold for this attempt
  state = awaiting
  adapter.beginDisplayOnlyThresholdCheck(activeAttempt, threshold)

onEvent(token, event):
  ignore unless token == activeAttempt and attempt is still live
  if event is declined, canceled, failure, or timeout:
    close attempt; show corresponding non-success state
  if event is completed_supported_visual_workflow:
    state = awaiting_staff_observation   // not approved
  if event is staff_observation:
    require supported completed visual workflow for this attempt
    if observation explicitly confirms threshold AND portrait match:
      state = staff_confirmed_age_check
    else if observation is negative:
      state = not_passed
    else:
      state = not_completed
    close attempt

cancel_or_interrupt_or_reset():
  invalidate activeAttempt BEFORE requesting adapter cancellation
  clear sensitive/transient observation state
  ignore all subsequent callbacks for the invalidated token
```

The adapter may map system-owned requester choices into conceptual observations only if the real integration supports it. Do not synthesize an age boolean or portrait from Display Only. If completion and observation are delivered together by the supported interaction, validate them atomically. No arbitrary app timeout duration is prescribed: use documented integration limits, and treat expiry as incomplete. No automatic retries. No gate-opening side effect is defined by this specification.

## Worked before → after

**Before (from the brief):** At a 21+ event, staff initiate verification; the proposal displays approval before the response. It also exposes address/birth details and retains a full identity image forever. If the attendee declines, staff may already have acted on the premature approval.

**After (illustrative sequence):** Staff see “Required age: 21+” and select “Verify Age.” The app shows “Waiting for verification. Age has not been confirmed.” The attendee declines in the supported interaction. The app shows “Verification not completed” and offers the alternative check; it never shows a positive result or stores identity imagery. On a separate voluntary attempt, the system displays the threshold and portrait to staff. After staff explicitly confirm both, the app shows “Staff confirmed age requirement and portrait match,” then staff continue other entrance checks. “Next Attendee” clears the result. A late completion from the declined attempt cannot change the new attendee’s state.

## Acceptance checks and evidence status

**Passed — document inspection only:** The revised contract uses a threshold rather than birth/address details; distinguishes Display Only from Data Transfer; removes indefinite image storage; gates unavailable capability; separates waiting, refusal, failure, negative and staff-confirmed results; includes an alternative path and stale-response protection. These are specification properties, not executed behavior.

**Failed — supplied proposal, as explicitly described:** Minimization/retention expectations, necessary-only staff disclosure, and truthful result timing. Capability is unconfirmed, rather than proven unsupported. The brief provides no evidence about existing button geometry, accessibility, or actual system integration; no defects are inferred for those.

**Not executed — implementation acceptance scenarios:**

| Check | Required observable result |
|---|---|
| Unknown capability, unsupported device, missing eligibility, incompatible ID | Digital start unavailable; approved alternative remains reachable. No unsupported API assumption. |
| Double tap Verify; delayed response | Exactly one active attempt; visible waiting indication; no positive outcome before completion and explicit staff observation. |
| Positive threshold with no observation; portrait nonmatch; negative threshold | No positive result for any of these cases. Unable to determine remains incomplete. |
| Decline, cancel, technical failure, timeout | Distinct neutral/incomplete or failure states with specified recovery; no inferred underage result. |
| Retry, Next Attendee, Back or interruption followed by stale/duplicate callbacks | Old callbacks cannot overwrite state; no old positive result reappears. Event/threshold survive interruption; pending verification must restart. |
| Data inspection including logs, crash reports, caches, network and backend | No app-held identity image/address/birth data or raw identity payload; no person-linked result history. Confirm provider handling separately. |
| Portrait/landscape, at least 200% text, light/dark and Increase Contrast | Essential text and actions remain readable, reachable and unclipped; content reflows; contrast is measured on actual colors. |
| Touch geometry and repeated use | At least 44 × 44 pt nonoverlapping targets; custom press feedback; comfortable repeated activation tested on iPhone. |
| Assistive input and feedback | Controls expose names/roles/enabled states; status is available without color or sound; complete flow operable with relevant VoiceOver, Switch Control, Full Keyboard Access and AssistiveTouch paths. No positive outcome selected merely by default activation. |
| Result persistence and alternative check | Result does not disappear on a timer; Next Attendee clears it; alternative procedure is usable without digital consent. |

The accessibility criteria apply [Accessibility — Vision, Mobility and Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility). They are requirements for future evaluation, not claims that assistive technology ran. Staff requiring an alternative to visual portrait inspection need an approved equivalent operating procedure; do not claim that accessible app controls alone make the identity inspection accessible.

## Evidence limits and local audit route

Only supplied local files and installed guidance were used; no web requests were made. Official links identify the source articles recorded in the local snapshot, not independently checked current web content. Installed references are dated 2026-10-25; ID Verifier records a September 12, 2023 source revision. HIG is design guidance, not API documentation or certification of legal compliance.

Explicit read order, rooted at `.agents/skills/apple-hig/`: root `SKILL.md`; supplied `interface.md`; relevant rows of `references/topic-index.md`; Getting started family → Designing for iOS topic → its reference; Technologies family → ID Verifier topic → its reference; Foundations family → Privacy topic → its reference; Menus and actions family → Buttons topic → its reference; Accessibility topic in the already-read Foundations family → its reference. Each file was consumed with its own `cat` or `rg` command before applying its guidance.

No implementation, SDK documentation, entitlement, certificate, registered organization, real mobile ID, device, screenshot, GUI, network service or accessibility execution was available or tested. Release remains dependent on current capability/eligibility validation, the supported system outcome contract, approved threshold and alternative-entry policy, actual privacy/security review, and device/accessibility acceptance checks. This document does not establish statutory age-verification sufficiency or a legal basis for Data Transfer.
