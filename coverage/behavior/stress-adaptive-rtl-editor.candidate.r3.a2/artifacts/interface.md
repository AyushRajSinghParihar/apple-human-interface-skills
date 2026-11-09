# iPadOS invoice editor — adapted specification

This is an implementable interface and state contract, not an executed app. The source describes fixed left-aligned columns, clipping at 200%, red/green-only payment status, mechanical numeral/play-icon mirroring, inaccessible Add line via Tab, and quantity resets on resize. The following replaces those behaviors.

## Content and invariants

Preserve vendor `مؤسسة النور`, invoice ID `INV-2026-04`, email `accounts@example.test`, currency SAR and amount `1,240.50 SAR` (canonical decimal 1240.50). No line-item breakdown, tax rules, payment value or calculation implementation was supplied. Do not invent a breakdown or infer Paid from color. Preserve the existing payment value and calculation/rounding rules when implementing this specification.

Formatting, language, text-size, orientation and window changes must never mutate monetary values, quantities or payment state. Calculate from canonical decimal data, never from rendered currency strings. The unchanged sample remains exactly 1240.50 SAR across every presentation transition.

## Arabic and mixed-direction content

Use the existing framework's locale-aware leading/trailing layout and native bidirectional text handling. Arabic interface leading is right; short labels and row groups align consistently to leading. Translate interface labels and validation messages; proposed Arabic strings below require native-language review. Paragraphs follow their own language. Do not mirror the entire view with a transform.

| Element | Required behavior |
|---|---|
| Vendor | Display `مؤسسة النور` naturally RTL; preserve stored characters and shaping. |
| Invoice ID | Treat `INV-2026-04` as an isolated LTR token inside the RTL label/value group. Copy returns the exact original string. |
| Email | Treat `accounts@example.test` as isolated LTR text; preserve punctuation, cursor editing and copy order. |
| Amount | Format canonical 1240.50 with the selected Arabic regional locale and SAR currency. Locale chooses numeral forms, separators and currency placement; never reverse digits or glyphs. Western or Eastern numeral forms may be appropriate. Keep currency associated with the amount. |
| Back/forward navigation | Mirror reading-order navigation through system direction behavior. |
| Play icon | Preserve the conventional playback triangle orientation; playback is not reading-order navigation. Retain its existing playback outcome and give it a localized action name. Its exact media target remains unspecified. |
| Logos, checkmarks, physical-direction imagery | Preserve meaning and orientation; do not mechanically flip them. |

Use directional isolation at rendering boundaries without inserting control characters into saved IDs/emails. A locale change during editing retains the raw draft and its parsing locale until explicit commit or cancel, avoiding reinterpretation of separators.

## Resizing and 200% text

At the supplied compact window width of **420 pt**, use one vertically scrolling editor, inside system safe areas and clear of window controls. Preserve iPadOS system window chrome. No horizontal page scrolling or fixed column widths are required to finish editing.

Order: invoice identity and vendor → email → payment status → line items → Add line → totals. Each line is a stable identified group containing its existing fields; description, quantity, unit price and line amount, where present, each retain persistent labels. At compact width, place each label above its value/control. Totals remain a labeled summary after the items, with label above value when needed. Keep the full total and currency reachable; do not hide totals behind a collapsed section.

At wider widths, aligned comparison columns may return only when all labels, values and controls fit at the current text size. Determine fit using available content width and actual localized text; 420 pt is a supplied test case, not a universal Apple breakpoint. Reflow before clipping. At 200% text use the stacked arrangement, flexible row heights and wrapping labels/buttons. Long ID/email display values can wrap at display boundaries without changing their content; editing fields retain native caret scrolling and full selection/copy access. No shrink-to-fit for essential text.

Prefer system semantic text styles: title for invoice identity, headline for section headings and total, body for fields and values, supporting style for explanatory messages. Honor Dynamic Type and Bold Text, scaling meaningful symbols too. Explicitly verify at least 200% of baseline text: a 17 pt body baseline needs a measured size of at least 34 pt; Dynamic Type categories are not uniform percentages. Do not cap larger accessibility settings to 200%.

One primary vertical scroll owner reveals the focused field/insertion point only as much as necessary. Respect software keyboard insets even when hardware keyboard use is expected. Retain an item-based scroll anchor during reflow. A short window may require vertical scrolling to totals, but no overlay may cover them or Add line.

## Fields, status and actions

Persistent localized labels include Vendor / المورد, Invoice number / رقم الفاتورة, Email / البريد الإلكتروني, Quantity / الكمية, Unit price / سعر الوحدة, Total / الإجمالي, and Add line / إضافة بند. Retain the existing editable/read-only distinction for identity fields; the supplied brief does not establish their editability.

