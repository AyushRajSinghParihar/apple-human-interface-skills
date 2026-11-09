# Selected-observation sharing audit

Scope: iPhone/iOS research notebook. Evidence is the single paragraph in `interface.md`, treated as the supplied behavior specification, not an executed interface. Rankings below reflect consequence and task impact. No application source, screenshot, payload, or runtime was supplied.

## Ranked verified findings

| Rank | Evidence in interface.md | Effect | Decision and basis |
| --- | --- | --- | --- |
| 1 — High | “sends the entire notebook regardless of selection” | Sharing one observation exposes unrelated notebook content and defeats the selected scope. | Build a copy from the selected observation only. Never silently fall back to the notebook. Precise scope applies the HIG privacy principle; this exact export boundary is a product decision. [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices). |
| 2 — Medium | “Share opens a home-built grid of email and social logos” | Replaces familiar contextual system sharing with an app-maintained destination set. | Use the standard Share entry point and system share sheet, supplying supported content representations. Let the system determine available destinations and ordering. [Activity views — Best practices](https://developer.apple.com/design/human-interface-guidelines/activity-views#Best-practices). |
| 3 — Medium | “includes an unrelated Delete notebook action” | Introduces whole-notebook destruction into an observation-sharing task. | Remove Delete notebook from this flow. It belongs to a separate notebook-management task; its existing confirmation and recovery behavior are unknown and outside this correction. HIG says to exclude irrelevant activities. [Activity views — Best practices](https://developer.apple.com/design/human-interface-guidelines/activity-views#Best-practices). |
| 4 — Medium | “hides the content preview” | Prevents inspection of the outgoing content before choosing a destination, compounding the scope defect. | Expose an accurate preview with observation title, “1 observation,” and readable content; it must match the actual export. This is a product safeguard derived from clear data-use communication, not a claimed universal HIG requirement for a particular preview layout. [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy). |

Recipient requirement, not a verified defect: “Offline recipients may not have the app installed.” The current payload format and recipient opening behavior are unspecified. A link-only or proprietary-only payload would fail this requirement, but neither is established by the brief.

## Decisions and control contract

Use **send a copy**, not a collaboration invitation. Sharing must not create ongoing access, edit rights, participants, or an app-install dependency. No collaboration backend is evidenced. HIG distinguishes copies from shared access and recommends a file or plain-text representation for custom sharing infrastructure. [Collaboration and sharing — Best practices](https://developer.apple.com/design/human-interface-guidelines/collaboration-and-sharing#Best-practices).

Supply a self-contained UTF-8 plain-text copy of the selected observation as the baseline. Include its title and observation text; include only explicitly defined observation fields. If the actual data model contains images or other essential nontext content, specify and verify an additional self-contained format before calling that export complete; do not silently omit material. The brief supplies no schema or attachments. Text format is a product choice, not an Apple-prescribed format. A recipient with a compatible general-purpose reader should be able to read the received copy without this app, authentication, or network retrieval. Transport may still need connectivity; offline reading does not imply offline email delivery.

| Supplied control | Candidate procedure | Corrected contract |
| --- | --- | --- |
| Share | Buttons; Activity views | Standard Share symbol/label, normal nondestructive role; opens sharing for exactly the selected observation. Enabled when one valid observation is selected. Otherwise explain “Select an observation to share.” |
| Email/social logos | Activity views | Replace the custom destination grid with system-provided destinations eligible for the payload. Do not promise a particular app, fixed order, or universal format support. |
| Delete notebook | Buttons; Activity views | Absent from sharing. This review makes no claim about styling, confirmation, or undo elsewhere. |

Use system control states where available. For the Share control, target at least 44 × 44 pt with separation from adjacent controls; an unseen glyph does not establish target size. If copy preparation is delayed, show activity in the activating button and prevent duplicate presentation. These are specifications to verify, not measured defects. [Buttons — Best practices and iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons).

Data-purpose boundary:

| Data | Purpose | Allowed behavior |
| --- | --- | --- |
| Selected observation | Recipient reads a copy | Build locally from an explicit allowlist of export fields. Preview exactly this representation. |
| Other observations/notebook metadata | No need for this task | Exclude from body, filename, preview metadata, hidden fields, and attachments. |
| Contacts, destination credentials | No app-owned need established | Do not add permission requests or collect credentials to replace system destination handling. |

The exact allowlist must be settled against the real schema. The design does not certify privacy enforcement or require a new permission alert merely to export existing content.

## Framework-agnostic behavior

`platformShare` below is an abstract integration boundary, not an SDK/API claim. Production iOS integration must supply the system share sheet; no SDK installation is required to specify it here.

```text
on Share:
    require exactly one valid selected observation
    remember selection and navigation context
    snapshot = immutable copy of selected observation at this moment
    enter Preparing; suppress duplicate activation
    export = encodeSelfContainedCopy(allowlistedFields(snapshot))
    assert export contains no other notebook records or metadata
    if generation fails or required local content is unavailable:
        return to observation with actionable error and Retry
        do not send partial content or substitute the whole notebook
    preview = renderFrom(export)   // same snapshot and scope as payload
    show preview, title, "1 observation", and explicit Continue/Cancel

on Cancel before presentation:
    discard temporary export; restore prior context; send nothing

on Continue:
    platformShare.present(export, accuratePreviewMetadata,
                          customActivities = [])
    // no destination order, recipient, or remote-delivery guarantee

on system dismissal/cancellation:
    restore prior observation, selection, and navigation context
    release temporary export only when the integration no longer needs it

on reported handoff result:
    show an actionable problem if one is reported
    never equate handoff or dismissal with recipient delivery
```

The preview step is an explicit product choice to guarantee inspection without depending on unknown system preview capabilities. It occurs before system presentation, not as a second modal stacked over a share extension. If the eventual integration provides equivalent full inspection within system sharing, remove the extra step after verifying equivalence. No custom extension or app-owned background upload is specified. If one is later introduced, define continuation and problem status separately; HIG recommends background continuation for long extension work. [Activity views — Share and action extensions](https://developer.apple.com/design/human-interface-guidelines/activity-views#Share-and-action-extensions).

## Worked before/after

Illustrative fixture, not supplied research data: notebook N contains observation A, “North plot: three seedlings,” and observation B, “Private participant notes.” A is selected.

**Before, per brief:** Share opens the app's email/social grid, offers Delete notebook, hides the preview, and sends notebook N including B.

**After, proposed:** Share prepares a copy of A. Preview reads “1 observation — North plot” and “North plot: three seedlings.” Continue opens system sharing with that same self-contained text. B, notebook-wide metadata, and Delete notebook are absent. Cancel returns to A without changing either record. After an actual transfer, a recipient without the notebook app can read the received text offline in a compatible reader. Editing A later does not change the already exported copy.

## Acceptance checks and status

**Passed — local static review only:** installed root skill explicitly read; topic index searched for sharing, activities, buttons, and privacy; each owning family and topic procedure read before its source guide. All three supplied control groups were mapped above. The proposed contract distinguishes copy from access and covers cancellation, unavailable content, and handoff failure.

**Failed — supplied behavior specification:** selected-scope export, system sharing presentation, relevant-actions-only scope, and preview visibility. These are specification findings, not reproduced runtime failures.

**Not executed — implementation acceptance:**

1. With fixture A/B, decode every outgoing representation and inspect preview metadata, filename, and attachments: A is present; B and notebook-only metadata are absent. Change selection during preparation: preview and payload remain the same captured observation. Invalid selection never triggers notebook export.
2. Inspect preview against the decoded payload; verify full selected content can be inspected. Cancel both before and within system sharing: no app-owned transmission or notebook mutation; selection and navigation persist.
3. On iPhone, verify standard system sharing, payload-eligible destinations, unavailable destination behavior, and no app-added Delete notebook or duplicate system actions. Do not require a fixed destination order.
4. Transfer the baseline copy, then open it offline on a recipient device without the app. Verify all required content is available without links, login, or downloads. Exercise any essential nontext representation separately once the schema is known.
5. Inject missing local content, export failure, and handoff failure: no broader or incomplete fallback; useful error and retry; duplicate taps cannot produce multiple presentations. Confirm dismissal does not falsely report delivery.
6. Measure Share's hit region and separation; verify name, focus return, enlarged text, press/busy feedback, and cancellation with assistive technology on the actual interface. No accessibility failure is inferred from missing markup.

## Evidence limits and provenance

Only `interface.md` and installed instructions/guides were used; no web browsing occurred. Official links above identify the sources recorded in the local snapshot, not live verification. Installed guidance is dated 2026-10-25 and is not SDK documentation or proof of independent source review.

Read route under `.agents/skills/apple-hig/`: root `SKILL.md` → `references/topic-index.md` search → menus-and-actions family → Activity views and Buttons procedures; patterns family → Collaboration and sharing procedure; foundations family → Privacy procedure; then each corresponding reference guide. Each file was read in its own shell command. No screenshot-specific route was needed because no screenshot or animation was supplied.

No device, GUI, SDK compilation, accessibility execution, export generation, recipient delivery, backend permission enforcement, or runtime test was performed. Current visual geometry, accessible names, cancellation, storage cleanup, encryption, schema, destination eligibility, and offline compatibility remain unverified. This artifact specifies corrected behavior; it does not claim to implement or execute it.
