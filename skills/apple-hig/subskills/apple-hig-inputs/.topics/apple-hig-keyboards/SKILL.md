---
name: apple-hig-keyboards
description: Use when designing or reviewing physical-keyboard navigation, Full Keyboard Access, standard or custom shortcuts, modifier behavior, and shortcut discoverability.
---

# Make commands discoverable and preserve familiar keys

Read [Keyboards](../../references/keyboards.md). Inspect task commands, text-entry contexts, current bindings, supported platforms/locales, and requested design/review/adaptation. Physical keyboards are covered on every listed platform except watchOS. Preserve the existing stack and identify actual keyboard evidence before claiming complete navigation.

Build a command inventory from frequent actions. Reuse familiar standard shortcuts for their expected meanings; consult the guide's mapping in context rather than treating legacy/system entries as universally available app APIs. A standard combination may serve another meaning only when its normal action has no place in this app. Avoid deriving an unrelated command by adding modifiers to a familiar one.

For app-specific commands, prefer a learnable Command-based combination, Shift for related variants, and sparing Option; avoid Control conflicts. Check international keyboards where Option makes characters. Preserve expected modifier-drag/resize behavior and clear smallest-increment arrow adjustment. Games may use single keys and customization while retaining system actions.

Trace ordinary content focus and Full Keyboard Access separately. On iPad, content/text/sidebar/collection focus is not proof that every button/switch is reachable; Full Keyboard Access supplies the broader route. Preserve accessibility shortcuts. On visionOS, make each Command-discoverability title meaningful without submenu context because the displayed list is flattened.

**Worked transformation:** Before, a diagram app uses Command-C to create a shape, binds Control-based shortcuts for everything, and has an unreachable Done button. Decision: copy semantics and a complete keyboard task outweigh shortcut novelty. After, Command-C copies selection, shape creation gets a suitable distinct command, and focus/activation can reach Done; the command title explains itself in discoverability UI.

Deliver a corrected command/binding inventory and keyboard task path or implementation. Fail if text editing invokes an unrelated command, shortcuts collide with system access, or the task cannot finish without a pointer. Actual OS shortcuts, international layouts, and Full Keyboard Access need supported-device execution; static binding inspection is narrower evidence.

Use [Focus and selection](../apple-hig-focus-and-selection/SKILL.md) for grouping/order or [Game controls](../apple-hig-game-controls/SKILL.md) for gameplay-specific bindings.
