---
name: apple-hig-toggles
description: Use when creating, reviewing, or adapting binary settings, checkboxes, radio choices, mixed state, and stateful buttons.
---

# Expose state rather than disguise an action

Read [the toggle guide](../../references/toggles.md). This procedure is application advice; preserve the source's style and platform distinctions.

Inspect setting meaning, affected content, dependencies, aggregate selection, platform, and create/review/adapt mode. Determine whether the control changes opposing states, executes a command, or selects one value from a list. Record actual state and immediate/deferred persistence; a colored switch does not prove the setting applied.

Use a toggle for state and name its affected content clearly. Differentiate on/off beyond color. On iOS/iPadOS use switches in labelled list rows and appropriate stateful buttons outside; do not add brand color without a reason. On Mac preserve established checkbox patterns, use a prominent switch to enable a group where appropriate, and keep switches/checkboxes/radios in the window body. Reflect mixed aggregate checkbox state when children differ. Use independent checkboxes for multiple choices and radio groups for mutually exclusive choices; larger sets can fit a pop-up. Do not replace a single binary checkbox with an unexplained multi-choice radio model.

Implement the state/dependency binding, provide a state table, or review exact contradictory state and labeling defects. If applying the setting can fail, specify truthful state/recovery according to the product rather than allowing the visual toggle to imply success.

**Worked transformation:** Before: selecting some folders leaves a master “Include All” checkbox checked, and red alone signals disabled sync. Decision: aggregate state and binary meaning are misleading. After: show mixed selection with a dash, allow explicit all/none behavior, and use distinct state shape/fill plus clear sync status.

Deliver the artifact, state meanings, dependencies, aggregate behavior, and persistence contract. Verify both directions, mixed children, unavailable dependencies, and noncolor interpretation. Fail for state displayed opposite to applied behavior, independent options made exclusive, or no way to perceive mixed/off state. Report native value announcement/input separately.

Use [pop-up-buttons](../../../apple-hig-menus-and-actions/.topics/apple-hig-pop-up-buttons/SKILL.md) for larger exclusive sets or [buttons](../../../apple-hig-menus-and-actions/.topics/apple-hig-buttons/SKILL.md) for commands.
