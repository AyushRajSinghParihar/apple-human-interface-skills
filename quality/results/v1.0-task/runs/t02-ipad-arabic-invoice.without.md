The editor should use an Arabic right-to-left layout, reflow into a single column at 420 pt, and preserve the invoice draft throughout resizing and text-size changes. Totals must remain available without covering the fields being edited.

### Revised layout and behavior

| Area | Specification |
|---|---|
| Reading order | Use leading/trailing alignment and native RTL layout. In Arabic, headings, labels, and ordinary text start at the right. Visual order, VoiceOver order, and keyboard order follow the same logical sequence. |
| Compact layout | At 420 pt, replace fixed columns with vertically stacked sections: invoice details, line items, totals, and actions. Each line item becomes a grouped card with its description, quantity, unit price, line total, and actions. |
| 200% text | Support the requested size through Dynamic Type. Put labels above fields, wrap labels and values, and let rows and controls grow vertically. Do not truncate essential invoice information or shrink text to fit. Avoid horizontal scrolling for the form. |
| Resizable window | Choose layouts from the actual available width and text metrics. Wider windows may use columns only while every label and control fits comfortably. Changing layout must not recreate the draft or interrupt an edit. |
| Totals | Keep the full totals section in the document flow. A compact persistent total summary may appear when sufficient vertical space exists; it must reserve space and never obscure content or keyboard focus. At short heights or large text sizes, let it scroll with the document and provide a keyboard-accessible “Go to totals” action. |
| Payment state | Show a localized text label, such as “Paid” or “Unpaid,” with an optional status symbol. Color is supplementary. Expose the same state to VoiceOver; ensure sufficient text and control contrast. |
| Touch targets | Keep interactive targets at least 44 × 44 pt, with enough separation to distinguish adjacent line-item actions. |

### Arabic content and direction

Use semantic direction for each value instead of reversing characters:

- **Vendor:** `مؤسسة النور` uses RTL Arabic text.
- **Invoice ID:** `INV-2026-04` remains an isolated LTR value, with character order and hyphens intact.
- **Email:** `accounts@example.test` remains isolated LTR, including during selection, editing, and copying.
- **Amount:** Format the numeric value `1240.50` and currency `SAR` using the selected Arabic locale’s number and currency formatter. The locale determines digits, separators, currency placement, and spacing. Never mirror digits or manually reverse the formatted string.

Use direction-aware native text controls and bidirectional isolation around embedded identifiers. Do not insert formatting characters into stored invoice IDs or email addresses.

Mirror only icons whose meaning depends on reading direction, such as navigation arrows. Do not mechanically mirror plus signs, checkmarks, trash icons, logos, or other nondirectional symbols. Give icon-only controls localized accessible names.

### Hardware keyboard behavior

- Tab and Shift-Tab reach every editable field and action, including **Add line**, in logical document order. Focus indicators remain visible.
- Activating Add line creates one item, moves focus to its description field, and scrolls it into view. It does not change existing items.
- Return or Space activates focused buttons using native platform behavior. Return inside a multiline description inserts a newline.
- Provide discoverable shortcuts for Add line and Go to totals through the system keyboard shortcut interface. Avoid conflicts with standard editing shortcuts.
- After deleting a line, move focus to the next line, then the previous line if necessary, or Add line when none remain.
- Resizing preserves focus on the same logical field, its selection or insertion point, and any in-progress text composition. Scroll only as needed to keep that field visible.

### State and calculation decisions

1. **Keep draft state independent of layout.** Store fields and line items in a stable draft model with stable item identifiers. Width and text-size changes affect presentation only.
2. **Preserve unfinished input.** Retain raw field text as well as validated numeric values, so resizing does not discard partially typed quantities or force a commit.
3. **Keep calculation rules unchanged.** Preserve existing tax, discount, currency precision, and rounding rules. Reflow and localization must not alter invoice amounts.
4. **Handle invalid edits explicitly.** Show a localized inline error with an accessible association to the field. If totals retain the last valid calculation while input is invalid, label them as awaiting correction; do not present them as current.
5. **Separate formatting from data.** Locale changes affect display, not stored identifiers, quantities, or monetary values. Accept supported localized number input without ambiguous silent conversion.
6. **Keep validation non-destructive.** Resizing, navigating to totals, or changing text size must neither clear errors nor discard entered values.

### Acceptance checks

| Check | Pass condition |
|---|---|
| Compact Arabic at 200% | At 420 pt, all essential labels, values, errors, and actions are readable without clipping, overlap, text shrinking, or form-wide horizontal scrolling. |
| Short window and keyboard | With the software keyboard visible or the window height reduced, every field and total remains reachable; no persistent summary covers content or focus. |
| Bidirectional sample data | Vendor text reads correctly. Invoice ID and email preserve their exact character order when displayed, edited, selected, and copied. |
| Currency | The sample amount represents exactly 1,240.50 SAR in the selected locale’s format. Digits are never geometrically mirrored or reversed. |
| Icons | Directional navigation follows RTL conventions; nondirectional icons retain their meaning and orientation. |
| Payment status | Paid and unpaid states remain distinguishable in grayscale, with color disabled, and through VoiceOver. |
| Keyboard traversal | Tab reaches Add line and every other enabled control; Shift-Tab reverses the sequence. Focus is visible and there is no trap. |
| Add and delete | Add line focuses the new description. Deletion places focus predictably without losing another line’s edits. |
| Resize during editing | Enter quantities, leave one field partially typed, select text, and resize repeatedly. Values, raw input, selection, focus, validation, and composition survive. |
| Totals stability | Capture all totals before resizing and changing text size. After each change, totals are numerically identical; subsequent valid quantity edits recalculate correctly. |
| Assistive technology | VoiceOver announces section and line-item context, field labels, values, errors, payment state, and totals in logical RTL reading order. |
| Layout transitions | Repeat the checks at 420 pt and on both sides of each layout transition. No duplicated controls, lost state, or unexpected focus jumps occur. |