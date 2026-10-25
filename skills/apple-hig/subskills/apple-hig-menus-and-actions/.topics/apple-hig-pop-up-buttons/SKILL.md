---
name: apple-hig-pop-up-buttons
description: Use when creating, reviewing, or adapting compact single-choice menus that display a selected option.
---

# Choose one state without hiding its meaning

Read [the pop-up-button guide](../../references/pop-up-buttons.md). This procedure is application advice; distinguish selection from command execution.

Inspect the option set, current/default value, label, platform, and create/review/adapt request. Establish whether the list is flat and mutually exclusive. If it contains commands, multiple selection, or submenus, evaluate a pull-down instead. Record actual selected value from data, not solely a possibly stale button title.

Use a pop-up when space is limited and options need not remain exposed. Give the control or nearby introduction a predictive purpose; start with a useful likely default when appropriate. After choosing, close the menu and reflect the value. A rare Custom option can open less-common choices; define how cancellation retains the prior value so entering customization does not imply commitment. On iPad, a small well-defined set may replace unnecessary detail navigation inside a modal/popover. Do not prescribe the component on tvOS/watchOS.

Implement the selection model, provide a label/options/default/commit specification, or review concrete mismatches. Keep value persistence and preview effects explicit rather than assuming a framework's automatic behavior.

**Worked transformation:** Before: `Options` mixes `Portrait`, `Landscape`, and `Print Now`, with no selected state. Decision: orientation is one persistent choice while printing is an action. After: a labelled Orientation pop-up displays the selected orientation; Print becomes a separate direct command.

Deliver the artifact and selection/customization contract. Verify default, repeated selection, external value change, cancellation of Custom, and long labels. Fail for a displayed value differing from stored state, hidden command disguised as a choice, or ambiguous list purpose. State native keyboard/assistive selection checks separately.

Load [pull-down-buttons](../apple-hig-pull-down-buttons/SKILL.md) for commands, [pickers](../../../apple-hig-selection-and-input/.topics/apple-hig-pickers/SKILL.md) for other choice presentations, or [menus](../apple-hig-menus/SKILL.md) for organization.
