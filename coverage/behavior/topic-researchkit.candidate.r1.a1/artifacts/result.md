# Consent and study-task entry: revised interaction specification

## Scope and release decision

Target: iPhone/iOS. This specification is framework agnostic; it requires no Apple SDK.

The supplied interface.md describes prechecked consent beneath an unreadable paragraph, enrollment despite declining, a movement task without a stop control, public sharing of answers by default, and no supplied study approval. These are description-level findings; no UI, code, measurements, or approved protocol were supplied.

Live enrollment and research collection must remain unavailable until the study owner supplies and verifies the applicable approval, eligibility criteria, versioned consent, confirmation requirements, data policy, investigator contact, and movement protocol. This is a proposed product safeguard given the missing evidence, not a claim that approval was denied or that Apple has adjudicated the study. Show “Study enrollment is not available yet” with “Study Information” and “Done.” Design previews may use sample content without collecting participant data.

Required content slots below must be filled from reviewed study material before release: [purpose], [eligibility], [activities], [time], [risks], [benefits], [data categories], [authorized recipients and uses], [retention and deletion limits], [withdrawal consequences], [investigator contact], [movement instructions, conditions, duration and endpoint], and [partial-data policy]. Never expose unresolved placeholders to participants. Interface structure cannot establish ethical or legal consent sufficiency.

## Decisions and evidence

Official links identify articles represented in the installed local snapshots; they were not opened online.

