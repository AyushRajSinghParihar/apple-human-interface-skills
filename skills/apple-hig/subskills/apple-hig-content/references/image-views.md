# Image views

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/image-views)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

An image view presents a still image or a sequence of frames, with an opaque or transparent background. Its sizing and positioning behavior can fit, scale, stretch, or pin the content; interaction is usually outside its purpose.

<a id="Best-practices"></a>
## Best practices

Use an image view for image presentation. When activating an image must perform an action, put the image in a system button so the action has standard button behavior and accessibility. For interface glyphs, prefer SF Symbols or template icons: they support contextual rendering, opacity, and the person's selected accent color more naturally than arbitrary image content.

<a id="Content"></a>
## Content

Rich formats include PNG, JPEG, and PDF. Protect both image clarity and text legibility when adding text overlays; provide sufficient contrast, with a supporting layer or shadow where appropriate. Prepare animation frames at a consistent size and shape, ideally already scaled to the view, to avoid unnecessary runtime scaling and inconsistent performance.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS or iPadOS rules are specified.

<a id="macOS"></a>
### macOS

Choose an image well when the picture must support editing through copy, paste, drag, or Delete. Use an image button for a clickable picture that triggers an immediate app action.

<a id="tvOS"></a>
### tvOS

Layered imagery can use transparency across layers to create depth; preserve that structure when the design calls for the platform's layered-image treatment.

<a id="visionOS"></a>
### visionOS

Image views in windows can present 2D, stereoscopic, and spatial-photo content. RealityKit can present images alongside 3D content outside an image view and can generate a spatial scene from an existing 2D image. Choose the image presentation mechanism to fit the window, volume, or 3D scene rather than treating all imagery as a flat control.

<a id="watchOS"></a>
### watchOS

Prefer SwiftUI for animation. Where needed, WatchKit can animate a sequence of images through its image-animation support.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Images](https://developer.apple.com/design/human-interface-guidelines/images)
[Image wells](https://developer.apple.com/design/human-interface-guidelines/image-wells)
[Image buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Image-buttons)
[SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/Image> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UIImageView> — UIKit
<https://developer.apple.com/documentation/AppKit/NSImageView> — AppKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2023/10181>
  <https://developer.apple.com/videos/play/wwdc2021/10021>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 21, 2023.
