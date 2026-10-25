# Installed-package enabled trial

Fresh context; package root `/tmp/apple-hig-enabled-trial-dl2bkinw/apple-hig/`; every read command ran with cwd `/tmp`. Started with installed `SKILL.md`, then family skills and targeted references. Only shell `cat` and `sed` consumed files. No network/browser, Python, package runtime, subagents, authoring cache, source-checkout content, tests, baseline answers or other agents' output was read. The two requested evaluation artifacts are the only writes.

“Current” below means the installed snapshot, `2026-10-25T12:38:49+00:00`; linked Apple sources were not fetched. No blanket pass/fail is self-assigned.

## Prompt 1

> For a current Apple HIG accessible iOS screen, where should I look for Dynamic Type and VoiceOver guidance, and what concrete design checks apply?

Use Foundations → Typography (Supporting Dynamic Type) plus Accessibility, then Technologies → VoiceOver; Designing for iOS supplies platform context. Test every text size, including Larger Accessibility Text: allow wrapping, grow rows/containers, stack inline metadata, reduce columns, scale meaningful symbols, and preserve information and hierarchy. Custom fonts need equivalent Dynamic Type and Bold Text behavior. Accessibility calls for at least 200% text enlargement and checking contrast in light/dark and Increase Contrast; its iOS reference sizes are 17 pt default and 11 pt minimum, not a reason to use tiny text. For VoiceOver, label important/custom controls with their actual function, update descriptions with state, give pages unique titles and headings, use logical locale reading order and grouping, describe meaningful images, hide decoration, expose chart interactions, and notify layout/content changes. Verify with VoiceOver and Accessibility Inspector rather than inferring accessibility from appearance.

Trace: `SKILL.md` → `references/platforms-and-tasks.md` → `subskills/apple-hig-foundations/SKILL.md` → `subskills/apple-hig-foundations/references/accessibility.md` → `subskills/apple-hig-foundations/references/typography.md` → `subskills/apple-hig-technologies/SKILL.md` → `subskills/apple-hig-technologies/references/voiceover.md`.

