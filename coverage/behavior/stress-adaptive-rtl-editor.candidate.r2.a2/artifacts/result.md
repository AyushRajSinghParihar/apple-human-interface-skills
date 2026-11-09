# Adaptation result

Edited interface.md in place into an implementable iPadOS interface and state contract. The supplied artifact was a short prose brief; no application code, framework, screenshots, or executable editor was supplied. This result is a specification adaptation.

## Concrete decisions

| Supplied problem | Result in interface.md |
| --- | --- |
| Fixed left-aligned columns at 420 pt | RTL leading/trailing layout; stacked labeled line groups; one vertical scroll owner; fit-based columns at wider widths |
| Labels clip at 200% | Semantic system text, growing rows, wrapping labels, scaled meaningful symbols, no essential-label truncation; 34 pt body fixture from 17 pt default |
| Red/green-only payment state | Actual state expressed by localized text plus distinct symbols; no payment-state inference |
| Numerals/play icons mechanically mirrored | Native bidirectional text; isolated LTR invoice ID/email; locale-formatted amounts with unchanged digit order/value; conventional Play orientation; reading-order navigation mirrors |
| Tab cannot reach Add line | Visible system button, explicit Full Keyboard Access path, ordinary field/group focus distinguished, proposed discoverable Command-Shift-L command |
| Resize resets quantities | Session owned outside layout, stable invoice/line IDs, preserved raw drafts, parse locale, focus/caret/composition, validation, undo and scroll anchor |
| Preserve totals | Canonical decimal model and unchanged calculation/rounding; resize performs no commit; synchronized total displays; last-valid-total explanation for incomplete input |

The supplied vendor, invoice ID, email and amount remain explicitly present. Arabic labels are proposals requiring linguistic review. Exact breakpoints beyond the supplied 420 pt, shortcut compatibility, numeric input constraints, and persistence support require implementation evidence. The 44 × 44 pt activation target is the chosen iPad design baseline; the local accessibility guide also lists a smaller minimum, which is not used to justify dense controls here.

## Acceptance checks and status

Passed — static artifact inspection only:

- All four supplied content fixtures occur verbatim in interface.md.
- The adaptation explicitly covers Arabic direction, 420 pt, 200% text, keyboard access, payment-state meaning, totals and editing-state invariants.
- Root, selected family routes, topic procedures and supporting local guidance were read by installed package path. Commands read one file each. No web sources were fetched.

Failed — supplied baseline behavior, as stated in the original brief (not independently reproduced): enlarged-label clipping, color-only state, indiscriminate mirroring, unreachable Add line, and quantities reset by resize. Fixed columns also need the specified adaptation. Their runtime resolution is unverified.

Not executed — implementation acceptance matrix:

| Check | Procedure and pass condition |
| --- | --- |
| Combined worst case | Arabic at 420 pt, 200% text, keyboard attached, short available height (proposed 600 pt fixture); all fields, full labels, payment state, Add line and totals readable/reachable without overlap or horizontal page scrolling |
| Continuous adaptation | Wide (proposed 1024 pt) → 420 pt → wide at default and 200%, plus intermediate widths/heights; no lost/duplicated line, action, draft, error or selection; window controls never overlap app controls |
| Mixed-direction content | Render مؤسسة النور, INV-2026-04, accounts@example.test and 1,240.50 SAR together; verify shaping, punctuation, digit order, selection, caret movement, paste and exact copy round trip; review with Arabic speaker |
| Locale formatting | Western/Eastern numeral preferences and Arabic regional formats; amount remains decimal 1240.50 and SAR, no internal reversal or currency conversion; active draft retains original parse locale |
| State preservation | Enter a valid quantity, then a partial decimal and invalid text in other lines; select part of a draft, resize repeatedly and enlarge text; compare session snapshots including raw text, committed numbers, totals, validation, caret, focus, scroll anchor, dirty state and undo history |
| Arithmetic | Load known real line/tax/discount fixtures and existing rounding expectations; baseline amount remains 1,240.50 SAR before edits; valid commits change totals exactly once; invalid/partial entry retains last-valid totals with explanation; undo restores expected data and totals |
| Keyboard without Full Keyboard Access | Traverse text fields/groups forward and backward; native text arrows and editing shortcuts work; discover and invoke Add line command; exactly one draft line inserted and focused; no input-source/system shortcut collision |
| Full Keyboard Access | From invoice entry, reach and activate every control including Add line, Clear and existing Play, then return through reverse traversal; visible focus, no trap, no unintended Return activation; repeat in Arabic keyboard layout |
| Field validation | Empty, partial decimal, invalid, valid, pasted localized digits, long email/ID, and trailing Clear; persistent labels/errors stay associated; no coercion to zero or loss on blur/reflow |
| Visual access | Default/200%/largest supported accessibility sizes, Bold Text, light/dark and Increase Contrast; inspect actual text and focus geometry; measure foreground/background contrast with a calculator; measure targets at least 44 × 44 pt and separation |
| Assistive access | Supported Apple accessibility tools and VoiceOver/Switch Control traversal identify correct field labels, values, errors, payment state and actions; editing and Add line complete without touch; spoken order follows logical form order |
| Lifecycle | Switch input methods, deactivate/reactivate window, close/reopen and restore after termination as supported; verify draft persistence policy, correct invoice identity and no silent overwrite; document unsupported restoration explicitly |
| List boundaries | Empty, one-line and long invoices; all lines accessible and totals correct; Add line reveals new field without excessive scroll jump |

## Guidance and audit trail

Installed root: `.agents/skills/apple-hig/SKILL.md`. Searched `references/topic-index.md` for task concepts before completing routing. Read these families and their selected `.topics/apple-hig-<topic>/SKILL.md` procedures before supporting `references/<topic>.md` files, all under that installed root:

| Family | Topics |
| --- | --- |
| apple-hig-getting-started | designing-for-ipados (platform procedure and guide read first) |
| apple-hig-foundations | layout, right-to-left, typography, accessibility |
| apple-hig-inputs | keyboards, focus-and-selection |
| apple-hig-selection-and-input | text-fields |
| apple-hig-menus-and-actions | buttons |
| apple-hig-presentation | windows, scroll-views |
| apple-hig-layout-and-organization | lists-and-tables, labels |

Official article/section attribution is included beside the specification's guidance basis in interface.md. These links were taken from supplied local references; no current online verification is implied. Some batched tool output was truncated; relevant text/focus procedures and source sections were subsequently read with bounded output. Typography's full numeric table was unnecessary; the relevant legibility, system-font and Dynamic Type sections were read. No source conflict affecting these decisions was identified.

## Missing evidence

Need the actual editor implementation and supported iPadOS versions/framework to verify feasibility, build it, and run the matrix. Need real line/tax/discount fixtures, rounding rules, quantity constraints, actual payment-state enum and Play behavior; none were supplied. Need native Arabic review, rendered layouts, measured colors/targets, device or simulator resize/text tests, hardware-keyboard and Full Keyboard Access execution, accessibility execution, and draft-restoration evidence. No device, SDK, GUI, accessibility, build or runtime execution is claimed.
