---
name: apple-hig
description: Use when designing, implementing, or reviewing interfaces for iOS, iPadOS, macOS, tvOS, visionOS, watchOS, CarPlay, or other Apple system experiences using Apple's Human Interface Guidelines. Routes to current platform, foundation, pattern, component, input, and technology guidance.
license: MIT
metadata:
  author: AyushRajSinghParihar
  source: https://developer.apple.com/design/human-interface-guidelines
---

# Apple Human Interface Guidelines

Use the relevant Apple guidance to make concrete design decisions. This package
contains a router, 13 topic skills, and original article-level references. It is
independent of Apple. The sources are a dated English HIG snapshot; check the
official source when a task depends on a newer release or a disputed detail.

## Route the task

1. Identify the target platform, device context, and user task from the request or
   project. Ask for the platform only when it materially affects the answer and
   cannot be inferred. Preserve the user's framework and product requirements.
2. Select the relevant family below. Read that family's `SKILL.md`, then only the
   article references needed for the task. Nested skills are explicitly read by
   file path; automatic nested discovery is not required.
3. For an exact component, technology, or unfamiliar term, search the
   [complete topic index](references/topic-index.md). It links directly to local
   article references. Do not load the full corpus for a narrow question.
   For a screenshot-specific or animated example, also consult its
   [original visual explanation](references/media/index.md) when available.
4. Apply shared guidance and the target platform's documented differences. A
   missing platform subsection means no additional rule is stated; it does not
   prove support, nonapplicability, or identical behavior across platforms.
5. Compose families when the task crosses them: a component can also require
   accessibility, typography, localization, input, or system-experience guidance.
   Use [platform and task routes](references/platforms-and-tasks.md) when useful.

All paths are relative to **this installed package**, not the shell's current
directory. No Python, network, sibling skill installation, or authoring cache is
required to read the guidance.

| Task | Read this topic skill |
|---|---|
| Platform conventions, design principles, games, device adaptation | [Getting started](subskills/apple-hig-getting-started/SKILL.md) |
| Accessibility, typography, color, materials, layout, localization, privacy | [Foundations](subskills/apple-hig-foundations/SKILL.md) |
| Onboarding, loading, search, sharing, accounts, feedback, media, settings | [Patterns](subskills/apple-hig-patterns/SKILL.md) |
| Charts, images, text views, embedded web content | [Content](subskills/apple-hig-content/SKILL.md) |
| Lists, collections, split views, tab views, disclosure and grouping | [Layout and organization](subskills/apple-hig-layout-and-organization/SKILL.md) |
| Buttons, menus, toolbars, menu bar, ornaments and actions | [Menus and actions](subskills/apple-hig-menus-and-actions/SKILL.md) |
| Sidebars, tab bars, search fields, tokens and path controls | [Navigation and search](subskills/apple-hig-navigation-and-search/SKILL.md) |
| Alerts, sheets, popovers, panels, scrolling and windows | [Presentation](subskills/apple-hig-presentation/SKILL.md) |
| Text fields, pickers, sliders, toggles, selection controls | [Selection and input](subskills/apple-hig-selection-and-input/SKILL.md) |
| Progress, activity, gauges and ratings | [Status](subskills/apple-hig-status/SKILL.md) |
| Widgets, Live Activities, notifications, Siri snippets and system surfaces | [System experiences](subskills/apple-hig-system-experiences/SKILL.md) |
| Touch, keyboard, pointer, focus, eyes, gestures, controllers and sensors | [Inputs](subskills/apple-hig-inputs/SKILL.md) |
| Apple Pay, purchases, Siri, VoiceOver, AI, CarPlay and integrations | [Technologies](subskills/apple-hig-technologies/SKILL.md) |

## Apply the guidance

- **Design:** connect each important choice to the user's task and target
  platform. Include necessary interaction states, adaptation, and accessibility.
- **Implement:** prefer the project's native system components when they supply
  the needed behavior. HIG explains experience requirements; verify API names,
  availability, and code against the appropriate SDK documentation.
- **Review:** describe the observed problem, its effect, the relevant HIG rule,
  and a concrete correction. Separate source-backed findings from your own
  suggested improvements. Do not invent violations without inspecting evidence.

Include official article/section links for material recommendations. Preserve
qualifications such as “consider,” “prefer,” and “avoid”; do not turn design
advice into invented universal requirements. Retain units and platform scope for
numerical specifications. If source passages conflict, describe the conflict
and the conservative application rather than silently changing the source.

## Source boundaries

This is comprehensive local guidance, not a verbatim Apple manual or an SDK API
reference. Original media explanations are supplementary to article references;
the source page remains useful for visual demonstrations. Source snapshots and
review status live in the repository's coverage report, outside ordinary skill
loading. Do not infer that a source has been independently reviewed just because
its local file exists.

Historical `navigation-bars` links now resolve to current Toolbars guidance;
`in-app-purchase` resolves to Apple In-App Purchase. The old Touch Bar and Messages
for Business HIG pages were unavailable at this snapshot. Do not fabricate their
current rules. Translations, archived pages, and complete linked SDK/WWDC libraries
are outside the source boundary.
