# iPhone adaptation result

Patched `interface.md` in place from a one-paragraph desktop-port brief into a screen, action, layout and connectivity contract. The technician can now follow Tasks → task detail → Record Work → Review Completion, with a defined return path and preserved drafts.

## Decisions and rationale

| Supplied issue/context | Revised specification | Guidance and qualification |
|---|---|---|
| Eight dense columns | Scannable task rows; labeled full detail retains every field. Requires an implementation-time inventory because column names were not supplied. | [Lists and tables: Content](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables#Content) supports summaries with details for long content. Field priorities and sorting are product assumptions. |
| Hover-only actions; one free hand | Visible labeled actions, broad lower-screen primary button, no essential hidden gesture; product hit-region minimum 44 × 44 pt. | [iOS best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices), [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices). Accessibility's local source lists a 44 pt default and 28 pt minimum; this design adopts 44 pt, consistent with the button guide, without treating the smaller minimum as a recommendation. Reach remains untested. |
| Windows for every detail | One navigation stack with visible Back and preserved system swipe-back. | [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices). The exact screen sequence is a product decision. |
| Bottom action under home indicator | Safe-area constrained bottom container, matching scroll inset, keyboard and short-height fallback. | [Layout: Guides and safe areas](https://developer.apple.com/design/human-interface-guidelines/layout#Guides-and-safe-areas). No fixed bottom offset is invented. |
| Interrupted work, intermittent network | Durable drafts, usable cache, explicit pending/accepted/error/conflict states and API-gated queued completion. | [Loading](https://developer.apple.com/design/human-interface-guidelines/loading#Best-practices) supports useful content during waits; operation IDs, conflict policy and server acknowledgment rules are engineering decisions, not HIG mandates. |
| Enlarged text and alternative input | Semantic type, wrapping and stacking, explicit status words, named controls and execution checks. | [Typography: Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type), [Accessibility: Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility). These are specified requirements, not demonstrated accessibility support. |

## Worked before/after

Illustrative data, not supplied production records: task M-104, “Inspect pump,” location Plant 2, high priority, due today, assigned and unfinished.

Before: the technician scans eight dense columns, attempts to find a hover-only row action on touch, opens another detail window, and reaches for an action obscured by the home indicator. The supplied brief says nothing about completion storage or retry behavior, so no existing data-loss claim can be made.

After: a row reads “Inspect pump · M-104 / Plant 2 / High · Due today · Assigned.” Tap it, read instructions, tap Record Work, enter “Seal inspected,” then Review Completion. With no connection, Save Completion for Sync stores the reviewed payload and displays Pending sync; the queue still shows M-104 unfinished. On reconnect, the same operation ID is submitted. Only acknowledgment displays Completed and removes it from the assigned unfinished queue. If the response is lost, reconcile that operation rather than creating another. If the API gate is unmet, the same offline notes stay a draft and Connect to Submit explains the limitation.

## Acceptance checks and status

Passed — static specification inspection only:

- All four supplied presentation problems have concrete replacements in interface.md.
- Entry, detail, editing, review, acceptance and Back transitions are specified, including identity and queue restoration.
- All eight original fields must be mapped and preserved; unspecified schema and commands are explicitly identified as missing evidence.
- Local draft, queued submission and server-completed states are distinct; retry, duplicate prevention, conflict and API fallback contracts are present.

Failed: no failure found in these document-level checks. This is not a runtime pass.

Not executed — implementation acceptance scenarios:

| Scenario | Pass condition |
|---|---|
| Queue and identity | Every authorized task is reachable online; offline coverage is labeled. Tap M-104 opens M-104. Empty, long/paginated and failed-page states remain actionable. Back restores scope/order/scroll; accepted removal anchors to the next row. |
| Touch and geometry | Measure all activation regions at ≥44 × 44 pt without overlap. Every command is reachable by a visible control. On supported iPhones, test with either hand; primary action is comfortable to reach. |
| Safe areas and keyboard | At smallest/largest supported widths, intermediate widths, portrait/landscape and Display Zoom, no essential control overlaps system regions. Last field and primary action remain reachable with keyboard shown. |
| Text and appearance | At default, ≥200% and largest accessibility text, plus Bold Text, full identity/instructions and all actions remain available. Labels wrap without collisions. Measure contrast for actual light/dark and Increase Contrast combinations. |
| Interruption | Background, terminate and relaunch during editing and pending submission; recover the correct task, durable notes, operation and navigation context. Local persistence failure must never report saved success. |
| Network and recovery | Test no cache, partial cache, slow refresh, offline submission, reconnect, server rejection, permission change, revision conflict and lost acknowledgment. No cached content disappears during refresh; no task becomes confirmed complete before acknowledgment; retry produces one server completion. |
| Accessible completion | On an Apple environment, traverse and activate the full flow with VoiceOver, Switch Control and Full Keyboard Access. Names, roles and state are meaningful; no required content or action is unreachable, gesture-only, color-only or sound-only. |

## Evidence limits and instruction route

Used only the supplied local interface.md and installed guidance. Explicitly read the installed `.agents/skills/apple-hig/SKILL.md`, then the Getting started family → Designing for iOS procedure → iOS source guide. Searched the installed topic index for platform, list, layout, touch, button, accessibility and loading concepts. Read the Foundations, Layout and organization, Menus and actions, and Patterns family routes before their selected procedures and source guides: Layout, Accessibility, Typography, Lists and tables, Buttons, and Loading. Each instruction/source read used a separate single-file cat or head command; index search used single-file rg. Paths were resolved within the installed apple-hig package.

Official links above identify the local snapshot's source articles; they were not browsed or independently verified. The local source guides are derived guidance dated 2026-10-25, not SDK documentation. No screenshots, original column schema, command inventory, code, API contract, cache policy or executable application were provided. Task fields, completion workflow, queue ordering and sync mechanics are proposed product decisions needing implementation mapping. No device, simulator, SDK build, GUI, contrast measurement, accessibility execution, timing or physical-comfort test was performed. The patch establishes a concrete specification and test obligations only.
