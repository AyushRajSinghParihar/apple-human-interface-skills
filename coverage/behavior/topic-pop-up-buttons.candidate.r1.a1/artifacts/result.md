# Mac export-format chooser

## Evidence and decisions

`interface.md` describes a macOS button labelled **Export** that immediately assigns a random saved format and never displays it. The format set is PDF, CSV, and image; CSV is unavailable for image-only documents. No implementation or rendered interface was supplied.

Replace that control with a **pop-up button** beside the label **Export Format:**. The closed button displays the actual selected format: **PDF**, **CSV**, or **Image**. The flat menu contains exactly those mutually exclusive choices, in that order. Opening it does not change the format. Selecting an enabled item saves that choice and closes the menu. Mark the saved item with a checkmark when open.

This follows [Pop-up buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons#Best-practices): use a flat single-choice menu, explain its purpose, supply a useful default, and reflect selection. A command button communicates an immediate action ([Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)); the existing Export label therefore misrepresents the setting change. The revised chooser performs no file export. Any actual export command is a separate product concern; this brief supplies no export workflow to revise.

Keep **CSV** visible and dimmed for image-only documents; it cannot be committed. Show adjacent text, **CSV is unavailable for image-only documents.**, while that restriction applies. Keep the chooser openable. This applies [Menus — Labels](https://developer.apple.com/design/human-interface-guidelines/menus#Labels) to preserve discovery of unavailable capabilities. A checkmark indicates the applied choice ([Menus — Toggled items](https://developer.apple.com/design/human-interface-guidelines/menus#Toggled-items)).

The following persistence and fallback rules are product decisions, not requirements attributed to Apple:

- Store one selected format per document; reopening that document restores it.
- Use PDF for a new document with no saved choice. PDF and Image are assumed valid for both document types because the brief gives only a CSV restriction.
- If a saved choice is missing, unknown, or becomes invalid, save PDF and display PDF together. When replacing CSV after a document becomes image-only, show **Format changed to PDF because CSV is unavailable for image-only documents.** Keep this notice until the next explicit selection or document switch.
- Preserve **Image** as the supplied format name. Its encoding and extension are unspecified; this specification does not silently equate it with PNG or JPEG.

## Interaction and state contract

Place the label and chooser together in the existing control's content location. Allow the control to fit the longest localized option and its indicator without clipping; wrap explanatory text below the row. No toolbar placement or pixel dimensions are inferred from the brief.

State consists of document identity, document revision, document type, saved format, menu-open state, and an optional highlighted menu item. The closed title and checkmark are derived from saved format, never stored independently. Highlight is tentative and has no save or preview effect.

| Event | Result |
| --- | --- |
| Load or switch document | Close any open menu; load and validate this document's saved choice; apply the fallback if necessary; render the resolved value. |
| Activate chooser | Open the menu with the current choice identified; do not save anything. |
| Move pointer or keyboard highlight | Move tentative highlight only. |
| Commit enabled option | Revalidate document identity, revision, and availability; save the option; update title/checkmark; close menu and return focus to chooser. |
| Commit current option again | Close menu; retain value; no duplicate save or other side effect. |
| Attempt disabled CSV | No state change or save. |
| Escape or click outside | Close menu, discard highlight, retain saved choice. |
| External saved-value/type change | Close stale menu; validate and render the latest state, applying fallback if needed. |

Framework-agnostic implementation contract:

```text
resolve(document):
    allowed = [PDF, IMAGE] if document.imageOnly else [PDF, CSV, IMAGE]
    value = document.savedFormat if document.savedFormat in allowed else PDF
    persist and publish value as one logical update if normalization is needed
    return value

openMenu():
    capture current document identity and revision
    show [PDF, CSV, IMAGE], with CSV disabled when imageOnly
    indicate resolve(currentDocument) as selected

commit(option, capturedIdentity, capturedRevision):
    if current identity/revision differs: close menu; refresh; return
    if option unavailable: return
    if option differs from savedFormat:
        persist and publish option as one logical update
    close menu; focus chooser

render():
    title = displayName(resolved savedFormat)
    checkedItem = resolved savedFormat
```

Persistence is a logical commit: do not publish a new selected value if saving fails. Keep the prior value and show **Couldn’t save the export format. Try again.** This error handling is a proposed product rule; no storage mechanism was supplied.

Keyboard contract for implementation: Tab can reach the chooser; Space opens it; arrow keys move among enabled choices; Return commits the highlighted choice; Escape dismisses without commitment. Return while the menu is open must not trigger any surrounding export command. Use the host platform's established pop-up behavior where available. Do not add Custom, submenus, multiple selection, or an Export item to this option list.

## Worked before/after

**Before:** A document has saved format PDF. The user clicks **Export**. The brief says a random format is saved, so CSV is one possible result; the interface still says Export. The user cannot inspect or predict the saved choice. The brief does not establish whether the existing implementation prevents invalid CSV assignments.

**After:** The same document shows **Export Format: [PDF ▾]**. Opening the menu shows PDF checked, with CSV and Image available. Highlighting CSV and pressing Escape leaves PDF saved and displayed. Reopening and committing CSV saves CSV, closes the menu, and shows **Export Format: [CSV ▾]**. Repeated selection of CSV has no further effect.

If that document becomes image-only, the chooser closes, PDF is saved and displayed, and the fallback notice explains why. Opening the menu now shows PDF checked, CSV dimmed, and Image enabled. Committing Image saves and displays Image. No random selection or file export occurs.

## Acceptance checks and status

**Passed — static specification review:** the revised contract names a persistent single choice; defines label, options, default, persistence, commit, dismissal, repeat selection, external changes, invalidation, and long-label handling; separates selection from command execution. These are document checks, not executed behavior.

**Failed — supplied interaction against the requested goal:** the brief explicitly says selection is random and shown nowhere. Thus the supplied design fails predictable choice and visible current-state checks. No runtime failure is claimed.

**Not executed — implementation acceptance checks:**

1. With no saved value, load a document: PDF is saved and displayed; reopen it and confirm restoration.
2. Select each enabled format: title, saved value, and menu checkmark agree; exactly one item is checked.
3. Open, highlight a different item, then Escape or click outside: saved value remains unchanged. Re-select the current option: no duplicate write.
4. Load an image-only document: CSV remains visible and disabled; attempted pointer/keyboard selection cannot save CSV; the reason is visible.
5. Change a CSV document to image-only: PDF is saved/displayed with the explanation. Change document or external value while the menu is open: stale events cannot modify the wrong document or overwrite newer state.
6. Inject a save failure: retain the previous value and display the error; retry succeeds without a hidden intermediate selection.
7. Exercise the specified keyboard flow, focus restoration, and surrounding Return behavior on macOS. Verify assistive technology identifies the chooser's purpose, current value, selected option, and disabled CSV state.
8. Test long translated labels and narrow layouts for readable full option labels, no overlap, and usable targets. Inspect actual native/custom rendering and press/focus feedback.

Custom cancellation is not applicable: there is no Custom option. Empty selection, nested menus, and all-disabled options are outside this fixed format model; PDF and Image remain available under the stated assumption.

## Evidence limits and audit route

Only local files were used. Explicitly read the installed root `apple-hig/SKILL.md`, then `interface.md` and relevant rows of `references/topic-index.md`; read `subskills/apple-hig-menus-and-actions/SKILL.md`; read the Pop-up buttons and Buttons topic procedures before their supporting guides; then read the Menus topic procedure before its supporting guide. All paths resolve within `.agents/skills/apple-hig/`. Each file was consumed in a separate shell command.

The local supporting guides identify a 2026-10-25 snapshot. Official links above are attribution from those files, not live verification. No web access, SDK/API verification, implementation, builds, GUI interaction, device testing, or accessibility execution occurred. Native appearance, keyboard behavior, assistive behavior, storage reliability, format encoding, and actual export results remain unverified. The proposed document scope, PDF default, invalid-value fallback, and error behavior require implementation against the eventual product data model.
