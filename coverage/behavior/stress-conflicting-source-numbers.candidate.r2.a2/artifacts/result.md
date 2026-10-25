# Qualified specification

This is a design review of `interface.md`, not an implementation or runtime certification. The supplied evidence is a custom iPad footer action with a stated 28×28 pt hit region and 2 pt gap, plus a Mac widget rendering promise. No rendered app exists. Only supplied local files and installed instructions were consulted; no web verification was performed. Official links below identify the source sections, not pages checked live.

## Decisions and conflict resolution

| Proposal | Decision | Basis and qualification |
|---|---|---|
| Call the iPad 28×28 pt region “Apple default” | Reject that description; specify at least 44×44 pt activation area. | The Accessibility Mobility table lists **44×44 pt default** and **28×28 pt minimum** for iOS/iPadOS. Buttons recommends general hit regions of at least 44×44 pt. These are different levels of guidance, not contradictory defaults. Meeting the smaller table minimum alone does not establish comfortable or accessible operation. |
| Keep a 2 pt gap | Revise the spacing specification and verify geometry. | Both guides call for sufficient separation. Neither supplied passage establishes a universal iPad numerical gap rule. A 2 pt gap is not proven adequate; it is also not, by itself, a demonstrated violation of a numerical HIG gap requirement. |
| Promise Mac accented rendering | Remove the unconditional promise. | The Widgets appearance table explicitly marks Mac accented mode “Not supported,” while the accented section records conflicting prose about Mac group tinting. Preserve that conflict; do not treat prose as proof of support or claim it has been resolved for current releases. |

