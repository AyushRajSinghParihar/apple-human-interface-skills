# Mac catalog author entry audit

Scope: the proposed macOS control described in `interface.md`. This is a specification review, not an inspection of running software. The brief permits both existing authors and new text.

## Ranked verified findings

Ranks reflect task impact, not measured frequency. All three findings are verified against the supplied description only.

| Rank | Observed behavior | Effect and decision | Guidance |
|---|---|---|---|
| 1 — High | “silently selects the first suggestion on blur” | An unrelated name can replace the intended author without deliberate acceptance. Remove implicit selection on focus departure; preserve typed text and commit only the intended value. | Combo-box procedure requires explicit commit policy and stored/displayed agreement; [Combo boxes — Best practices](https://developer.apple.com/design/human-interface-guidelines/combo-boxes#Best-practices) preserves free entry. The exact blur policy below is an application decision. |
| 2 — High | “prevents any unlisted text” | Blocks the explicitly supported task of entering a new author. Accept custom names; absence from suggestions is not an error. Retain the editable combo-box model. | [Combo boxes](https://developer.apple.com/design/human-interface-guidelines/combo-boxes) combines suggestions with custom entry; [Text fields — macOS](https://developer.apple.com/design/human-interface-guidelines/text-fields#macOS) recommends this combination for the task. |
| 3 — High | “no way to navigate suggestions by keyboard” | Keyboard users cannot inspect and choose suggestions through the offered list. Provide a complete keyboard route for opening, navigating, accepting, dismissing, and leaving it. | [Keyboards — Best practices](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices) calls for Full Keyboard Access support and testing; [Focus and selection — Best practices](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices) covers reachability and focus feedback. Exact bindings below are proposed behavior, not quoted HIG requirements. |

## Decisions and corrected contract

Use one editable author combo box with a persistent **Author:** label. Keep an existing record’s author as its initial value. For a new record, start empty: the brief supplies no meaningful default, so choosing the first author would invent data. Apple advises a meaningful listed initial value *where possible*, not an arbitrary first item. Keep suggestion names readable without truncation, sizing to content where practical. These choices follow [Combo boxes — Best practices](https://developer.apple.com/design/human-interface-guidelines/combo-boxes#Best-practices).

Treat the 1,200 entries as a suggestion pool, not a whitelist. As an application recommendation, filter by typed text with stable ordering and let users scroll through every matching result. Do not impose a hidden results cap. An empty match list says “No matching suggestions — you can use this name”; it does not invalidate the field. No evidence establishes that the existing list is slow or visually unusable.

Maintain separate state:

```text
draftText                 // visible editable value
suggestions               // curated existing-author records {id, name}
matchingSuggestions       // derived from draftText; filtering never rewrites it
activeSuggestionId = none // navigation target, not a committed selection
committedAuthor           // Existing(id, name) | Custom(text) | Empty
listOpen
```

Preserve spelling, diacritics, punctuation, script, and internal spacing. Do not introduce a name-format restriction unsupported by the catalog requirements. Match filtering may be forgiving without changing stored text. For this specification, exact unique name equality resolves to an existing author; duplicate names require explicit record selection, otherwise retain a custom value rather than guess an identity. Explicit suggestion selection stores its ID and displays its name. Editing that text clears the explicit identity association. Custom entry does not append to the curated suggestion list. Persistence or creation of a reusable author record is outside this control’s contract.

```text
on edit or paste(text):
    draftText = text
    clear explicit identity and activeSuggestionId
    recompute matches; open list

on Down when closed:
    open list; highlight first match if present; leave draftText unchanged
on Down/Up when open:
    move highlight through matches; reveal active row; do not wrap
    leave draftText and committedAuthor unchanged
on Return when list open and active row exists:
    accept that row explicitly; set draftText = row.name
    commit Existing(row.id, row.name); close list; retain field focus
    consume this Return so it cannot also submit the surrounding form
on Return otherwise:
    commitDraft(); close list
on pointer selection(row):
    perform the same explicit acceptance as Return on an active row
on Escape when list open:
    close list; clear highlight; preserve draftText and prior committed value
on Tab, Shift-Tab, or pointer focus departure:
    commitDraft(); close list; clear highlight; allow normal focus traversal
    never accept a merely highlighted row

commitDraft():
    if unchanged explicitly selected name: retain its Existing identity
    else if exactly one suggestion has exactly draftText: commit that Existing
    else if draftText is empty or whitespace-only: commit Empty
    else: commit Custom(draftText)
```

Here, committing updates the form’s author value; it does not save the entire catalog record. Empty is a neutral field state because requiredness is unspecified. If the product requires an author at record save, reject Empty with “Enter or choose an author,” retain the draft, and identify the field. List membership is never a validation condition. Validation timing, useful feedback, and logical Tab traversal are supported by [Text fields — Best practices](https://developer.apple.com/design/human-interface-guidelines/text-fields#Best-practices).

Allow ordinary text selection, caret movement, copy, paste, and undo. Do not intercept keys during input-method composition. A keyboard-operable disclosure affordance can toggle the suggestion list without changing the value; preserve platform focus conventions. Show field focus and the active row distinctly from a committed author. On filtering, clear stale highlights rather than silently accepting a replacement. These are implementation requirements for the proposed contract; native behavior must be checked in the eventual stack. Escape with the list closed delegates to the surrounding form’s established cancellation behavior.

## Worked before/after

Illustrative fixture, not supplied catalog data: suggestions include `Ada Lovelace` and `Alan Turing`; `N. K. Jemisin` is absent.

| Action | Before, as described | Corrected behavior |
|---|---|---|
| Type `N. K. Jemisin` | Unlisted entry is prevented; rejection UI is unspecified. | Text remains editable; no matching suggestion is an informational state. |
| Tab to next field | First suggestion is silently selected; the exact name is unknown. | Commit `Custom("N. K. Jemisin")`; displayed and stored name agree; suggestions remain unchanged. |
| Type `Al`, press Down, Return | Suggestions cannot be navigated by keyboard. | Highlight `Alan Turing` without changing `Al`; Return explicitly commits that existing record and displays its name. |
| Type `Al`, highlight a row, press Tab instead | Blur selects the first suggestion. | Commit custom `Al`; highlighting alone is not consent to replace it. |
| Open suggestions, move highlight, Escape | Not specified. | Close list; preserve draft and committed value. |

## Acceptance checks and status

**Passed — static review:** platform, free-entry requirement, suggestion count, and all three reported behaviors are explicit in `interface.md`. Local installed procedures and guides support the audit route. The corrected specification separates draft, navigation target, and committed value.

**Failed — supplied proposal:** custom-entry preservation, noncoercive blur behavior, and keyboard suggestion navigation. These are failures of the documented proposal, not executed test results.

**Not executed — implementation acceptance:**

- Select an existing author by pointer and keyboard; both store the same ID and display name. Typing an exact unique name gives the intended equivalent result.
- Enter an unlisted Unicode name, paste it, then Tab or click away: preserve it exactly; never replace it with the first suggestion or mutate the suggestion pool.
- Traverse suggestions with arrows, including first/last boundaries; reach every matching item among the 1,200. Highlight alone changes neither draft nor committed author.
- Escape dismisses without replacement; Return accepts only an active suggestion, otherwise the draft. Tab and Shift-Tab leave in logical order without a focus trap.
- Exercise empty, whitespace-only, partial, no-match, duplicate-name, edited-existing-name, and long localized-name cases. Empty has no invented requiredness; any later required-field error preserves input and explains correction.
- Verify long suggestions remain identifiable and full entered text is inspectable by caret navigation without data loss. Check filtering responsiveness with the actual dataset; no latency threshold is established here.
- On an actual Mac, test ordinary keyboard navigation and Full Keyboard Access, focus indication, text editing shortcuts, input-method composition, and assistive output for the label, value, expanded state, and active suggestion. No accessibility execution or conformance conclusion is claimed.

## Evidence limits and route

Only a short textual brief was supplied: no markup, source implementation, screenshot, dataset, persistence model, form layout, validation policy, or executable app. Labeling, dimensions, contrast, truncation, loading speed, duplicate identities, and assistive semantics are unknown, not verified defects. Examples and state transitions above are proposed corrections. There was no device, GUI, SDK, compilation, or runtime execution, and no web browsing. Official links identify the articles underlying local guidance; they were not fetched.

Installed package root: `.agents/skills/apple-hig/`. Read order: root `SKILL.md`; `interface.md`; relevant rows of `references/topic-index.md`; Selection and input and Inputs family `SKILL.md` files; their Combo boxes, Text fields, Keyboards, and Focus and selection topic `SKILL.md` procedures; then each corresponding local reference guide. These routes cover the supplied combo box, its editable field and suggestion list, commit semantics, and keyboard interaction. This review does not assume AppKit, SwiftUI, or another Apple SDK. Local guides identify a 2026-10-25 snapshot; current online behavior was not verified.
