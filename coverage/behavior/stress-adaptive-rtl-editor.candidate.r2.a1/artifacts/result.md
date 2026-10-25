# Adaptation result

Edited `interface.md` in place into an implementable iPadOS design contract. It preserves the supplied vendor, ID, email, decimal amount 1240.50 and SAR, replaces fixed columns with compact cards at 420 pt, specifies 200% reflow, semantic RTL behavior, labeled payment states, and keyboard access to Add line. No executable app was supplied or changed.

## Decisions

- Presentation changes never mutate the draft or totals. Stable invoice/line/field identities preserve raw input, composition, quantities, validation, undo, selection, caret, focus, and scroll anchor. Invalid numeric edits retain the last valid total with an explicit pending indication.
- Arabic layout mirrors reading order; email/ID and digit order remain intact. Playback Play is preserved. Arabic–Saudi Arabia is a provisional formatter locale, not an inferred user preference. Translations need review.
- At 420 pt and enlarged text, all fields, Add line, Save, and total remain in a vertical flow. Wider columns depend on measured fit. System window controls and keyboard occlusion are accounted for.
- Ordinary iPad focus and Full Keyboard Access have distinct acceptance paths. Standard editing keys remain intact; Add line has an explicit focus destination and activation result.

## Acceptance checks and status

Passed — static specification inspection only: supplied strings and amount are retained; each reported barrier has an explicit correction; resizing is prohibited from changing quantities/totals; invalid drafts and focus restoration have defined outcomes; source links and evidence limits are documented.

Failed — the original supplied description explicitly reported clipping at 200%, red/green-only status, mechanically mirrored numbers/Play, unreachable Add line, and quantities reset by resizing. These are described defects, not independently reproduced runtime failures. No adapted runtime pass/failure can be established from prose.

Not executed — run the following against an implementation:

| Check | Observable pass condition |
|---|---|
| Arabic mixed content | Vendor shapes correctly; ID `INV-2026-04`, email `accounts@example.test`, and decimal 1240.50 retain internal order; copy/paste preserves content; Arabic/Latin cursor, selection, composition and localized numeric entry work. Reading-order arrows adapt; Play/checkmark/logo retain meaning. |
| Compact and resizing | At 420 pt, short and tall windows, default and 200% text: every field/action/total is readable and reachable without overlap or essential truncation. Resize continuously to a wider supported window and back; no control crosses safe areas or window controls. Record actual dimensions. |
| Type | Measure 17 pt default body and 34 pt equivalent 200% body; test Bold Text and supported Dynamic Type sizes through the largest accessibility size. Labels wrap, amounts remain fully readable, symbols scale, controls grow, hierarchy persists. Record actual font metrics. |
| Draft and totals | Capture draft/model/undo/caret/scroll state with edited quantity and with incomplete localized decimal input. Resize repeatedly and change text size/direction; assert identical raw/parsed values and total before/after. Valid edits use existing arithmetic rules; invalid edits preserve last valid total visibly. |
| Add line | With ordinary focus, Tab reaches Add line after line content, reverse traversal exits, activation adds exactly one line and focuses description without changing total. Repeat with Full Keyboard Access for all controls; native text arrows still edit text. |
| Keyboard completion | Edit vendor and quantity, add a line, correct validation, read total and Save without pointer; Copy/Paste, Undo/Redo, Command-S, discoverability and Arabic/Latin input switching retain expected behavior. Focus and selected state remain distinct after resize/removal. |
| Status and access | Paid/unpaid are distinguishable without color. Measure text contrast in light/dark and Increase Contrast using the source table's scope; measure activation areas against the specified 44 × 44 pt default. Verify names, values, errors and reading order with Accessibility Inspector/VoiceOver and task access with Switch Control. |
| Lifecycle | Deactivate/reactivate and close/reopen same invoice: recover draft including incomplete edits; save failure allows retry without loss. Explicit discard is distinct from resize. If multiple documents are supported, ensure invoice identity prevents cross-document edits or wrong-draft reuse. |

## Evidence still missing

There is no implementation, SDK target/version, build output, financial calculation policy, sample line-item fixture, actual payment state, screen rendering, measured geometry/contrast, or device execution evidence. A known-good fixture with expected totals is needed to verify arithmetic preservation beyond the supplied amount. The supported window-height range and widest supported window must be established and recorded during testing.

Native Arabic review must confirm wording, regional numeral/currency conventions, shaping, punctuation, and mixed-script editing. Apple-environment execution is needed for actual Dynamic Type behavior, safe areas/window controls, focus engine, command discoverability, physical keyboard layouts, and assistive technology. No device, SDK, GUI, accessibility, or compilation execution is claimed.

## Local instruction audit

Read installed root `.agents/skills/apple-hig/SKILL.md` explicitly, then selected family procedures before topic procedures and supporting guides. Each file read used its own `cat` or `sed` command, resolved inside that installed package.

- Foundations family → Right to left, Typography, Accessibility, Layout topic `SKILL.md` files → corresponding local reference articles.
- Inputs family → Keyboards, Focus and selection topic `SKILL.md` files → corresponding local reference articles.
- Presentation family → Windows topic `SKILL.md` → local Windows reference article.

Accessibility and Layout reference passages were read again separately after aggregate output truncation. Official source links are in `interface.md`; all guidance came from local snapshots. No web browsing occurred.
