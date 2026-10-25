# Fresh-context no-package control

Date: 2026-10-25. Harness: Codex collaboration agent `baseline_control`, inherited
session model, no explicit model override. The evaluator received no source files,
candidate skill, browsing, or other tools. These are observed answers, not proposed
outcomes. Only concise excerpts are retained here; they are not scored as a
statistical benchmark.

| ID | User task | Observed response |
|---|---|---|
| N1 | For a current Apple HIG accessible iOS screen, where should I look for Dynamic Type and VoiceOver guidance, and what concrete design checks apply? | Named Accessibility and Typography, then general implementation documentation. Correctly mentioned scaling, wrapping, order, labels, states and non-color cues, but explicitly had not verified current page organization; did not identify VoiceOver's current own HIG article. |
| N2 | Explain current HIG Liquid Glass material choices across iOS and watchOS, including readable content and platform exceptions. | Recalled regular/clear variants and contrast/layering concerns. Said it could not reliably state current iOS versus watchOS exceptions or exact selection rules. |
| N3 | Which current HIG guidance applies to Siri snippets, an iPhone Duo layout, and widgets in Apple HomeView? | Suggested Siri/App Intents generally; did not recognize iPhone Duo or Apple HomeView and marked high uncertainty. |
| N4 | A designer references Apple's older navigation-bars and Touch Bar HIG URLs: how should we use these sources today? | Recommended checking redirects and context, but had not established their current outcomes. |
| N5 | Give key differences between tvOS focus navigation and visionOS eye/hand input. | Described indirect focus/activation versus eye targeting and hand activation, spacing/comfort, multiple inputs and avoiding hover-only essential content. |
| N6 | For Arabic UI, which layout elements reverse and which retain direction? | Distinguished reading flow/leading-trailing/navigation from semantic direction of media, clocks, literal imagery, numbers and mixed text; marked charts/timelines/symbols as requiring specific checks. |
| N7 | For a macOS toolbar invoking a destructive action from a contextual menu, what interconnected HIG topics must be considered? | Identified toolbars, buttons, menus, alerts, undo/redo, keyboard and accessibility; gave sensible contextual action/undo/confirmation advice, while marking exact current prescriptions uncertain. |

The useful baseline gaps are current source ownership, current platform-specific
material rules, unfamiliar current topics, and actual historical URL disposition.
N5–N7 show that a capable model already knows many general principles; the package
must improve retrieval and application rather than merely repeat those principles.

Package-enabled trials should use the same seven prompts, permit installed-file
reading, disable external research, record actual opened paths and outputs, and
distinguish successful retrieval from unsupported confidence. Additional scenarios
in the evaluation contract remain unexecuted until separately recorded.
