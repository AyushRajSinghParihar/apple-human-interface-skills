---
name: apple-hig-entering-data
description: Use when creating, reviewing, or adapting data-entry flows, known defaults, required fields, validation, and efficient input alternatives.
---

# Ask only for information the task still needs

Read [the data-entry guide](../../references/entering-data.md). This workflow is application advice; permission and authentication remain distinct from cosmetic entry behavior.

Inspect required information, existing system/account data, sensitivity, constraints, platform/input, and create/review/adapt intent. Identify redundant questions, reasonable nonsecret defaults, and information requiring permission. Record actual validation/gating behavior rather than assuming disabled Continue explains itself.

Reuse known appropriate data or request relevant permission; never prepopulate passwords. Prefer meaningful choices over typing and allow appropriate paste/drop. Keep persistent purpose labels, secure sensitive entry, and locale-aware numeric formatting. Validate while mistakes can be fixed in context without rejecting harmless intermediate entry. Make missing requirements understandable before gating Next/Continue. On Mac expansion tooltips can reveal clipped values; on visionOS secure entry protects AirPlay viewing according to the source, but do not claim arbitrary mirrored content is private.

Implement the authorized flow, provide a field/data-source/validation/gating specification, or review exact effort/error defects. Keep the user's task and stack rather than turning ordinary entry into an unsolicited account overhaul.

**Worked transformation:** Before: an expense form asks for known currency twice, prefills a stored password, blocks paste into the receipt ID, and disables Continue without explanation. Decision: defaults and friction are misapplied. After: reuse a suitable currency default, request secure authentication explicitly, permit useful paste, and identify the specific missing required input.

Deliver the artifact, requested versus reused data, input alternatives, and validation/continuation contract. Verify partial/invalid/valid values, locale, paste, sensitive fields, and the reason for gating. Fail for exposed secrets, unnecessary re-entry, valid input silently changed, or unexplained dead-end completion. Separate static/form logic from native input/permission/device execution.

Load [text-fields](../../../apple-hig-selection-and-input/.topics/apple-hig-text-fields/SKILL.md), [virtual-keyboards](../../../apple-hig-selection-and-input/.topics/apple-hig-virtual-keyboards/SKILL.md), or [privacy](../../../apple-hig-foundations/.topics/apple-hig-privacy/SKILL.md) as needed.
