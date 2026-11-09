Use a single-column RTL editor at **420 pt**, with expanding fields and a complete totals section. Resizing changes presentation while preserving the invoice draft and editing context.

**Revised layout and behavior**

Top-to-bottom order at 420 pt, including at 200% text:

| Area | Specification |
|---|---|
| Header | Localized invoice title and Save action. Move secondary commands into an accessible menu when space runs out. |
| Invoice details | Vendor, invoice ID, email, and payment state. Each field has a persistent label above its value. |
| Line items | Each item becomes a vertical group: description, quantity, unit price, existing adjustments, calculated line total, and labeled item actions. |
| Add line | Full-width labeled button immediately after the last item. |
| Totals | Preserve every existing subtotal, discount, tax, and grand-total entry. Stack each label above its amount when necessary; emphasize the grand total. |

Use one vertical scroll region without horizontal page scrolling. Keep totals expanded in the document flow so they remain reachable without consuming the editing viewport. Scroll the focused field into view when a keyboard or window resize reduces available height.

Use semantic system text styles, Arabic-capable system fonts, Dynamic Type, and Bold Text support. Labels, buttons, validation messages, and groups grow vertically; essential text must not shrink or truncate to preserve columns. Use at least 44 × 44 pt activation areas for controls.

At wider widths, restore columns only when the actual localized content at the current text size fits. Keep the stacked layout at 200% wherever columns would clip. These are product layout decisions grounded in Apple’s [layout](https://developer.apple.com/design/human-interface-guidelines/layout) and [accessibility guidance](https://developer.apple.com/design/human-interface-guidelines/accessibility).

**Arabic and mixed-direction content**

Use semantic leading/trailing alignment: short Arabic labels align to the right. Apply direction to individual content runs rather than reversing strings or the entire screen.

| Content | Required treatment |
|---|---|
| مؤسسة النور | Natural Arabic shaping and RTL direction; allow wrapping. |
| `INV-2026-04` | Isolated LTR value; preserve its exact character order. |
| `accounts@example.test` | Isolated LTR field with normal email editing, selection, and copying. |
| `1,240.50 SAR` | Preserve numeric value **1240.50** and currency **SAR**. Format using the selected region and numbering preferences; never reverse digits. |
| Back/forward navigation | Adapt to RTL reading direction using system directional symbols. |
| Plus, checkmark, trash, logos | Preserve their meaning and ordinary orientation; do not mechanically flip them. Review custom composite icons individually. |

Keep labels aligned consistently across the form while giving Latin values their own LTR direction. Directional isolation belongs to presentation; copied IDs and emails must contain the original text. Arabic does not imply one universal numeral system. Have a native Arabic reviewer check wording, shaping, and mixed-script balance. These distinctions follow Apple’s [RTL guidance](https://developer.apple.com/design/human-interface-guidelines/right-to-left).

Replace color-only payment status with localized text and a supporting symbol—for example, “Paid” / “مدفوعة” with a checkmark, and “Unpaid” / “غير مدفوعة” with a distinct symbol. Retain red/green only as supplementary cues. Expose the status text to assistive technology.

**Keyboard and state decisions**

- Maintain logical editing order: invoice fields → each item’s editable fields → subsequent items. Shift-Tab reverses traversal.
- With **Full Keyboard Access enabled**, every action—including Add line, item actions, menus, and Save—must be reachable and activatable using system keyboard commands. Ordinary iPad text/content focus and Full Keyboard Access are separate test paths.
- Provide Add line as a discoverable keyboard command as well as an onscreen button. Choose its binding after checking existing commands and Arabic/Latin keyboard layouts. Preserve standard copy, paste, undo, redo, and save meanings.
- Activating Add line inserts one item and focuses its description. Focus remains visibly indicated and scrolls into view. Return inside an editable field must not unexpectedly save the invoice.

Apple distinguishes ordinary iPad keyboard focus from the broader access supplied by [Full Keyboard Access](https://developer.apple.com/design/human-interface-guidelines/keyboards).

Keep a stable draft model independent of the layout, with stable item identifiers. Preserve quantities, raw partially entered text, validation state, selected item, focused field, caret/selection, undo history, and scroll anchor across resizing. Reflow must not commit, cancel, reload, or create an undo step.

Retain the existing calculation and rounding rules. Valid edits update totals normally; incomplete numeric input remains editable and shows corrective feedback without silently becoming zero. If totals temporarily use the last valid value, label them as awaiting a valid entry. Persist the draft for interruption recovery.

**Acceptance checks**

| Check | Pass condition |
|---|---|
| Combined constraints | At 420 pt, Arabic, 200% text, and hardware keyboard attached, every field, action, status, and total remains readable and usable. |
| Text and height | Long Arabic labels, Bold Text, and reduced window height cause wrapping and vertical scrolling without overlap, clipped glyphs, or hidden focused controls. |
| Mixed direction | Vendor shapes correctly; ID and email display, edit, paste, and copy in exact order. Currency formatting preserves 1240.50 SAR. |
| Icons | Navigation adapts to RTL; ordinary object symbols and logos retain their meaning. |
| Payment status | Paid/unpaid remain distinguishable in grayscale and are announced with their text meaning. |
| Keyboard completion | Complete an invoice without touch. With Full Keyboard Access, reach and activate Add line and Save; traverse backward without traps. Test Arabic and Latin layouts. |
| Resize continuity | Enter quantities, select text, then repeatedly resize wide → 420 pt → wide. Draft values, partial input, focus, selection, and undo history survive. |
| Totals | Reflow alone leaves all totals identical. Valid quantity edits recalculate correctly; invalid input never silently alters amounts. |
| Recovery | Switch apps and return; restore the same draft and editing context. |
| Accessibility | Verify reading order, field names, status meaning, focus visibility, activation geometry, and contrast in light/dark appearances on iPad. |

The supplied description establishes the current clipping, color-only status, mechanical mirroring, unreachable Add line, and resize data-loss failures. **Runtime acceptance checks have not been executed**; this is the revised specification.