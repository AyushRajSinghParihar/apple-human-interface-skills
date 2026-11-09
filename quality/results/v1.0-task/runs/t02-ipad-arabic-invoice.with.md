At 420 pt, use a single-column Arabic editor with stacked line items and a complete totals section. Resizing changes presentation while preserving the invoice draft, quantities, focus, and undo history.

The following is the proposed behavior contract; spacing choices are product decisions, informed by Apple’s guidance.

**Revised layout**

| Area | Specification at 420 pt and 200% text |
|---|---|
| Page | One vertical scrolling surface within safe areas. Start with 16 pt horizontal margins; no horizontal page scrolling. |
| Header | Wrapping invoice title, invoice ID on its own line, and explicit payment status. Put editing actions on a separate row when needed. |
| Invoice details | Persistent label above each value or field. Arabic labels align to the right. Vendor, invoice ID, and email each occupy a full-width group. |
| Line items | Replace fixed columns with vertically stacked groups: description → quantity → unit price → line total → line actions. Repeat labels for every item. |
| Add line | A visible, full-width labeled button immediately after the last item. Accessible through touch, keyboard, and assistive navigation. |
| Totals | Keep every existing total component and its calculation rules. Place the full breakdown after Add line. Stack each label above its amount when a pair cannot fit. Give the grand total stronger typographic emphasis. |
| Wider windows | Restore aligned columns only when all labels, fields, amounts, and actions fit at the current text size. Base this on available space and measured content, rather than orientation alone. |

Use system text styles with Arabic shaping and Dynamic Type. At 200%, grow rows and controls, wrap labels, and preserve full values; do not shrink text to recover columns. Use at least 44 × 44 pt activation areas as this editor’s touch target specification.

Keep totals in the document flow so they cannot obscure the active field or consume a short window. Keyboard navigation must scroll focused controls into view. These choices follow Apple’s [layout adaptability](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability), [typography](https://developer.apple.com/design/human-interface-guidelines/typography), and [accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) guidance.

**Arabic and mixed-direction content**

| Content | Required behavior |
|---|---|
| Interface structure | Use semantic leading/trailing layout. Arabic reading order begins at the right; stacked content remains top-to-bottom. |
| `مؤسسة النور` | Render naturally as Arabic, right-aligned, with correct joining and room for wrapping. |
| `INV-2026-04` | Preserve the exact identifier as an isolated left-to-right run. Do not reverse characters, digits, or hyphens. |
| `accounts@example.test` | Use an isolated left-to-right value and native email editing behavior. Preserve exact copy/paste content. |
| `1,240.50 SAR` | Preserve the numeric value **1240.50** and currency **SAR**. Format for the selected Arabic region and numbering preference; never reverse digits or mirror glyphs. |
| Icons | Use system directional variants for Back/Next and reading-order arrows. Preserve checkmarks, plus signs, logos, and ordinary object/tool icons. Review custom composite icons individually. |

Arabic alone does not determine the numbering system. Use Arabic–Saudi Arabia as the initial formatting assumption, while respecting the person’s region and numbering preference. Apply bidirectional isolation at presentation boundaries without inserting formatting characters into stored identifiers or email addresses. Have a native Arabic reviewer verify wording, punctuation, and mixed-script rendering.

This replaces mechanical mirroring with Apple’s [right-to-left guidance](https://developer.apple.com/design/human-interface-guidelines/right-to-left).

**Keyboard, status, and editing behavior**

- **Navigation:** Define the logical route as invoice details → each item’s editable fields and actions → Add line → remaining editing actions. Shift-Tab reverses traversal. Within native iPad focus groups, preserve expected arrow navigation; arrows inside text fields retain native caret behavior.
- **Add line:** Include it in Full Keyboard Access traversal with a visible system focus indicator. Support native button activation. After activation, append one item and focus its description. Expose the same command in the app’s keyboard command interface so ordinary keyboard users also have a discoverable route.
- **Keyboard modes:** Test ordinary content focus and Full Keyboard Access separately. Ordinary iPad Tab navigation alone does not establish reachability of every button.
- **Editing conventions:** Preserve standard copy, paste, selection, undo, and redo. Do not intercept character-entry keys or system accessibility shortcuts for invoice actions.
- **Payment status:** Show localized text such as “Paid” or “Unpaid,” paired with an appropriate symbol. Red/green may supplement meaning. Expose the actual status to assistive technology; do not infer it from color.
- **Validation:** Accept supported localized numeric input using locale-aware parsing. Preserve incomplete input while typing. Explain invalid quantities beside the field; never silently replace them with zero.

These decisions follow Apple’s [keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards), [focus](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection), and [text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields) guidance.

**State and totals contract**

Keep the draft model independent of the compact/wide layout, with stable invoice and line-item identities. Resizing, rotation, text-size changes, and keyboard attachment must preserve:

- Entered quantities and other draft values, including incomplete numeric text.
- Active line and field, caret/selection, validation feedback, and undo/redo history.
- Editing route and a scroll anchor that keeps the active field visible.

A layout transition must neither save nor cancel an edit. Totals use the same decimal arithmetic, rounding, taxes, and discounts as before. Valid quantity changes update dependent totals; incomplete or invalid input retains the last valid totals with an explicit “Totals awaiting valid quantity” message.

**Acceptance checks**

Run the combined case first: **Arabic + 420 pt + 200% text + hardware keyboard**.

| Check | Pass condition |
|---|---|
| Reflow | All labels, fields, actions, and totals remain readable and reachable without overlap, clipped Arabic glyphs, reduced text size, or horizontal page scrolling. |
| Sample content | Vendor shapes correctly; ID and email retain exact character order when viewed, edited, and copied. Amount remains 1240.50 SAR under localized formatting. |
| Direction | Back/Next adapt correctly; digits, checkmarks, plus signs, logos, and object icons retain meaning. |
| Keyboard completion | With Full Keyboard Access, reach and activate Add line, edit the new item, and reach remaining editing actions without touch. Reverse navigation works; no focus traps occur. |
| Ordinary keyboard use | Native text editing works, focus groups behave predictably, and Add line is available through its discoverable command. Test Arabic and Latin keyboard layouts. |
| Resize continuity | Enter quantities, leave one field partially edited, select text, and repeatedly resize wide ↔ 420 pt. Values, partial text, focus, selection, and undo history survive. |
| Totals integrity | With no data edits, every total is identical before and after adaptation. A valid quantity edit changes only dependent totals; invalid input shows feedback without fabricating a result. |
| Noncolor status | Paid/unpaid remain distinguishable in grayscale and with Differentiate Without Color enabled. Assistive output names the status. |
| Accessibility | Verify labels, field values, item context, reading order, focus visibility, touch geometry, and contrast in light/dark appearances, Bold Text, and Increase Contrast. |

**Evidence status:** The supplied current behavior fails text enlargement, color-independent status, numeral/icon direction handling, Add line reachability, and resize continuity. The revised specification addresses each failure; runtime acceptance checks have **not been executed**.