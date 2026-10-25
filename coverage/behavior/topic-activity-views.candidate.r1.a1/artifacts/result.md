# Selected-observation sharing audit

## Scope and decisions

Target: an iPhone research notebook on iOS. Evidence is the single paragraph in [interface.md](interface.md); “verified” below means explicitly described there, not exercised in software.

Share sends a **copy of the selected observation**. It does not grant notebook access or start collaboration. Use the standard Share entry and system sharing presentation through a platform integration boundary. This specification requires no particular framework or Apple SDK on this machine. The system integration remains implementation work.

Offer a self-contained, readable copy for recipients without the app. Choose UTF-8 plain text as the baseline representation; if observation content includes essential nontext material, define an appropriate self-contained attachment representation before release. Do not silently omit essential material. No account, app installation, or live notebook URL should be needed to read the delivered baseline copy offline. Delivery itself can require connectivity; this does not promise offline email or social-service transmission.

## Ranked verified findings

| Rank | Observed evidence | Effect and correction | Basis |
| --- | --- | --- | --- |
| 1 — High | “sends the entire notebook regardless of selection” | The payload exceeds the selected observation and can disclose unrelated research. Build the payload from a fixed snapshot of the selected observation only; exclude other observations and notebook-wide private data. Block handoff if that payload cannot be prepared. | Contextual content in [Activity views — Best practices](https://developer.apple.com/design/human-interface-guidelines/activity-views#Best-practices); precise data scope in [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices). Applying minimization to this export is a product decision grounded in that guidance. |
| 2 — Medium | “hides the content preview” | People cannot inspect the outgoing scope. Show the observation title, “1 observation · Copy,” and a readable preview of the exact outgoing content before destination selection. Make the full representation inspectable. | Concrete review safeguard proposed here, supporting clear usage in [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices). The supplied local HIG does not establish a universal preview requirement. |
| 3 — Medium | “includes an unrelated Delete notebook action” | A destructive notebook-wide command appears in an observation-sharing task. Remove it from sharing. Preserve any existing deletion workflow elsewhere; its confirmation and recovery behavior are outside the supplied evidence. | Exclude irrelevant tasks: [Activity views — Best practices](https://developer.apple.com/design/human-interface-guidelines/activity-views#Best-practices). [Buttons — Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role) identifies destruction as data loss, but no claim about current role styling is possible. |
| 4 — Medium | “home-built grid of email and social logos” | It replaces the standard contextual sharing experience. Use the standard Share button and system share sheet; let available destinations and actions depend on the payload and environment. Do not hard-code destination order or imply every service accepts the content. | [Activity views — Best practices](https://developer.apple.com/design/human-interface-guidelines/activity-views#Best-practices) and [Collaboration and sharing — Best practices](https://developer.apple.com/design/human-interface-guidelines/collaboration-and-sharing#Best-practices). |

Ranks reflect consequence and task disruption, not measured incident frequency. The preview and grid findings do not prove an accessibility defect.

**Unverified compatibility risk:** “Offline recipients may not have the app installed” establishes a requirement, but the brief gives no current file format, link behavior, or recipient test. App-dependent sharing is therefore not a verified fifth defect. The portable-copy decision above addresses that risk. No collaboration backend, permissions, participant management, or revocation is evidenced or required for this copy flow. A received copy cannot be revoked through notebook access controls.

## Control inventory and corrected contract

| Supplied control | Owning procedure | Corrected contract / evidence question |
| --- | --- | --- |
| Share | Buttons; Activity views; Collaboration and sharing | Standard Share symbol with action name “Share”; opens review/sharing for the selected observation, normal nondestructive role. Preserve the selection and navigation context. Existing symbol, placement, accessible name, target size and feedback are unknown. |
| Email/social logo destinations | Activity views; Buttons | Replace the custom grid with system-provided eligible destinations. Selecting one begins its composition or handoff, rather than claiming delivery. Current labels, installed-app detection and destination support are unknown. |
| Delete notebook | Activity views; Buttons | Absent from this flow. Actual deletion, destructive styling, undo and confirmation are unknown; no new deletion behavior is specified. |

New app-owned controls: “Continue to Share” opens the system presentation after preview; “Cancel” abandons preparation/review; “Retry” repeats failed preparation. Give each an action-identifying accessible name and press feedback. App-owned iOS button hit regions should be at least 44 × 44 pt, with separation; visual size alone does not prove this. These are implementation acceptance requirements from [Buttons — Best practices and Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), not measured findings. The review screen precedes system sharing; do not stack a custom modal on a share extension.

## Worked before/after

Illustrative fixture, not supplied notebook data: notebook N contains observation A, “Leaf edges,” and observation B, “Participant interview.” A is selected.

**Before, as described:** Share → custom email/social grid, no preview, Delete notebook available → outgoing content contains A and B.

**After:** Share → review titled “Leaf edges,” scope “1 observation · Copy,” with A’s exported text → Continue to Share → system share sheet with eligible destinations → destination composition → user sends or cancels. B never enters the export, preview, attachment, or handoff. A recipient can open the delivered text without the notebook app and read it with networking disabled. Cancel returns to A in N without deleting, changing, or deselecting it.

## Framework-agnostic behavior

```text
on Share(selectedID):
    capture origin context and selected observation revision
    if selection absent or inaccessible:
        explain "Select an observation to share"; do not hand off
    prepare locally a self-contained copy of that revision
    allow cancellation; suppress duplicate preparation requests
    if preparation fails:
        show error with Retry and Cancel; retain original context
    else:
        review = title + "1 observation · Copy" + exact payload preview

on ContinueToShare:
    pass the reviewed immutable payload to platformSharingAdapter
    request standard system presentation, no unrelated custom activities
    do not enumerate or order system destinations in application logic

on adapter unavailable or handoff failure:
    retain reviewed payload; explain failure; allow Retry or Cancel
on system cancellation:
    return to original observation and selection
on reported completion:
    return to original context; do not claim recipient delivery
on unknown result:
    return without claiming success
```

If the observation changes during review, keep the captured revision and identify it as a snapshot; an explicit refresh rebuilds both payload and preview together. Never regenerate different bytes silently at handoff. Preparation transfers nothing to a server. Destination selection uses the reviewed payload only. Any destination-owned queued transfer and delivery status belong to that destination; do not invent background-work guarantees. If future app-owned background transfer is added, specify status and recovery in the main app as advised in [Activity views — Share and action extensions](https://developer.apple.com/design/human-interface-guidelines/activity-views#Share-and-action-extensions).

Data-purpose boundary: selected observation content → readable copy; other observations, notebook database, credentials and access tokens → excluded; destination → receives only reviewed copy after user handoff. Metadata and attachment fields are unknown and must be inventoried before implementation. No additional protected-data permission is justified by this specification alone.

## Acceptance checks and current status

**Passed — document inspection:** platform and sharing task identified; all supplied controls mapped to procedures; four described defects ranked; copy versus access distinguished. These passes establish review coverage only.

**Failed — described current flow:** selected-only scope, visible preview, relevant-only actions, and standard system sharing. Each failure follows the explicit brief; none was reproduced at runtime.

**Not executed — release acceptance:**

1. With A selected and B containing a unique sentinel, inspect all exported bytes, attachments and metadata: A is present; B’s sentinel and notebook-wide data are absent.
2. Compare full preview with handed-off content, including a concurrent edit: the same revision is shared. Verify missing selection, export failure, retry and duplicate activation.
3. Inspect the actual iPhone presentation: standard Share entry and system share sheet; eligible destinations only; no Delete notebook or duplicate custom system actions. Unavailable adapter/destination fails recoverably without substituting a whole-notebook export.
4. Cancel during preparation, review and destination composition: observation, selection, edits and navigation context remain intact. A completion callback alone never produces “Delivered.”
5. Deliver the baseline copy to a recipient without the app; then disable networking and read the saved content. Check representative essential attachments separately. Do not equate queued sending with completed delivery.
6. Verify action names, focus return, VoiceOver operation, text enlargement, unclipped preview, press feedback and measured 44 × 44 pt app-owned targets on the implemented interface. No current accessibility failure is established.

## Evidence and source limits

Only local interface.md and installed skill instructions/references were used; no web browsing occurred. Official links above identify the source articles, not pages fetched during this audit. The package identifies its article snapshot as 2026-10-25; this is local guidance, not an SDK reference or a claim of independent source validation.

Read order: installed apple-hig root → Patterns and Menus and actions families → Collaboration and sharing, Activity views and Buttons topic procedures → their source guides; Foundations family → Privacy topic procedure → Privacy source guide. Paths were resolved within `.agents/skills/apple-hig/`, and each file was read in a separate shell command.

No app code, screenshot, payload, schema, runtime, backend, device, SDK, GUI or accessibility execution was supplied or performed. Destination availability, actual disclosure, native rendering and recipient readability remain untested. The corrected behavior is a reviewable specification, not an implemented or validated integration.
