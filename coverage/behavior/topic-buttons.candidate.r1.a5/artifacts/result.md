# Export-control correction plan

This is a static review of `interface.md` for an iPadOS field-report editor. All four functions remain available. Findings are verified against the supplied description, not against an executing application. Priorities below are product risk judgments, not severity labels supplied by Apple.

## Ranked findings

| Rank | Verified evidence | Effect | Correction and source |
|---|---|---|---|
| 1 · High | Repeated Publish taps create duplicate uploads during the stated 8-second operation. | One intended publication creates multiple requests/results. | Atomically guard activation before starting work; deduplicate the publication operation beyond the button. This engineering safeguard supports the delayed-action contract; HIG does not prescribe a backend algorithm. See [Buttons: iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS). |
| 2 · High | Delete is primary/default; all four controls have equally prominent fills. | Destruction is presented as the expected action, while useful action hierarchy is absent. | Make Publish the sole prominent action, Preview and Save Draft secondary, and Delete destructive with lower emphasis. Remove Delete's editor default binding. HIG generally reserves primary for a likely nondestructive action and recommends one or two prominent actions: [Buttons: Style and Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Style). |
| 3 · High | Every activation region is 20 × 20 pt, with 2 pt gaps. | Small, crowded targets make selection harder and increase accidental activation risk, especially near Delete. | Specify at least 44 × 44 pt hit regions for all four, without overlap, and increase separation. See dimension qualifications below and [Buttons: Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), [Accessibility: Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility). |
| 4 · High | Glyph-only Preview has no accessible name. | Assistive interaction cannot reliably identify its action. | Use visible text “Preview” and accessible name “Preview”; expose button semantics. A glyph may accompany the text as decoration. [Accessibility: Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |
| 5 · Medium | Nothing changes during the described 8-second Publish upload. | People cannot distinguish accepted input from an unresponsive control and may retry. | Show immediate press feedback, then an activity indicator inside Publish and label “Publishing…” until resolution. Provide honest success/error status. [Buttons: iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS), [Loading: Showing progress](https://developer.apple.com/design/human-interface-guidelines/loading#Showing-progress). |

No missing press-feedback defect is separately asserted: “nothing changes during upload” does not establish whether a transient pressed state exists. It remains an acceptance check.

## Decisions and action contract

These are framework-agnostic requirements for the corrected design, not claims that an Apple SDK is installed.

| Control | Outcome and scope | Role, appearance and default | Availability |
|---|---|---|---|
| Publish | Publish a captured revision of the current report. | Primary; sole prominent fill; label/name “Publish”. Eligible for an explicit default activation only when valid, editor is active, and no operation is pending. Never activate from ordinary text-entry Return. | Available when report is publishable; pending activation is guarded and disabled. |
| Preview | Open a preview of the current report revision without publishing it. | Normal, secondary; visible label/name “Preview”; no default. | Available during upload; identify the revision being previewed. |
| Save Draft | Persist the current report as a draft without publishing. | Normal, secondary; label/name “Save Draft”; no default. | Remains available during upload if independent of publication. Store by revision so it cannot overwrite the captured publication payload. |
| Delete | Remove the current report, subject to an explicit recovery policy. | Destructive, lower emphasis; visible label/name “Delete”; never the editor default. Meaning must survive without red alone. | Temporarily unavailable during an unresolved publication to avoid delete/publish races; explain “Delete is unavailable while publication is being resolved.” Reenable after resolution. |

The scope/outcomes above are proposed contracts: the brief does not define Preview rendering, draft persistence, publish validation or deletion recovery. Implementers must verify those semantics rather than silently attaching different behavior to these labels. These are immediate command buttons, not toggles or persistent selectors; each maps to the Buttons procedure. The footer is not established to be system toolbar chrome, so no toolbar implementation is assumed.

Keep peer target heights consistent and use style, not unequal button sizes, for hierarchy. Proposed layout: Delete at the leading edge, then a flexible separation, with Preview, Save Draft and Publish grouped in task order. Start with 12 pt clear separation between filled/bounded targets and larger separation before Delete; this is a product layout choice informed by the source's approximate padding advice, not a universal HIG gap minimum. Reflow into multiple rows when width or enlarged labels require it. Never shrink targets or overlap expanded hit regions to retain one row.

Dimension qualification: the Buttons guide says general hit regions should be at least 44 × 44 pt. The Accessibility guide separately lists iOS/iPadOS default controls as 44 × 44 pt and minimum controls as 28 × 28 pt. These are different stated thresholds; 20 × 20 pt fails both. Use the conservative 44 × 44 pt target here, not the smaller accessibility minimum as a density goal. Physical ease still needs device evaluation.

Delete recovery is a release decision, not a verified finding. Establish actual reversibility first. Common undoable deletion generally needs no confirmation; retain a discoverable recovery path. If deletion is irreversible or otherwise warrants interruption, show “Delete Report?” with an accurate consequence message, “Cancel” and “Delete Report”. Use no default to require deliberate choice; Cancel is not default. Dismissal/Escape/Command-Period cancels without changes. Return alone must not commit this proposed no-default dialog. Do not assert irreversibility in copy until verified. [Alerts: Best practices and Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons) permits an explicitly requested destructive confirmation to have a normal default; this plan deliberately chooses no default, rather than claiming destruction can never be default. If Assistive Access is supported, separately apply its difficult-to-reverse-action confirmation requirements from [Accessibility: Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive).

## Slow-publication state specification

Keep the report visible and independent work usable; do not replace the editor with a blocking loading screen. Use an in-button spinner because duration and whole-operation measurement are not supplied. Do not display an invented percentage or an eight-second countdown. If a future implementation can measure whole-task completion, use a consistent progress representation covering upload and server finalization; do not swap the spinner into a differently shaped bar midtask. [Progress indicators: Best practices](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices), [Loading](https://developer.apple.com/design/human-interface-guidelines/loading).

```text
state = ready | publishing | reconciling | succeeded | failed

on Publish:
    atomically:
        if state in {publishing, reconciling}: return
        if report is not publishable: expose the reason; return
        capture immutable report revision
        create operation ID bound to report + captured revision
        state = publishing
    render disabled Publish: spinner + "Publishing…"
    expose busy/disabled semantics and readable publication status
    submit captured revision using operation ID

on acknowledged committed publication(operation ID):
    state = succeeded
    remove spinner; show persistent "Published" status for captured revision
    if newer edits exist: say "Earlier revision published; current edits are unpublished"
    restore appropriate actions; prevent re-publication of unchanged revision

on definite rejection before commit:
    state = failed
    remove spinner; preserve report and edits
    show specific actionable failure and a retry path

on timeout, connection loss, or uncertain response:
    state = reconciling
    show "Publication status unknown. Checking…"
    query the same operation ID; never start a new publication blindly
    if connection unavailable: show persistent status and "Check Status"
    reconcile to committed or definitely uncommitted before enabling a fresh operation

on retry after a failure:
    reuse operation identity where commit is uncertain
    submit only under a service contract that deduplicates repeated delivery
```

The service must return the existing result for the same operation ID and reject mismatched payload reuse. A UI guard alone cannot guarantee duplicate prevention across retries, reconnection or another client. Backend capabilities are unknown; this is an implementation dependency. If the service cannot reconcile or deduplicate, report that limitation and keep uncertain publication unresolved rather than promising safe retry.

Show success only after authoritative publication confirmation, not after bytes are sent or a request is merely accepted. Remove temporary activity on completion or definite failure; uncertain connectivity gets explicit status and recovery rather than an endless unexplained spinner. Retain focus on the initiating control where feasible, with a separate perceivable status update; announce meaningful state transitions without repeatedly announcing animation frames. No detailed VoiceOver order is claimed or specified here.

Safe cancellation is not established. Do not add a “Cancel” control that implies undoing a server commit. If the transport/service supports safe cancellation before commit, expose it and preserve the draft; explain any partial-work loss and permit resume where consequential. Otherwise retain independent Preview/Save Draft and explain why publication must resolve. This conditional policy follows [Progress indicators](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices).

## Worked before/after

**Before, supplied:** A person taps Publish, sees no change, then taps twice more during the stated eight seconds. Duplicate uploads result. Four filled controls compete for attention, and default activation is assigned to Delete.

**After, proposed trace:** At the first tap, a synchronous guard captures revision 7 and operation A. Publish immediately shows a spinner and “Publishing…”. Two further taps produce no additional submission. Preview remains usable; Save Draft may save revision 8 without mutating revision 7. At eight seconds, if the service confirms A committed, the spinner disappears and status reads “Revision 7 published; current edits are unpublished.” If the response is lost instead, the editor shows unknown status and checks A; it does not claim failure and create operation B. Delete remains unavailable only while A is unresolved. This is a worked specification, not an executed timing result.

## Acceptance checks and evidence status

**Passed — static review only:** All four supplied controls were inventoried and retained in the proposal; each has a named outcome, role, target contract and availability policy. Installed root, relevant family procedures, topic procedures and supporting local guides were read. No application behavior passed by execution.

**Failed — supplied specification:** Duplicate suppression; safe editor default/hierarchy; target size; Preview naming; delayed-operation feedback. The 2 pt gaps are evidence of crowding, not proof of violating a universal numerical gap rule.

**Not executed — required implementation acceptance:**

- Simulate the eight-second upload with rapid taps, keyboard activation and programmatic duplicate activation: exactly one operation begins; repeated delivery resolves to one committed publication.
- Test success, definite failure, offline start, lost response after server commit, reconnect, slow/stalled work and stale callbacks. No false success, duplicate commit, unexplained endless wait or data loss occurs; retry/reconciliation uses the correct operation identity.
- Confirm in-button activity starts with accepted activation and disappears at terminal resolution; custom buttons have perceivable pressed feedback. Unknown duration has no fabricated estimate.
- Preview and Save Draft perform their named outcomes during upload; captured publication revision remains immutable. Delete availability and explanation track unresolved work. Confirm recovery/confirmation against actual deletion semantics, including dismissal and keyboard paths.
- Measure actual hit regions at least 44 × 44 pt, nonoverlap and proposed spacing across supported iPad layouts. At 200% text enlargement, reflow preserves every function and readable status without clipped labels.
- Inspect semantics: all four are named buttons with correct enabled/busy states. Complete the flow with keyboard and supported assistive input; default activation never accidentally deletes or publishes from text entry. Check actual status announcement and focus behavior using an appropriate Apple environment.
- Measure final foreground/background contrast in supported appearances and accessibility preferences; ensure role and status meanings do not depend on color alone. These were not measurable from the brief.

## Evidence limits and source record

Only `interface.md` and installed instructions/guides informed this review. There is no rendered app, implementation, backend contract, runtime trace, screenshot or test harness. The reported eight seconds is supplied evidence, not measured latency. Reversibility, validation, actual colors, focus behavior, persistence and cancellation support are unknown. No device, SDK, GUI, accessibility tool, network test or compilation was executed. This document is a correction specification; it does not establish implementation conformance.

Installed route used, relative to `.agents/skills/apple-hig/`: `SKILL.md` → relevant rows of `references/topic-index.md` → `subskills/apple-hig-{menus-and-actions,status,patterns,foundations,presentation}/SKILL.md` → their `.topics/apple-hig-{buttons,progress-indicators,loading,accessibility,alerts}/SKILL.md` → corresponding `references/*.md`. Each file was read individually by command, with procedures read before source guides. Local references identify a 2026-10-25 snapshot/retrieval. Official links above identify the supporting articles/sections; they were not opened or verified online. No SDK or newer-release claim is made.
