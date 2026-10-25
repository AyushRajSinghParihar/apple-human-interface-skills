# NFC repair result

Patched `interface.md` in place, replacing the one-paragraph defect description with an implementable iPhone scanning and checkout specification. No application code was supplied or changed.

## Decisions and changes

- Explain the task before deliberate foreground scanning. Use the system scanning sheet with “Hold iPhone near the equipment label.” Update it for the next item. This follows locally read [NFC guidance](https://developer.apple.com/design/human-interface-guidelines/nfc).
- Separate read, identification, review, submission and confirmed completion. Unknown labels cannot register equipment or create checkouts. Explicit Check Out follows review; the service revalidates eligibility. These are product safeguards addressing the supplied defects.
- Replace indefinite waiting with 30-second scanning and 15-second lookup/submission/status deadlines, earlier system termination, truthful errors and recovery. Durations are proposed product defaults; temporary, honest activity follows [progress guidance](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices).
- Specify labeled native controls, iPhone target dimensions, submission-button activity, duplicate activation handling and cancellation semantics using [button guidance](https://developer.apple.com/design/human-interface-guidelines/buttons).
- Retain uncertain checkout outcomes for reconciliation; require duplicate-safe service operations. Preserve equipment context, define subsequent scans and keep foreground reading complete when optional background entry is unavailable.

## Worked before/after

Before, according to the supplied file: scanning starts without explanation, success appears before a read, an unknown label creates a checkout, and no-label timeout leaves a permanent spinner.

After, specified example: Alex reads the explanation and selects Scan Equipment. The system sheet says “Hold iPhone near the equipment label.” An unknown label ends the session and shows “This label doesn’t match registered equipment.” Checkout count remains zero. Alex selects Scan Again and reads the label for Drill D-104. Identification opens Review without claiming checkout success. Only selecting Check Out and receiving a confirmed commit displays “Checked out: Drill D-104.” Duplicate callbacks do not create another record. Scan Next Item names the next equipment label; no read within 30 seconds ends activity and offers Try Again or Cancel. This is a specification trace, not an executed test.

## Acceptance checks

All behavioral checks below are **not executed**; they are the implementation acceptance contract.

| Check | Expected result |
| --- | --- |
| Enter screen; activate scan twice | Explanation precedes scan; one system session; no early success |
| Read known eligible label | Correct name, ID and availability in Review; no checkout before explicit Check Out |
| Read unknown, malformed or ambiguous label | Unrecognized state; zero registration/checkout writes |
| No label; early system timeout; app deadline | Session/sheet ends; no spinner remains; retry and cancel work |
| Cancel scan/lookup, then deliver late callback | Prior context retained; stale response cannot navigate or mutate |
| Reader unavailable, startup error, lookup failure | Truthful recovery, bounded activity and no checkout |
| App leaves foreground during read or submit | Reader stops without automatic restart; submitted operation retained |
| Duplicate detections, Check Out taps and delivery retries | One checkout per operation ID |
| Availability/authorization changes after Review | Commit rejects ineligible item; no false success |
| Commit succeeds but response is lost | Unknown outcome, no duplicate retry; Check Status finds confirmed result |
| Status remains pending or lookup fails | Activity ends at deadline; context and status recovery persist |
| Scan Next Item; rescan same equipment | Updated instruction; prior records intact; actual availability prevents duplicates |
| Optional background notification entry | Matching equipment validated/reviewed; no automatic checkout; foreground fallback remains |
| Inspect controls on iPhone with enlarged text and assistive technology | Usable labels, separated targets at least 44 × 44 pt, no unintended checkout activation |

**Passed — static specification inspection:** the revised artifact explicitly addresses all four reported defects and defines entry instructions, first/subsequent results, destination, foreground fallback, state transitions, deadlines, mutation gates and recovery. Both requested files were written and checked for the key contracts.

**Failed:** no revised-artifact check failures observed. Initial defects are supplied reports, not independently reproduced runtime failures.

**Not executed:** the behavioral checks above, physical NFC reads, label compatibility, background restrictions, timing, native sheet lifecycle/rendering, SDK compilation, backend atomicity, GUI or accessibility execution. No executable app or device evidence was supplied.

## Source audit and evidence limits

Explicitly read the installed root `apple-hig/SKILL.md`, then inspected the supplied interface and searched relevant NFC/progress/buttons rows in `references/topic-index.md`. Read each selected family, exact topic procedure and supporting guide in that order, one file per command:

1. `subskills/apple-hig-technologies/SKILL.md` → `.topics/apple-hig-nfc/SKILL.md` → `references/nfc.md`.
2. `subskills/apple-hig-status/SKILL.md` → `.topics/apple-hig-progress-indicators/SKILL.md` → `references/progress-indicators.md`.
3. `subskills/apple-hig-menus-and-actions/SKILL.md` → `.topics/apple-hig-buttons/SKILL.md` → `references/buttons.md`.

Each chain resolves within `/tmp/hig-eval-1c1uhlf7/.agents/skills/apple-hig/`, with topic/reference paths relative to its named family. The local source guides identify a 2026-10-25 snapshot. Official links attribute local guidance; no browsing or current SDK validation occurred. No platform adaptation or new hardware feasibility claim is made: supported iOS NFC hardware is the supplied premise. Actual label format, deployment target, framework, backend contract and device matrix remain unspecified and require implementation verification. Reading guidance does not establish runtime support or independent review of the source snapshot.
