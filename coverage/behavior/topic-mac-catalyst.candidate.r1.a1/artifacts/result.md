# Mac Catalyst adaptation result

Edited interface.md in place, replacing the one-paragraph problem statement with an implementable Mac Catalyst specification. No application code or native build was provided or changed.

## Decisions and patch summary

| Supplied issue | Revised contract |
| --- | --- |
| Fullscreen touch assumption | Standard resizable Mac windows; full screen optional; keyboard and pointer paths |
| Commands hidden behind long press | Menu command inventory, standard shortcuts, shared toolbar enablement, mandatory audit of remaining existing commands |
| Floating software keyboard | Standard Catalyst text input; remove app-drawn keyboard and reserved space while preserving system assistive input |
| Narrow window failure | Proposed 560 × 400 pt minimum; two columns from 900 pt, stacked scrolling content below; preserve draft, focus and selection |
| Multiple recipes needed | Independent windows keyed by recipe ID; repeated opens raise the existing window; active editor owns commands |

Selected Mac idiom deliberately, with metric/type/image review rather than assuming unscaled iPad layouts work. Added draft persistence, close/reopen and failed-save rules to make parallel editing safe. Dimensions, breakpoints, one-window-per-ID policy and persistence details are product design decisions, not HIG mandates. Existing schema, storage and commands remain authoritative; the brief supplies none of their implementation details.

Source support is linked by decision in interface.md. In particular, [Mac Catalyst](https://developer.apple.com/design/human-interface-guidelines/mac-catalyst) supports deliberate idiom/input/menu adaptation; [Windows](https://developer.apple.com/design/human-interface-guidelines/windows) supports useful parallel windows and system controls; [Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars#macOS) requires menu alternatives for toolbar actions. The [virtual-keyboard guide](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#Platform-considerations) marks that component unsupported on macOS; this does not establish absence of macOS accessibility keyboards.

## Worked before/after

Illustrative task: compare “Soup” with “Bread” while revising a preparation paragraph. Those names and fields are examples, not inspected schema.

Before, the supplied brief establishes that editing assumes fullscreen touch, commands require long press, narrowing breaks the editor, and a floating keyboard occupies the experience. It does not establish how saving or opening a second recipe currently behaves.

After, open Soup through File > Open Recipe… (⌘O), edit with the physical keyboard, then open Bread through the same command. Bread gets another window while Soup retains its draft, insertion range, scroll anchor and undo history. Switch back through Window > Soup. Resize Soup from 1000 to 700 pt wide: its sections stack, the focused paragraph stays visible and unchanged, and Save remains available through ⌘S even with the toolbar hidden. Saving Soup must not affect Bread. If saving fails, Soup retains its draft, shows the failure and permits retry; a close request cannot silently discard it. Opening Soup again raises its existing window.

## Acceptance checks and status

Static specification checks performed on the revised text:

- **Passed:** every issue explicitly named in the supplied brief has a corresponding revised behavior.
- **Passed:** required toolbar commands have named menu equivalents and consistent target/availability requirements.
- **Passed:** the specification defines wide/narrow transitions, input switching, window reuse, activation, close, reopen and persistence failure outcomes.
- **Passed:** proposed dimensions and implementation assumptions are identified separately from source-backed platform guidance.
- **Failed:** none of these document checks. This is not an application conformance result.

All following execution checks are **not executed** and remain implementation acceptance gates:

| Scenario | Required observation |
| --- | --- |
| Open Soup and Bread; edit both; reopen Soup | Two independent drafts; existing Soup raised; no extra same-ID editor |
| Activate each window and invoke Save/Undo through menu, toolbar and shortcut | Same target and availability for all routes; independent undo histories |
| Resize through 1000, 900, 899, 700 and 560 pt widths; 400 pt height; then enlarge | No overlap or lost actions; expected stacking; focus, draft and insertion range survive |
| Long names, longer translations, enlarged text, narrow/short and very large windows | Wrapping/reflow stays usable; title can be identified; no ordinary text-editing horizontal scroll |
| Hide toolbar; use only keyboard from Open through edit, save and close | Complete task without long press/pointer; no text-editing shortcut collisions |
| Enable Full Keyboard Access; traverse and leave all controls, multiline editors and recipe selector | Visible focus, no traps, selection distinct from focus, cancel returns appropriately |
| Mouse/trackpad selection, configured secondary click, hover and keyboard switching | Standard cursor/gesture meanings; essential actions remain available; state retained |
| Switch to another app and back; minimize, zoom and enter/exit full screen | Draft/context intact; native window-state cues; zoom distinct from full screen |
| Delay/fail persistence; edit during save; close/quit; retry and reopen | Later edits stay dirty; failed saves retain draft/window; persisted revision restores correctly |
| Inspect Catalyst rendering at actual Mac idiom scale and build against chosen SDK | Type/assets/layout usable; APIs supported; no unavailable hardware dependency blocks editing |
| Audit every existing long-press command with no editor, active selection and multiple windows | Complete menu coverage, correct scopes and disabled states; no toolbar/context-only essentials |

## Evidence and routing limits

Read the installed root at `.agents/skills/apple-hig/SKILL.md` explicitly. Then read the Getting started family and iPadOS/macOS topic procedures before their guides, and searched the installed topic index for Catalyst, desktop input, menus, windows, layout and keyboard concepts. Read owning families, topic procedures and local guides for Mac Catalyst, keyboards, pointing devices, focus and selection, windows, menu bar, toolbars, layout and virtual keyboards. Each read used a separate single-file shell command. All paths resolved from this installed package.

The supplied interface.md was the only product evidence used. Local references identify a 2026-10-25 snapshot and are derived guidance, not SDK documentation or independently verified live Apple pages. Official links are citations only; no web browsing occurred. The menu-bar guide notes inconsistent general-versus-specialized custom-menu ordering wording; the specification uses concrete scope and familiar menu order rather than inventing an absolute ordering rule.

No Mac device, SDK compilation, GUI, native menu/overflow, persistence backend, pointer behavior, accessibility or assistive-technology execution was performed. The Mac minimum size and breakpoints require validation. Existing schema, complete command inventory, deployment target, scene support, storage behavior and hardware dependencies remain unknown. The revised document is a concrete design contract; it is not evidence that the app already satisfies it.
