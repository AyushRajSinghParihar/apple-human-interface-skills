# Finance report hierarchy repair

Patched interface.md in place, replacing its one-paragraph defect description with an implementable text specification for iPhone and Mac. The changes define semantic text roles, system fonts and legible weights, live text headings, sentence-case emphasis, expanding rows, width-dependent stacked records, and stable financial columns. They preserve data precision and give unusually long values a full-text route.

## Decisions and rationale

The supplied brief explicitly reports tiny thin text, image headings, clipping at larger text, horizontally shifting figures, and all-caps paragraph emphasis. These are documented observations from the brief, not independently observed rendering defects.

- Replace the thin 9 pt face with system typography: iPhone Body at the default 17 pt reference and Mac body at 13 pt. Use size, weight, and grouping to distinguish title, section, body, total, and detail. Apple recommends legible weights and semantic styles; its minimum sizes are not comfortable body defaults. See [Typography — Ensuring legibility and Conveying hierarchy](https://developer.apple.com/design/human-interface-guidelines/typography).
- Replace heading images with resizable text and all-caps prose with sentence case and short semibold emphasis. This makes the hierarchy adaptable and avoids relying on rasterized text; sentence case is a product editorial decision here.
- Use all iPhone Dynamic Type categories and Bold Text. Give Mac an explicit 100–200% report-size setting because macOS has no Dynamic Type. Grow rows, wrap prose, and stack comparison columns when measured content no longer fits. See [Typography — Supporting Dynamic Type and macOS](https://developer.apple.com/design/human-interface-guidelines/typography) and [Layout — Adaptability](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability).
- Use tabular numerals, trailing alignment, and reserved widths for updates. This is a product engineering prescription for the reported movement; the consulted HIG guidance supports readable hierarchy but does not establish this specific numeric algorithm as an Apple requirement.
- Preserve complete values at enlarged sizes, including signs, currencies, periods, and precision. The last-resort overflow region is explicitly testable. See [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

## Worked before/after

Illustrative content only; the brief supplies no actual financial data.

Before: an image says “QUARTERLY REPORT”; one thin 9 pt face displays “REVENUE IMPROVED THIS QUARTER.” An inline Revenue value changes from USD 1,111.11 to USD 8,888.88 and shifts horizontally. Enlarged text clips the amount.

After at default iPhone size:

- “Quarterly report” uses emphasized Title 1 (28 pt reference).
- “Revenue” uses emphasized Title 2 (22 pt reference).
- The comparison shows “Previous period — USD 1,111.11” and “Current period — USD 8,888.88” in Body (17 pt reference), with tabular numeric advances and a stable trailing anchor.
- “Revenue improved this quarter.” uses regular Body; only a meaningful phrase needs emphasis.

At a narrow width or enlarged text setting, each period/value pair stacks beneath its metric label, rows expand, and the explanation wraps. A value moves below its period label before any overflow route is needed. The Mac counterpart uses the specified 22/17/13 pt hierarchy at 100%, scaling to 44/34/26 pt at 200%; supporting detail grows from 12 to 24 pt. These examples describe required behavior, not rendered measurements.

## Acceptance checks and status

Passed — static specification checks: the patch addresses all five supplied problems; it distinguishes iPhone Dynamic Type from Mac resizing; it defines text roles, expansion/fallback rules, and numeric update behavior. Essential values retain their formatting and full-text access contract.

Failed — no executed validation check failed. The original brief describes defects; the revised runtime has not been tested, so this is not a runtime pass.

Not executed — interface.md's acceptance contract requires every iPhone text category with Bold Text off/on; all Mac 100–200% steps; narrow/wide and intermediate widths; long labels, prose, currencies, negatives and changing digit counts; and accessibility/keyboard reading of headings and complete values. Also pending are native font measurements, light/dark and Increase Contrast measurements, actual viewing-distance legibility, and verifying the overflow fallback is usable. These require an implementation and appropriate Apple execution evidence.

## Audit and evidence limits

Read the installed apple-hig root SKILL.md, then the Foundations family. Searched the complete topic index for typography, accessibility, and text-view concepts. Selected Typography and Accessibility for text hierarchy/enlargement, then followed Typography's route to Layout for reflow. Read each selected topic procedure before its supporting source guide, using one file per command. All guidance paths resolve beneath `.agents/skills/apple-hig/`; the consumed procedures are `subskills/apple-hig-foundations/.topics/apple-hig-{typography,accessibility,layout}/SKILL.md`, and their guides are the corresponding `subskills/apple-hig-foundations/references/*.md` files. Text-view editing/selection behavior is outside the supplied brief; no existing control implementation was provided to review.

Only interface.md and installed local guidance informed the revision. The guides identify themselves as a dated English HIG snapshot, retrieved 2026-10-25; official links above are citations, not evidence of web access or fresh verification. No source code, font files, screenshots, devices, SDK, GUI, accessibility tree, or runtime results were supplied or executed. No compilation, measured contrast, native shaping, VoiceOver order, or accessibility conformance is claimed. The deliverable is a revised specification, not an implemented or device-validated application.
