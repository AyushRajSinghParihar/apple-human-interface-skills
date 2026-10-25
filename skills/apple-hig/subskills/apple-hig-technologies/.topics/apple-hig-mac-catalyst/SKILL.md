---
name: apple-hig-mac-catalyst
description: Use when adapting or reviewing an iPad app for Mac Catalyst, including idiom scaling, keyboard/pointer input, desktop navigation, menus, windows, and unavailable device features.
---

# Turn a suitable iPad foundation into deliberate Mac work

Read [Mac Catalyst](../../references/mac-catalyst.md). Inspect the iPad task, essential hardware/API dependencies, existing scenes/resizing/drag-drop/keyboard support, and requested design/review/adaptation. Preserve Catalyst when it is the chosen stack. If the core task requires unavailable device functions, identify an alternative or suitability limit rather than promising an unchanged port.

Choose the idiom deliberately. Default iPad idiom scales to 77%; Mac idiom renders at 100% and needs layout/text/image review. Compare actual content/control metrics, semantic styles, and any separate Mac assets rather than treating scale as a cosmetic switch. Use only supported shared/native customizations.

Adapt navigation around desktop context. Prefer a suitable sidebar split view for hierarchy or segmented control for flat exclusive categories, replacing an imported bottom tab bar where appropriate. Put top-level destinations in View, useful main commands in toolbars and menus, and provide Next/Previous alongside swipe shortcuts. Use adjacent inspectors where desktop space makes a popover unnecessary.

Trace mouse, trackpad, keyboard, file, and multiwindow work. Preserve context menus and standard command behavior. For pinch/rotation, remember trackpad touches are delivered to the view under the pointer, not separately targeted views. Reconsider placements driven by phone/tablet thumb reach and inspect the actual Mac transformations supplied by the platform.

**Before → decision → after:** An iPad drawing catalog port keeps bottom tabs, a touch-only swipe to change items, and a popover covering the artwork. Decision: Mac users need persistent hierarchy and precise commands. After, a sidebar preserves selection, toolbar/menu Next and Previous complement gestures, an adjacent inspector exposes tools, and idiom-specific type/image sizes are reviewed at actual scale.

Deliver a suitability/idiom decision and corrected navigation/input/window specification or implementation. Fail if an essential unavailable feature blocks the task, shortcuts are missing, scaling clips content, or gestures are the only path. Linux source review cannot verify Catalyst rendering, menus, file handling, or focus; identify pending Mac checks.

Use [Designing for macOS](../../../apple-hig-getting-started/.topics/apple-hig-designing-for-macos/SKILL.md), [Keyboards](../../../apple-hig-inputs/.topics/apple-hig-keyboards/SKILL.md), and [Pointing devices](../../../apple-hig-inputs/.topics/apple-hig-pointing-devices/SKILL.md) for the selected desktop work.
