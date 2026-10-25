# Adaptation result

Updated `interface.md` in place from the supplied defect description to an implementable iPadOS interface and state specification. This deliverable is a specification change; no application code or executable interface was supplied or implemented.

## Concrete decisions

| Supplied behavior | Replacement contract |
|---|---|
| Fixed left-aligned columns | Locale-aware leading/trailing alignment; one stacked scrolling editor at 420 pt, columns only when content fits. |
| Labels clip at 200% | Semantic scalable typography, growing rows, wrapping labels and stacked totals; no essential shrink-to-fit. |
| Arabic mechanically mirrors numbers/play | Native bidirectional layout; isolated LTR ID/email, locale-formatted SAR amounts with preserved numeric order, unchanged conventional play triangle. |
| Payment state only red/green | Preserve the actual status and add localized text plus a distinct symbol; color supplements meaning. |
| Tab cannot reach Add line | Explicit ordinary-focus and Full Keyboard Access contracts, visible Add line and proposed discoverable Command-L command. |
| Resize resets quantities | Stable invoice/line/field identity and draft state outside adaptive views; reflow does not commit, reset or recalculate. |

The original vendor `مؤسسة النور`, ID `INV-2026-04`, email `accounts@example.test` and exact decimal amount 1240.50 SAR remain in the specification. Taxes, rounding, payment value and line breakdown are unknown; the result requires preserving existing rules rather than deriving them from the sample amount. Invalid drafts stay editable and totals identify when they exclude uncommitted edits.

## Acceptance checks and evidence status

**Passed — document inspection only:** the revised artifact retains every supplied sample value, defines corrections for all six reported barriers, distinguishes numeric data from formatting, and specifies survival of raw edits, caret/focus, validation, selection, undo history and scroll anchor. Both requested Markdown files exist. These checks establish specification coverage only.

**Failed — supplied baseline report:** clipping at 200%, color-only state, blanket mirroring, inaccessible Add line and quantity loss on resizing are explicitly described in the original brief. These are reported defects, not failures reproduced on a device. The revised design replaces their contracts; runtime resolution is unverified.

**Not executed — implementation acceptance matrix:**

| Check | Procedure and pass condition |
|---|---|
| Combined stress case | Arabic RTL, 420 pt window, measured ≥200% text, hardware keyboard attached. Read all labels/values/status, edit a quantity, add a line and reach the full total with vertical scrolling. No clipping, overlap, horizontal page scroll or hidden action. Repeat with Bold Text. |
| Resize continuity | Record model values and total, dirty draft such as an incomplete decimal, field/line IDs, caret selection, errors, undo stack and scroll anchor. Resize wide → 420 pt → wide repeatedly, including while composing Arabic text. All survive; no forced commit. Reformatting alone leaves total exactly 1240.50 SAR. |
| Valid calculation | On a fixture with known lines/tax/rounding rules, commit a valid quantity change and compare with an independent expected total. Resize and switch direction/text size; updated total remains identical. Undo/redo retains expected model and totals. The supplied amount alone cannot validate arithmetic. |
| Invalid numeric entry | Exercise empty, partial, malformed, valid Western and Eastern digit input, local decimal separators and paste. Invalid drafts remain intact with corrective text and clearly marked last-committed totals; no silent zero or separator stripping. Change locale mid-edit without reinterpreting the draft. |
| Mixed text | Render vendor beside ID/email and SAR total in RTL; inspect native shaping, punctuation and digit order. Select/copy ID/email and compare exactly with original strings. Test insertion, deletion and selection at Arabic/Latin boundaries. Native Arabic reviewer approves labels and regional numeral/currency choice. |
| Keyboard without FKA | Traverse text/content groups with Tab/Shift-Tab and native in-group navigation. Command-L inserts exactly one line while preserving other drafts and focuses the new line's first field. Verify localized discoverability and no collisions on Arabic and Latin layouts. Standard editing/input-source shortcuts retain meaning. |
| Full Keyboard Access | With FKA enabled and its configuration recorded, reach/activate every field, Clear, Add line and playback through keyboard navigation; Tab/Shift-Tab reach Add line in that configuration. Focus stays visible and exits each group. This is separate from ordinary content-focus testing. |
| Status and accessibility | In grayscale or Differentiate Without Color, status remains unambiguous from text/symbol. Check meaningful field associations, button names/roles and status values with VoiceOver/Accessibility Inspector. Verify Switch Control reachability. |
| Appearance and geometry | Measure light/dark and Increase Contrast combinations with a contrast calculator under the local guide's stated scope; measure ≥44 × 44 pt button activation regions, separation and focus-ring clearance. No measurements exist yet. |
| Overflow and boundaries | Test empty and long invoices, long Arabic labels, long ID/email, shortest supported window height, software keyboard shown/hidden and intermediate widths. All items/totals reachable; caret reveal is minimal, safe areas/window controls respected. Test 100%, 200% and largest supported accessibility text. |
| Lifecycle | Deactivate/reactivate, close/reopen with a valid and an invalid draft. Restore the same invoice and draft, focus context and values without silently dropping work. Confirm storage guarantees separately from resize behavior. |
| Playback semantics | Identify what supplied play controls operate, test their localized name, unchanged orientation and activation with touch/FKA. No media target or implementation was supplied. |

## Guidance audit and limits

Explicitly read the installed root `.agents/skills/apple-hig/SKILL.md` from disk, then searched `references/topic-index.md`. Read the Getting started family and Designing for iPadOS topic before its source guide. Also read the Foundations, Inputs, Layout and organization, Selection and input, Menus and actions, and Presentation family procedures; routed topic procedures were read before their supporting article references.

Selected topics: Designing for iPadOS; Right to left; Layout; Typography; Accessibility; Keyboards; Focus and selection; Text fields; Buttons; Lists and tables; Labels; Windows; Scroll views. Reads used one file per shell command. Material source links are included in `interface.md`; they refer to installed snapshots, not web verification. No browsing was performed.

Missing evidence: application source/framework and deployment target, actual field inventory and payment model, calculation/rounding fixtures, persistence implementation, supported window bounds and OS versions, font/rendering measurements, regional Arabic preference and language review, shortcut collision results, screenshots and recorded device/assistive-input runs. No SDK compilation, GUI, device, accessibility execution or runtime success is claimed. API availability and current OS window/keyboard behavior remain to be verified against the implementation and supported Apple environments.
