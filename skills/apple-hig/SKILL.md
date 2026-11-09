---
name: apple-hig
description: Applies Apple's Human Interface Guidelines (HIG) to design, build, review, or adapt user interfaces for iPhone, iPad, Mac, Apple Watch, Apple TV, Apple Vision Pro, and CarPlay, in SwiftUI, UIKit, AppKit, or any other stack. Use for layout, navigation, tab bars, sidebars, toolbars, sheets, alerts, buttons, menus, forms, pickers, typography, Dynamic Type, color, Dark Mode, Liquid Glass, SF Symbols, accessibility, VoiceOver, widgets, Live Activities, notifications, onboarding, settings, and screenshot or design reviews. Also use when a web, Android, or Windows app must follow Apple-style design. Do not use for build setup, crashes, performance, binary size, backend code, or App Store submission, unless the question is about the user interface.
license: MIT
metadata:
  author: AyushRajSinghParihar
  source: https://developer.apple.com/design/human-interface-guidelines
  snapshot: "2026-11-09"
---

# Apple Human Interface Guidelines

This package applies Apple's Human Interface Guidelines (HIG) to real product
work. It has 158 topic procedures from a dated English HIG snapshot. It is
independent of Apple. If a task depends on a newer release or a disputed detail,
check the official source.

## Find the guidance

1. Find the target platform, the device context and the user task from the
   request or the project. Ask for the platform only when the answer depends on
   it and the project does not show it. Keep the user's framework and product
   requirements.
2. If the product runs outside Apple platforms (web, Android, Windows), read
   [Beyond Apple platforms](references/beyond-apple/README.md) first.
3. Search the [topic index](references/topic-index.md) for the concepts of the
   task, for example "paywall", "delete", "offline" or "Dynamic Type", and for
   component names. Use a text search; do not load the full index for a narrow
   question. Open each matching topic procedure directly.
4. For a new surface, platform support or a platform change, also read the
   Getting started procedure of each target platform. See
   [platform and task routes](references/platforms-and-tasks.md).
5. Read one procedure for each material decision. A component can also need
   accessibility, typography, privacy, localization or input guidance; a
   reminder in a nearby procedure does not replace the owning procedure. In a
   review, map each control to its topic even when its code is missing. Missing
   evidence does not prove a defect.
6. Follow the procedure's link to its source guide for exact rules, numbers and
   platform differences. [Key numbers](references/key-numbers.md) collects common
   sizes and limits. A missing platform subsection means that no more rules are
   stated; it does not prove support, nonapplicability or identical behavior.

Use a family file only to compare the topics of one area:
[Getting started](subskills/apple-hig-getting-started/SKILL.md) ·
[Foundations](subskills/apple-hig-foundations/SKILL.md) ·
[Patterns](subskills/apple-hig-patterns/SKILL.md) ·
[Content](subskills/apple-hig-content/SKILL.md) ·
[Layout and organization](subskills/apple-hig-layout-and-organization/SKILL.md) ·
[Menus and actions](subskills/apple-hig-menus-and-actions/SKILL.md) ·
[Navigation and search](subskills/apple-hig-navigation-and-search/SKILL.md) ·
[Presentation](subskills/apple-hig-presentation/SKILL.md) ·
[Selection and input](subskills/apple-hig-selection-and-input/SKILL.md) ·
[Status](subskills/apple-hig-status/SKILL.md) ·
[System experiences](subskills/apple-hig-system-experiences/SKILL.md) ·
[Inputs](subskills/apple-hig-inputs/SKILL.md) ·
[Technologies](subskills/apple-hig-technologies/SKILL.md)

All paths are relative to this installed package. No Python, network or other
skill is necessary to read the guidance.

## Do the requested work

Examine the supplied brief, flow, code, specification or image before you decide
what is wrong or choose a framework.

- **Design:** give an implementable specification with states, transitions and
  acceptance checks, linked to the user's task and platform.
- **Implement:** prefer the project's native system components. The
  [implementation map](references/implementation-map.md) lists the API links of
  each guide; check names and availability in the SDK documentation. Change the
  code; an explanation alone does not complete an implementation request.
- **Review:** for each finding, give the observed problem, its effect, the HIG
  rule and a concrete correction. Rank the findings. Keep source-backed findings
  apart from your own suggestions, and do not invent violations.
- **Adapt:** keep the product task, data and useful state, and apply the
  destination platform's interaction model. Change the supplied artifact, or give
  an explicit before and after contract when a specification is requested.

Procedures are framework agnostic. Their examples teach decisions; they do not
ask you to replace the project's technology.

## Report the result

- Link the official article or section for each material recommendation.
- Keep qualifications such as "consider", "prefer" and "avoid". Do not turn
  advice into a universal rule.
- Keep units and platform scope for numbers.
- If sources conflict, describe the conflict and the conservative choice.
- Report checks as passed, failed or not done. Static code or a screenshot
  cannot prove assistive technology behavior, native rendering, haptics,
  comfort or a successful build.

## Source limits

This is local guidance, not a verbatim Apple manual or an SDK reference.
Historical `navigation-bars` links now go to Toolbars, and `in-app-purchase` goes
to Apple In-App Purchase. The old Touch Bar and Messages for Business pages were
not available in this snapshot; do not invent their rules. Translations, archived
pages and the linked SDK and WWDC libraries are outside the source.
