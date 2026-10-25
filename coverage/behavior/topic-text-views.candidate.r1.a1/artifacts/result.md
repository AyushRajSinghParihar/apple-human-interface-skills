# Revised Mac long-form note interaction specification

## Scope and evidence

`interface.md` reports that notes are screenshots, editing cannot select text, formatting resets scrolling, read-only notes show an active insertion cursor, and content includes long URLs and mixed scripts. These are supplied descriptions, not independently reproduced defects. This specification replaces that behavior; it does not implement an editor or assume an Apple SDK.

The primary task is sustained reading, selecting and copying, with editing when permission allows. Use a resizable Mac document workspace, a persistent textual note body, and one vertical scrolling owner. Keep app commands reachable through the menu bar in a Mac host; an implementation must supply an equivalent discoverable command surface if its host cannot integrate there. Preserve selection and work across app activation changes. These decisions follow [Designing for macOS, Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Best-practices).

## Decisions

### Actual text and independent permissions

Represent the note as Unicode text plus formatting spans and stable paragraph identifiers. Render a multiline, selectable text surface in both states. Screenshots may be supplementary previews, but cannot be the reading/editing representation. Retrieve original text and formatting for existing screenshot notes; if unavailable, mark migration unresolved rather than silently treating OCR as authoritative.

This follows the recommendation to choose a text view for lengthy or formatted content and allow useful text to be selected and copied: [Text views, Best practices](https://developer.apple.com/design/human-interface-guidelines/text-views#Best-practices). “Text view” here describes capabilities, not a particular class or framework.

| Capability | Read-only | Editable |
|---|---|---|
| Read, scroll, select across lines, Select All, Copy, Find | Available | Available |
| Text insertion caret | Never shown | Shown only when body has input focus and an insertion target |
| Selection highlight and keyboard focus indication | Available; distinct from an insertion caret | Available |
| Type, paste, cut, delete, drop text, format, undo/redo mutations | Rejected at the command/model boundary | Available for valid target and permission |
| Status | Persistent “Read-only” with known reason, if supplied | “Editable” and save status |

Read-only does not disable the entire body: it remains focusable and selectable. Typing must neither mutate text nor silently change mode. Do not invent a reason for missing permission. A pointer text-selection cursor can remain appropriate in either mode; the misleading behavior being removed is the active insertion caret.

Open according to authoritative write permission; do not require an extra Edit mode for writable notes. Permission changes update the same surface without rebuilding the document. On revocation, stop mutations immediately, finish or cancel composition without committing unauthorized text, retain existing unsaved work as a recoverable draft, and display “Read-only — unsaved changes retained” when applicable. Restoring permission retains selection and viewport; do not unexpectedly focus the body or show a caret until it has input focus. These transition details are product decisions.

### Reading, reflow and scripts

Use semantic title, body and supporting-status roles. Prefer the host's system text font with appropriate script fallback; otherwise use a legible installed font stack. Initial product choices: body 15 pt Regular, line height approximately 1.4 times body size, title 22 pt Semibold, supporting text 13 pt. These are proposed defaults, not HIG-mandated editor dimensions. Prefer a reading column around 70 body-character widths, shrinking to available width with margins; use all necessary vertical space.

Provide View > Text Size at 100%, 125%, 150%, 175% and 200%, plus reset. This scales presentation and controls without changing saved formatting. Reflow and expand controls; no essential text is truncated. Support an optional heavier reading weight without changing document styles. macOS has no Dynamic Type; this is an explicit accommodation. Loose leading and adaptable hierarchy are supported by [Typography](https://developer.apple.com/design/human-interface-guidelines/typography#Using-system-fonts), its [macOS qualification](https://developer.apple.com/design/human-interface-guidelines/typography#macOS), and [Accessibility, Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

Wrap paragraphs to the column. Permit an unbroken URL to wrap visually at safe character/grapheme boundaries when needed; never insert spaces, hyphens or newlines into stored/copied content. Do not ellipsize, clip, or require horizontal scrolling to read prose or URLs. Copy returns the selected underlying text; a full selected URL remains byte-for-byte equivalent in its original encoding after round-trip serialization.

Use a Unicode-aware shaping and bidirectional text engine. Paragraph alignment follows its own language/direction; short interface labels follow interface direction. Preserve internal order of URLs, numbers and identifiers; isolate embedded directional runs through presentation metadata without adding invisible characters to the stored note. Selection endpoints follow valid grapheme boundaries, including combining marks and emoji. Do not reverse strings manually. These implementation choices apply [Right to left, Text alignment and Numbers and characters](https://developer.apple.com/design/human-interface-guidelines/right-to-left#Text-alignment); shaping and mixed-direction editing remain runtime verification requirements.

### Commands, focus and persistence

The body accepts precise pointer selection, word selection and keyboard range extension. Separate document selection from the control receiving commands. Opening a menu retains the document selection; formatting acts on that range. After a formatting menu command, return input to the originating body. App switching preserves selection, viewport, draft and undo history, while active/inactive selection appearance indicates the command target. Follow [Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices).

| Command surface | Binding | Availability/result |
|---|---|---|
| Edit > Select All / Copy | Command-A / Command-C | Body target in either state; Copy requires selection |
| Edit > Cut / Paste | Command-X / Command-V | Editable body; Cut requires selection |
| Edit > Undo / Redo | Command-Z / Shift-Command-Z | Editable and corresponding history available |
| Edit > Find / Find Next / Previous | Command-F / Command-G / Shift-Command-G | Either state; matches are text ranges |
| Format > Bold / Italic / Underline | Command-B / Command-I / Command-U | Editable; range changes style, collapsed selection changes subsequent typing style |
| File > Save | Command-S | Writable draft; requests persistence immediately |
| View > Text Size | No new shortcut assigned | Either state; preserves document content |

Use the same command dispatch and availability for menus and any future contextual controls. Preserve system shortcuts, input-source switching and Option-character entry; do not capture all keystrokes globally. These bindings use [Keyboards, Standard keyboard shortcuts](https://developer.apple.com/design/human-interface-guidelines/keyboards#Standard-keyboard-shortcuts); the guide's legacy/system entries are not an implementation API contract.

Keyboard completion path: reach the body through host keyboard navigation, select with Shift-arrow or Select All, Copy; in editable notes type or format, then Save. Find opens a labeled query control; Enter advances, Shift-Enter reverses, Escape closes Find and restores body focus/selection. Find's query is short entry, while the note remains the multiline body. Preserve host text-navigation conventions; Tab/Shift-Tab must offer a route into and out of the body without a keyboard trap. Full Keyboard Access must reach every exposed action. No essential action depends on a bottom-of-window control: [Layout, macOS](https://developer.apple.com/design/human-interface-guidelines/layout#macOS).

Apply each edit/format as one undoable transaction. Autosave after a settled transaction; show “Saving…”, then “Saved” only after persistence acknowledges that revision. Failure retains the draft and displays a persistent error with a keyboard-reachable Save retry. Closing or switching notes cannot discard an unacknowledged draft: retain it durably or keep the note open with the failure visible. Persistence timing and draft recovery are product requirements, not inferred existing capabilities.

### Stable scrolling

Use one primary vertical scroller for the body, no outer same-axis page scroller. Keep its scrollbar consistent with host preferences. Put commands and status outside the body viewport so they do not obscure text. Preserve host scroll gestures and keyboard scrolling.

Before formatting, resizing, text enlargement or mode changes, capture a logical anchor: the first visible text position, its paragraph identifier and offset, and its vertical position relative to the viewport. Restore that position after layout; do not reuse a raw scroll offset when wrapping changed. Preserve the selected range and active end as separate state. If an anchor was deleted, choose the nearest surviving text position; clamp at document boundaries.

Typing, Find, selection extension and an explicit action on an offscreen selection may reveal the relevant target, moving only enough to expose the caret, match or active selection edge. Formatting an already visible selection must not center it or jump to the top. If formatting an offscreen selection, minimal reveal is permitted. Manual scrolling alone must not snap back to the caret. These rules apply [Scroll views, Best practices](https://developer.apple.com/design/human-interface-guidelines/scroll-views#Best-practices).

```text
mutate(command):
    require currentWritePermission AND editable
    capture selection, activeEnd, visibleTextAnchor
    apply command as one transaction; map text positions through change
    layout without replacing document identity
    restore mapped selection and visibleTextAnchor; clamp to bounds
    if command needs target reveal: minimallyReveal(activeTarget)
    persist revision; retain draft until acknowledged

setPermission(permission):
    capture selection and visibleTextAnchor
    update write gate and exposed readOnly state
    if readOnly: remove insertion caret; disable mutation commands
    retain selection, recoverable draft and viewport
```

### Accessible state contract

Expose the body as named multiline text (“Note body”), including its text value, selectable range and read-only/editable state through the host accessibility bridge. Expose status as text, not color alone. Keep task order predictable: note context/status, commands, body, with Find entering the order when opened. Use host text semantics rather than exposing each painted glyph as a separate element. This is a required interface contract, not evidence that a particular bridge supports it.

Use adaptive text/background and selection colors; measure actual light, dark and Increase Contrast combinations. Follow the local guide's contrast-table scope rather than claiming numeric ratios alone establish conformance. Verify keyboard and assistive navigation along the same read/select/copy/edit/save task: [Accessibility, Vision, Mobility and Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

## Worked before/after

Fixture: a note with 200 paragraphs. Paragraph 120 contains:

```text
Review café 👩🏽‍💻 before release.
مراجعة الإصدار 123 — https://example.test/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa?release=123
עברית עם English 456
```

Before, as described in the brief: a screenshot prevents selecting the URL; editable text cannot be selected; applying formatting returns the reader to the top; a read-only note still promises entry with an active caret. The brief does not establish exact geometry, font, script ordering or saved-data behavior.

After: open read-only, scroll to paragraph 120, select the entire wrapped URL and Copy. The clipboard contains exactly the original URL with no visual wrap characters; “Read-only” is visible and there is no insertion caret. Typing, paste and Bold leave the document unchanged. Permission becomes writable without changing the reading anchor. Focus the body, select “café 👩🏽‍💻” across its full graphemes and invoke Command-B. The range becomes bold, selection remains, paragraph 120 remains at its previous viewport position unless boundary clamping is necessary, and Undo restores the previous style. Save acknowledgement changes status to “Saved”. Increase text size to 200%: the URL rewraps, the Arabic paragraph retains its own alignment and digits, and the same logical reading location remains visible.

## Acceptance checks and current results

These are implementation gates; runtime results are **not executed**. Proposed dimensions are test fixtures, not Apple minimum window sizes.

| Check | Pass condition | Current result |
|---|---|---|
| Specification coverage | Every reported issue has a replacement behavior and check below | Passed: document inspection |
| Read-only safety | Pointer/keyboard selection and Copy work; typing, IME commit, paste, cut, delete, drop, format and stale mutation commands cannot change content; no insertion caret | Not executed |
| Editable task | Select across wrapped lines, type, paste, format, Undo/Redo, Save and reopen; text/styles match acknowledged revision | Not executed |
| Position retention | At paragraph 120 apply formatting, undo, resize and scale; anchor stays at same viewport position within one rendered pixel unless boundary clamping/minimal reveal is required | Not executed |
| Reveal and boundaries | Type at offscreen caret, extend selection past edges, find first/last match, scroll to document ends; only necessary reveal occurs; manual scrolling does not snap back | Not executed |
| Long content | 200-paragraph fixture and 300-character unbroken URL fully readable; cross-line selection copies exact text; one vertical owner | Not executed |
| Mixed scripts | Arabic/Hebrew/Latin, combining accents, emoji and numbers retain logical data and correct shaping/direction; grapheme-safe editing and copied text round-trip | Not executed; needs competent language review |
| Enlarged and resized | At 100%, 150%, 200%, in 480×400 and 1440×900 pt content areas, text and commands remain reachable without clipping or same-axis nesting | Not executed |
| Keyboard and activation | Complete read/copy/edit/save and Find without pointer; exit every focus target; menus use same selection; app switch preserves work; system/international shortcuts work | Not executed on Mac |
| Permission/save races | Revocation blocks queued edits, preserves draft/anchor; save failure never claims Saved or loses work; older acknowledgements cannot mark a newer revision saved | Not executed |
| Accessibility and appearance | Actual accessible text, name, state, range and navigation work with VoiceOver/Full Keyboard Access; light/dark/Increase Contrast measured and readable | Not executed |

Failed checks: none executed and failed. This is not a claim that the described current interface passes; its supplied behaviors remain the problems this specification addresses.

## Evidence limits and route audit

Only local `interface.md` and installed instructions/references were used. No browsing occurred. Official URLs above identify the sources named by local guides; they were not fetched or verified live. The installed articles describe a 2026-10-25 snapshot and original application guidance derived from Apple sources, not a verbatim manual or SDK contract. No source conflict was found except the general text-view Dynamic Type advice needing the explicit macOS typography qualification; the specification uses custom resizing accordingly.

Audit route, resolved under `.agents/skills/apple-hig/`: explicitly read root `SKILL.md`; searched `references/topic-index.md`; read each selected family's `SKILL.md`, then its `.topics/apple-hig-<topic>/SKILL.md`, then `references/<topic>.md`. Families/topics: getting-started → designing-for-macos; content → text-views; foundations → typography, accessibility, right-to-left, layout; inputs → keyboards, focus-and-selection; presentation → scroll-views. Each file was read with an individual `cat`, `sed` or `rg` command. Typography's relevant opening/platform sections and accessibility were reread separately after aggregate output truncation.

No executable app, original note data, screenshots, SDK, GUI, device or accessibility runtime was inspected or executed. Font metrics, contrast, actual focus behavior, shaping, menu integration, persistence and migration feasibility remain unverified. Linux file inspection establishes the specification and source route only. Implementation must select and verify a text engine, accessibility bridge and persistence adapter in the project's actual framework; nothing here asserts Apple SDK availability.
