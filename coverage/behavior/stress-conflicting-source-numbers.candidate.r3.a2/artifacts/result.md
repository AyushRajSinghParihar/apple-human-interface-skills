# Qualified specification and decision record

Based on `interface.md` and the installed apple-hig local snapshot dated 2026-10-25. No web lookup, SDK build, rendered app, GUI inspection, device test, or accessibility execution was performed. Official links below identify the source sections; they were not fetched. This is a design specification, not implementation approval or demonstrated accessibility conformance.

## Decisions resolving the apparent contradictions

| Proposal | Source interpretation | Decision |
| --- | --- | --- |
| iPad custom footer action: 28×28 pt hit region, 2 pt gap, described as “Apple default” | Accessibility’s Mobility table lists **44×44 pt default** and **28×28 pt minimum** for iOS/iPadOS. Buttons recommends general hit regions of at least **44×44 pt**. A smaller minimum does not establish a default or a recommendation for dense controls. | Correct the default claim. Adopt a minimum **44×44 pt activation region** for this footer action as the project specification. The supplied 28×28 pt proposal fails that chosen baseline, although it equals the accessibility table’s minimum. |
| Mac widget promises accented rendering from prose about Mac group tinting | The widgets rendering table explicitly marks Mac accented mode **Not supported**, while the local guide records the conflicting prose. This is an unresolved source inconsistency, not evidence of support. | Remove the unconditional promise. Specify Mac full-color rendering on Desktop and Notification Center, plus vibrant rendering on Desktop, following the table conservatively. Accented Mac rendering remains unverified and outside the promised behavior. |

