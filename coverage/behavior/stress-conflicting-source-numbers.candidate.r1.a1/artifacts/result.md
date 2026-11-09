# Qualified specification and review

The iPad footer proposal needs revision: use at least a 44×44 pt activation region and adequate separation; do not describe 28×28 pt as Apple’s default. Remove the Mac widget’s accented-rendering promise. Treat accented support on Mac as unresolved in the supplied guidance, and plan for the modes its platform table lists.

This is a design review of `interface.md`, not an implementation or runtime validation. The brief supplies a custom 28×28 pt hit region with a 2 pt gap and a Mac accented-mode promise; it explicitly says no rendered app exists. No code, screenshot, SDK evidence, product action definition, or widget content model was supplied.

## Decisions and their qualifications

| Issue | Source-backed interpretation | Decision |
| --- | --- | --- |
| iPad 28 versus 44 pt | Accessibility’s Mobility table lists **44×44 pt default**, **28×28 pt minimum** for iOS/iPadOS. Buttons recommends general hit regions of **at least 44×44 pt**. These are different levels of guidance, not interchangeable defaults. | Adopt at least 44×44 pt for this footer. The smaller minimum alone does not justify the proposed dense layout. This does not establish that every 28 pt control universally violates HIG. |
| 2 pt gap | Both guides call for sufficient separation and comfortable selection. Accessibility suggests around 12 pt padding for bezelled elements and 24 pt outside visible edges for elements without a bezel. Those suggestions do not establish a universal edge-to-edge gap formula. | Reject 2 pt as an adequately justified specification. Start with a **12 pt clear gap between activation regions** as a project design choice, then validate the actual footer. Do not call that gap an Apple minimum or equate it with the source’s padding suggestion. |
| Mac accented rendering | The Widgets appearance table says Mac accented is “Not supported,” while the guide records a prose sentence mentioning Mac group tinting. The topic procedure explicitly warns against inferring support from that sentence. | Preserve the conflict, prioritize the explicit platform table for conservative planning, and withhold the promise. This local snapshot cannot prove that no Mac release supports it. |

