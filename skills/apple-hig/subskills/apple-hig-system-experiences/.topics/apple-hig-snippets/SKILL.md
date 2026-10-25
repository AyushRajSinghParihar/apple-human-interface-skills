---
name: apple-hig-snippets
description: Use when creating, reviewing, or adapting compact App Intents confirmation and result views with spoken responses.
---

# Separate confirmation from a completed result

Read [the snippet guide](../../references/snippets.md). The workflow is application advice; every snippet intent needs a result, with confirmation optional.

Inspect the invoked task, required confirmation, actual outcome, dialogue, custom view, platform, and create/review/adapt request. Establish which information must be understood with no screen. Do not present an accepted request as a completed operation without evidence.

Use confirmation only when a decision is needed, with system Cancel and a concrete action label. Provide the required result with useful outcome and Done. Keep essential spoken dialogue complete for eyes-away use while generally omitting its repeated visible text; the custom view should independently communicate purpose. Fit content within the documented height even with Dynamic Type, and deep-link to longer details instead of cramming them in. Preserve light/dark contrast and margins. Snippets are unsupported on TV/visionOS/watchOS; do not imply audio-only availability proves their visual component support.

Implement the intent confirmation/result or specify dialogue/view/action states; reviews identify missing results, premature success, or incomprehensible audio. Use Live Activities instead for evolving progress rather than a static result that appears current forever.

**Worked transformation:** Before: a reservation shortcut shows `Proceed`, repeats all spoken text visually, and disappears after confirmation without a result. Decision: confirmation is not completion and the compact view lacks independent hierarchy. After: use `Reserve Desk`, speak essential location/time and outcome, show a compact reservation result, and link full details.

Deliver the artifact, confirmation criteria, primary label, complete dialogue, result, and detail link. Verify cancel/confirm, failure, large text height, audio-only comprehension, and long details. Fail for no result, false success, required information omitted from speech, or overflowing custom content. Native intent/snippet/Siri execution remains separate from static checks.

Load [app-shortcuts](../apple-hig-app-shortcuts/SKILL.md) for invocation or [live-activities](../apple-hig-live-activities/SKILL.md) for continuing progress.
