# iPadOS budget screen — Arabic/English RTL specification

## Scope and retained behavior

Adapt the budget hierarchy and its existing actions to an Arabic RTL interface. Preserve budget IDs, amounts, currencies, sorting, selection, expansion, current detail route, and unsaved edits. No framework or screen geometry was supplied; use the existing stack and standard directional layout behavior. The example labels below are proposed fixtures, not recovered product copy. Arabic region and preferred numeral system require product/native-language confirmation; do not assume all Arabic locales format alike.

## Layout and hierarchy

- Set interface direction from the app's selected language. Use semantic leading/trailing constraints, never a negative scale transform on the screen. In Arabic, leading is right and trailing is left; English UI remains LTR.
- Put primary headings and hierarchy origins at the top/leading edge. Arabic category rows start on the right; each child is inset one existing hierarchy spacing step from the right. Preserve parent/child relationships and logical item order; do not reverse the data array merely to mirror presentation.
- For navigation into a child, put its disclosure indicator at trailing (left in RTL), pointing left. Back is at leading (right), pointing right. Returning restores the selected item and prior expansion/scroll context. An expand/collapse indicator instead points toward reading progression when collapsed and down when expanded; toggling changes expansion without navigating.
- Retain the existing pane model. If it displays hierarchy beside detail, hierarchy occupies leading/right and detail follows to the left. When available width cannot fit both readable panes, show the current route in one pane with a visible Back action; restore the same selection, route and draft on widening. Determine the transition from measured content fit, not orientation or a fabricated device breakpoint.
- A budget row places its title at leading and amount at trailing. When either cannot fit, wrap the full title and put the amount below in the same row. Keep the value visibly associated with its label; never overlap the disclosure control. Important content and actions respect safe regions.

## Directional asset contract

| Element | Arabic presentation | Meaning to preserve |
|---|---|---|
| Back / Next / Previous navigation | Mirror reading-order direction; Back right, Next left | Parent/forward route, not physical direction |
| Hierarchy indentation and disclosure | Leading/right origin, deeper indentation toward left | Same hierarchy and state |
| Media Play | Keep right-pointing triangle; remove mechanical flip | Conventional playback, not forward navigation |
| Literal left/right arrow or arrow to an onscreen target | Keep physical meaning; target-pointing arrows follow the actual target location | Correct place/direction |
| Logos, photographs, ordinary objects, checkmarks | No automatic flip | Identity and real-world meaning |

Let standard controls supply RTL behavior and prefer available directional/localized symbols. Apply a manual asset override only after confirming it is needed, so symbols are not mirrored twice. Audit each existing arrow by its action rather than its shape. Do not infer that every media glyph is a navigation arrow.

## Mixed text and money

- Short labels and one/two-line UI blocks follow interface alignment. Keep category list titles consistently leading/right aligned even for an English entry such as `Cloud Storage`.
- For longer paragraphs (three or more lines), use the paragraph's own base language: Arabic right, English left. Embedded English tokens retain their internal LTR order inside Arabic prose.
- Treat a standalone email value such as `finance@example.com` as LTR and left aligned in its own value field; its Arabic label stays leading/right aligned. A list title containing an email still follows the list's consistent alignment, with the email run LTR. Alignment and text direction are separate properties.
- Store money as the existing numeric value plus currency identity. Use a locale-aware currency formatter for the selected region and numbering preference, including separators, currency placement, spacing and signs. Never reverse digits, reverse a formatted string, mirror glyphs, or concatenate currency fragments to force a visual order.
- Isolate embedded email, identifier and formatted money runs from surrounding text using the existing text system's bidirectional facilities. Preserve formatter output and logical storage/copy order; presentation controls must not become part of saved values. Do not force the entire Arabic sentence LTR to repair a number.
- Numeric fixture: amount 1234.50, currency SAR. With Western digits its numeric run remains `1,234.50`; with Eastern Arabic digits an illustrative run is `١٬٢٣٤٫٥٠`. Exact whole currency strings, negative-sign placement and numeral defaults come from the chosen locale formatter and need native review. Neither rendering may change the amount to 5432.10 or reverse the digit sequence.

## Readability and operation

Use semantic system text roles: screen title, category headline, body label/value and supporting detail. Support Dynamic Type and Bold Text with Arabic shaping and diacritics intact. Allow full category labels such as `المصروفات المنزلية والاشتراكات الشهرية` to wrap into growing rows; remove fixed one-line heights. Stack values and reduce visible columns before shrinking text or clipping essential content. Do not impose a fixed line cap on essential labels. Keep navigation and actions reachable with touch and the existing keyboard/pointer paths after reflow. Use the iPadOS 44 × 44 pt default activation area as the design starting point for controls; verify actual geometry in implementation.

## Acceptance contract

1. Arabic UI: child disclosure points left, Back points right, indentation starts at right. Opening/returning preserves item identity and expansion. English UI: corresponding directions and leading edges return to LTR without double mirroring.
2. Play remains a right-pointing triangle in both interfaces and starts the same media action. Literal physical arrows retain their meaning.
3. Format 1234.50 SAR, -1234.50 SAR, zero and 1234567.89 SAR under the selected Arabic region with both supported numeral preferences and an English locale. Values and digit order survive display, copy/paste and edit/save round trips; signs and currency remain attached to the correct amount.
4. Render Arabic prose containing `finance@example.com`, `Cloud Storage`, parentheses and a currency value. Verify punctuation boundaries, LTR token order, paragraph alignment, and consistent list alignment. In editable fields exercise cursor movement, selection, deletion and pasted mixed text.
5. At smallest/largest supported iPad window sizes and intermediate resizing, default and every supported Dynamic Type size including the largest accessibility size, plus Bold Text: full Arabic labels and amounts remain readable, no overlaps occur, and all actions remain reachable. Include at least 200% text enlargement. Record actual dimensions and settings when executed.
6. Navigate parent → category → item, resize narrow → wide, then return. Selection, route, expansion and any existing draft remain intact. Verify touch, keyboard and assistive navigation on the implementation; visible mirroring alone is insufficient evidence.

## Guidance basis

These decisions apply the installed local snapshot of Apple's [Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left) guidance (Text alignment, Numbers and characters, Controls, Images, Interface icons), [Layout](https://developer.apple.com/design/human-interface-guidelines/layout) (Visual hierarchy, Adaptability), [Typography](https://developer.apple.com/design/human-interface-guidelines/typography) (Supporting Dynamic Type), [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) (Vision, Mobility), and [Designing for iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados). Links identify sources; no web retrieval or SDK validation was performed.
