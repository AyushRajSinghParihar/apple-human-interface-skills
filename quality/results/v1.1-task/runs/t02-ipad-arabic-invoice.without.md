The editor should use a responsive, right-to-left layout for Arabic while preserving invoice values, calculated totals, and unsaved edits through every window resize.

### Revised layout and behavior

| Area | Specification |
|---|---|
| Layout direction | Use semantic leading/trailing alignment. In Arabic, place labels and navigation according to right-to-left reading order. Replace fixed columns with an adaptive layout. |
| At 420 pt and 200% text | Use a single scrolling column. Show each invoice line as a card with its description, quantity, unit price, and line total stacked vertically. Put each label above its field; allow labels and values to wrap without clipping. No horizontal scrolling is required for the editor. |
| Wider windows | Use columns only when labels, values, and controls fit at the current text size. Choose the layout from available space and content fit, rather than device orientation. |
| Invoice header | Display vendor **مؤسسة النور** in RTL. Display **INV-2026-04** and **accounts@example.test** as isolated LTR runs, preserving their character order and punctuation. Keep the email field’s typing direction LTR. |
| Numbers and currency | Format monetary values using the selected Arabic locale and SAR currency formatting. Preserve the numeric value **1240.50**. Never reverse digit sequences or punctuation mechanically. Accept appropriate localized digits and separators in numeric fields. |
| Totals | Keep subtotal, applicable tax/discount rows, and grand total in the same logical sequence. At compact width, give each total enough space to wrap or stack. Keep totals in the scrolling content so an enlarged sticky panel cannot obscure editing fields. |
| Payment state | Pair color with localized text, such as “Paid” or “Unpaid,” and an appropriate symbol. Expose the state as text to VoiceOver; color alone must never carry its meaning. |
| Icons | Mirror directional navigation and reading-order icons where appropriate. Do not mechanically mirror logos, checkmarks, currency symbols, or other nondirectional icons. Use system-provided RTL behavior where available. |
| Controls | Support the requested 200% text size throughout, including fields, buttons, validation messages, and totals. Allow multiline button labels and maintain at least 44 × 44 pt touch targets. |

### Editing and hardware keyboard behavior

- **Tab / Shift-Tab:** Move through editable fields and actions in logical reading order, including **Add line**, remove-line actions, and save. Every reachable control has a visible focus indicator.
- **Add line:** Activate using the platform’s standard keyboard action. Insert the new line and focus its first editable field. Announce insertion to assistive technology.
- **Editing:** Preserve standard text selection, cursor movement, clipboard, and undo behavior. Do not reinterpret left/right arrow keys merely because the interface is RTL.
- **Validation:** Keep invalid or incomplete input visible, associate a localized error with the field, and preserve focus. Do not silently replace it with zero or discard it during resizing.
- **Visibility:** Scroll the focused field into view when needed, including when the software keyboard appears. Do not move focus merely because the layout changes.
- **Resize continuity:** Preserve line identities, quantities, raw field text, validation state, selection, keyboard focus, and unsaved-change status. Reflow the existing editor rather than recreating the invoice.
- **Calculation:** Keep the existing calculation and rounding rules. A resize, text-size change, or language change must not alter totals. Valid value edits continue to update totals under the existing editing rules.

### Decisions

1. **Stack line items at compact widths.** A 420 pt window at 200% text cannot reliably support a fixed invoice grid.
2. **Separate direction from formatting.** Arabic layout is RTL; identifiers, email addresses, and digit sequences retain their correct internal order.
3. **Keep editing state outside the layout.** Responsive views render the same invoice draft, with stable line and field identities.
4. **Keep totals in document flow at compact sizes.** This preserves access to all totals without taking space away from enlarged fields.
5. **Use text and symbols alongside status colors.** Payment state remains understandable without color perception.

### Acceptance checks

- [ ] At **420 pt width and 200% text**, every label, field, action, error, and total is readable without clipping, overlap, or editor-wide horizontal scrolling.
- [ ] The vendor renders correctly as **مؤسسة النور**. **INV-2026-04** and **accounts@example.test** retain their exact character order when displayed, edited, selected, and copied.
- [ ] The sample amount remains numerically **1240.50 SAR**, with correct locale formatting and no reversed digits.
- [ ] Directional icons adapt appropriately; nondirectional icons retain their meaning and orientation.
- [ ] Payment state is understandable in grayscale and announced meaningfully by VoiceOver.
- [ ] Using only the hardware keyboard, a person can reach and activate **Add line**, edit the new line, navigate backward, and reach save without a focus trap.
- [ ] Focus order follows the visible reading order in both stacked and column layouts.
- [ ] After entering quantities, repeatedly resizing between compact and wider windows preserves all entered values and calculated totals.
- [ ] Resizing while a field contains an incomplete or invalid number preserves its exact text, error state, focus, and selection.
- [ ] Changing text size or interface direction preserves the draft and unsaved-change state.
- [ ] The focused field remains visible, and every total remains reachable by scrolling at the smallest supported window height.