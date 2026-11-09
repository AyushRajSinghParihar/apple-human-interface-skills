# Attachment-action repair

Patched `interface.md` in place with a concrete action/state contract. Changes cover row-bound attachment context, missing selection, anchored wide-iPad presentation and compact adaptation, explicit labels, a separate six-field form sheet, and cancellation/save/draft outcomes. Delete Everything and its handler are removed from this flow.

## Decisions

- Retain a short action sheet after deliberate Use Attachment activation. It is a decision rather than an explicit request to reveal a menu; the latter would call for a menu. See [Action sheets](https://developer.apple.com/design/human-interface-guidelines/action-sheets#iOS-iPadOS).
- Anchor the wide-layout choice to its row and adapt compact windows. Outside dismissal cancels without mutation; native iPad presentation may omit a visible Cancel row. See [Popovers](https://developer.apple.com/design/human-interface-guidelines/popovers#Best-practices).
- Replace Yes with Use Attachment and Other with Enter Details Manually. The exact positive outcome is an explicit product assumption: the supplied text does not explain Yes. Clear outcome labels follow [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Content).
- Move the six-field task into a centered iPad form sheet, with Cancel/Done, validation, pending/failure handling, and explicit resolution of unsaved edits. Centering suits the form task; the short wide-layout choice requires anchoring. See [Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets#iOS-iPadOS).
- Remove unrelated destruction rather than merely relabeling or recoloring it. No attachment deletion command is invented. Captured IDs and revalidation prevent a later selection from redirecting an operation. These are product scope and data-integrity decisions.
- Use destructive semantics only for explicit Discard Changes, with Keep Editing providing safe cancellation. No critical alert is needed for the ordinary attachment alternatives. See [Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices). The guidance permits different treatment of deliberately requested destruction; this report does not impose a universal ban on destructive defaults.

## Worked before/after

Example fixture: claim C17 contains receipt.pdf (attachment A4); claim C18 is unrelated.

| Step | Before, as supplied | After, specified |
| --- | --- | --- |
| Start from A4 | Choice centered far from trigger | Use Attachment opens a choice anchored to A4's row in a wide window, naming receipt.pdf |
| Positive path | Yes has no stated outcome | Use Attachment associates A4 with C17 once |
| Manual path | Other starts six fields | Enter Details Manually closes the choice, then opens Attachment Details with the existing six fields |
| Leave manual edits | Unspecified | Cancel/swipe offers Discard Changes or Keep Editing; dismissing that decision retains edits |
| Destruction | Delete Everything removes unrelated claims | No claim-deletion action or handler exists in this flow; C18 is unchanged |
| Missing selection | Selection may be absent; outcome unspecified | Explicit row context suffices; without row context or selection, no choice opens and selection guidance appears |
| Selection changes mid-flow | Unspecified | Captured C17/A4 remain the target; missing/invalid A4 prevents mutation and preserves any manual draft |

This is a worked specification example, not an executed test.

## Acceptance checks and status

**Passed — static document inspection:** the revised specification addresses all supplied defects: distant presentation, ambiguous labels, questionnaire scope, unrelated destruction, and missing selection. It includes an action-to-outcome table, dismissal outcomes, compact adaptation, pending/failure states, and stale-context protection. Both requested artifacts are written.

**Failed:** no outstanding revised-document check identified during static review. The supplied original fails the document-level scope and labeling checks. No runtime failure or runtime pass is claimed.

**Not executed:** all behavioral checks in `interface.md`, including idempotent association, unchanged unrelated claims, stale-ID rejection, missing-selection controls, save retry, draft restoration, all dismissal routes, repeated invocation, and nonstacking replacement. Implement these with fixture C17/A4/C18 and inspect stored data as well as visible outcomes. Also exercise wide/compact iPad layouts, rotation, enlarged text, keyboard visibility and cancellation, 44 × 44 pt target regions, return context, and assistive-technology interaction on the implementation.

## Evidence and limits

Explicitly read the installed root `.agents/skills/apple-hig/SKILL.md`, inspected the original `interface.md`, and searched the installed topic index. Read the Presentation and Menus and actions family routes, then the Action sheets, Popovers, Sheets, Alerts, and Buttons topic procedures before their corresponding source guides. Each file was read with its own cat command; index searches used rg. All paths were resolved within this installed package.

Only supplied local files and installed instructions were used. Official links identify the local snapshot's source sections; they were not browsed or independently verified. The guides identify a 2026-10-25 snapshot. They supply design guidance, not SDK verification. No app implementation, questionnaire schema, persistence model, device, SDK build, GUI session, native rendering, or accessibility execution was supplied or exercised. The revised file specifies required behavior rather than proving an app performs it.
