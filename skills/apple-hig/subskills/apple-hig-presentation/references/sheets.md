# Sheets

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/sheets)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A sheet supports a short, scoped task closely connected to its parent, such as choosing a save location or attaching a file.

<a id="Anatomy"></a>
## Anatomy

Sheets are modal on macOS, tvOS, visionOS, and watchOS. iOS and iPadOS also allow nonmodal sheets that affect the parent while leaving it interactive. Cancel/Close dismisses without saving; Done finishes or saves; Back moves to an earlier step rather than dismissing the sheet.

<a id="Best-practices"></a>
## Best practices

For lengthy or complex tasks, evaluate fullscreen editing/media presentation, a separate Mac window, or a visionOS Full Space. Keep only one sheet from the main interface at a time. Close an existing sheet before a new one, restoring it later if necessary. For ongoing supplementary work, use nonmodal iOS/iPadOS sheets, macOS panels, or a visionOS split view. Pair Done with Cancel or Back to make an alternative route clear, but avoid showing Cancel, Back, and Done together.

<a id="Platform-considerations"></a>
## Platform considerations

No additional tvOS rules are specified.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

For a single-view sheet, Cancel belongs at the leading top edge and Done at the trailing edge. In a multistep flow, the first step can show Cancel with disabled Done, subsequent steps Back with disabled Done, and the final step Back with enabled Done.

Resizable sheets rest at detents. Large is fully expanded; medium is about half height; custom heights are possible. Large is automatic, adding medium permits both, and medium alone prevents full-height expansion. On iPhone, medium can reveal common content first while allowing expansion; composition flows often benefit from large only. Show a grabber for resizable sheets: dragging changes height, tapping cycles detents, and VoiceOver can use it. Support vertical swipe dismissal and use an action sheet to resolve unsaved changes. On iPad, prefer centered page/form styles with standard sizing over a dimmed background.

<a id="macOS"></a>
### macOS

A rounded card floats over and dims its parent, but other app windows remain usable. Choose a useful default size, with resize support where expanding helps. Bring forward the parent and its modeless document panels on presentation, and allow other windows to come forward before dismissal. Repeated input-and-observe workflows belong in a panel rather than a sheet.

<a id="visionOS"></a>
### visionOS

The sheet floats before its dimmed parent. Center it in the field of view instead of emerging from the window bottom. Keep enough parent visible for context, and consider optional resizing.

<a id="watchOS"></a>
### watchOS

A sheet slides over the screen with semitransparency and system blur/desaturation. Use it only for a brief occasional task requiring custom title or content; alerts and action sheets better fit basic information or choices. Do not use sheets as content navigation. Keep the leading dismissal unmistakable; if replacing its default label, use a suitable SF Symbol rather than Back or a page-like title.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Modality](https://developer.apple.com/design/human-interface-guidelines/modality)
[Action sheets](https://developer.apple.com/design/human-interface-guidelines/action-sheets)
[Popovers](https://developer.apple.com/design/human-interface-guidelines/popovers)
[Panels](https://developer.apple.com/design/human-interface-guidelines/panels)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/View/sheet(item:onDismiss:content:)> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UISheetPresentationController> — UIKit
<https://developer.apple.com/documentation/AppKit/NSViewController/presentAsSheet(_:)> — AppKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: March 24, 2026, March 29, 2024, December 5, 2023, June 21, 2023, June 5, 2023.
