---
name: apple-hig-carekit
description: Use when designing or reviewing CareKit care plans, task styles, symptom/event logging, progress charts, care contacts, and contextual sensitive-data access.
---

# Match care UI to the action and its schedule

Read [CareKit](../../references/carekit.md). Inspect the prescribed/wellness task, schedule, instructions, patient/caregiver roles, stored data, and requested design/review/adaptation. Preserve the existing stack and clinical content; do not invent care instructions or imply clinical validation from a UI review. The main CareKit UI scope here is iOS/iPadOS, with Watch notifications separately described.

Choose the task view by completion semantics: simple for one action, instructions for necessary explanatory detail, log for timestamped events, checklist for individually described steps, or grid for compact short-labeled steps. Every task needs a concise title and schedule. If each step needs detail, use a checklist rather than compressing it into cryptic grid buttons. Combine category color with another signal and demonstrate complex actions when supplied material permits.

Use charts for a meaningful care narrative: label time/units, distinguish datasets with legends/contrast, and consolidate or restructure ranges so small values remain visible. Choose contact detail appropriate to phone/message/email/map communication; keep care roles explicit. Let framework constraints organize added subviews instead of breaking the model with decorative content.

Request only clinically/task-relevant HealthKit, motion, photo, or research inputs in context, rechecking current permissions. Keep sharing consistent with system privacy settings rather than inventing conflicting switches. Coalesce reminders when many tasks are due and avoid advertising in the care plan.

**Worked transformation:** Before, recovery exercises appear as unlabeled colored grid squares with no schedule and a reminder for every substep. Decision: detailed exercises require explicit step instructions and manageable reminders. After, a scheduled checklist names each supplied exercise, completion is per step, a progress chart has clear time units, and a coalesced reminder opens the pending plan context.

Deliver corrected task/chart/contact mappings and reminder/data-access behavior. Fail if completion semantics misrepresent the plan, a color alone identifies a task, or changed permissions leave misleading data. State whether actual Store/UI synchronization and authorization were exercised; static work does not verify clinical effectiveness or health-data sharing.

Use [HealthKit](../apple-hig-healthkit/SKILL.md) for health access and [ResearchKit](../apple-hig-researchkit/SKILL.md) when consent/study tasks are explicitly part of care.
