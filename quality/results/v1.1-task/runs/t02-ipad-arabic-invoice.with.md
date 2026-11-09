Use an RTL, vertically scrolling editor at 420 pt, with each line item presented as a labeled group. Resizing changes the arrangement while preserving the invoice, entered quantities, totals, focus, and undo history.

**Revised layout and behavior**

| Area | Specification at 420 pt and 200% text |
|---|---|
| Header | Localized invoice title, invoice ID, and explicit save/editing status. Allow wrapping and growing height. Keep primary actions reachable in the toolbar; use a labeled overflow menu when needed. |
| Invoice details | Stack each label above its field. Arabic labels align to the leading edge—right in Arabic. Show vendor, invoice ID, email, and payment status without clipped labels. |
| Line items | Replace fixed columns with vertically stacked groups: description, quantity, unit price, and calculated line total. Keep each label adjacent to its value. Allow descriptions and errors to wrap. |
| Add line | Place a visible, labeled “Add line” button immediately after the items. Support touch and keyboard activation. Adding a line focuses its description field. |
| Totals | Keep every existing subtotal, adjustment, tax, and grand-total component. Place the complete breakdown after Add line. Stack a total’s label above its amount whenever they cannot fit together. Emphasize the grand total with weight and spacing. |
| Persistent total | When height permits, show a compact grand-total summary in a safe-area footer. If enlarged text or reduced height crowds editing, let it flow with the document. The complete breakdown always remains reachable. |

Use semantic system text styles with Arabic shaping and Dynamic Type. Grow field and row heights; do not shrink text to recover the columns. Provide vertical scrolling without requiring horizontal page scrolling. Use touch targets of at least 44 × 44 pt as the design baseline.

At wider widths, restore aligned columns only when the localized labels, values, and controls fit at the current text size. Choose the layout from available space and content measurements; 420 pt uses the stacked version. These are product decisions informed by Apple’s [Layout](https://developer.apple.com/design/human-interface-guidelines/layout), [Typography](https://developer.apple.com/design/human-interface-guidelines/typography), and [iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados) guidance.

**Arabic and mixed-direction decisions**

| Content | Required treatment |
|---|---|
| `مؤسسة النور` | Render as Arabic text with native shaping; preserve the name exactly. |
| `INV-2026-04` | Preserve this exact identifier. Isolate it as an LTR run inside the RTL interface so punctuation stays attached correctly. |
| `accounts@example.test` | Use an LTR email field/run with native selection, cursor movement, and copy/paste. Preserve the exact address. |
| `1,240.50 SAR` | Store the numeric value as decimal `1240.50` and currency as `SAR`. Format for the selected Arabic region and numbering preference. Arabic does not imply one universal numeral system. Never reverse digits or reflect their glyphs. |
| Navigation and icons | Use system RTL variants for Back/Next and reading-direction symbols. Preserve checkmarks, logos, and ordinary object/tool icons. Review custom composite icons individually. |

Use bidirectional isolation at presentation boundaries rather than inserting directional characters into stored invoice data. Keep the interface RTL while allowing fields and paragraphs to follow their content’s direction. Arabic translations and the chosen regional currency presentation need native-language review. See Apple’s [Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left) guidance.

Replace color-only payment indicators with localized text such as “Paid” or “Unpaid,” paired with a distinct symbol. Red/green may remain supplementary. Expose the same status to accessibility APIs, independently of “Unsaved changes” or “Saved.” See [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility).

**Keyboard and editing-state contract**

- Tab and Shift-Tab follow the document’s logical reading order: invoice fields, each item’s editable fields and actions, Add line, then subsequent controls. RTL changes spatial placement; it does not reverse characters or create an unrelated focus order.
- Include Add line in the editor’s keyboard traversal. With Full Keyboard Access enabled, every button, menu, and payment control must also be reachable and activatable using system conventions. Ordinary text-field traversal and Full Keyboard Access require separate testing.
- Show a visible focus indicator and scroll the focused control clear of toolbars, the footer, and either keyboard.
- Preserve native Arabic/Latin text editing, selection, copy/paste, undo, and redo shortcuts. Expose Save through Command-S if the editor has an explicit save action. Publish available shortcuts through system discoverability.
- After deleting a line, move focus to the nearest remaining line or Add line.

These choices follow Apple’s [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards) guidance.

Keep the draft model independent of the compact/wide views, with stable invoice, line, and field identities. Preserve quantities as they are typed, including unfinished input such as a decimal separator; retain validation state, active field, selection, input composition, expanded sections, scroll anchor, and undo history across reflow.

Resizing must not reload sample data, recreate the draft, commit incomplete input, or trigger validation errors. Calculate totals from valid decimal values using the existing rounding rules. While a field is incomplete or invalid, retain the last valid totals and mark them as awaiting valid input. Reformatting or reflow must not change the underlying amount. Preserve the draft through app switching and restoration using the app’s draft-saving mechanism. See [Multitasking](https://developer.apple.com/design/human-interface-guidelines/multitasking).

**Acceptance checks**

All checks below are **not done**; this is a specification based on the supplied current state.

| Check | Pass condition |
|---|---|
| Combined stress case | At 420 pt, Arabic, 200% text, and hardware keyboard attached, the entire invoice can be edited and saved. No essential label, total, error, or action clips or overlaps. |
| Text adaptation | Test default, 200%, and the largest supported accessibility size, including Bold Text. Labels wrap, controls grow, Arabic marks remain visible, and all content is reachable. |
| Mixed-direction data | The vendor shapes correctly. ID and email display and copy exactly as supplied. Amount remains numerically `1240.50 SAR`; regional formatting never reverses digits. Test caret movement, selection, and punctuation editing. |
| Icon direction | Back/Next follow RTL navigation. Checkmarks, logos, and nondirectional object icons retain their meaning. |
| Payment status | Paid and unpaid remain distinguishable in grayscale and without color. VoiceOver announces the explicit payment state. Measure contrast in light, dark, and Increase Contrast appearances. |
| Keyboard completion | Tab reaches Add line; Shift-Tab returns predictably. Activation adds exactly one line and focuses its description. Full Keyboard Access reaches all controls without a pointer or focus trap. Test Arabic and Latin keyboard layouts. |
| Resize continuity | Enter quantities and prices, leave one field partially edited, then repeatedly resize between 420 pt and wider layouts. Draft values, selection, focus, validation state, and undo history survive; valid totals stay identical. |
| Totals integrity | Compare every total before and after resize, text-size change, and locale reformatting. Values and rounding remain identical. Incomplete input produces the specified pending state. |
| Short window and interruption | Reduce height, show the software keyboard, switch apps, and return. Focused fields and all totals remain reachable; entered quantities and draft state persist. |
| Assistive access | On iPad, verify VoiceOver reading order, field labels/values/errors, payment status, and total associations. Confirm touch target geometry and visible keyboard focus. |