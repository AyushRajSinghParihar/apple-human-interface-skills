# Selected-observation sharing audit

Scope: iPhone/iOS research notebook. Evidence: the complete supplied `interface.md`, a brief rather than executable UI. “Verified” below means explicitly stated in that brief; it does not mean reproduced on a device. No framework or Apple SDK is assumed.

## Ranked findings

| Rank | Verified observation | Effect | Decision and source |
| --- | --- | --- | --- |
| 1 — High | Sends the entire notebook regardless of selection. | Sharing one observation exposes unrelated notebook content and contradicts the selected scope. Actual recipients and sensitivity are unknown. | Bind the payload to the selected observation; never fall back to the notebook. Apply precise data scope from [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices) and contextual sharing from [Activity views](https://developer.apple.com/design/human-interface-guidelines/activity-views#Best-practices). The selection-bound export is this audit’s concrete application of those principles. |
| 2 — High | Includes an unrelated “Delete notebook” action. | Introduces a data-loss command into a transfer task. Accidental activation and actual deletion are not established. | Remove this custom activity from sharing. HIG says to exclude irrelevant tasks: [Activity views — Best practices](https://developer.apple.com/design/human-interface-guidelines/activity-views#Best-practices). Any separate notebook deletion flow needs its own review; this audit does not prescribe its confirmation or undo policy. |
| 3 — Medium | Share opens a home-built grid of email and social logos. | Replaces familiar contextual system sharing with an app-maintained destination surface. Destination coverage and accessibility are unknown. | Use the standard Share entry and system share presentation through an available host integration. Supply content types; let the system determine compatible destinations and their order. [Activity views — Best practices](https://developer.apple.com/design/human-interface-guidelines/activity-views#Best-practices). No requirement to adopt UIKit or SwiftUI is implied. |
| 4 — Medium | Hides the content preview. | Prevents checking the scope before handoff, especially harmful with finding 1. | Provide a visible summary and inspectable preview generated from the exact export. This is a product safeguard, not a claim that the local HIG snapshot universally mandates a preview. It supports clear data usage under [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy). |

Recipient constraint, not a verified defect: offline recipients may lack the app. The brief gives no payload format, link behavior, or recipient test. Choose a self-contained, broadly readable copy rather than relying on an app-only link. HIG supports file/plain-text representations for send-a-copy in [Collaboration and sharing — Best practices](https://developer.apple.com/design/human-interface-guidelines/collaboration-and-sharing#Best-practices); the exact offline export format below is a product decision.

## Corrected behavior and decisions

Share means **send a copy of the selected observation**. It creates no ongoing access, participants, edit permissions, or collaboration updates. Do not add collaboration solely because the button says Share. No backend sharing model is supplied.

Control inventory:

| Supplied control | Owning procedure | Corrected contract |
| --- | --- | --- |
| Share | Buttons; Activity views | Familiar Share symbol with accessible name “Share Observation,” normal nondestructive role. Opens preparation and then system sharing; does not itself send. Retain its existing convenient placement; toolbar presence is unknown. |
| Email/social logos | Activity views; Buttons | Replace app-owned destination controls with system-managed eligible destinations. Do not hard-code presence, availability, or order. |
| Delete notebook | Buttons; Activity views | Absent from app-supplied sharing activities. No deletion side effect on any share exit. |

Use system button styling where available. For an app-owned Share control, specify a selectable region of at least 44 × 44 pt on iOS with clear separation; supply press feedback if custom. These are future checks, not measured defects. See [Buttons — Best practices, Style, Content and iOS](https://developer.apple.com/design/human-interface-guidelines/buttons).

Data-purpose contract:

| Data | Use and boundary |
| --- | --- |
| Selected observation’s title and body | Included in the copy and its preview. |
| Selected observation’s attachments | Include embedded readable representations when present; never silently omit them. If unavailable locally, explain what must be downloaded or let the user explicitly choose a clearly described reduced copy. |
| Other observations and notebook-wide metadata | Excluded, including hidden fields and export metadata that could disclose unrelated content. |
| Credentials, internal identifiers, collaboration tokens | Excluded. No new permission request or upload is justified merely by exporting locally available content. |

Prepare a self-contained PDF with selectable text and embedded images for supported observation content. A plain-text representation may also be supplied where it preserves meaning. Validate fidelity for actual attachment types; PDF is not assumed sufficient for unknown audio, video, or interactive content. An unsupported attachment blocks the complete export until a portable representation or explicit reduced-copy choice exists. The preview states the title, “1 observation,” format, and included/omitted attachments. PDF and these labels are design choices, not HIG format mandates.

A recipient who already has the complete file must be able to read its supported content offline without the notebook app or an account. Delivery through email or a social service may still require connectivity; offline readability does not promise offline delivery.

## Framework-agnostic state contract

```text
on Share(selectedObservationId):
    require exactly one existing selected observation
    capture selection, navigation/scroll context, and observation revision
    enter Preparing; prevent duplicate requests; show activity in Share control
    snapshot = copy only that observation and explicitly included attachments
    payload = buildPortableCopyLocally(snapshot)
    if incomplete or failed:
        show actionable preparation error in current context
        offer Retry or Cancel; never substitute the whole notebook
    else:
        preview = derivePreview(payload)  // same immutable bytes/content
        present standard system share surface with payload and visible preview
        customActivities = []             // no Delete notebook or duplicates

on selection or source revision changing before presentation:
    invalidate preparation; require a fresh snapshot and matching preview

on share cancellation:
    release temporary resources when safe; restore captured context and selection
    do not send, delete, mutate source, or create collaboration access

on destination acceptance:
    hand off immutable payload; retain temporary data for required consumer lifetime
    return to preserved notebook context
    report only the outcome actually known (handoff is not recipient delivery)

on destination error or unavailable destination:
    preserve context; allow retry or another eligible destination
    never broaden payload or silently switch to an app-only link
```

Use a host adapter for system sharing; its implementation and availability must be established in the eventual stack. The adapter must expose payload types, preview metadata, cancellation/error outcomes, and file lifetime needs. If unavailable, report that implementation gap rather than presenting the old logo grid as system integration. No custom upload or share extension is specified. If one is later introduced, define its dismissal, background status, and problem reporting separately.

## Worked before/after

Illustrative fixture, not additional supplied evidence: notebook “Field notes” contains A “Leaf discoloration” and B “Private interview.” Select A, whose body is “Yellow edges on the lower leaves” and whose attachment is `leaf.jpg`.

**Before, applying the supplied behavior:** Share opens email/social logos with no content preview. Choosing a destination sends A and B because the entire notebook is exported. “Delete notebook” is also offered.

**After:** Share prepares `Leaf discoloration.pdf` from A only. The visible preview shows “Leaf discoloration · 1 observation · PDF · 1 image” and lets the user inspect the body and image. The system presents compatible destinations; Delete notebook is not supplied. Choosing one transfers the same immutable copy shown in the preview. B’s title, text, attachments, and metadata are absent. After the complete file is received, it opens in a compatible general-purpose reader offline without this app. Canceling instead returns to A with the selection and scroll position preserved.

## Acceptance checks and status

**Passed — static audit/specification only:** Read `interface.md`; mapped every supplied control to candidate procedures; separated copy transfer from access; specified selection, payload, preview, destination eligibility, cancellation, failure, and recipient constraints. Reviewed this contract against the loaded guidance. These passes do not establish implementation correctness.

**Failed — supplied design, per brief:** Selected-only scope; exclusion of unrelated Delete notebook; standard system sharing; visible preview. Preview failure is against the proposed product acceptance criterion, not a universal HIG rule.

**Not executed — implementation acceptance tests:**

1. With fixture A/B above, inspect exported bytes and metadata: only A and its permitted attachments appear. Changing selection during preparation cannot send stale or broader content.
2. Verify preview and transferred file represent the same snapshot; no notebook-wide fallback exists. Missing/unsupported attachments produce an explicit decision or error, not silent loss.
3. Open Share on iPhone: system presentation appears, eligible destinations reflect payload types, and app-supplied actions contain no Delete notebook or duplicate system actions. Do not assert fixed system ordering.
4. Cancel at preparation, preview, and destination composition: no transfer is initiated by the app, no source is mutated, and selection/navigation context survives. Verify callback semantics with the actual host integration.
5. Remove/unavailable destination, export failure, interruption, and rapid repeat taps: no duplicate transfer, leaked broader data, or loss of context; retry stays scoped to A. Verify temporary-file lifetime and cleanup.
6. Receive the complete copy on a device without the notebook app, disconnect networking, and read text/images in a compatible reader. Test real supported attachment types. Separately verify that network-dependent delivery does not falsely report success while offline.
7. Inspect the Share control’s accessible name, actual ≥44 × 44 pt selectable region, press feedback, and enlarged-label layout. On a real iPhone, verify assistive-technology navigation through preview, destinations, and dismissal. None of these properties is inferable from the brief.
8. Confirm no collaborative access, invitations, or permission changes result from sharing a copy. Distinguish destination handoff from confirmed recipient delivery in any status text.

## Evidence limits and guidance trail

Only local files and installed instructions were used; no web browsing, SDK compilation, device, GUI, accessibility, recipient delivery, or runtime testing occurred. There is no screenshot, implementation, schema, attachment inventory, deployment target, or backend evidence. No claim is made about current hit regions, logo labels, destination compatibility, deletion execution, research consent, security certification, or medical-study integration. “Research notebook” alone does not establish a ResearchKit or health-data workflow.

Installed package root: `.agents/skills/apple-hig/`. Read the root `SKILL.md`, searched `references/topic-index.md`, and followed these family → topic procedure → supporting guide routes:

- `subskills/apple-hig-menus-and-actions/SKILL.md` → `.topics/apple-hig-activity-views/SKILL.md` and `.topics/apple-hig-buttons/SKILL.md` → `references/activity-views.md` and `references/buttons.md`.
- `subskills/apple-hig-patterns/SKILL.md` → `.topics/apple-hig-collaboration-and-sharing/SKILL.md` → `references/collaboration-and-sharing.md`.
- `subskills/apple-hig-foundations/SKILL.md` → `.topics/apple-hig-privacy/SKILL.md` → `references/privacy.md`.

Each path after a family is relative to that family directory. All were explicitly read from this installed package, one file per shell command. The local references identify a 2026-10-25 snapshot/retrieval; official links above identify source articles and sections, not live verification or SDK documentation. No source conflict was encountered in the guidance used.