Sources: [typography](https://developer.apple.com/design/human-interface-guidelines/typography), [accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [voiceover](https://developer.apple.com/design/human-interface-guidelines/voiceover).

## Prompt 2

> Explain current HIG Liquid Glass material choices across iOS and watchOS, including readable content and platform exceptions.

Reserve Liquid Glass for navigation and important functional controls, with standard materials beneath for content. Regular glass adjusts blur/luminosity for substantial text and uncertain or complex backgrounds; clear suits rich photos/video. Bright media may need a 35%-opacity dark layer behind clear controls; omit it for dark media or AVKit controls already providing dimming. Both adapt to accessibility/appearance settings. On iOS/iPadOS choose ultra-thin/thin/regular/thick content materials by separation/readability; prefer vibrant semantic foregrounds and avoid quaternary labels on thin/ultra-thin materials. Thicker materials help fine text. On watchOS preserve default material backgrounds in full-screen modal sheets; inline buttons use contrasting capsules, while corner actions belong in the toolbar so the system gives them Liquid Glass and relocates title/time. Do not infer that watchOS lacks Liquid Glass from its short Materials subsection. Platform exceptions also matter: visionOS uses unmodifiable adaptive window glass and has no separate Dark Mode; tvOS includes glass in focus states as well as navigation.

Trace: `subskills/apple-hig-foundations/SKILL.md` → `subskills/apple-hig-foundations/references/materials.md` → `subskills/apple-hig-menus-and-actions/SKILL.md` → `subskills/apple-hig-menus-and-actions/references/buttons.md` → `subskills/apple-hig-menus-and-actions/references/toolbars.md`.

Sources: [materials](https://developer.apple.com/design/human-interface-guidelines/materials), [buttons](https://developer.apple.com/design/human-interface-guidelines/buttons), [toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars).

## Prompt 3

> Which current HIG guidance applies to Siri snippets, an iPhone Duo layout, and widgets in Apple HomeView?

The installed snapshot has explicit articles for all three. Siri snippets: use App Intents, always provide a result, optionally confirmation; keep custom content at most 400 pt high including Dynamic Type, deep-link longer detail, use a concrete primary action, and make spoken dialogue sufficient without looking. Snippets are unsupported on tvOS, visionOS, and watchOS in this article. iPhone Duo: preserve state and hierarchy through opening/closing; use size classes, safe areas and reserved-region adaptation instead of fixed panels. Standard split views expand/collapse; arrangements lay out content and do not replace navigation containers. Respect system vertical controls, stable toolbar groups, overflow priorities, and hardware-side placement even for RTL. Apple HomeView: small-family widgets can occupy a household-shared Modular face (up to four) or each member's personal Home Screen. Account for shared-calendar privacy; allow background removal/scaling and test red monochrome Night Mode. Widget updates are periodic, so show available data and freshness rather than assuming continuous updates. HomeView supports full-color/accented contexts and vibrant Modular Night Mode as specified by the local rendering matrix.

Trace: `references/topic-index.md` → `subskills/apple-hig-system-experiences/SKILL.md` → `subskills/apple-hig-system-experiences/references/snippets.md` → `subskills/apple-hig-system-experiences/references/widgets.md` → `subskills/apple-hig-getting-started/SKILL.md` → `subskills/apple-hig-getting-started/references/designing-for-iphone-duo.md` → `subskills/apple-hig-technologies/references/siri.md`.

Sources: [snippets](https://developer.apple.com/design/human-interface-guidelines/snippets), [siri](https://developer.apple.com/design/human-interface-guidelines/siri), [designing-for-iphone-duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo), [widgets](https://developer.apple.com/design/human-interface-guidelines/widgets).

## Prompt 4

> A designer references Apple's older navigation-bars and Touch Bar HIG URLs: how should we use these sources today?

The root Source boundaries explicitly records historical navigation-bars links as resolving to current Toolbars guidance: route the design question to the installed Toolbars article and link Apple's current Toolbars URL. It records the old Touch Bar HIG page as unavailable at this snapshot. Treat that older URL as a historical reference, not evidence of current rules; this package cannot substantiate Touch Bar-specific current recommendations. No live redirect or availability check was made in this network-free trial.

Trace: `SKILL.md` → `references/topic-index.md` → `subskills/apple-hig-menus-and-actions/SKILL.md` → `subskills/apple-hig-menus-and-actions/references/toolbars.md`.

Sources: [toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars).

## Prompt 5

> Give key differences between tvOS focus navigation and visionOS eye/hand input.

tvOS uses directional remote/controller navigation: every interactive item must be reachable, focus is clearly raised/lit/enlarged, and activation is normally separate from focus. Distinguish unfocused, focused, pressed, selected and unavailable states and leave enlargement room. visionOS usually uses looking to identify a target and a resting-hand finger/thumb tap to activate; direct touch is available but prolonged raised-arm work causes fatigue. Gaze hover is distinct from keyboard/controller focus, stays private before activation, and must not itself mutate app state. Keep stable hover landmarks and spacious targets (the Eyes article specifies 16 pt around bounds or 60 pt between centers), avoid repeated large eye/depth shifts, and supply accessible alternatives. Standard focus still applies when visionOS uses a connected keyboard/controller.

Trace: `subskills/apple-hig-getting-started/SKILL.md` → `subskills/apple-hig-getting-started/references/designing-for-tvos.md` → `subskills/apple-hig-getting-started/references/designing-for-visionos.md` → `subskills/apple-hig-inputs/SKILL.md` → `subskills/apple-hig-inputs/references/focus-and-selection.md` → `subskills/apple-hig-inputs/references/eyes.md` → `subskills/apple-hig-inputs/references/gestures.md`.

Sources: [focus-and-selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection), [eyes](https://developer.apple.com/design/human-interface-guidelines/eyes), [gestures](https://developer.apple.com/design/human-interface-guidelines/gestures), [designing-for-tvos](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos), [designing-for-visionos](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos).

## Prompt 6

> For Arabic UI, which layout elements reverse and which retain direction?

Mirror reading-order layout: short labels/one- or two-line blocks, Back/Next navigation, progress/sliders/ratings with endpoint labels, ordered image-sequence positions, and directional/text-alignment symbols. Align paragraphs of three or more lines to their own language and keep lists consistently aligned. Preserve number, phone and card digit order; localize numeral forms without reflecting glyphs. Keep photos/art, logos, universal signs such as checkmarks, clocks and ordinary real-world/handed tools unchanged unless their directional meaning specifically requires adaptation. Literal physical-direction controls and arrows pointing at actual screen locations must keep that meaning. Prefer localized SF Symbols; inspect complex icons piece by piece. Device-specific exception: Duo side controls remain on the same physical hardware side in RTL.

Trace: `subskills/apple-hig-foundations/SKILL.md` → `subskills/apple-hig-foundations/references/right-to-left.md` → `subskills/apple-hig-foundations/references/layout.md` → `subskills/apple-hig-foundations/references/writing.md` → `subskills/apple-hig-getting-started/references/designing-for-iphone-duo.md`.

Sources: [right-to-left](https://developer.apple.com/design/human-interface-guidelines/right-to-left), [layout](https://developer.apple.com/design/human-interface-guidelines/layout), [designing-for-iphone-duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo).

## Prompt 7

> For a macOS toolbar invoking a destructive action from a contextual menu, what interconnected HIG topics must be considered?

Compose Toolbars, Context menus, Menus/Menu bar, Buttons, Undo and redo, Alerts, and accessibility/writing. Keep the command scoped to the selected object, named with a clear action, and accessible in the menu bar: Mac toolbars can hide/customize and contextual menus are hidden shortcuts. Keep the contextual menu short, hide unavailable contextual actions (ordinary main-menu commands remain disabled/visible), and show keyboard equivalents in main menus. Do not import the iOS/iPadOS/visionOS context-menu rule to put a red destructive item last as an asserted Mac rule. Use semantic button roles and clear feedback. Make ordinary deletion undoable, with a specific Undo target in Edit and Command-Z/Shift-Command-Z; common undoable deletion generally needs no alert. Confirm uncommon irreversible destruction with clear consequences and Cancel. The alert article explicitly allows a normally styled default for deliberately requested destruction such as Empty Trash, qualifying the Buttons article's general advice to reserve primary for nondestructive actions. Retain accessible labels, keyboard access and current selection/state.

Trace: `subskills/apple-hig-menus-and-actions/SKILL.md` → `subskills/apple-hig-menus-and-actions/references/toolbars.md` → `subskills/apple-hig-menus-and-actions/references/context-menus.md` → `subskills/apple-hig-menus-and-actions/references/menus.md` → `subskills/apple-hig-menus-and-actions/references/the-menu-bar.md` → `subskills/apple-hig-menus-and-actions/references/buttons.md` → `subskills/apple-hig-patterns/SKILL.md` → `subskills/apple-hig-patterns/references/undo-and-redo.md` → `subskills/apple-hig-presentation/SKILL.md` → `subskills/apple-hig-presentation/references/alerts.md` → `subskills/apple-hig-foundations/references/accessibility.md` → `subskills/apple-hig-foundations/references/writing.md`.

Sources: [toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars), [context-menus](https://developer.apple.com/design/human-interface-guidelines/context-menus), [menus](https://developer.apple.com/design/human-interface-guidelines/menus), [the-menu-bar](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar), [buttons](https://developer.apple.com/design/human-interface-guidelines/buttons), [undo-and-redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo), [alerts](https://developer.apple.com/design/human-interface-guidelines/alerts), [accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [writing](https://developer.apple.com/design/human-interface-guidelines/writing).

## Cross-family retrieval/application

Application proposal: a resizable data-analysis pane with a date-range picker, time-series chart and editable records table. The following choices apply retrieved guidance to this hypothetical design; no actual product UI was inspected.

- Content: use a line for change over time, a title and short takeaway, explicit units/dates and a table for exact sortable records. Encode series with shape as well as color. Provide chart summary/Audio Graphs and accessible values/interactions; allow plot-wide scrubbing rather than requiring tiny-point hits and a predictable keyboard traversal.
- Layout/organization: coordinate table selection with the chart. On iPad, adapt two/three panes continuously to narrow window sizes, preserve selection and a logical route back, and use edit mode for table-item editing selection. On Mac, offer sortable headings, resizable columns and useful pane min/max sizes; dividers can resize panes and supporting panes can hide with toolbar/menu/shortcut restoration.
- Selection/input: keep the date picker near its field. On iPad, compact style conserves room and opens calendar/time editing with touch/keyboard/pointer support; use inline only when browsing deserves space. On Mac, textual date entry favors precision, while graphical selection suits browsing/date ranges. Localize value order and prefill reasonable values. Validate edits near the field and support paste where appropriate.
- Status: show real measurable completion for data import and unknown-duration activity otherwise. Keep indicator shape stable rather than switching a spinner to a bar. Mac background refresh can use a small adjacent spinner, usually without a redundant label; iPad pull-to-refresh supplements automatic updates and may show last-update time. Offer safe cancellation or pause if partial work matters.
- Patterns: immediately show useful scaffolding or retained data while loading in the background; leave other features usable. For waits longer than a moment or two, communicate ongoing work and an estimate when known. Preserve chart encodings between overview/detail, progressively disclose complexity, retain edits/selection on resizing, announce meaningful updates and respect Reduce Motion. Support Undo/Redo for edits through standard platform routes.
- Foundation/platform qualification: test Dynamic Type and Larger Accessibility Text on iPad; the installed Typography article explicitly says macOS has no Dynamic Type, so use standard Mac control typography and accessible adaptable layouts rather than promise iPad-style Dynamic Type on native Mac. Avoid putting essential Mac controls only at the window bottom.

Trace: `subskills/apple-hig-content/SKILL.md` → `subskills/apple-hig-content/references/charts.md` → `subskills/apple-hig-layout-and-organization/SKILL.md` → `subskills/apple-hig-layout-and-organization/references/lists-and-tables.md` → `subskills/apple-hig-layout-and-organization/references/split-views.md` → `subskills/apple-hig-selection-and-input/SKILL.md` → `subskills/apple-hig-selection-and-input/references/pickers.md` → `subskills/apple-hig-status/SKILL.md` → `subskills/apple-hig-status/references/progress-indicators.md` → `subskills/apple-hig-patterns/SKILL.md` → `subskills/apple-hig-patterns/references/loading.md` → `subskills/apple-hig-patterns/references/entering-data.md` → `subskills/apple-hig-patterns/references/charting-data.md`.

Sources: [charts](https://developer.apple.com/design/human-interface-guidelines/charts), [charting-data](https://developer.apple.com/design/human-interface-guidelines/charting-data), [lists-and-tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables), [split-views](https://developer.apple.com/design/human-interface-guidelines/split-views), [pickers](https://developer.apple.com/design/human-interface-guidelines/pickers), [progress-indicators](https://developer.apple.com/design/human-interface-guidelines/progress-indicators), [loading](https://developer.apple.com/design/human-interface-guidelines/loading), [entering-data](https://developer.apple.com/design/human-interface-guidelines/entering-data), [undo-and-redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo), [typography](https://developer.apple.com/design/human-interface-guidelines/typography), [layout](https://developer.apple.com/design/human-interface-guidelines/layout).

## Materials visual sequence

The installed original explanation reports a Music window whose glass brightness changes as its room darkens and viewpoint changes, while text remains readable and the background still suggests the room without giving every object equal prominence. It identifies visionOS adaptive glass responding to surrounding luminance, not a manual light/dark switch. The design lesson is to preserve the system material's adaptation instead of baking in a fixed background appearance. I read that written local observation; I did not inspect Apple's raw video or independently validate its review provenance.

Trace: `references/media/index.md` → `subskills/apple-hig-foundations/references/materials.md` → `references/media/materials.md`.

Source: [materials](https://developer.apple.com/design/human-interface-guidelines/materials).

## Routing, limitations and uncertainty

- All intentionally followed package links opened successfully; nested skills worked by explicit installed paths from /tmp without runtime setup.
- Root explicitly handles navigation-bars migration and missing Touch Bar coverage. The latter is a documented source boundary, not a broken route.
- One manually typed path omitted apple-hig/subskills and produced a No such file error outside the package path. No file content was read there; corrected routed Buttons path opened successfully. This was evaluator error, not a package link defect.
- An initial combined output was truncated. Materials, VoiceOver, Snippets and Duo were reread separately; Typography's relevant opening sections were reread with sed. No decision relies on an unseen truncated specifications row.
- Materials plus Buttons supports watchOS glass exceptions; brief or absent platform subsections were not treated as proof of unsupported behavior.
- Package warns about source conflicts: widget accented-mode prose conflicts with its Mac support matrix; use the explicit matrix conservatively, without asserting accented Mac support.
- Source links were supplied from installed references only. Current means the package's 2026-10-25 snapshot here; Apple pages, redirects, API availability and newest releases were not independently checked.
- No blanket pass/fail is self-assigned. The traces and concrete applications show consumption, but this trial does not establish full corpus accuracy or independently reviewed provenance.

## Actual opened relative paths

Unique files: 52. Repeated reads are deduplicated. All successful reads were beneath the installed package root. The unsuccessful manual typo was `/tmp/apple-hig-enabled-trial-dl2bkinw/apple-hig-menus-and-actions/references/buttons.md` and is not a successfully opened file.

- `SKILL.md`
- `references/topic-index.md`
- `references/platforms-and-tasks.md`
- `references/media/index.md`
- `subskills/apple-hig-foundations/SKILL.md`
- `subskills/apple-hig-technologies/SKILL.md`
- `subskills/apple-hig-system-experiences/SKILL.md`
- `subskills/apple-hig-getting-started/SKILL.md`
- `subskills/apple-hig-inputs/SKILL.md`
- `subskills/apple-hig-menus-and-actions/SKILL.md`
- `subskills/apple-hig-content/SKILL.md`
- `subskills/apple-hig-layout-and-organization/SKILL.md`
- `subskills/apple-hig-selection-and-input/SKILL.md`
- `subskills/apple-hig-status/SKILL.md`
- `subskills/apple-hig-patterns/SKILL.md`
- `subskills/apple-hig-foundations/references/accessibility.md`
- `subskills/apple-hig-foundations/references/typography.md`
- `subskills/apple-hig-technologies/references/voiceover.md`
- `subskills/apple-hig-foundations/references/materials.md`
- `references/media/materials.md`
- `subskills/apple-hig-system-experiences/references/snippets.md`
- `subskills/apple-hig-getting-started/references/designing-for-iphone-duo.md`
- `subskills/apple-hig-system-experiences/references/widgets.md`
- `subskills/apple-hig-inputs/references/focus-and-selection.md`
- `subskills/apple-hig-inputs/references/eyes.md`
- `subskills/apple-hig-inputs/references/gestures.md`
- `subskills/apple-hig-getting-started/references/designing-for-tvos.md`
- `subskills/apple-hig-getting-started/references/designing-for-visionos.md`
- `subskills/apple-hig-foundations/references/right-to-left.md`
- `subskills/apple-hig-foundations/references/layout.md`
- `subskills/apple-hig-foundations/references/writing.md`
- `subskills/apple-hig-technologies/references/siri.md`
- `subskills/apple-hig-menus-and-actions/references/toolbars.md`
- `subskills/apple-hig-menus-and-actions/references/context-menus.md`
- `subskills/apple-hig-menus-and-actions/references/menus.md`
- `subskills/apple-hig-menus-and-actions/references/the-menu-bar.md`
- `subskills/apple-hig-patterns/references/undo-and-redo.md`
- `subskills/apple-hig-presentation/SKILL.md`
- `subskills/apple-hig-presentation/references/alerts.md`
- `subskills/apple-hig-menus-and-actions/references/buttons.md`
- `subskills/apple-hig-content/references/charts.md`
- `subskills/apple-hig-layout-and-organization/references/lists-and-tables.md`
- `subskills/apple-hig-layout-and-organization/references/split-views.md`
- `subskills/apple-hig-selection-and-input/references/pickers.md`
- `subskills/apple-hig-status/references/progress-indicators.md`
- `subskills/apple-hig-patterns/references/loading.md`
- `subskills/apple-hig-patterns/references/entering-data.md`
- `subskills/apple-hig-patterns/references/charting-data.md`
- `subskills/apple-hig-getting-started/references/designing-for-ios.md`
- `subskills/apple-hig-getting-started/references/designing-for-ipados.md`
- `subskills/apple-hig-getting-started/references/designing-for-macos.md`
- `subskills/apple-hig-getting-started/references/designing-for-watchos.md`
