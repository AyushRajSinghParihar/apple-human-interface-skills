# Revised iPhone study entry and consent specification

This is a framework-agnostic design contract, based on `interface.md` and the installed local HIG package. It does not require ResearchKit or another Apple SDK. Proposed behavior below is not evidence of an implemented app.

## Decisions and rationale

| Supplied behavior | Decision | Reason and source |
|---|---|---|
| Prechecked consent beneath a long unreadable paragraph | Remove the checkbox. Present short, navigable consent sections, a complete-form view, and explicit agreement and decline commands. Initial decision is unset. | Agreement is a consequential action, not a persistent preference. HIG recommends understandable consent sections and access to the whole form before agreement: [ResearchKit — informed consent](https://developer.apple.com/design/human-interface-guidelines/researchkit#3-Get-informed-consent); [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons); [Toggles](https://developer.apple.com/design/human-interface-guidelines/toggles). |
| Declining still enrolls | Decline exits without enrollment, device requests, or study-answer collection. Enforce this in the enrollment service as well as navigation. | Proposed product invariant applying meaningful consent and accurate action labels: [ResearchKit — onboarding](https://developer.apple.com/design/human-interface-guidelines/researchkit#Creating-the-onboarding-experience). |
| Movement task has no stop control | Require a visible, immediately effective Stop Task action throughout preparation/countdown/recording. Never confirm before stopping capture. | Product safety decision applying clear active-task conditions/endpoints and accessible commands; HIG does not prescribe this exact stop implementation: [ResearchKit — conducting research](https://developer.apple.com/design/human-interface-guidelines/researchkit#Conducting-research), [Accessibility — mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility). |
| Answers shared publicly by default | Remove public publishing from this flow and deny it in storage/export policy. Approved study recipients must be disclosed before agreement; study consent never implies public sharing. | Conservative product scope applying data minimization and clear use disclosure: [Privacy — best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices). |
| Study approval not supplied | Keep real enrollment and task collection unavailable until study readiness is verified. Permit a clearly marked, noncollecting preview. | Proposed release gate, not a finding that approval was denied. HIG calls for relevant ethics/legal requirements; interface design cannot establish compliance. [ResearchKit — informed consent](https://developer.apple.com/design/human-interface-guidelines/researchkit#3-Get-informed-consent). |

## Study readiness and screen sequence

A versioned study configuration must contain purpose and sponsor/contact, essential eligibility criteria, approved consent text/version, collection and recipient details, risks/benefits, time commitment, retention and withdrawal rules, task conditions/duration/endpoint, and documented applicable study approval/review. An authorized study owner must verify these. Do not fabricate values or infer that review is unnecessary. With supplied evidence, readiness is **unknown**, so the real enrollment gate stays closed.

1. **Study introduction.** Show study name, purpose, responsible organization, participation time and voluntary nature from verified content. Actions: Review Eligibility; Sign In for returning participants; Leave. Returning participants resume only after checking current consent and study status. Until readiness is verified, replace enrollment entry with “Study enrollment is unavailable” and “Preview Study”; preview uses synthetic data and requests no permissions.
2. **Eligibility.** Ask only essential criteria, in plain language, before consent. No inferred eligibility or prefilled affirmative answers. Keep answers transient unless an approved, disclosed retention purpose exists. An ineligible result says “You aren’t eligible for this study” and offers Return to Introduction; it never reaches consent or enrollment. Unknown criteria block real entry.
3. **Consent overview and sections.** Show “About joining this study,” with a short summary and entries for What You’ll Do; Information Collected; How Information Is Used and Who Receives It; Risks; Possible Benefits; Time Commitment; Leaving the Study; Study Contact. Each opens a readable page with Back, Next Section, View Full Consent and Decline Participation. Optional detail expands without hiding the essential explanation. Back preserves reading position, not an agreement. The complete form is available before any agreement action and later from Profile. Reading has no timer; scrolling to the bottom is not treated as proof of understanding.
4. **Consent decision.** Display “Joining is voluntary,” the approved decision statement, View Full Consent, Agree to Participate, and Decline Participation. Both decision buttons have equal target dimensions and remain visible/discoverable in the layout. Use restrained style emphasis; no preselected decision or automatic Return-key agreement. Decline returns to introduction with persistent “You have not joined the study.” No persuasion loop. Agreement enters confirmation, not task recording.
5. **Confirmation and copy.** Show consent version, study name and the decision for review, with Back and Confirm Enrollment. Collect signature and contact only as required by the verified protocol; do not invent a quiz, signature requirement, or mandatory email. Back abandons pending agreement. Show activity within Confirm Enrollment while committing; ignore duplicate activation with an idempotency key. Success alone establishes enrollment. Failure says “Enrollment wasn’t confirmed. Try again.” An unknown network outcome says “Checking enrollment status”; reconcile the same transaction before retrying. Do not claim failure if the server may have committed. Provide an accessible consent copy in Profile and a download; offer approved delivery where available. A delivery failure does not erase a confirmed enrollment and has a retry path.
6. **Task dashboard and Profile.** Dashboard shows upcoming work and honest completion state. Profile is always reachable outside active recording and exposes consent copy, privacy/recipient information, study contact, changing participant details, and Leave Study. Leaving immediately blocks new capture and cancels queued uploads; show withdrawal receipt/status, and explain approved handling of already submitted records. Do not promise deletion where the protocol does not permit it. A withdrawal service failure leaves local collection blocked, clearly marks withdrawal pending, and retries idempotently.

The order follows [ResearchKit — onboarding](https://developer.apple.com/design/human-interface-guidelines/researchkit#Creating-the-onboarding-experience). Exact screen grouping and state guards are product decisions.

## Study-task entry and stopping

**Movement task entry:** heading and verified task description; expected duration; exact movement, physical setting, device placement, risks, stop conditions and endpoint from the approved protocol; what is captured and where it goes. Actions: Start Task, Not Now, View Consent. Start Task is unavailable with an explanation if protocol details, enrollment, consent, readiness, or essential access are missing. Do not invent a safe movement prescription, duration, or clinically equivalent alternative. Not Now returns to dashboard with no penalty or completed-task mark. Any accessible alternative needs study-owner validation for measurement validity.

Request only the task’s actual required device access after enrollment and when Start Task invokes the feature. Do not assume HealthKit, location, microphone, or motion permissions without a concrete data dependency. Use the genuine platform authorization mechanism if required and supported by the eventual stack. Denial leaves collection off and explains which task is unavailable; unrelated permitted tasks remain usable. Avoid a custom pre-permission screen if task context suffices. If essential, it has one Continue action leading to the real prompt, not imitation Allow/Don’t Allow buttons. Ordinary study consent and task-entry screens are distinct from this restricted pre-alert. [Privacy — requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission).

**Preparing/countdown:** no research capture until the explicitly disclosed recording start. Show start state/time and Stop Task. **Recording:** show “Recording,” elapsed/remaining time as appropriate to the verified protocol, current instruction, and Stop Task in a stable location independent of scroll content. No navigation gesture is the sole escape. Visual instructions carry essential information without sound; sound may supplement them.

**Stop Task:** synchronously invalidate the capture session, detach input, cancel timers and block submission before any network call or follow-up question. Show “Task stopped. This attempt wasn’t submitted.” Discard this attempt’s research payload; do not label it complete. Retain only a nonpayload status if disclosed and necessary. Offer Return to Tasks and Review Instructions. A fresh attempt requires Start Task again. Backgrounding, locking, interrupted access, or capture failure uses this same stopped path; never resume recording automatically. If capture cannot be shut down reliably, the implementation fails this contract.

**Normal endpoint:** stop capture automatically at the approved endpoint; show “Recording finished — not submitted” with Submit Task and Discard Attempt. Discard clears the private staged attempt and returns to dashboard. Submit shows an in-button activity indicator and prevents duplicates; only a confirmed server receipt yields “Task submitted” and completion. Failure retains an encrypted private draft only under the disclosed retention policy, with Retry Submission and Discard Attempt. Unknown outcomes reconcile by attempt ID before retry/discard; do not falsely promise erasure of an already accepted submission. No public export occurs.

**Survey entry:** show verified question count and estimated duration before Start Survey. Use one question per screen, suitable answer controls, explicit question progress, Back and Next; disclose required/optional answers. Exit preserves a draft only if disclosed, otherwise discards it. Review precedes Submit Survey; confirmed completion is explicit. This applies the survey guidance in [ResearchKit — conducting research](https://developer.apple.com/design/human-interface-guidelines/researchkit#Conducting-research).

## Data and state contract

| Data | Purpose and access | Default and lifecycle |
|---|---|---|
| Eligibility responses | Resolve approved criteria; no device permission implied | Transient, no research enrollment on decline/ineligibility |
| Consent receipt/signature/contact if required | Record actual agreement, version and required delivery | Restricted recipients; retention must be disclosed and approved |
| Movement samples | Only verified task measurements, permissions only if needed | No collection before explicit start; stopped attempt discarded; successful attempt privately staged |
| Survey answers | Approved study questions | Private; transmit only on explicit submission |
| Public sharing | No requirement supplied | Disabled; no public endpoint or public storage access for participant records |

Retention durations and named recipients are unresolved content inputs, not invented defaults. Block affected collection until resolved. Future public sharing would require a separate reviewed design and specific optional authorization; changing a default is insufficient. No analytics may collect study answers or movement payloads incidentally. Security, privacy disclosures, backups, and withdrawal handling need implementation review.

```text
initial: readiness = UNKNOWN; consent = NONE; enrolled = false
         capture = OFF; publicPublishing = DENIED

canEnroll = verifiedReadiness && eligible && explicitAgreement
            && requiredConfirmationComplete && consentVersionCurrent
confirmEnrollment():
    require canEnroll
    commitEnrollmentOnce(receipt, idempotencyKey)
    enrolled = (confirmed server receipt exists)

decline():
    cancelPendingAgreement(); clearTransientEligibilityAndDrafts()
    consent = DECLINED; enrolled = false; capture = OFF
    // Never call enrollment or task-upload services.

canStart = verifiedReadiness && enrolled && consentVersionCurrent
           && !withdrawn && protocolComplete && requiredAccessGranted
start():
    require canStart && explicitStart
    createFreshAttempt(); showPreparing()
    atDisclosedStart: recheck(canStart); capture = ON

stop(reason):
    invalidateAttemptToken() // Late sensor callbacks are ignored.
    capture = OFF; detachInputs(); cancelTimers(); prohibitUpload(attempt)
    discardAttemptPayload(); showStopped(reason)

submit(attempt):
    require enrolled && !withdrawn && consentVersionCurrent
            && attempt.normalEndpoint && explicitSubmit
    uploadPrivateOnce(attempt.id)
    markCompleteOnlyAfterConfirmedReceipt()
```

Enforce enrollment and upload authorization server-side, including current consent/version, withdrawal and attempt identity. Reject direct or stale client requests. If protocol/consent becomes invalid during capture, stop; require review before a new attempt. The pseudocode is an intended contract, not executable proof.

## Readability and action presentation

Use semantic title, heading, body and action-label roles. Body starts from the iOS 17 pt default, regular weight, with comfortable leading; prefer platform text styles where available or equivalent scaling in the chosen stack. Do not use the 11 pt minimum as the consent target. Support at least 200% text enlargement and all supported iPhone accessibility text settings without clipping, horizontal reading scroll, or losing actions. Grow text containers and wrap/stack buttons; keep the full consent readable. [Typography](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type).

Specify at least 44 × 44 pt activation regions for these iPhone buttons, with separated, nonoverlapping targets. This deliberately adopts the button guide’s general target rather than treating the accessibility table’s 28 × 28 pt minimum as a recommendation. Stop Task remains reachable at enlarged sizes. Use text/state shape as well as color; custom buttons need press feedback, visible focus and accurate pending/disabled states. Names match visible labels; expose button roles and state. Reading order follows heading, content, then actions; screen changes place assistive focus at the heading without trapping navigation. No required action depends on a swipe, speech or timed reaction. [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility).

Use persistent, plain-language status and corrective messages. Approved consent wording still needs study review; these labels do not establish its sufficiency. [Writing](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices).

## Worked before/after

**Before (supplied):** A participant encounters a long unreadable paragraph and an already checked box. They decline but become enrolled. They enter movement recording, cannot stop it, and answers are shared publicly.

**After, with the supplied unknown approval status:** Entry shows enrollment unavailable; Preview Study demonstrates screens with synthetic content. Declining the preview creates no enrollment, recording, answers, or public records.

**After, conditional on verified readiness:** An eligible participant reads short consent sections, opens the full form, then selects Decline Participation. They return to the introduction with “You have not joined the study.” Enrollment count and task uploads remain unchanged. On a separate attempt they explicitly agree, complete required confirmation, receive confirmed enrollment and access their consent copy. They review task duration and conditions, grant only required access, and select Start Task. Halfway through they select Stop Task: capture ends immediately, late callbacks are ignored, no attempt is submitted, and the dashboard shows the task incomplete. They can leave the study from Profile. At every point public publishing remains denied. These are specified outcomes, not observed executions.

## Acceptance checks and current evidence

| Check | Expected result | Status now |
|---|---|---|
| Inspect supplied flow | Identify prechecked consent, false decline, absent stop and public default | Passed: explicitly stated in `interface.md` |
| Evaluate supplied flow against revised consent/stop/privacy contract | No enrollment on decline; accessible stop; no public default | Failed: supplied behavior contradicts these requirements; no runtime inspected |
| Inspect this specification | Eligibility precedes consent; full form before agreement; permissions follow consent; task completion and withdrawal defined | Passed: document-level inspection only |
| Missing readiness inputs | Real enrollment/start APIs and UI remain blocked; preview collects nothing | Not executed; intended gate specified |
| Decline, back, close, interruption and direct API calls | No consent inferred; decline never enrolls or uploads | Not executed |
| Consent transaction double press/network timeout/relaunch | One receipt; reconcile unknown outcome; no premature enrollment | Not executed |
| Start without consent, with stale consent, denial or withdrawal | No capture or upload; understandable recovery | Not executed |
| Stop during countdown/recording; sensor callback after stop; app background/lock | Immediate capture invalidation; no upload; incomplete status; no auto-resume | Not executed |
| Normal finish, duplicate submit, offline/unknown receipt | Capture ends; private staging; one confirmed submission; truthful status | Not executed |
| Public access and export inspection | Anonymous/unauthorized reads denied; no public publishing of answers | Not executed; requires service/storage/security evidence |
| Withdrawal during pending upload | Local capture blocked; queued upload canceled; server receipt/status and prior-data policy truthful | Not executed |
| Consent copy and Profile navigation | Copy, privacy, upcoming tasks and withdrawal reachable; delivery failure recoverable | Not executed |
| iPhone text scaling and input access | Complete path at 200% and largest supported sizes/Bold Text; readable labels, nonoverlapping ≥44 pt targets; Stop reachable | Not executed; needs rendered geometry and supported environment |
| Contrast and nonvisual operation | Measure actual light/dark/Increase Contrast combinations; no color/sound-only meaning; all actions named, reachable and activatable | Not executed; no palette, rendering or assistive runtime supplied |

Runtime acceptance must exercise the same entry-to-completion/decline/stop paths with VoiceOver, Switch Control and Full Keyboard Access on supported Apple environments. Contrast measurements and physical reach/comfort also remain outstanding. A written semantic order does not prove spoken order.

## Evidence limits and route audit

Only `interface.md` and installed instructions/references were used; no web access occurred. Official links above identify the sources described by the local snapshot, not live verification. The installed references describe themselves as application guidance derived from HIG, with retrieval/snapshot date 2026-10-25; their existence does not establish independent source review.

Read the installed root `.agents/skills/apple-hig/SKILL.md`, searched `references/topic-index.md`, then read owning family routes before topic procedures and source guides: Technologies → ResearchKit; Foundations → Privacy, Accessibility, Typography and Writing; Menus and Actions → Buttons; Selection and Input → Toggles. ResearchKit was selected for its study-participation trigger, not an assumed SDK dependency. Each instruction/reference read used a separate single-file command.

No screenshots, implementation, study protocol, approval record, SDK, device, GUI, accessibility runtime, security audit, measurement-validity study or consent comprehension evidence was supplied or executed. No legal/ethical approval or clinical safety is claimed. The readiness gate is a conservative design decision under missing evidence; it does not assert that the study lacks approval. Verified study content and actual implementation validation remain prerequisites for deployment.
