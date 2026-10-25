# Dark Mode

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/dark-mode) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Respect system light/dark appearance preferences on iOS, iPadOS, macOS, and tvOS. Dark Mode uses darker backgrounds and lighter foregrounds with purpose-specific contrast, rather than mechanically inverting every color.

<a id="Best-practices"></a>
## Best practices
Avoid a separate app appearance switch that duplicates system settings. Handle automatic appearance changes while the app is running. Test both appearances with Increase Contrast and Reduce Transparency separately and together; increased contrast can expose unexpected low-contrast dark text. A permanently dark presentation is an uncommon exception for contexts such as immersive media where surrounding UI should recede.

<a id="Dark-Mode-colors"></a>
## Dark Mode colors
Choose semantic adaptive colors and asset-catalog Color Sets for custom bright/dim variants, rather than fixed values. Maintain at least 4.5:1 foreground/background contrast; aim for 7:1 with custom colors, especially small type. Slightly dim white-background images if they glow harshly in a dark interface.

<a id="Icons-and-images"></a>
### Icons and images
Prefer SF Symbols with dynamic tint or vibrancy. Test full-color art in both modes; reuse one asset when it works, otherwise provide mode-specific versions under one asset name. Custom interface icons may need different outlines to keep their edges readable against light and dark surfaces.

<a id="Text"></a>
### Text
Use the primary through quaternary system label colors. Prefer system text fields/views, which adjust text and vibrancy to their actual background, over drawing text manually.

<a id="Platform-considerations"></a>
## Platform considerations
No extra tvOS rules are given. This source says Dark Mode is not supported on visionOS or watchOS.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS
System backgrounds distinguish dimmer base surfaces from brighter elevated foreground surfaces. Sheets, popovers, multitasking apps, and multiple windows use this difference to clarify depth. Preserve automatic system background adaptation instead of replacing it with a static custom fill.

<a id="macOS"></a>
### macOS
With the graphite accent setting, desktop tinting subtly picks up wallpaper color in window backgrounds. A neutral custom component with a visible bezel/background can use some transparency to share that harmony. Avoid transparency in colored states because movement or wallpaper changes would unpredictably alter their meaning-bearing colors.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/dark-mode) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Videos"></a>
#### Videos
Apple’s linked design sessions provide demonstrations and additional implementation context; no video review is implied here.

<a id="Change-log"></a>
## Change log
Source revision dates: August 6, 2024.
