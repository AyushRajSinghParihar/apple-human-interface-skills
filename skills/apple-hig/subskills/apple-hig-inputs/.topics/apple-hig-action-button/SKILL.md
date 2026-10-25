---
name: apple-hig-action-button
description: Use when designing or reviewing an Action button function or App Shortcut on supported iPhone or Apple Watch models.
---

# Make a press perform a useful recurring function

Read [Action button](../../references/action-button.md). Inspect the recurring task, existing App Shortcuts, supported devices, and whether the request is design, review, or adaptation. Treat hardware availability as conditional: this guide excludes iPadOS, macOS, tvOS, and visionOS. Preserve the existing stack and produce a shortcut/action contract or implementation, not just setup instructions.

Choose an essential function rather than another Open App command. Define its precondition, immediate result, and how the same intent works through another shortcut entrypoint. Name it for Settings with a present-tense verb, title case, and at most three words. Rely on system assignment education instead of duplicating it.

On iPhone, keep the person in the current context where lightweight snippets or a Live Activity can complete the task. Opening the full app needs a task reason. On Watch, define the first press and one memorable later-press behavior that supports the same activity; avoid many hidden contextual meanings. Provide completion in UI rather than normally ending the activity through repeated presses. Preserve Action-plus-side-button pause except where pausing would harm the experience or safety, such as losing dive tracking.

**Before → decision → after:** A field-notes app exposes “Open Field Notes” and later presses unpredictably alternate save/delete. Decision: a recurring entrypoint should perform a stable useful task. After, “Record Waypoint” saves the current waypoint and confirms it in context; subsequent presses repeat that meaningful action, while destructive management stays in labeled UI.

Deliver the label, first/subsequent press state mapping, result feedback, and fallback action. Fail if presses unexpectedly destroy/end work, a Watch secondary action contradicts the main task, or a simple iPhone action needlessly loses context. Hardware presses, shortcut invocation, and Live Activity behavior need actual supported-device checks; static artifacts do not verify them.

Use [Siri](../../../apple-hig-technologies/.topics/apple-hig-siri/SKILL.md) for shared shortcut intent and [Always On](../../../apple-hig-technologies/.topics/apple-hig-always-on/SKILL.md) when Watch feedback continues at wrist down.
