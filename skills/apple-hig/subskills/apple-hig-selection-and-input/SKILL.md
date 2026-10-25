---
name: apple-hig-selection-and-input
description: Use when choosing Apple-platform text entry, keyboards, pickers, switches, checkboxes, sliders, steppers, color/image wells, or segmented controls.
---

# Apple HIG: Map the data domain to the control

Use this family to select and compose topic procedures. Infer the platform and
requested work from the supplied project; preserve its framework and constraints.

## Work through the decision

1. Identify value type, range, precision, number of choices and whether selection commits immediately. Enter the procedure for fields, pickers, sliders, toggles or other suitable controls.
2. Choose a control according to the person’s input task, available space and precision needs. Preserve valid values, locale conventions and useful defaults without silently changing user input.
3. Specify validation and correction in context, including keyboard/paste and alternative access where relevant. Distinguish unavailable actions from invalid entered data.
4. Deliver a field/control contract or a patch that includes value representation, commit/cancel behavior and concrete invalid/edge-value checks.

## Enter the topic procedure

Read the selected topic’s SKILL.md before its supporting guidance. For a review,
inspect actual evidence and return findings; for an implementation request, make
the authorized change; for design or adaptation, produce a usable specification
or patch. Load related topics only when the chosen procedure calls for them.

- [Color wells](.topics/apple-hig-color-wells/SKILL.md)
- [Combo boxes](.topics/apple-hig-combo-boxes/SKILL.md)
- [Digit entry views](.topics/apple-hig-digit-entry-views/SKILL.md)
- [Image wells](.topics/apple-hig-image-wells/SKILL.md)
- [Pickers](.topics/apple-hig-pickers/SKILL.md)
- [Segmented controls](.topics/apple-hig-segmented-controls/SKILL.md)
- [Sliders](.topics/apple-hig-sliders/SKILL.md)
- [Steppers](.topics/apple-hig-steppers/SKILL.md)
- [Text fields](.topics/apple-hig-text-fields/SKILL.md)
- [Toggles](.topics/apple-hig-toggles/SKILL.md)
- [Virtual keyboards](.topics/apple-hig-virtual-keyboards/SKILL.md)

## Completion evidence

Report the concrete decisions or changes, their source support, and which checks
passed, failed or were not executed. A source citation or a list of links is not
the requested work product. Retain platform exceptions and unresolved source
conflicts; the absence of a platform subsection does not establish support.