Sources: [Buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility), [Widgets — Appearances](https://developer.apple.com/design/human-interface-guidelines/widgets#Appearances), and [Widgets — Accented](https://developer.apple.com/design/human-interface-guidelines/widgets#Accented). Links identify official sources; they were not opened for this review.

## iPad footer contract

- Retain the immediate footer action, subject to confirmation of its actual outcome. Prefer a system button in the existing framework; retain a custom button only with explicit press feedback and appropriate semantics/states. No framework replacement is specified.
- Each activation region is at least **44×44 pt**, distinct and nonoverlapping. A 28×28 pt glyph or visual treatment may remain inside a larger activation region if it stays legible; visual size and hit size are separate. If a centered 28 pt visual uses a 44 pt region, that adds 8 pt per side. Adjacent centers therefore need at least 56 pt separation for the proposed 12 pt clear hit-region gap; merely expanding two targets whose centers are 30 pt apart would overlap them.
- Expand or reflow the footer rather than reducing targets to fit. Preserve the action and label with enlarged/localized text and supported window sizes. Review bezelled versus unbezelled spacing against the guide’s suggestions in the actual layout.
- Before implementation, supply a short outcome-specific label, affected object, reversibility, semantic role, and availability conditions. An icon-only button needs an accessible action name. Do not assign destructive or default behavior without knowing the consequence. Prefer style over unequal peer target sizes for emphasis. [Buttons — Style, Content, Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Style)
- Enabled activation performs the named action; disabled presentation prevents activation and explains the reason where context is insufficient. If completion is delayed, show activity in the activating button, preserving context; define duplicate-activation handling and success/failure behavior once the operation is known. [Buttons — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS)

## Mac widget contract

Assume a **system-small desktop widget** as the initial variant; the brief does not identify a family or surface. Plan a Notification Center variant only if required. The supplied table supports both surfaces for system-small.

| Context | Qualified rendering specification |
| --- | --- |
| Desktop | Full-color light/dark and vibrant treatments according to system context. |
| Notification Center, if included | Full-color light/dark; no vibrant or accented promise from this table. |
| Accented on Mac | Excluded from committed deliverables pending authoritative, version-specific resolution of the conflict. |

Use semantic colors and actual text. Preserve state through text/symbols rather than color alone. In vibrant mode, use grayscale brightness for hierarchy: opaque white/light gray for primary content and darker opaque grays for supporting content; opacity alone is not the hierarchy strategy. Keep layout flexible rather than inventing a fixed Mac canvas. [Widgets — Rendering modes](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes)

Product content remains unresolved: identify one useful changing fact/glance question, the relevant object, and its precise app destination before visual sign-off. Ordinary activation opens that content; add no in-place controls without a defined simple action. Specify realistic preview data, initial placeholder, signed-out/unavailable states where applicable, and last-known data with freshness wording when age matters. Retain available data during refresh; refresh opportunities are system-controlled, not continuous. These are required completion inputs, not claims about an existing widget. [Widgets — Best practices](https://developer.apple.com/design/human-interface-guidelines/widgets#Best-practices), [Previews and placeholders](https://developer.apple.com/design/human-interface-guidelines/widgets#Previews-and-placeholders)

## Acceptance checks and evidence status

**Passed — local document review:** read the installed root skill, the Menus and actions, Foundations, and System experiences family procedures, their Buttons, Accessibility, and Widgets topic procedures, then their supporting guides. The topic index confirms these installed routes. All file reads used separate commands. The revised specification distinguishes default/minimum, visual/hit geometry, project spacing choice/source advice, and conflicting Mac claims.

**Failed — supplied proposal against this qualified specification:** the stated iPad target is below the adopted 44×44 pt baseline; its “Apple default” attribution is incorrect. Its 2 pt separation lacks evidence of comfortable selection. The Mac accented promise lacks consistent source support. These are proposal findings, not observed device failures.

**Not executed — implementation acceptance:**

- Measure actual iPad hit bounds and separation, including enlarged targets, window resizing, orientation, localized labels, and at least 200% text enlargement. Pass when the target/gap contract holds, essential labels/actions remain usable, and targets never overlap. Test physical selection comfort and accidental neighboring activation on iPad; adjust spacing if needed.
- Confirm the named outcome, relevant disabled/pending/success/failure behavior, custom press feedback if retained, accessible name/role/state, focus order, and activation using supported keyboard and assistive paths. Use Accessibility Inspector and relevant VoiceOver, Full Keyboard Access, Switch Control, AssistiveTouch, and Pointer Control checks. No accessibility execution is claimed. [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
- On the target Mac release, preview and run each included surface/mode with realistic, long/localized, stale, unavailable, and relevant account-state data. Pass when the glance remains readable, state survives grayscale/background changes, activation reaches the intended object, and previews match delivered variants. Measure contrast in actual appearances; no rendering, timeline, deep-link, or contrast result is established here.

## Evidence still missing

Record supported iPadOS/macOS versions, framework/SDK versions, actual footer layout and action semantics, widget purpose/data/privacy requirements, and chosen surfaces before implementation approval. Obtain SDK compilation and API-availability evidence for the selected implementations.

To reopen Mac accented support, compare the current official HIG prose/table and versioned WidgetKit documentation, then demonstrate the system-selected rendering behavior on the supported Mac OS/SDK combination. An API symbol’s existence or successful compilation alone would not prove the mode is delivered in that context. Record versions and observations, and revise the promise only when the discrepancy is resolved. This external verification was deliberately deferred under the local-files-only instruction.

The installed guides identify a 2026-10-25 snapshot/retrieval date; they are derivative local guidance, not independently verified current SDK documentation. No web, GUI, device, SDK build, accessibility tooling, or runtime tests were used. No claim of overall HIG compliance is made.
