# Mac catalog author entry audit

## Scope and decisions

Reviewed `interface.md`, a behavioral brief for macOS: authors may come from 1,200 suggestions or be entered as new text. No implementation or screenshot was supplied. “Verified” below means explicitly stated in that brief, not observed in a running application.

Retain an editable combo box: this is an open text domain with suggestions, not a closed choice. Use a persistent **Author:** label. On an existing record, show its saved author; on a new record with no meaningful author, leave the field empty. Do not invent an author merely to supply a default. Apple recommends a meaningful listed initial value where possible, not necessarily the first item. Custom entry must not automatically mutate the suggestion list. [Combo boxes — Best practices](https://developer.apple.com/design/human-interface-guidelines/combo-boxes#Best-practices), [Text fields — macOS](https://developer.apple.com/design/human-interface-guidelines/text-fields#macOS).

## Ranked verified findings

| Rank | Observation and effect | Correction and basis |
| --- | --- | --- |
| 1 — High | The control prevents all unlisted text. This blocks the explicitly supported task of entering a new author. | Accept custom author text independently of suggestion membership. A Mac combo box combines suggestions with free entry. [Combo boxes](https://developer.apple.com/design/human-interface-guidelines/combo-boxes). |
| 2 — High | Blur silently selects the first suggestion. Leaving the field can replace the intended author and create an incorrect attribution. | Preserve the draft on blur; only explicit suggestion activation substitutes its value. Keep displayed and stored values consistent. This correction applies the installed combo-box procedure’s preservation/commit guidance; the article’s meaningful-default recommendation does not authorize replacing entered text. [Combo boxes — Best practices](https://developer.apple.com/design/human-interface-guidelines/combo-boxes#Best-practices). |
| 3 — High | Suggestions have no keyboard navigation. Keyboard users cannot complete the suggestion-selection task. | Provide opening, traversal, activation, dismissal, and exit using the keyboard, with focus distinct from committed selection. Apple calls for Full Keyboard Access support and testing. Exact bindings below are the proposed contract, not quoted HIG mandates. [Keyboards — Best practices](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices), [Focus and selection — Best practices](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices). |

Ranks prioritize task blockage, then attribution integrity, then suggestion access; all three should be fixed before release. No evidence establishes missing labels, truncation, inaccessible semantics, latency, or a bad visual layout.

## Corrected behavior contract

Framework independent; no Apple SDK is required to express or implement this contract.

State:

```text
draft: exact editable text
accepted: null | { text, suggestionId?: id }
saved: previously persisted author (changed only by the enclosing Save)
matches: relevant suggestions derived from draft
activeId: highlighted suggestion, or null
open: whether suggestions are shown
```

Keep suggestion identity separate from display text. Choosing a suggestion stores its full text and identity. Typing exactly one uniquely matching suggestion name may resolve to the same identity on acceptance. Duplicate names must not resolve arbitrarily: retain text without an identity until the person explicitly chooses a distinguishable entry. These identity rules are proposed product decisions, not facts supplied by the brief.

```text
on edit or paste(text):
    draft = text
    invalidate any accepted identity that no longer matches
    matches = relevantMatches(text)
    activeId = null                 // no implicit first choice
    open = true

on Down with list closed:
    open list; highlight first available match without changing draft
on Up/Down with list open:
    move highlight among matches; scroll highlighted row into view
    do not change draft, accepted, or saved
on Return with an active row, or pointer activation of a row:
    draft = row.fullText
    accepted = {text: draft, suggestionId: row.id}
    close list; clear highlight; keep field focus
    consume Return so it does not also submit the form
on Return without active row:
    acceptDraft(); close list       // no first-result fallback
on Escape with list open:
    close list; clear highlight; preserve draft and accepted
on Tab / Shift-Tab / blur:
    acceptDraft(); close list; clear highlight
    allow normal focus departure; never activate highlighted row
on enclosing Save:
    acceptDraft()
    persist accepted only if product validation succeeds

acceptDraft():
    preserve draft text; never substitute a suggestion based on rank
    resolve identity only for an exact, unique name match
    otherwise accept as custom text without suggestionId
    do not append custom text to the suggestion corpus
```

Treat suggestion highlight as a navigation target, not an accepted author. Preserve ordinary editing, selection, copy/paste, undo, and input-method composition; suggestion key handling must not intercept keys while composing text. Tab must leave the field in logical form order, with a visible focus indicator. [Text fields — Best practices](https://developer.apple.com/design/human-interface-guidelines/text-fields#Best-practices), [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards).

No author syntax, requiredness, or length limit is supplied. Do not fabricate an alphabetic-only rule, strip punctuation/diacritics, or reject text because no suggestion matches. Proposed policy: allow an empty draft and represent an accepted empty value as null; the enclosing catalog may require an author at Save, showing “Enter an author” and retaining the draft if so. Any additional domain validation needs a documented product rule and understandable inline feedback. [Text fields — Best practices](https://developer.apple.com/design/human-interface-guidelines/text-fields#Best-practices).

For 1,200 suggestions, propose filtering as people type and a scrollable result list with all matching entries reachable; avoid an arbitrary inaccessible result cap. Show “No suggestions” without disabling custom entry. Choose relevance and locale-aware matching deliberately; matching must not rewrite the accepted spelling. This is a usability recommendation, not a verified performance finding or an Apple numerical limit. Keep full names available during editing and selection; widen or wrap suggestion rows where needed rather than abbreviating stored names. Test long localized names rather than claiming they already fit. [Combo boxes — Best practices](https://developer.apple.com/design/human-interface-guidelines/combo-boxes#Best-practices).

## Worked before/after

Illustrative fixture: suggestions include `Ada Lovelace` and `Alan Turing`; `N. K. Jemisin` is absent.

| Action | Before, as specified | Corrected result |
| --- | --- | --- |
| Type `N. K. Jemisin`, then Tab | Custom entry is blocked; blur selects the first suggestion. | Text remains `N. K. Jemisin`; accepted as custom; focus advances; suggestions remain unchanged. |
| Type `Al`, press Down to highlight `Alan Turing` | Keyboard navigation is unavailable. | Highlight appears; draft remains `Al`; no author is selected yet. |
| Press Return on that highlighted row | No keyboard route is supplied. | Field and accepted value become `Alan Turing` with its ID; list closes; form is not submitted. |
| Instead press Escape or Tab while `Alan Turing` is highlighted | Blur substitutes the first suggestion. | Escape preserves `Al` and closes; Tab accepts `Al` as custom and advances. Neither activates the highlight. |

The brief does not specify the exact ordering or intermediate text behavior of the original list; these examples do not claim a runtime trace.

## Acceptance checks and status

**Passed — document inspection:** macOS and the open author domain are explicit; an editable combo box fits that domain. The proposed contract covers choosing a listed author, custom entry, focus departure, cancellation, identity, and preservation of the suggestion corpus. This is specification coverage only.

**Failed — supplied behavioral specification:** permitted custom entry; preservation on blur; keyboard navigation of suggestions. These correspond to the three ranked findings, not executed test failures.

**Not executed — implementation acceptance:**

| Scenario | Required observable result |
| --- | --- |
| Choose a listed author by pointer and keyboard | Same full text and identity; Return is consumed; saving persists the displayed value. |
| Type/paste an unlisted name, then Tab, blur, or Save | Exact text is retained; no first-result substitution; no suggestion-list mutation. |
| Highlight a row, then Escape or Tab | Escape dismisses without substitution; Tab accepts draft and exits, without activating the row. |
| Empty, partial, and zero-match input | Editing remains possible; empty follows documented requiredness; partial/unlisted text is not itself invalid. |
| A documented invalid domain value, if any | Understandable corrective feedback; draft retained; no unrelated author persisted. No such rule is currently supplied. |
| Type a unique exact suggestion name; test duplicate names | Unique exact entry agrees with explicit selection; duplicates never silently pick an identity. |
| Traverse all matches from the 1,200-item corpus | Filtering preserves reachability; active row stays visible; boundaries do not trap focus. |
| Long names, accents, apostrophes, non-Latin text, locale changes, IME composition | Full values survive display, editing, selection, and persistence; composition keys are preserved. |
| Tab/Shift-Tab, arrows, Return, Escape, editing shortcuts | Field is reachable and escapable; target highlight is distinct from accepted value; normal editing works. |
| Mac Full Keyboard Access and assistive technology | Entire task can be completed; label, expanded state, active suggestion, and accepted value can be determined. Actual semantics and announcement order require execution. |

## Evidence limits and route

Only `interface.md` supplies interface evidence. No code, image, runnable UI, Apple SDK, Mac device, GUI, performance measurement, accessibility tree, or assistive-technology execution was available or used. No web browsing occurred. Official links above identify the sources represented by the installed snapshots; they were not fetched or checked for newer changes. Accessibility execution remains unverified, not a claimed defect.

Installed package route, read explicitly from `.agents/skills/apple-hig/`: root `SKILL.md`; Selection and input family → Combo boxes and Text fields procedures → respective source guides; Inputs family → Keyboards and Focus and selection procedures → respective source guides. The complete topic index was searched for combo boxes, text fields, keyboard, and related concepts before finalizing the route. Each file was read in its own command. No closed-choice control or other supplied control needed a separate route.