Sources: [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility), [Buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), [Widgets — Appearances](https://developer.apple.com/design/human-interface-guidelines/widgets#Appearances), [Widgets — Accented](https://developer.apple.com/design/human-interface-guidelines/widgets#Accented).

## iPad footer action contract

- Preserve the footer action’s product purpose; its actual label, affected object, outcome, reversibility, and availability conditions are absent. These must be supplied before finalizing its semantic role or default activation. Do not infer a destructive or primary role from its location.
- Prefer a system button in the existing framework. If custom treatment remains necessary, provide visible press feedback and explicit accessible name, button role, and enabled state. Use a short action-specific label; an icon-only version needs an action-specific accessible name. [Buttons — Style and Content](https://developer.apple.com/design/human-interface-guidelines/buttons#Style)
- Make the actual selectable rectangle at least **44×44 pt**, enlarging it when content needs more room. Visible artwork can remain smaller; its size must not be confused with the hit region. Enlarged regions must not overlap or steal neighboring actions.
- Replace the **2 pt gap** as the accepted spacing specification. Require clear, comfortable separation, measured independently from the hit region. The accessibility guide suggests **around 12 pt padding for bezelled elements** and **24 pt outside visible edges for elements without a bezel**. Preserve those qualifications and measurement contexts: they are not a universal numeric edge-to-edge hit-region gap. The brief gives neither bezel treatment nor a spacing diagram, so final spacing requires an annotated layout and touch review. The 2 pt figure alone does not prove a universal numeric HIG violation. [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility)
- On activation, perform the named action once and expose its result. If completion is delayed, specify waiting, duplicate-activation handling, success, and failure; use the activating button’s activity indication while preserving context. Cancellation/recovery depends on the missing action semantics. [Buttons — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS)
- Keep the action usable by touch without accessories; verify supported keyboard and assistive activation. Enlarged labels must remain usable at at least 200% text enlargement. Check the footer in supported orientations and multitasking widths. These are acceptance requirements, not observed behavior. [Designing for iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados#Best-practices), [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

## Mac widget contract

Provisional scope: **system small on Mac Desktop and Notification Center**, the smallest supported system family for a focused glance. Product purpose is missing, so this is a surface/rendering contract pending content definition, not a completed widget content design. Mac app window/menu conventions do not establish widget rendering support. [Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos), [Widgets — System family widgets](https://developer.apple.com/design/human-interface-guidelines/widgets#System-family-widgets).

| Context | Required treatment in this proposal |
| --- | --- |
| Desktop, full color | Light/dark variants using semantic colors or suitable assets; one primary fact and a short contextual label. |
| Notification Center, full color | Same core glance and meaning, adapted to actual system layout. |
| Desktop, vibrant | Preserve the primary/supporting hierarchy in grayscale. Use opaque white/light gray for prominent content and darker opaque grays for supporting content; changing white opacity alone is insufficient. |
| Accented on Mac | No customer-facing promise or dependency. Reopen only after evidence resolves support for the selected OS, surface, and SDK. |

State must remain understandable through text, symbols, or shapes when color/background changes. Do not claim vibrant Notification Center support from this table: it lists vibrant only for Desktop. “No additional macOS rules” in the platform section does not override the rendering table. [Widgets — Full-color](https://developer.apple.com/design/human-interface-guidelines/widgets#Full-color), [Widgets — Vibrant](https://developer.apple.com/design/human-interface-guidelines/widgets#Vibrant), [Widgets — Using color](https://developer.apple.com/design/human-interface-guidelines/widgets#Using-color).

Before content design can pass, identify the glance question, primary value, sensitivity, configuration/auth needs, data source, freshness threshold, and precise app destination. Then specify realistic preview data, initial placeholder, signed-out/unavailable states, and stale wording. Keep useful existing data during refresh; updates remain system-controlled rather than continuous. Ordinary activation should open the relevant app content. Add in-place actions only if a simple product task justifies them and availability is verified. No sample product data or action is supplied here, so none is represented as real. [Widgets — Best practices](https://developer.apple.com/design/human-interface-guidelines/widgets#Best-practices), [Updating widget content](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content), [Adding interactivity](https://developer.apple.com/design/human-interface-guidelines/widgets#Adding-interactivity), [Previews and placeholders](https://developer.apple.com/design/human-interface-guidelines/widgets#Previews-and-placeholders).

## Acceptance checks and present status

| Status | Check and acceptance condition |
| --- | --- |
| Passed — local documentary review | Read the installed root skill, searched the topic index, read each selected family and topic procedure before its reference: Getting started → iPadOS/macOS; Menus and actions → Buttons; Foundations → Accessibility; System experiences → Widgets. Paths resolve under `.agents/skills/apple-hig/`. |
| Passed — specification | Correctly distinguishes iPad default from minimum; retains pt units and platform scope; documents the Mac source conflict and removes reliance on accented support. |
| Failed — supplied proposal | “28×28 pt is Apple default” contradicts the local table. The proposed hit region is below this specification’s 44×44 pt baseline. |
| Failed — evidence for promise | Unconditional Mac accented support is not substantiated by the supplied local guidance. This is a failed proposal claim, not a runtime test showing that an OS lacks the capability. |
| Not executed | Measure actual hit rectangles and visible-edge/padding geometry; confirm ≥44×44 pt, clear separation, no overlapping targets, and correct activation near every edge. |
| Not executed | Exercise touch comfort and accidental neighboring activation on supported iPads, including held/table use and supported compact widths. |
| Not executed | Verify button press/disabled/waiting/result behavior, correct outcome, duplicate handling, and recovery against the completed action contract. |
| Not executed | Use Accessibility Inspector and relevant VoiceOver, Full Keyboard Access, Switch Control, and other supported input paths; confirm name/role/state, order, focus, and activation. Verify enlarged text without clipped labels or inaccessible actions. |
| Not executed | Render Mac small widget in Desktop full-color light/dark, Desktop vibrant, and Notification Center full-color light/dark; verify hierarchy, noncolor meaning, actual text, long/localized content, edge values, contrast, and system sizing. |
| Not executed | Verify previews, stale/unavailable/auth states, timeline behavior and exact deep links after the product contract exists. Build with the chosen Apple SDK and deployment target. |

## Missing evidence and release gates

1. **Product and geometry:** action semantics, labels, neighboring controls, bezel treatment, annotated spacing measurements, supported iPad sizes, input paths, and OS targets. A claimed 2 pt gap lacks the measurement context needed to judge the padding advice.
2. **Widget requirements:** useful glance, content/data model, family/surface confirmation, privacy needs, freshness policy, auth/configuration requirements, and navigation destination. Until defined, the content contract is incomplete.
3. **Mac support resolution:** current authoritative Apple HIG clarification and version-specific WidgetKit documentation/API availability, followed by SDK and runtime evidence on the intended macOS release and surface. No current external verification was allowed or attempted. Local dated guidance is not an SDK capability guarantee; table-based exclusion is conservative, not a claim about every Mac release.
4. **Execution:** implementation, Apple build environment, rendered variants, measurements, and device/accessibility test records. Code/build work can remain on the headless server where feasible; interactive Mac checks belong on the MacBook and iPad checks on a supported iPad. This document establishes no device, SDK, GUI, or assistive-technology pass.

Proceed with the revised 44×44 pt iPad baseline and the table-supported Mac rendering scope. Final implementation acceptance remains pending the evidence above; the disputed accented capability must stay conditional until resolved.
