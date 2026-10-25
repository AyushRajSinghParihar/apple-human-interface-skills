# Formatting palette repair

Patched interface.md in place, replacing the supplied defect summary with a concrete presentation, editing, and exit contract.

## Decisions and changes

- Wide layouts use a single content-sized popover anchored to the actual Format control. Secondary options stay within that surface, replacing the cascading popover.
- Compact layouts use an expanded modal sheet. Available space and size class determine adaptation, including narrow iPad windows; device identity alone does not.
- A stable selection, opening baseline, and working draft define the editing session. Multiple choices keep it open. Done and automatic dismissal commit; explicit Cancel alone rolls back.
- Rotation/resizing preserves the draft and route. Added focus restoration, save-failure retention, parent-interaction rules, and one undo operation per committed session.

The first three decisions follow [Popovers](https://developer.apple.com/design/human-interface-guidelines/popovers#Best-practices). Sheet action placement and sizing draw on [Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets#iOS-iPadOS); adaptive sizing draws on [Layout](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability). Large-only initial sizing, draft/preview mechanics, undo grouping, and saving on sheet swipe are product decisions. The sheet guide calls for resolving unsaved work on swipe; this specification resolves it by committing, consistent with the transient palette's automatic-save policy. A future deferred-save task would need a separate dismissal-protection design.

## Worked before/after

Illustrative scenario: a person selects a heading, opens Format, selects Bold, then Italic, and opens secondary options.

Before, the brief says the first choice closes the palette, secondary options cascade, and outside tapping discards edits. On compact iPhone the same tiny floating geometry is used. The brief does not provide a rendered example or concrete formatting controls; Bold and Italic here are illustrative.

After, both choices remain in one draft while the palette stays open. Secondary options replace its body; Back retains the choices. On wide iPad, tapping outside commits both choices and closes the anchored popover. Explicit Cancel instead restores the opening formatting. If the window narrows mid-session, the same target, choices, and detail route move to the sheet. Done or swipe dismissal commits; no tiny popover remains on the phone.

## Acceptance checks and status

Static specification checks passed by reading the revised artifact:

| Check | Required contract now present |
|---|---|
| Anchor and context | Arrow targets the visible trigger; unavailable anchor falls back to sheet. |
| One presentation | No cascades; replacement closes and saves in one activation. |
| Repeated choices | Multiple choices retain the open palette and draft. |
| Data outcomes | Outside dismissal saves; Cancel discards only this session; Done commits. |
| Compact adaptation | Large sheet, safe-area controls, scrolling, no tiny floating geometry. |
| Continuity | Resize, rotation, interruption, and internal Back retain state. |

Runtime acceptance checks — all **not executed**:

1. On wide iPad, open Format near each window edge; verify arrow attachment and visible essential preview context. Resize through intermediate widths and rotate while on a detail route; verify one surface, unchanged target/draft, and preserved route.
2. Choose two independent formatting options; verify neither closes the palette. Exercise Done, Cancel, outside tap, replacement trigger, and supported Escape separately; reopen and inspect document formatting and undo history against the exit table.
3. On compact iPhone and narrow iPad, verify expanded sheet geometry, unavailable parent interaction, no outside-tap dismissal, and save-on-swipe. Verify Back only navigates, and Cancel remains available at the root.
4. Repeat in short landscape space and with enlarged text and long labels; verify scrolling reaches every action without overlap or shrunken controls. Exercise touch and supported keyboard/pointer paths.
5. Interrupt and resume; verify selection and draft survive. Inject a persistence failure and verify the draft remains available for retry. Verify actual focus restoration and assistive-technology navigation separately.

Failed checks: none established by static review. The original brief describes failures, but no executable UI was supplied to reproduce them. Static passes establish specification coverage only.

## Evidence and limits

Read the installed root apple-hig/SKILL.md explicitly, searched references/topic-index.md, then read the Getting started family and iOS/iPadOS topic procedures before their source guides; Presentation family and Popovers/Sheets procedures before their guides; and Foundations family and Layout procedure before its guide. All paths resolved within .agents/skills/apple-hig, with one file read per shell command.

Only supplied local text and installed guidance were used. Official links above are attribution from those local guides; no web browsing occurred. The snapshot is dated 2026-10-25 and is independent application guidance. No device, simulator, SDK compilation, GUI, physical reach, animation, native positioning, or accessibility execution was performed. Framework, OS availability, actual control inventory, and native dismissal implementation remain unspecified and require implementation validation.
