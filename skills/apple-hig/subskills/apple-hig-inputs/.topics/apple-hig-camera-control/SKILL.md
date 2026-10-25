---
name: apple-hig-camera-control
description: Use when designing or reviewing iPhone Camera Control overlay functions, slider or picker choices, capture-mode availability, or locked capture entry.
---

# Make hardware adjustments predictable during capture

Read [Camera Control](../../references/camera-control.md). Inspect capture modes, existing controls, value models, viewfinder layout, and supported devices. The source describes iPhone 16/16 Pro and excludes other platforms; verify current hardware/API availability when implementing beyond that snapshot. Choose design, review, or adaptation mode and retain the existing capture stack.

Inventory the fixed control set. Use sliders for ranges and pickers for discrete choices; enable/disable controls by capture mode rather than dynamically adding/removing them. Put common functions near the middle and rare ones at the ends, accounting for the system remembering the last-used control.

Give each function a short name and an available SF Symbol representing function rather than live state; custom symbols are unsupported here. Expose meaningful units/localized values and useful prominent range values so sliding can settle precisely. Reserve overlay/label space beside the hardware control in portrait and landscape, allowing Dynamic Type enlargement. Hide duplicate app controls while the overlay is present without hiding unrelated needed information. Consider the locked camera capture extension for relevant system entrypoints.

**Before → decision → after:** A camera app adds/removes white-balance choices whenever modes change and uses a custom icon whose shape varies with temperature. Decision: the hardware overlay needs a stable function set and function identity. After, white balance remains in its fixed position but is disabled in unsupported modes, uses an available function symbol, and displays a localized temperature value while duplicate onscreen controls recede during adjustment.

Deliver the fixed function inventory, slider/picker/value contract, and overlay layouts or implementation. Fail if a remembered control disappears unexpectedly, labels overlap essential capture content, or a slider provides no usable value feedback. Static review cannot verify light-press/double-press/sliding ergonomics or lock-screen launch; list actual supported-device checks separately.

Use [SF Symbols](../../../apple-hig-foundations/.topics/apple-hig-sf-symbols/SKILL.md) for available symbol configuration and [Layout](../../../apple-hig-foundations/.topics/apple-hig-layout/SKILL.md) for adaptive overlay space.