Sources: [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility), [Buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), [Widgets — Appearances](https://developer.apple.com/design/human-interface-guidelines/widgets#Appearances), [Widgets — Accented](https://developer.apple.com/design/human-interface-guidelines/widgets#Accented).

## iPad footer action contract

- Keep touch operation available without accessories. Use a system button/style where it serves the product; if custom rendering remains, supply perceivable press feedback and appropriate enabled/disabled and focus states. A system control does not eliminate geometry verification.
- Allocate an activation rectangle at least **44×44 pt**, growing for its label. Visible artwork may remain 28×28 pt if legible and understandable; artwork size and activation size are separate specifications.
- As a provisional project layout choice, use **12 pt clear separation between adjacent activation rectangles**, with no overlap. This is not an Apple-mandated iPad gap. The Accessibility guide separately suggests around 12 pt padding for bezelled elements and 24 pt outside visible edges for unbezelled elements; those recommendations are not interchangeable with a universal inter-target gap. Revisit visual padding once bezel treatment and surrounding controls are known.
- Do not simply expand the existing regions in place. If the stated 2 pt is between two 28 pt targets, their centers are 30 pt apart; symmetric expansion to 44 pt would overlap by 14 pt. Relayout the footer. For two 44 pt targets with the proposed 12 pt clear gap, centers are at least 56 pt apart.
- Give the action a short outcome-specific verb label and an accessible name identifying the same action. Do not invent a label or assign primary/destructive/default behavior before the actual outcome, affected object, and reversibility are supplied. Assume only that this is an immediate command; persistent selection or menu opening requires reclassification.
- Activation invokes the named action once and shows press feedback. If completion is delayed, show an activity indicator within the activating button, replacing an image where applicable, retain context, and prevent duplicate submission. Product-specific success, error, recovery, and availability rules remain open.

Support: [Buttons — Style, Content and Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Style), [Buttons — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS), [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility), [Designing for iPadOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados#Best-practices).

## Mac widget contract

For the rendering review, provisionally select a **system-small widget on the Mac desktop**, also considering Notification Center. The local supported-context table lists this family for both surfaces. This is a scope assumption, not evidence that the product's unspecified content fits it.

| Surface | Rendering specification from the local table |
|---|---|
| Mac desktop | Full color, with light/dark adaptation; vibrant with meaningful grayscale hierarchy. |
| Mac Notification Center | Full color, with light/dark adaptation. Do not infer vibrant support from desktop support. |
| Mac accented mode | No shipping promise or dependency; unresolved pending target-release verification. |

Design the desktop vibrant variant with grayscale brightness establishing emphasis; varying white opacity alone is not a substitute. Preserve meaning with text, symbols or shapes when color disappears. Do not infer accented mode merely from an appearance that looks tinted, or from the absence of additional macOS rules in the article.

Proposed behavior: present one useful changing fact; ordinary activation opens the corresponding app content. Do not add in-place controls without a defined simple action. Use available data during refresh, distinguish stale/unavailable content when age affects interpretation, and avoid a continuous-refresh promise. Use realistic gallery previews, explicitly marking simulated data. The exact glance question, data fields, deep link, freshness threshold, signed-out/configuration behavior and sensitivity policy require product evidence; no invented example is being approved as the product specification.

Support: [Widgets — System family widgets](https://developer.apple.com/design/human-interface-guidelines/widgets#System-family-widgets), [Rendering modes](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes), [Updating widget content](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content), [Adding interactivity](https://developer.apple.com/design/human-interface-guidelines/widgets#Adding-interactivity), [Previews and placeholders](https://developer.apple.com/design/human-interface-guidelines/widgets#Previews-and-placeholders). Desktop conventions were checked against the local [Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos) guide; an app-window command model is not being imposed on a system-owned widget.

## Acceptance checks and current status

**Passed — local documentary review only:** inspected the supplied brief; read the installed root skill, searched the topic index, read the four owning families and five topic procedures before their supporting guides; separated iPad default from minimum; retained the Mac source conflict and surface-specific support limits. This document supplies the revised design contract.

**Failed — proposal claims:** “28×28 pt is Apple default” contradicts the local iPad default table. The supplied 28×28 pt activation region falls short of the selected 44×44 pt specification and general Buttons recommendation. The unconditional Mac accented-mode promise lacks consistent source support. These are specification findings, not observed runtime failures.

**Not executed — implementation acceptance:**

| Check | Required evidence / acceptance condition |
|---|---|
| Hit geometry and separation | Inspect implemented layout and runtime hit testing: each iPad target is at least 44×44 pt, proposed clear gaps are maintained, targets never overlap, and edge presses invoke only the intended action. Clarify what the original 2 pt gap measures. |
| Task and states | Supply action semantics, then verify label/name, role, activation outcome, availability, press feedback, and any pending/success/error/recovery behavior. |
| Adaptation and readability | On supported iPad sizes, orientations and narrow multitasking widths, preserve usable action and labels with text enlargement of at least 200%; no clipping or overlapping targets. Physical reach and accidental activation require device use. |
| Assistive operation | Use Accessibility Inspector and relevant VoiceOver, Voice Control, Switch Control, AssistiveTouch and Full Keyboard Access paths to confirm naming, reachability and activation. No assistive-technology results are available. |
| Mac appearance | Render selected widget family on desktop and Notification Center in applicable full-color light/dark and desktop vibrant contexts; confirm legibility, noncolor meaning and measured foreground/background contrast. No screenshots, measurements or GUI results exist. |
| Mac support conflict | Record exact deployment OS versions and SDK; obtain current official HIG clarification, applicable WidgetKit availability documentation and compiled/runtime evidence of rendering modes on those releases. A result on one release does not establish all-release support. Keep accented mode conditional until this evidence resolves the promise. |
| Widget usefulness and states | Supply the glance question and data contract; verify realistic preview, stale/unavailable/refresh/auth/configuration states, precise deep link and system-controlled refresh behavior. |

The installed articles are derivative local snapshots dated 2026-10-25, not SDK references or independently verified current capability evidence. Future official-source checks are explicitly deferred because this task prohibits browsing. No device, SDK build, GUI, accessibility execution, contrast measurement or physical-comfort test is claimed.

## Audit trail

All paths below resolve within `.agents/skills/apple-hig/`. Each consumed file was read with a separate `cat` command, except the topic index, searched with a single-file `rg` command.

1. `SKILL.md`, then project `interface.md`, then `references/topic-index.md` (relevant concept rows).
2. Family `SKILL.md` files under `subskills/apple-hig-getting-started/`, `apple-hig-foundations/`, `apple-hig-menus-and-actions/`, and `apple-hig-system-experiences/`.
3. Topic `SKILL.md` files: Getting started `.topics/apple-hig-designing-for-ipados/` and `.topics/apple-hig-designing-for-macos/`; Foundations `.topics/apple-hig-accessibility/`; Menus and actions `.topics/apple-hig-buttons/`; System experiences `.topics/apple-hig-widgets/`.
4. Corresponding family `references/` files: `designing-for-ipados.md`, `designing-for-macos.md`, `accessibility.md`, `buttons.md`, and `widgets.md`.
