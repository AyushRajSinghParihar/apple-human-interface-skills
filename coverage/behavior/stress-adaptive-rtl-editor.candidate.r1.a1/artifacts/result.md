# Adaptation result

Edited `interface.md` in place into an implementable iPadOS design contract. The supplied artifact was a one-paragraph brief; no implementation, screenshot, SDK project or runtime was supplied. This result specifies behavior rather than claiming an application fix was executed.

## Concrete changes and decisions

| Supplied problem | Result in interface.md |
|---|---|
| Fixed left-aligned columns | Semantic leading/trailing Arabic layout; one scrolling column at 420 pt, with labeled stacked line editors and reachable totals. Wider layouts depend on actual content fit. |
| Clipping at 200% | Semantic system type, growing/wrapping containers, explicit 34 pt body fixture from 17 pt, plus largest system accessibility sizes and Bold Text checks. |
| Red/green-only payment state | Actual localized status text plus distinct symbols; no assumed payment status. |
| Mechanical numeral/icon mirroring | Preserve digit order, exact ID/email strings, isolated LTR runs and native bidi editing; adapt reading-direction navigation while retaining conventional Play orientation. |
| Tab cannot reach Add line | Separate ordinary content groups from Full Keyboard Access to every control; Add line has a discoverable keyboard command as well as an onscreen action. Command-L is provisional until collision testing. |
| Resize resets quantities | Draft ownership outside layout, stable identities and preservation of edit buffers, caret/composition, validation, selection, undo and scroll anchor. Reflow cannot commit edits or recalculate totals. |

Retained `مؤسسة النور`, `INV-2026-04`, `accounts@example.test`, SAR and the exact supplied amount 1,240.50 (124050 minor units). No invented tax, lines, payment state or accounting formula. Arabic/Saudi formatting is an explicit design assumption pending language/region review. Save and close/reopen behavior are specified to protect work, but no persistence implementation exists in the supplied evidence.

## Instruction/source audit

Read the installed `/tmp/hig-eval-tgi2fv_s/.agents/skills/apple-hig/SKILL.md` explicitly before routing. Read `interface.md` before selecting corrections. All following paths resolve within that installed package, not another skill installation.

- Read family `subskills/apple-hig-foundations/SKILL.md`, then `.topics/apple-hig-right-to-left/SKILL.md`, `.topics/apple-hig-typography/SKILL.md`, `.topics/apple-hig-accessibility/SKILL.md` and `.topics/apple-hig-layout/SKILL.md`, before their respective `references/right-to-left.md`, `typography.md`, `accessibility.md` and `layout.md` source guides.
- Read family `subskills/apple-hig-inputs/SKILL.md`, then `.topics/apple-hig-keyboards/SKILL.md` before `references/keyboards.md`. Followed its focus route by reading `.topics/apple-hig-focus-and-selection/SKILL.md` before `references/focus-and-selection.md`.
- Read family `subskills/apple-hig-presentation/SKILL.md`, then `.topics/apple-hig-windows/SKILL.md` before `references/windows.md`.

Each instruction/source read used a separate single-file `cat` or `sed` command. Relevant accessibility and layout source sections were read again individually after combined tool output was truncated. No web access was used. Official article links in `interface.md` identify sources from the local snapshot, not pages independently verified online. No newer SDK API or release behavior is asserted.

## Acceptance checks

Status distinguishes specification inspection from application execution.

| Check | Required observable result | Status |
|---|---|---|
| Fixture preservation | All four supplied strings/amount and SAR remain in the edited artifact; no invented accounting inputs. | Passed: static file check. |
| Barrier coverage | Specification addresses Arabic/bidi, 420 pt, 200%, payment semantics, Add line access and resize state loss. | Passed: static specification review. |
| Original behavior | Supplied brief reports clipping, color-only status, reversed numerals/icons, unreachable Add line and quantity reset. | Failed as described by the brief; not independently reproduced. |
| Combined stress case | At 420 pt, Arabic UI and 200% text, all labels/values/errors and Add line/Save remain readable and reachable; no horizontal form scrolling or overlapping controls. | Not executed. |
| Resize and text transition | Enter quantity, leave partial decimal or marked composition active, record committed total; resize wide → 420 pt → wide, change text size and direction. Same buffer, caret, selected line, error, undo and scroll anchor; no extra save/commit or amount change. | Not executed. |
| Totals correctness | Initial 124050 minor-unit amount survives presentation changes. Valid committed edit recalculates exactly once using existing rounding; undo restores prior values/total. Invalid draft retains last committed total with clear status. | Not executed; formula and fixtures missing. |
| Bidi round-trip | Arabic vendor shapes correctly; ID/email copy back exactly; amount retains value and digit order under selected numeral formats. Cursor/selection and punctuation work in Arabic and Latin input. Back adapts; Play retains its meaning. | Not executed. |
| Keyboard completion | With ordinary focus, traverse content groups and edit fields. Separately with Full Keyboard Access, reach/activate Add line, Total and Save without pointer; reverse traversal exits every group. Add creates one line and focuses description. | Not executed. |
| Shortcut safety | Native editing/undo remain intact; app commands appear in discoverability; Command-L has no collision on supported Arabic/Latin layouts and OS versions. | Not executed. |
| Focus and state | Resize does not change focus/selection; deliberate removal chooses nearby target, undo restores data; errors stay associated and visible above keyboard. | Not executed. |
| Window lifecycle | Repeated activation/reopen restores correct invoice draft; close/save failure retains work; system window controls do not cover toolbar actions. | Not executed. |
| Type/environment matrix | Exercise default, exact 200% and all supported Dynamic Type sizes through maximum, Bold Text, wide/420 pt/intermediate widths and short heights, Arabic/English, software keyboard shown/hidden and hardware keyboard. | Not executed. |
| Perception and assistive access | Status understandable without color; measure contrast in light/dark/Increase Contrast and activation geometry. Verify spoken field names/values/errors and reading order with VoiceOver, plus Full Keyboard Access and Switch Control completion. | Not executed. |

## Evidence still missing

Need the app/framework and supported iPadOS versions; real line-item, currency, tax and rounding rules with expected totals; draft persistence and undo implementation; actual payment states; playback action semantics; supported size bounds and measured layouts; native Arabic translation/numeral preference review; and target SDK validation of any chosen implementation APIs.

Need native rendering and interaction evidence on supported Apple environments for combined RTL/large-text layouts, real hardware keyboard layouts, Full Keyboard Access, bidirectional selection/composition, VoiceOver/Switch Control, safe areas/window management, measured contrast/activation regions and save/restore failures. No device, simulator, GUI, SDK build or accessibility execution occurred here. Static design checks do not establish any of those results.
