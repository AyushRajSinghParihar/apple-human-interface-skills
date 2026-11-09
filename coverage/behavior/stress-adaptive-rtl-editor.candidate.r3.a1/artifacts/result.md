# Adaptation result

Updated interface.md in place with an implementable iPadOS design contract. The original brief's fixed left columns become RTL-aware stacked groups at 420 pt; essential text grows and wraps at 200%; payment state gets text and symbols; Add line gains an explicit keyboard route; draft data and totals are owned outside layout reconstruction.

Preserved reference content: مؤسسة النور; INV-2026-04; accounts@example.test; 1240.50 SAR (original display 1,240.50 SAR). Numeric value and currency remain invariant under resizing, localization and text enlargement. No quantities, line prices, payment status or calculation rules were supplied, so none were fabricated.

## Decisions

- Arabic changes reading order and alignment while identifiers, email, digit order and Play orientation retain their meaning. Arabic region, numeral preference and final translations require confirmation through product/native-language review.
- At 420 pt use one scrollable stack, including totals. Expand controls instead of shrinking text. Wider columns depend on actual content fit at the selected text size.
- Specify ordinary iPad focus groups separately from Full Keyboard Access. Add line is reachable as a command and through the all-controls route; native text editing and standard shortcuts retain their meaning.
- Preserve raw partial edits, validated values, totals, stable field identity, caret, focus, selection, undo and dirty state across reflow. Invalid input retains the last valid totals with a pending-edit indication; presentation changes never recalculate or commit data.

## Acceptance checks and current status

**Passed — static specification checks only:** the revised artifact contains each supplied reference value, a 420 pt/200% stacked layout, element-specific RTL rules, non-color payment semantics, both keyboard routes, and explicit total/draft invariants. These checks establish requirements coverage, not functioning software.

**Failed — supplied baseline description:** labels clip at 200%; red/green alone carries payment state; numerals and Play are mechanically mirrored; Tab cannot reach Add line; resizing resets quantities. No executable baseline was available to reproduce these defects, and runtime fixes are not established.

**Not executed — required implementation acceptance:**

| Scenario | Pass condition / evidence to collect |
|---|---|
| Combined stress case | Arabic at 420 pt, 200% text and Bold Text: complete vendor, ID, email, labels, actions and 1240.50 SAR remain readable and operable without overlap, clipping or horizontal editor scrolling. Capture dimensions, text settings and screenshots. |
| Resize matrix | Start at 420 pt, expand to 768 and 1024 pt, test intermediate widths and return; test short 420 pt-high windows and software keyboard. Also test the actual OS-supported minimum/maximum sizes. Controls respect safe areas/window controls and focused fields remain visible. These are proposed test dimensions, not claimed OS limits. |
| State during resize | Enter a valid quantity and then a partial localized decimal edit; select text, select a line, scroll and create undo history. Repeated resize and text-size changes retain raw text, caret/selection, errors, document/line IDs, focus, dirty state and undo stack. Compare model snapshots before/after; no presentation-only undo entry appears. |
| Totals | Capture all existing decimal totals before presentation changes and compare afterward: identical values and currency, including 1240.50 SAR for the reference fixture. Test valid quantity edits against independently known line/rate/tax fixtures; invalid input cannot save inconsistent totals. |
| Mixed-direction text | Native Arabic reviewer verifies shaping, reading order, labels and chosen region formatting. Inspect ID/email punctuation and number order, select/edit at Arabic–Latin boundaries, and copy/paste exact original values. Play stays conventional; reading-direction navigation adapts. Screenshots alone cannot prove caret behavior. |
| Ordinary hardware keyboard | With Full Keyboard Access off, traverse logical groups forward/backward, reach and activate Add line, edit the new line and Save without a pointer. Arrows in text preserve native caret behavior; no focus trap or unsolicited activation. Check English and Arabic keyboard layouts. |
| Full Keyboard Access | With it on, reach/activate every control using configured system bindings, reverse out of groups, add a line, edit and Save. Focus remains visible and survives resize; standard editing and system shortcuts work. Record device, OS and settings. |
| Status and accessibility | Distinguish actual payment states in grayscale; verify accessible names/roles/values, associated errors and task order with Accessibility Inspector and VoiceOver. Measure actual light/dark/Increase Contrast color pairs and activation geometry. No contrast ratios or geometry have been measured. |
| Lifecycle | Background/reactivate, switch documents/windows, close/reopen and exercise implemented draft recovery. Restore correct document and edits; no wrong-document reuse or loss. Verify storage failures and any multiwindow conflict policy once implementation exists. |

## Evidence boundaries and audit

Used only interface.md and the installed local instructions; no web browsing. Explicitly read the installed apple-hig root SKILL.md, then family SKILL.md files for Foundations, Inputs and Presentation. Read routed topic SKILL.md files before their references: Right to left, Typography, Accessibility, Layout, Keyboards, Focus and selection, and Windows. Every instruction/source read used a separate cat or sed command resolving paths within this installed package. Official source links are included in interface.md as supplied by those local references.

Missing evidence: app source/framework and SDK target, runnable build, actual font/layout measurements, line-item and calculation fixtures, localization resources/region choice, asset inventory, persistence implementation and native-language review. No device, SDK compilation, GUI, keyboard, focus engine, accessibility tool or assistive-technology execution occurred. The deliverable is the adapted specification and acceptance contract; runtime checks remain unexecuted.
