---
name: apple-hig-printing
description: Use when creating, reviewing, or adapting system print entry points, options, document setup, and printable-content availability.
---

# Let the system own printing's common work

Read [the printing guide](../../references/printing.md). The workflow is application advice; supported printer options and availability require actual evidence.

Inspect printable content, printer/output support, document options, platform, and create/review/adapt mode. Distinguish frequently changed print choices from infrequent document setup. Record real compatibility and command enablement rather than assuming an available printer.

Use standard system printing and expected entry points. When nothing/printer is available, dim the Mac command, remove the mobile sheet action, and dim/hide custom controls as appropriate. Offer only relevant supported options rather than recreating copies/range/duplex. On Mac put genuinely custom settings in a clear category, infrequent size/orientation/scaling in document Page Setup, and rare settings behind Advanced Options. Explain incompatible choices and preview effects where useful; retain document settings at least while it remains open. tvOS/watchOS do not support printing in this guidance.

Implement the print/setup binding, produce an entry/availability/options specification, or review exact duplication/incompatibility defects. Do not actually submit print jobs without authorized scope; a reviewable configuration/artifact can satisfy design work.

**Worked transformation:** Before: a Mac label editor asks for printer/copy count in a custom Page Setup and silently permits transparent media with incompatible duplex. Decision: common print controls are duplicated and incompatibility hidden. After: use the system print panel, keep document dimensions in Page Setup, and clearly disable/explain incompatible custom choices.

Deliver the artifact and content/availability/options/document-retention contract. Verify no content/printer, supported option changes, incompatibility, preview, cancel, and reopen. Fail for falsely enabled printing, hidden incompatible output, or duplicated conflicting system options. Actual printer output, pagination, and device dialogs require execution evidence.

Load [file-management](../apple-hig-file-management/SKILL.md), [the-menu-bar](../../../apple-hig-menus-and-actions/.topics/apple-hig-the-menu-bar/SKILL.md), or [activity-views](../../../apple-hig-menus-and-actions/.topics/apple-hig-activity-views/SKILL.md) for the relevant entry route.
