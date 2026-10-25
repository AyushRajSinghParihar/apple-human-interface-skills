---
name: apple-hig-app-shortcuts
description: Use when creating, reviewing, or adapting discoverable App Shortcuts, activation phrases, optional parameters, and spoken or visual responses.
---

# Expose a complete task beyond the app

Read [the App Shortcuts guide](../../references/app-shortcuts.md). The workflow is application advice; distinguish App Shortcuts from App Intents actions available for custom Mac shortcuts.

Inspect common tasks, intent/entity model, required inputs, invocation surfaces, platform, and create/review/adapt request. Determine which task can finish in context and which must open relevant app content. Record existing intent behavior; do not assume a phrase demonstrates successful execution.

Choose important tasks within the supplied-shortcut limit, evaluating common app schemas where relevant. Keep phrases natural, memorable, and app-named without implying many parameters. An App Shortcut can expose one optional parameter with predictable options; clarify omitted values with a likely default/short alternatives and gather further required details later. Supply complete spoken dialogue for eyes-away devices. Use a snippet for static outcome/confirmation and a Live Activity for evolving bounded progress. Teach availability contextually rather than through repeated unsolicited promotion.

Implement the authorized intent/phrase/response behavior or specify invocation-to-outcome contracts; reviews identify concrete ambiguity, missing input, or incomplete audio output. Do not promise App Shortcuts on Mac/tvOS: Mac App Intents can remain usable in user-composed shortcuts.

**Worked transformation:** Before: “Reserve a desk with Campus” implies three simultaneous parameters and shows only a visual success checkmark. Decision: invocation complexity and audio-only output conceal essential booking details. After: expose a predictable optional location, gather missing time/details in subsequent steps, and speak the actual booking outcome while showing a concise result.

Deliver the artifact, phrases, parameters/defaults, app-opening boundary, and audio/visual responses. Verify omitted/ambiguous inputs, cancellation, entity removal, and eyes-away comprehension. Fail for claiming success before completion, missing essential spoken information, or unsupported surface promises. Siri/Spotlight discovery and native execution require actual client evidence.

Load [snippets](../apple-hig-snippets/SKILL.md), [live-activities](../apple-hig-live-activities/SKILL.md), or [siri](../../../apple-hig-technologies/.topics/apple-hig-siri/SKILL.md) according to the response task.
