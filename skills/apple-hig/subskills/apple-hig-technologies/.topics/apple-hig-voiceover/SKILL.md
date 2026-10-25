---
name: apple-hig-voiceover
description: Use when designing or reviewing VoiceOver names, dynamic values, reading order, grouping, headings/rotor structure, meaningful images/charts, or spatial gesture alternatives.
---

# Expose the task's structure without relying on sight

Read [VoiceOver](../../references/voiceover.md). Inspect the task, actual accessibility semantics when available, visible content, dynamic updates, and requested design/review/adaptation. Preserve the existing stack. A screenshot cannot establish spoken names, rotor behavior, focus order, or successful nonvisual operation; distinguish proposals from inspected runtime semantics.

Name important controls by actual function, improve unhelpful generic labels, and synchronize descriptions/values with changing content. Describe meaningful imagery only for information the image conveys beyond nearby captions; hide decoration from navigation. For charts, expose a concise purpose plus accessible equivalents for every interaction, not merely a label saying “Chart.”

Build navigation structure from the task. Give pages short unique titles and meaningful section headings. Express grouping, links, ordering, and relationships otherwise conveyed by proximity/alignment, following locale reading order and grouping captions with their own images. Mark headings/links for rotor navigation and notify assistive technologies of relevant content/layout changes without inventing untested announcement behavior.

On visionOS, custom-gesture apps do not normally receive hand input while VoiceOver exploration is active. Direct Gesture mode changes that relationship and disables standard VoiceOver gestures; provide an alternative task route instead of requiring every person to switch modes or depend on custom hands.

**Worked transformation:** Before, a sales chart exposes one unlabeled canvas and decorative stars interrupt the reading sequence, while changing a date updates only the visual title. Decision: nonvisual readers need structure, current values, and equivalent chart actions. After, a named section describes the chart's purpose, date controls expose current values, accessible summaries/actions cover comparisons, decorations leave navigation, and relevant updates are represented through supported semantics.

Deliver a semantic name/role/value/group/order specification or implementation with a nonvisual task walkthrough. Fail if a necessary action is unnamed/unreachable, values become stale, captions detach, or chart interaction has no equivalent. Report actual VoiceOver/rotor/device tests separately; Linux/static checks cannot claim screen-reader execution.

Use [Accessibility](../../../apple-hig-foundations/.topics/apple-hig-accessibility/SKILL.md) for broader sensory/input barriers, [Writing](../../../apple-hig-foundations/.topics/apple-hig-writing/SKILL.md) for descriptions, or [Gestures](../../../apple-hig-inputs/.topics/apple-hig-gestures/SKILL.md) for spatial alternatives.
