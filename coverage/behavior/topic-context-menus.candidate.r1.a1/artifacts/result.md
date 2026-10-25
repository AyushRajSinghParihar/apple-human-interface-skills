# Result

Patched interface.md in place, replacing the four-sentence description with an implementable action and selection contract for macOS and iPadOS.

## Decisions and patch summary

- Replace the all-app-command popup with a short item-specific Rename… / Delete contextual menu. Empty-space invocation offers no file menu.
- Preserve multiple selection when invoking on a selected entry; invoking on an unselected entry first selects that entry. Freeze target IDs and archive identity, then revalidate before mutation.
- Expose Rename… in File and Delete in Edit on Mac. Provide labeled, persistent in-app actions on iPad; its often-hidden menu bar cannot be the sole alternate route.
- Hide ineligible contextual commands consistently; retain dimmed ordinary commands. This is a surface-specific rule, so “stop hiding every disabled command” would be the wrong repair.
- Delete the entire eligible selection atomically, never just the last clicked item or an eligible subset. Add explicit failure, cancellation, undo/redo, and stale-target behavior.

The first, third, and fourth decisions follow the locally supplied [Context menus guidance](https://developer.apple.com/design/human-interface-guidelines/context-menus#Best-practices), [Menus labels guidance](https://developer.apple.com/design/human-interface-guidelines/menus#Labels), and [menu-bar platform guidance](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#iPadOS). Named recovery and Mac Undo/Redo shortcuts follow [Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#macOS). These official links identify the local snapshots' sources; they were not opened online.

Exact target replacement, atomic transactions, eligibility predicates, iPad command-area design, and session history boundaries are product decisions. They make the repair testable rather than implying Apple mandates those exact choices. The specification requires recoverable archive edits; archive-engine support remains unverified.

## Worked before and after

Given an editable archive containing A.txt, B.txt, and C.txt, select A.txt and B.txt, with B.txt last clicked, then secondary-click A.txt.

Before, the supplied description says the menu includes unrelated app commands, Rename is hidden-only, and Delete acts only on B.txt. Disabled commands disappear without a predictable rule.

After, A.txt and B.txt stay selected. The contextual title reads “2 Selected Files”; only Delete is offered because batch Rename is unsupported. Delete removes both entries as one operation while C.txt remains. Undo Delete restores both entries, their paths, bytes, metadata, and selection. With one file selected instead, Rename… is also available through File on Mac or the persistent iPad command area, without invoking a contextual menu. If either selected file is ineligible, contextual Delete is hidden and ordinary Delete is dimmed; no partial deletion occurs.

## Acceptance checks and status

| Check | Status | Evidence |
| --- | --- | --- |
| interface.md changed in place and covers all four supplied defects | Passed, static specification review | Read back revised file: item-only menu, alternate Rename routes, full selection targeting, explicit availability rules |
| One/multiple/empty selection and unselected-item invocation have deterministic outcomes | Passed, static specification review | Target contract and acceptance checks 1–5 |
| Read-only/mixed eligibility, stale targets, failure, and recovery are specified | Passed, static specification review | Revalidation and lifecycle sections; acceptance checks 5–7 |
| Local routing order followed | Passed, instruction audit | Explicit root read; topic-index search; menus-and-actions family; context-menus, menus, the-menu-bar procedures before their references; patterns family and undo-and-redo procedure before its reference |
| Source checks with no applicability here | Not applicable | No toggled commands, submenu children, previews, or continuous adjustments were introduced |
| Native menus, above/below placement, localization, keyboard, touch, and assistive navigation | Not executed | No running interface or device evidence supplied |
| Actual archive transaction, rename validation, rollback, undo/redo, and save/reopen behavior | Not executed | This task changed a specification; no implementation or archive-engine test was run |

No failed checks were observed in the revised document review. This does not assert that an application passes the acceptance contract. The original description itself fails the intended scope, discoverability, selection, and availability checks.

## Evidence limits

Only interface.md and the installed local skill package were used. Guidance files were consumed one file per command, using cat or rg, with family and topic procedures read before supporting source guides. No web browsing occurred. The references identify themselves as dated snapshots derived from Apple guidance, not SDK documentation; no newer-release or API feasibility claim is made.

There was no device, Mac/iPad GUI, SDK compilation, accessibility execution, screenshot inspection, or application runtime test. Native rendering, focus order, assistive behavior, touch usability, and the archive engine's ability to retain undo data remain to be verified. interface.md contains concrete execution acceptance checks for that follow-up work.