Quantity and price edits retain raw text while incomplete. Use locale-aware numeric parsing, including supported Western/Eastern digits. On explicit commit or leaving the field, validate against existing domain and precision rules; show an inline textual correction associated with the field for empty, partial or invalid required values. Never coerce invalid input to zero or discard it. Until corrected, show the last committed totals with a visible “Totals exclude uncommitted edits” explanation. Valid commit updates the canonical value and totals once; resizing never commits an edit. Provide trailing Clear for editable short fields, retaining an undoable draft edit. Validate email on leaving if editable; preserve rejected text for correction.

Payment status pairs its existing value with localized text and a distinct symbol: for example Paid / مدفوعة with a checkmark, or Unpaid / غير مدفوعة with an outlined pending symbol, only when those are actual model states. Color is supplementary. Use semantic system colors; measure actual light/dark and Increase Contrast combinations before claiming contrast compliance.

Add line is a visible system text button following the last line (also present in an empty invoice). Give it a normal nondestructive role, localized visible/accessibility name and at least a 44 × 44 pt activation region, growing for wrapped text. Activation inserts exactly one stable-ID blank draft line, preserves every existing line, and focuses its first editable field. An empty draft line does not silently contribute zero to a finalized total. Retain existing line order; no sorting or deletion behavior is introduced by resizing. Playback remains a separate named button with the same target-size and keyboard-access requirements; its availability depends on existing media state.

## Hardware keyboard contract

Preserve native text editing, selection, copy/paste, input-source switching and standard Undo/Redo meanings; do not intercept arrows inside fields for row navigation. Focus, active editing and persistent line selection are separate states, each surviving reflow.

Ordinary iPad content focus: Tab/Shift-Tab traverse logical groups in reading/task order (identity, line groups, actions, totals); within suitable custom groups arrows follow RTL reading order. Editable fields follow native logical field traversal. Do not assume ordinary Tab focus automatically reaches every system button.

Full Keyboard Access: every editable field, Clear, Add line and existing playback control must be reachable and activatable through the system's configured navigation/activation keys, with visible focus and no trap. Verify Tab/Shift-Tab reach Add line under the tested FKA configuration. Localize labels and keep focus identity independent of visual row/column positions.

Provide **Command-L: Add line** as a proposed app command available even while editing, subject to collision checks on the actual supported keyboard layouts. Show its localized title in system shortcut discoverability. It invokes the same insertion operation as the visible button; it does not commit or erase another field's raw draft. Preserve Command-C/X/V/A and Command-Z/Shift-Command-Z in their standard contexts. Return in a field commits that field when valid; it never silently submits the invoice or activates playback. Do not invent a Save/Send shortcut without an existing product action.

## State transitions

Own invoice and edit state outside width-dependent view instances. Key fields by invoice ID, stable line ID and field ID, never by row position. Retain canonical values, raw drafts, parsing locale, validation errors, dirty flag, current line selection, focus/caret selection, undo/redo history and scroll anchor.

| Event | Data and state outcome |
|---|---|
| Resize wider → 420 pt → wider, rotate, change text size or direction | Change presentation only. Reattach focus/caret to the same stable field, retain raw draft/errors/undo and scroll anchor, then minimally reveal focus. No reload, defaults, auto-commit or calculation change. |
| Valid explicit field commit | Update the existing model using its calculation/rounding policy; update totals once and retain ordinary undo behavior. |
| Invalid commit | Keep raw text and last committed canonical value; show correction and explain stale totals. Allow navigation without losing the draft. |
| Add line by touch, FKA or Command-L | Insert one draft line through one shared command; preserve all previous edits and totals until valid values are committed. |
| Window loses/recovers activation | Preserve invoice identity and all in-progress state; restore the same editor context. |
| Close/reopen | Checkpoint committed data and raw draft state before close; restore the same invoice/draft on reopening. Never silently discard dirty or invalid text. Storage and crash-recovery guarantees need implementation evidence. |

The state ownership, command binding, reflow rule and stale-total treatment are product design decisions applying the guidance, not mandated Apple APIs. No framework replacement is specified.

## Local source basis

These official links identify the articles represented by the installed local snapshot; no network lookup was performed.

- Resizable iPad task continuity: [Designing for iPadOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados#Best-practices), [Layout — Adaptability](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability), [Windows — iPadOS](https://developer.apple.com/design/human-interface-guidelines/windows#iPadOS).
- Arabic alignment, numerals and directional assets: [Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left#Numbers-and-characters).
- Text growth, hierarchy, status alternatives and targets: [Typography — Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type), [Accessibility — Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision), [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices).
- Reachable commands and separate focus modes: [Keyboards — Best practices](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices), [Focus and selection — iPadOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#iPadOS).
- Labeled editing, row context and reveal behavior: [Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields#Best-practices), [Labels](https://developer.apple.com/design/human-interface-guidelines/labels#Best-practices), [Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables#Content), [Scroll views](https://developer.apple.com/design/human-interface-guidelines/scroll-views#Best-practices).
