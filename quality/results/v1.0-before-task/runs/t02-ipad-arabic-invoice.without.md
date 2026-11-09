The editor should adapt to the window’s available width and Arabic reading direction, with a single-column editing flow at 420 pt and 200% text. Resizing must preserve entered quantities, calculated totals, focus, and unfinished edits.

## Revised layout and behavior

**Layout**

- Use leading/trailing alignment instead of fixed left/right columns. Arabic labels align to the leading edge on the right.
- At 420 pt, present vendor details, invoice details, line items, payment state, and totals in one vertically scrolling column.
- At 200% text, place each field’s label above its control. Let labels and values wrap; do not truncate essential content or shrink text to fit.
- Show each line item as a grouped section: description, quantity, unit price, calculated amount, and line actions. Put **Add line** immediately after the final item.
- Present totals after the line items in normal scroll flow. Keep subtotal, tax, and grand total labels paired with their values. Avoid a fixed footer that could obscure fields at large text sizes.
- At wider sizes, use additional columns only when the content fits at the current text size. Change presentation without recreating editing state.
- Keep touch targets at least 44 × 44 pt, including icon buttons.

**Arabic and mixed-direction content**

- Set the interface’s base direction to right-to-left. Use localized labels, reading order, and directional navigation.
- Display `مؤسسة النور` naturally in RTL.
- Treat `INV-2026-04` and `accounts@example.test` as isolated LTR runs so their characters and punctuation retain the correct order. Copying preserves the original strings.
- Format `1,240.50 SAR` using the selected Arabic locale’s currency and number conventions. Preserve the numeric value **1240.50 SAR**; never reverse digit sequences mechanically.
- Use locale-aware numeric input. Accept supported Arabic and Latin digit forms and normalize them to the same numeric value.
- Mirror directional navigation icons when their meaning follows reading direction. Do not mechanically mirror nondirectional symbols, logos, or icons containing text.
- Show payment state with localized text and a distinguishing symbol as well as color—for example, a checkmark plus “Paid.” Provide the same meaning to VoiceOver.

**Hardware keyboard**

- Make every action keyboard reachable, including **Add line**, line removal, and payment controls.
- Use a logical focus sequence matching the visual reading order: header fields, each line’s editable fields and actions, Add line, then remaining controls. Shift-Tab reverses it.
- Show a clear focus indicator. Keep the focused control visible when scrolling or resizing.
- Activating Add line creates one row and focuses its description field.
- Enter/Space activate focused buttons. Multiline fields retain normal newline behavior.
- After removing a line, move focus to the next line’s corresponding control, the previous line if necessary, or Add line when no lines remain.

**State and totals**

- Keep invoice data and the editing draft outside layout-specific views. Give line items stable identities.
- Preserve quantities, raw field text, validation messages, selection, and focus across resizing, text-size changes, and layout transitions.
- Recalculate totals from valid entered values using the existing calculation and rounding rules.
- During an incomplete numeric edit, preserve the raw text and the last valid totals. Mark the affected amount as awaiting valid input; do not silently substitute zero.
- Retain the current invoice, payment state, and unsaved changes throughout adaptation.

## Decisions

| Decision | Reason |
|---|---|
| Stacked fields at 420 pt and 200% text | Makes labels and values readable without horizontal scrolling. |
| Content-driven layout transitions | Available width alone does not determine whether enlarged Arabic text fits. |
| Totals remain in scroll flow | Keeps them accessible without covering editing controls. |
| Semantic RTL with isolated LTR content | Preserves identifiers, email addresses, and numeric meaning. |
| Text and symbols supplement payment colors | Makes state understandable without color perception. |
| Editing state is independent of layout | Prevents resizing from resetting quantities or unfinished edits. |
| Last valid totals remain during invalid edits | Preserves financial context while making incomplete calculations explicit. |

## Acceptance checks

- At **420 pt and 200% text**, all labels, controls, payment text, and totals remain readable and reachable without horizontal scrolling, overlap, or clipped essential text.
- Arabic reading order is correct visually, through keyboard navigation, and with VoiceOver.
- `مؤسسة النور` renders correctly; `INV-2026-04` and `accounts@example.test` display and copy in their original character order.
- The sample amount retains the value **1240.50 SAR** under localized formatting. Digits are never reversed.
- Directional navigation icons adapt appropriately; nondirectional icons remain unchanged.
- Payment state is understandable in grayscale and announced meaningfully by VoiceOver.
- Tab and Shift-Tab reach every interactive control, including Add line, with visible focus and no keyboard trap.
- Keyboard activation of Add line inserts exactly one item and focuses its description.
- Enter quantities, resize repeatedly between compact and wider windows, and change text size: quantities, item identities, payment state, and totals remain unchanged.
- Resize during an unfinished numeric edit: raw text, selection, focus, validation state, and last valid totals survive.
- After a valid quantity change, totals match the existing calculation and rounding rules, with no duplicate or dropped line items.
- The focused field and final totals remain reachable with both the onscreen keyboard and a hardware keyboard.