# Adaptation result

Edited interface.md in place into an implementable iPadOS specification. Replaced fixed left-aligned columns with an RTL-aware, scrolling compact form; specified full text reflow at 420 pt and 200%; retained the supplied vendor, ID, email, amount and currency. Specified numeric direction exceptions, unchanged media Play orientation, explicit payment labels/symbols, Add line keyboard access and draft preservation across resizing.

## Decisions

- Use one form and stable field identities across wide/compact layouts; preserve raw input, composition, caret, focus, selection, validation, scroll anchor and undo history. Resizing never commits or resets quantities.
- Keep 1240.50 SAR as the supplied numeric baseline. Localize its presentation without changing its value. Preserve existing financial rules; no line items or tax policy were supplied to reconstruct the amount.
- Separate locale-sensitive numeric parsing from display formatting. Invalid or partial edits retain their raw text and last valid totals with a visible qualification.
- Distinguish ordinary iPad focus groups from Full Keyboard Access. Make Add line a reachable action group and specify its insertion, focus and undo behavior. The proposed Command-Shift-L shortcut still needs conflict testing.
- Arabic interface labels are provisional translation proposals. Region, numeral preferences, payment state and the play control's actual purpose remain unspecified.

## Acceptance checks and evidence

Passed — static specification inspection only:

- All supplied literal content is preserved, including مؤسسة النور, INV-2026-04, accounts@example.test and the 1,240.50 SAR reference representation.
- Each supplied defect has a concrete replacement contract and an observable check below.
- Totals and editing-state invariants explicitly exclude resize-triggered resets, recalculation and commits.
- Installed root SKILL.md was explicitly read, then selected families and topic procedures were read before their source guides. Topic-index searches covered the task concepts and controls. No web sources were fetched.

Failed — supplied starting design, as described in the original interface.md, not independently reproduced: fixed left alignment for Arabic, clipped 200% labels, color-only payment state, mechanical numeral/play mirroring, Tab-unreachable Add line, and resize-reset quantities. These are addressed in the revised specification; runtime resolution is unverified.

Not executed — required implementation acceptance scenarios:

| Scenario | Pass condition |
| --- | --- |
| Arabic at 420 pt, 100% and 200% text | Full vendor, labels, ID, email, payment text and totals remain readable; all editing/actions are reachable; no overlap or required horizontal form scrolling. Check 34 pt body equivalent separately from all supported Dynamic Type sizes, including the largest accessibility sizes and Bold Text. |
| Continuous resize, wide → 420 pt → wide; rotation and short window | Enter quantities and a partial localized decimal, select text, retain active composition and scroll midway. Raw/committed values, errors, dirty state, line identity, focus/caret, composition, undo and totals survive. Active field remains visible above keyboard. Repeat without an active field to check scroll-anchor restoration. |
| Mixed direction and locale | Verify ID/email punctuation and copy round-trip; Western/Eastern digits retain order and parse to the same values. Check SAR currency placement and Arabic shaping. Back/Next mirror where present; media Play does not. |
| Keyboard, ordinary focus | Tab reaches Add line, Shift-Tab exits it, activation inserts exactly one draft line and focuses its first field. Native text arrows/selection and undo remain correct. Command discovery exposes the proposed shortcut; Arabic and Latin layouts have no conflicts. |
| Full Keyboard Access | Independently navigate and activate every interactive control without touch; indicators stay visible and no trap prevents completion. Do not count ordinary text traversal as evidence. |
| Financial preservation | Capture real baseline quantities and totals; resize and change text size/locale without edits and compare exact decimals. Valid commits use existing rounding rules and update atomically; undo restores prior totals. Partial/invalid/empty input is retained and qualified, never silently zeroed. |
| Status, touch and accessibility | Payment meaning remains clear in grayscale; verify accessible labels/values/errors and reading order with VoiceOver, plus Switch Control access. Measure ≥44 × 44 pt design targets and separation. Measure contrast in light/dark and Increase Contrast. |

## Guidance audit and limits

All paths resolve under `.agents/skills/apple-hig/`. Read the root, topic index matches, and these routes, with one file per shell command:

- Getting started → Designing for iPadOS → designing-for-ipados reference.
- Foundations → Right to left, Layout, Typography, Accessibility → corresponding references (relevant typography sections reread without truncation).
- Inputs → Keyboards, Focus and selection → corresponding references (keyboard best practices reread without truncation).
- Selection and input → Text fields → text-fields reference.
- Menus and actions → Buttons → buttons reference.

Official article/section links in interface.md identify the source basis from the installed snapshot. The snapshot is guidance rather than SDK verification; the contract's field grouping, test dimensions, draft model and arithmetic policy are application decisions. No framework migration or API availability claim is made.

Still missing: implementation/source code, actual line data and rounding/domain constraints, supported iPadOS versions, window-height bounds, real field/control geometry, fonts/colors/rendered screens, native Arabic translation review and configured regional preferences. The play-shaped control's purpose must be inspected before approving its semantics. No Apple device, simulator, SDK build, GUI, hardware keyboard or assistive-technology execution occurred. Runtime, shaping, contrast, accessibility order, comfort and financial regression results remain unverified.
