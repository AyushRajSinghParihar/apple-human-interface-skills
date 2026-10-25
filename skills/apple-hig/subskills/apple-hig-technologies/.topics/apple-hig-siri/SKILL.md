---
name: apple-hig-siri
description: Use when designing or reviewing Siri/App Intents actions, app entities and contextual references, relevant donation/indexing, spoken dialogue, snippets, or App Shortcuts.
---

# Expose useful intent and make spoken results stand alone

Read [Siri](../../references/siri.md). Inspect popular tasks, domain objects, hands-free/device context, existing intents/entities, response dialogue, and requested design/review/adaptation. Preserve the existing stack and verify current App Intents/schema availability; do not assume Siri understands private app capabilities without explicit integration.

Choose high-value actions and familiar audience nouns/verbs. Adopt existing domain schemas where they fit; use App Shortcuts for useful functions beyond those domains. Annotate onscreen objects with entities so contextual references resolve, index personally relevant content, and donate actual actions/interests rather than indiscriminately promoting everything. Keep ads, purchase pitches, and marketing out of delivered content.

Prefer built-in responses unless they cannot meet the task. Define required parameters and specific follow-up questions that name the requested object. When options are too numerous, narrow openly instead of reciting a long list. Provide audible and visual forms, with spoken text sufficient by itself. Optional snippets may be omitted, so essential information cannot exist only in a visual property.

Keep responses brief, device-independent unless the device is verified, and free of repeated app attribution supplied by the system. Consider bystanders, parental controls, and precise current-problem recovery. Refer to Siri by name, preserve localized invocation conventions, and avoid reserved system/emergency behavior or impersonating Apple.

**Worked transformation:** Before, a recipe shortcut says “Done—see this” while showing the only result in a card, indexes every promotion, and asks “Which one?” without context. Decision: hands-free results need independent meaning and relevant content. After, the response names the selected recipe/action, the follow-up asks which saved recipe is intended, and donation/indexing focuses on actual saved or used content rather than ads.

Deliver action/entity/parameter and audible/visual response contracts or implementation. Fail if essential results vanish without a snippet, ambiguous references trigger wrong actions, or dialogue requires unseen context. Source/code review cannot establish actual Siri recognition, entity resolution, system suggestions, or natural-language quality; list supported-device tests separately.

Use [Action button](../../../apple-hig-inputs/.topics/apple-hig-action-button/SKILL.md) for hardware shortcut invocation and [Writing](../../../apple-hig-foundations/.topics/apple-hig-writing/SKILL.md) for concise follow-up/recovery language.