| Decision | Source basis and qualification |
|---|---|
| Introduction → eligibility → consent → necessary confirmation → relevant permissions → tasks | [ResearchKit: onboarding](https://developer.apple.com/design/human-interface-guidelines/researchkit#Creating-the-onboarding-experience). Apply the study-flow guidance without requiring ResearchKit. |
| Replace the prechecked checkbox with deliberate agreement and decline commands | Product correction for the supplied behavior. [Toggles](https://developer.apple.com/design/human-interface-guidelines/toggles#Best-practices) distinguishes persistent state from commands; [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Role) informs action roles. |
| Short consent sections with optional depth and complete-form access before agreement | [ResearchKit: informed consent](https://developer.apple.com/design/human-interface-guidelines/researchkit#3-Get-informed-consent). Reading progress is not proof of understanding. |
| Preview movement, then explicitly start; make completion unambiguous | [ResearchKit: conducting research](https://developer.apple.com/design/human-interface-guidelines/researchkit#Conducting-research). Immediate stop and interruption behavior below are proposed safeguards, not quoted Apple mandates. |
| Remove public answer sharing from this version; restrict research access to disclosed recipients | Product privacy choice informed by [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices). Private does not mean anonymous. Any future public sharing needs separate review and explicit, unbundled agreement. |
| Plain language, scalable text, labeled controls and alternative input | [Writing](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices), [Typography](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type), and [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility). Runtime support remains unverified. |

## Screen and action contract

Use full-screen sequential views. Back preserves reading position but never creates agreement. Exiting before acknowledged enrollment leaves the person unenrolled. Reading has no time limit. No scroll-to-bottom requirement or timer is treated as evidence of consent.

All actions have visible text, matching accessible names and button roles, press feedback, and nonoverlapping activation regions of at least 44 × 44 pt. This uses the Buttons guide's general recommendation and the Accessibility guide's iOS default; its smaller minimum is not the chosen design target. Related actions have equal target sizes, with emphasis conveyed through style.

1. **Introduction.** Show [study name], [purpose], [responsible institution], activities and time. “Check Eligibility” begins essential screening; “Sign In” resumes an existing participant after status verification; “Not Now” exits. Explain screening-data use before collecting it and avoid unnecessary identifiers.
2. **Eligibility.** Ask only approved essential criteria in plain language before consent. An ineligible outcome explains that participation is unavailable and offers “Done.” It creates no enrollment. Screening retention follows the approved policy rather than an invented deletion promise.
3. **Consent sections.** Heading: “Decide whether to participate.” State “Taking part is your choice. You can decline.” Sections: Study activities; Data collected; Who can use the data and why; Risks; Possible benefits; Time commitment; Leaving the study; Questions and contact. Show short approved summaries, “Read More,” Back and Next. Risks and withdrawal essentials remain in the main summaries. “View Full Consent” exposes the complete versioned form before agreement and returns to the prior reading position.
4. **Decision.** Show recap, consent version, “View Full Consent,” “Agree to Participate,” and “Decline Participation.” Neither decision is preselected or automatically triggered by Return or entry. Both remain plainly visible. Agreement opens only the protocol-required confirmation/signature/contact steps; do not invent a quiz or mandatory email address. Decline exits immediately to “You have not joined the study,” with “Done” and “Review Study.” It creates no enrollment request, task, or research upload.
5. **Enrollment result.** Only durable acknowledgment of consent and required confirmation establishes enrollment. During submission, show “Saving Consent…” and an activity indication within the initiating button; suppress duplicate submissions using a stable operation identifier. A timeout remains unresolved until that operation's status is checked; do not blindly retry and duplicate enrollment. A confirmed failure says “Consent could not be saved. You have not joined the study,” with “Try Again” and “Leave.” Success says “You have joined the study,” exposes the matching consent copy in the approved format, and offers “View Study Tasks.” Email a copy only through an approved, disclosed contact mechanism.
6. **Movement preview.** Show the specific action, timing, endpoint, environment/device placement, approved safety instructions, data collected, and partial-data policy. “Start Task” begins only after the required gates pass; “Not Now” returns to tasks without penalty. Request only necessary device access at the feature's moment of use, after consent. No sensor category is assumed from the word movement. Denial keeps capture off, explains the dependency, and allows return to tasks; unrelated work remains usable. If an essential custom pre-permission explanation is used, follow the Privacy guide's special single-continuation rules without imitating the system permission choice.
7. **Running movement.** Keep current instruction, text progress/remaining time, and “Stop Task” visible in a stable reachable location. Stop requires one ordinary activation, no speech or complex gesture. It immediately closes capture before any result screen or confirmation. Then show “Task stopped,” the approved partial-data outcome, “Back to Tasks,” and “Review Task Instructions.” A retry begins at the preview. Backgrounding, interruption, access loss, consent invalidation, or capture error also stops; return never automatically resumes. The normal endpoint closes capture before “Task complete,” with truthful saving/saved/failed status. A stopped run is never complete.
8. **Profile and study information.** Accessible from the task list: participation status, upcoming tasks, consent copy, privacy/data policy, investigator contact, and “Leave Study.” Leaving immediately stops local collection and blocks new tasks; report withdrawal as pending until acknowledged remotely. Explain existing-data retention limits before participation and here. Withdrawal is not a promise to erase data already used. Do not invent a deletion mechanism without the policy.

## Data and state contract

| Data | Purpose and recipients | Gate and lifecycle |
|---|---|---|
| Eligibility responses | Essential screening only | Explain before entry; approved screening retention; no public access |
| Consent record and necessary contact | Document consent version and deliver copy | Deliberate agreement and required confirmation; minimum identifiers; restricted access |
| Answers and movement measurements | Approved study analysis by disclosed authorized recipients | Acknowledged enrollment, current consent, necessary permissions and explicit task start |
| Unfinished task data | Only protocol-defined use | Keep out of analysis/upload until the approved partial-data policy permits it; discard transient buffers if required |
| Public sharing | No purpose supplied | Disabled; no public endpoint, feed, inherited public flag, or publication job |

Enforce gates in the data service as well as the interface. Keep answers and sensor payloads out of general analytics/logs. Actual access control, encryption, retention enforcement and privacy disclosures require implementation review.

Framework-neutral transition rules:

    initial:
        participation = NOT_ENROLLED
        task = IDLE
        publicSharing = false
    liveReady = verifiedApproval AND completeApprovedProtocol AND completeApprovedConsent

    AgreeToParticipate:
        require liveReady AND eligible AND explicitUserActivation
        open required confirmation steps; capture remains off
    RequiredConfirmationComplete:
        submit versioned consent with stable operationId
        participation = SAVING
    SaveAcknowledged:
        participation = ENROLLED
        expose consent copy and tasks
    DeclineParticipation:
        require participation is not ENROLLED
        clear consent draft; participation = NOT_ENROLLED
        exit; do not call enrollment or research collection services
    StartTask:
        require liveReady AND participation == ENROLLED AND currentConsentValid
        require protocolComplete AND necessaryPermissionsGranted
        create fresh runId; task = RUNNING; open approved capture gate
    Stop / Interrupt / AccessLost / ConsentInvalid / CaptureError:
        synchronously close capture gate and invalidate run token
        reject late samples; cancel unfinished upload work
        task = STOPPED; apply approved partialDataPolicy
    NormalEndpoint:
        close capture gate; task = COMPLETE
        save once using runId; expose actual save result
    LeaveStudy:
        close capture gate; block new tasks
        participation = WITHDRAWAL_PENDING
        submit idempotent withdrawal; show actual acknowledgment state

Server-side status/version checks reject stale starts and unauthorized writes. Offline withdrawal still blocks local capture. Already received data follows the disclosed server policy; do not claim it can be recalled. Returning participants never restore a RUNNING task from stored UI state. Consent revisions requiring renewed agreement block new tasks until the approved renewal flow completes.

## Worked before/after

**Before, from the brief:** A person encounters unreadable consent with a checked box. They decline but are enrolled anyway. They enter movement without a stop control, and collected answers are publicly shared by default.

**After, proposed decline path:** Once release prerequisites are verified, an eligible person opens Risks, views the complete form, returns, and chooses “Decline Participation.” The result says “You have not joined the study.” Enrollment remains absent, task start is unavailable, and no movement collection or public sharing occurs.

**After, proposed participation path:** On a separate visit, the person deliberately agrees, completes required confirmation, and receives acknowledged enrollment plus a consent copy. They review movement instructions and duration, grant only required access, and choose “Start Task.” Midway, “Stop Task” closes capture before the result appears. The run reads “Task stopped.” Partial data follows the disclosed policy, no public publication is created, and a retry begins at the preview. These are specified traces, not executed participant tests. With the currently supplied evidence, live participation remains gated.

## Reading and alternative interaction

Use semantic title, heading, body and action-label roles. The local iOS guidance gives a 17 pt default body size; adopt that default with regular weight and comfortable leading, using scalable equivalents if native styles are unavailable. Support text preferences or equivalent resizing, at least 200% enlargement and supported iPhone accessibility sizes. Grow containers, wrap labels, stack actions vertically and let reading scroll without covering decisions or Stop Task. Do not shrink or truncate essential text.

Reading/activation order follows heading → content → detail link → navigation/decision actions. Saving, stopped, complete and error states must be available as text and accessible status, not color or sound alone. No countdown starts while instructions are being read. Movement remains a protocol constraint: offer an approved alternative or allow leaving; do not claim a substituted movement produces equivalent measurements. Test actual light/dark and Increase Contrast colors with a contrast calculator before claiming sufficiency.

## Acceptance checks and evidence limits

**Passed — static specification review:** The document supplies explicit decline, full-form access, separated enrollment and capture gates, immediate stop/interruption transitions, restricted sharing, and approval/content prerequisites. This establishes specification coverage only.

**Failed — supplied design description:** Preselected unreadable consent, enrollment after decline, no stop control, and default public sharing fail the revised contract. Missing approval evidence is an unresolved prerequisite, not evidence that approval was refused.

**Not executed — implementation acceptance checks:**

| Scenario | Observable acceptance result |
|---|---|
| Missing approval/content; direct task link or forged start request | No live enrollment/capture; service rejects bypass |
| Ineligible person | No consent demand or enrollment; screening data follows approved policy |
| Fresh visit, Back, exit, relaunch or decline | No implicit consent, enrollment, capture, or research upload |
| Agree without required confirmation; duplicate taps; timeout/retry | No premature enrollment; one resolved operation; truthful pending/failure status |
| Successful enrollment | Matching complete consent copy accessible; only acknowledged enrollment unlocks tasks |
| Denied/revoked permission or stale consent | No capture; clear dependency/remedy; unrelated work usable |
| Stop, interruption, background, error or withdrawal | Capture closes before accepting more samples; no auto-resume; partial-data policy enforced |
| Normal endpoint versus stopped run | Distinct outcomes; no duplicate save or false saved status |
| Data audit | Unauthorized recipients rejected; no public flags, endpoints or jobs; retention/withdrawal enforced |
| Default, 200%, largest supported accessibility text and Bold Text | Essential text and actions remain complete and reachable without overlap |
| VoiceOver, Switch Control, Full Keyboard Access and alternative activation | Full flow reachable; names, roles, state and order correct; Stop does not require speech or gestures |
| Geometry, appearance and physical movement | Measure 44 × 44 pt targets and separation, calculate contrast, verify actual reachability and protocol safety |

**Local evidence route:** Explicitly read the installed apple-hig root SKILL.md, then searched the topic index for research, consent, privacy, accessibility, buttons and onboarding. Read the Technologies, Foundations, Menus and actions, and Selection and input families. Read ResearchKit, Privacy, Accessibility, Typography, Buttons, Toggles and Writing topic procedures before their corresponding source guides. The supplied checkbox was mapped to Toggles and replaced with command buttons. Each file read used a separate command.

Only supplied local text and installed guidance were used. No web research, device/GUI interaction, SDK compilation, accessibility execution, contrast/geometry measurement, or participant study was performed. The derivative local references carry snapshot dates of 2026-10-25; their existence does not establish independent review or current online accuracy. Approval, consent validity, security, measurement validity and physical safety require separate evidence. This artifact is ready for implementation review, not proof that a live study is ready to recruit.
