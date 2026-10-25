---
name: apple-hig-designing-for-watchos
description: Use when creating, reviewing, or adapting an Apple Watch experience for brief glances, focused actions, complications, wrist-down states, and independence from iPhone.
---

# Fit the task to a wrist glance

Read [Designing for watchOS](../../references/designing-for-watchos.md). Inspect the proposed Watch task, frequency, urgency, companion-phone dependency, and supplied screens. Identify the information needed at wrist raise and the action worth performing there. Choose design, review, or adaptation mode; produce the requested revised artifact rather than transplanting the whole phone app.

Separate a glance from deeper interaction. Put the useful value and next action on one screen when possible, keeping navigation shallow and gestures few. Use the Digital Crown for vertical movement rather than requiring repeated precise swipes. If a task needs prolonged text entry or broad comparisons, simplify its Watch responsibility and provide a coherent continuation elsewhere without making the entire Watch app merely a remote notice.

Choose entrypoints by purpose: a complication supplies recurring glance value and opens the corresponding context; a timely notification should let people act without launching; an Action button suits an essential action useful without looking. Do not require sensor access just because the device provides sensors. Personalize only with an explained task benefit and appropriate permission.

Design wrist-up and Always On information together, including what remains useful and what should become less prominent. Provide independently useful app detail beyond the complication or notification. Preserve progress when the wrist lowers or an interruption occurs.

**Worked transformation:** Before, a tea timer copies a phone recipe browser and requires four screens before starting. Decision: the wrist task is checking and controlling the current steep. After, the first screen shows remaining time and a large Pause/Resume action; Crown navigation reaches saved presets, and a complication opens the running timer directly. The phone retains detailed recipe editing.

Deliver a glance/action flow, entrypoint destinations, and wrist-state behavior or implementation. Fail if a complication opens unrelated content, a routine action requires deep navigation, or lowering the wrist loses the timer. State whether actual Watch readability, Crown response, notification handling, and sensor access were tested; static evidence cannot prove them.

Continue with [Digital Crown](../../../apple-hig-inputs/.topics/apple-hig-digital-crown/SKILL.md), [Always On](../../../apple-hig-technologies/.topics/apple-hig-always-on/SKILL.md), or [Action button](../../../apple-hig-inputs/.topics/apple-hig-action-button/SKILL.md) only for the selected interaction.
