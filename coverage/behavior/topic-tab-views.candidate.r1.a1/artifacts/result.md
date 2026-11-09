# Revised Mac preferences interaction specification

## Basis and decisions

`interface.md` supplies macOS, nine icon-only tabs with duplicate icons, unrelated file saves on selection, large size changes that displace Close, and unspecified validation errors. It supplies no pane names, option inventory, code, or screenshots. Treat these as reported behavior, not independently reproduced results.

1. **Replace the nine-tab strip with one labeled pane-choice pop-up.** Keep the existing nine panes and their order; do not invent category mergers without their contents. The persistent label is **Preferences pane:**; the closed chooser displays the selected pane's name and the open menu marks that same choice. Use nine distinct, short, content-predictive noun phrases in title case. Remove duplicate icons; text is required, icons are optional. Do not ship numeric placeholders. The actual names are a content dependency, not evidence of a completed naming exercise. This is pane navigation within one preferences window, not app-level tab-bar navigation. Apple advises avoiding more than six tabs and evaluating another presentation already at six; a pop-up is the selected alternative here, accepting two activations in exchange for fitting nine choices. [Tab views — Best practices](https://developer.apple.com/design/human-interface-guidelines/tab-views#Best-practices), [Pop-up buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons#Best-practices).
2. **Navigation has no save side effects.** Choosing a pane changes only selection, title, and visible content. It never saves documents, unrelated files, or preferences, and never commits a field as a side effect of losing focus. Pane controls affect only their documented settings scope. If an existing control affects another pane, relocate it to the pane owning that effect, or identify a shared app-wide setting explicitly; do not duplicate independently editable values. The navigation prohibition and ownership contract implement Apple's self-contained-pane guidance. [Tab views — Best practices](https://developer.apple.com/design/human-interface-guidelines/tab-views#Best-practices).
3. **Keep the frame stable during pane changes.** Reuse one window; preserve its frame, top-left origin, and Close position across every selection, including panes with errors. Keep the chooser above the content, visible and inset within window-body margins. Fit larger content inside the body without automatic window growth; error text consumes body space rather than moving the frame. Choose initial dimensions from measured content and available display area, not invented universal pixel values. All content and correction paths must remain reachable at the smallest supported window size. This fixed-on-switch policy is a product decision addressing the reported failure. [Tab views — Anatomy](https://developer.apple.com/design/human-interface-guidelines/tab-views#Anatomy), [Windows — Best practices](https://developer.apple.com/design/human-interface-guidelines/windows#Best-practices).
4. **Preserve useful pane state.** Store selection, each pane's draft values, error details, focus target, and content position for the current app session. Closing hides the window and preserves drafts; reopening restores them and the last pane. Restart restores the last pane and committed preferences only. Explain near an uncommitted field: “Not applied. Press Return to apply a valid value. Unapplied edits are kept until you quit.” No silent normalization or loss on switching. These persistence and draft choices are explicit product policy, not guaranteed framework behavior. [Settings — macOS](https://developer.apple.com/design/human-interface-guidelines/settings#macOS).
5. **Handle validation locally without trapping navigation.** Keep raw text while editing, including harmless intermediate values. Show a field-associated explanation identifying the constraint and correction once an invalid complete value is evaluated. Keep the previous committed value active. Return explicitly requests validation and commitment for that field or declared atomic field group; invalid input produces no write and stays available for correction. Escape while editing restores the last committed field/group value and clears its error. Switching panes remains allowed; reopening the pane restores its invalid draft and explanation. Validate again before commitment. Persist only the owned setting, and report persistence failure locally while retaining the draft and previous committed value. The Return/Escape policy is a proposed interaction contract; actual constraints and atomic groups require the missing option inventory. [Entering data — Best practices](https://developer.apple.com/design/human-interface-guidelines/entering-data#Best-practices).

## State and transition contract

Each pane has a stable ID, unique display name, ordered fields, ownership mapping, and per-field constraints. Each setting declares app-wide or document-local scope before implementation. App preferences must not mutate open documents; document configuration should be separated from app preferences. Existing defaults remain unchanged pending an inventory; do not invent new defaults or system-preference overrides. [Settings — General settings and Task-specific options](https://developer.apple.com/design/human-interface-guidelines/settings#General-settings).

```text
state = {selectedPane, windowFrame, panes[id], committedSettings}
panes[id] = {drafts, errors, lastFocus, contentPosition}

selectPane(id):
    require id is one of the nine pane IDs
    if id == selectedPane: return                // no reset or write
    capture current pane's transient state       // navigation never commits
    selectedPane = id
    show retained state for id
    chooser.value = id; window.title = pane[id].displayName
    keep windowFrame unchanged
    keep focus on chooser                        // no surprise jump into content

edit(field, rawValue):
    retain rawValue in owning pane's draft
    evaluate only when meaningful; preserve intermediate entry
    do not write settings or documents

explicitCommit(fieldOrAtomicGroup):
    validate draft against declared constraints
    if invalid: show associated correction; keep committed value; return
    persist only declared setting keys
    if persistence succeeds: update committed values; clear draft errors
    otherwise: retain draft; show failure; keep previous active values

closeWindow(): hide; retain session drafts and pane state; do not commit
reopenWindow(): reuse same window; restore selected pane and session state
restart(): restore last pane ID if available, otherwise first pane;
           load committed values; do not restore session-only drafts
```

Chooser opening and cancellation leave selection unchanged. Committing a menu choice closes the menu and shows that pane; repeated selection is a no-op. The menu contains selections only, no Save or other commands, no Custom option, and no submenus. If restored selection no longer exists after a future version change, use the first available pane and update both title and chooser consistently. Longer localized labels must remain distinguishable in the open menu and selected display; widen or reflow the surrounding layout rather than reverting to icons.

Retain system window frame, movement, Close, and activation cues where the host supports them. Settings-specific guidance says to dim minimize/zoom, whereas generic Windows guidance supports normal minimization/resizing. Apply the more specific settings guidance for this auxiliary window; do not derive a general ban on resizing. The frame must never resize automatically on selection. [Settings — macOS](https://developer.apple.com/design/human-interface-guidelines/settings#macOS), [Windows — macOS](https://developer.apple.com/design/human-interface-guidelines/windows#macOS).

## Worked before/after

The following field names and values are illustrative, not supplied product facts. Assume pane A owns an app-wide retry interval accepting whole seconds from 1 through 60; pane B owns appearance.

**Before (reported pattern):** A person sees nine indistinguishable icons. They enter `0` in pane A, then select another icon. Selection saves an unrelated document and changes the window size enough to move Close out of reach. The brief does not establish whether the invalid edit survives.

**After:** The chooser displays A's approved text label. Entering `0` and pressing Return leaves the committed interval at its prior value, for example `10`, and displays “Enter a whole number from 1 to 60 seconds.” Choosing B changes only the pane, chooser selection, and title. The frame and Close coordinates stay fixed; neither preferences nor documents are written. Returning to A shows `0` and its correction. Entering `15` and pressing Return commits only the retry-interval setting; the error clears. Closing and reopening returns to A. A separate invalid draft would survive close/reopen during this session but would not survive app restart, as the nearby draft explanation states.

## Acceptance checks and status

**Passed — specification inspection only:** The contract provides a nine-choice alternative, text-label requirement, explicit ownership, navigation without saving, stable geometry, draft/error retention, close/reopen/restart behavior, and an illustrative correction path. Installed root, selected families, topic procedures, and supporting guides were read locally in that order for each route; no web lookup or SDK dependency was used.

**Failed — reported baseline, not runtime reproduction:** Nine duplicate icon-only choices fail distinguishability; unrelated file writes violate navigation isolation; moving Close out of reach violates reachability. The existence of validation errors alone is not a defect: the brief gives no evidence about their explanation or recovery.

**Not executed — implementation acceptance checks:**

| Check | Required observable result |
| --- | --- |
| Visit all nine choices, then reselect current choice | Every pane reachable; unique approved names; chooser, title, and displayed pane agree; no reset on reselection. |
| Open chooser, cancel it, then choose another pane | Cancel preserves current pane; committed choice closes menu and changes only navigation state. |
| Instrument preference and document writes while switching, including after editing | Zero writes caused by selection or focus loss; no unrelated file changes. |
| Commit valid, invalid, intermediate, and corrected values | Only explicit valid commits change owned settings; invalid/intermediate input remains editable; correction clears errors. Use actual constraints, locale-sensitive values, and appropriate paste input. |
| Switch away from an invalid draft and back | Draft and explanation retained; navigation remains available; previous committed value remains active. |
| Simulate persistence failure | No false success; previous committed value remains active; draft and actionable local failure remain available. |
| Switch between largest/smallest panes and add/remove errors | Window frame and Close coordinates unchanged; chooser remains visible; body content and error recovery reachable. |
| Test smallest supported display/window and expanded localized text | Labels distinguishable, no overlapping controls, no inaccessible content or displaced Close. |
| Close/reopen, restart, and restore an obsolete pane ID | Session drafts survive close/reopen; restart loads committed values and last available pane; missing ID safely falls back. |
| Open preferences repeatedly with several documents open | One reused app-preferences window; no wrong-document mutation or cross-pane side effects. |
| Keyboard, pointer, and assistive technology testing on Mac | Chooser can open, select, and cancel; selected state is exposed; field/error relationships and correction path are usable; focus survives switching as specified. |

## Evidence limits

This deliverable is a framework-agnostic design specification. No implementation, test runner, Mac device, Apple SDK, GUI, keyboard interaction, or accessibility execution was available or performed. No runtime check above is claimed to pass. Layout measurements, native rendering, assistive behavior, real setting constraints, defaults, capability handling, and storage atomicity remain unverified. Nine final pane names and actual control ownership require the absent content inventory; the worked example does not fill that gap.

Sources are the installed package's local English HIG-derived snapshots dated 2026-10-25, not SDK documentation or independently verified current web pages. Official links identify provenance and relevant sections; they were not fetched. No newer-release or API-availability claim is made.
