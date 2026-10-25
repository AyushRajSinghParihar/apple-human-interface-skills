---
name: apple-hig-virtual-keyboards
description: Use when creating, reviewing, or adapting software keyboard choice, content semantics, input accessories, or custom keyboard scope.
---

# Fit the keyboard to the entry task

Read [the virtual-keyboard guide](../../references/virtual-keyboards.md). The workflow is application advice; distinguish app input views from installable keyboard extensions.

Inspect expected text, semantic content type, active fields/actions, platform/input variants, and create/review/adapt request. Identify whether system input is sufficient or a custom layout solves a demonstrated app-specific or systemwide need. Record actual keyboard configuration and layout avoidance; a mock keyboard does not prove device behavior.

Choose keyboard and semantic content types together, exposing needed characters/correction behavior. Give Return a task-appropriate label such as Search. On iOS/iPadOS use layout guides to keep both the active field and its action visible as the keyboard moves; add only useful accessories. Choose an app-only input view for app-specific entry and an extension for genuine systemwide input. Extensions need an obvious switch route and containing-app tutorials, not help occupying keys; respect secure/phone-field exclusions and system-provided keys/sound settings.

Implement keyboard configuration/layout or provide a field-to-keyboard/content/submit specification; reviews identify a blocked entry or obscured action. On TV account for linear versus grid input and numeric digit entry. On visionOS the movable keyboard is a separate window, so do not reserve fixed app space for it. On watch content type can help, but keyboard type is not configurable. The source does not define this component for macOS.

**Worked transformation:** Before: an iPad parcel form chooses a phone pad for an alphanumeric tracking code and lifts only the input above the keyboard, hiding Track. Decision: semantic mismatch and incomplete clearance block completion. After: choose suitable entry semantics and keep both code field and Track action clear with the layout guide.

Deliver the artifact and input/submit/visibility contract. Verify required characters, correction behavior, keyboard movement, hardware-input alternative, and custom-keyboard switching if relevant. Fail for impossible characters, obscured completion, or claimed unsupported keyboard customization. Native device/extension execution remains separate from source inspection.

Load [text-fields](../apple-hig-text-fields/SKILL.md), [digit-entry-views](../apple-hig-digit-entry-views/SKILL.md), or [entering-data](../../../apple-hig-patterns/.topics/apple-hig-entering-data/SKILL.md) for the affected task.
