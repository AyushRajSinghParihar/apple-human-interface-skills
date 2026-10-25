# Live Activities

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/live-activities)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

## Contents

- [Anatomy](#Anatomy)
- [Best practices](#Best-practices)
- [Presentation](#Presentation)
- [CarPlay](#CarPlay)
- [Platform considerations](#Platform-considerations)
- [Specifications](#Specifications)

Live Activities track a bounded task or event through frequent updates over a few hours. They begin on iPhone or iPad and can appear on the Lock/Home Screen, Dynamic Island and StandBy, paired Mac menu bar, Apple Watch Smart Stack, and CarPlay Dashboard.

<a id="Anatomy"></a>
## Anatomy

Support compact, minimal, expanded, and Lock Screen presentations. The system composes these for available space and devices.

<a id="Compact"></a>
### Compact

A single Dynamic Island activity uses separate leading/trailing elements around the TrueDepth camera.

<a id="Minimal"></a>
### Minimal

Multiple activities use compact circular/oval treatments, up to three where supported: one attached and others detached. Tap opens the app; hold expands.

<a id="Expanded"></a>
### Expanded

Holding compact/minimal content reveals a larger presentation.

<a id="Lock-Screen"></a>
### Lock Screen

A bottom banner uses a layout related to expanded. On devices without Dynamic Island, essential update alerts can briefly overlay this banner on Home or another app.

<a id="StandBy"></a>
### StandBy

Minimal content expands on tap to a Lock Screen layout scaled 2×. A custom background extends across the screen.

<a id="Best-practices"></a>
## Best practices

Use tasks with clear starts and ends, ideally no more than 8 hours. Show only immediately useful information, with details in the app. Exclude ads and promotions. Avoid exposed sensitive content; summarize or redact and offer app access/configuration. Match app identity across appearances; a logo mark can appear without a container, but do not use the full app icon. Do not draw attention to Dynamic Island from inside the app. Use legible large text, generally medium weight or stronger.

<a id="Creating-Live-Activity-layouts"></a>
### Creating Live Activity layouts

Adapt to actual screens and scale factors. Keep layout only as large as content needs. For limited-width Dynamic Island contexts, fit compact/minimal content within a 28-pt circle with abbreviations or graphics; use leading-only when a meaningful trailing version cannot fit. Favor familiar templates, even concentric margins, and container-relative corner radii. Inset groups or use a thick dividing line instead of extending content to edges. A blurred drawing-tool preview can help align angular content within rounded corners. Adjust Lock Screen/expanded height as available information grows or shrinks.

<a id="Choosing-colors"></a>
### Choosing colors

Only Lock Screen permits custom background colors; compact, minimal, and expanded backgrounds are system-controlled. Dynamic Island is opaque black, so meaningful bold foreground color can express identity. Match its dark-background keyline to related content. Check custom Lock Screen contrast in both appearances and reduced-luminance Always On.

<a id="Adding-transitions-and-animating-content-updates"></a>
### Adding transitions and animating content updates

Animations can last at most 2 seconds and are not played in reduced-luminance Always On. Use numeric changes, fades, scale, or movement to explain updates. Preserve existing elements as layout grows rather than removing/readding everything. Avoid transition collisions; animate a moved item and fade other list elements when needed.

<a id="Offering-interactivity"></a>
### Offering interactivity

Deep-link to the relevant task. Favor one essential button or toggle for a direct action, pause/resume, or response to meaningful progress, preserving space for status and reducing accidental activation.

<a id="Starting-updating-and-ending-a-Live-Activity"></a>
### Starting, updating, and ending a Live Activity

Begin at expected moments, including automatic starts for followed events, with an easy opt-out in the corresponding app view. Offer an App Shortcut when useful. Update only for changed content. Alert only for crucial updates and avoid a parallel push for the same information. Prefer one dynamically changing activity for related simultaneous events. End immediately when the task ends: Dynamic Island/CarPlay remove it, while Lock Screen, Mac, and watch can retain it for up to 4 hours. Choose a shorter useful summary lifetime, commonly 15–30 minutes, proportional to the activity.

<a id="Presentation"></a>
## Presentation

Design the iPhone presentations first, then tailor layouts for StandBy, watch, and driving while supporting every destination.

<a id="Compact-presentation"></a>
### Compact presentation

Show essential changing data. Make both halves read as one through coherent color/type and balanced widths. Fit snugly against the camera without extra inner padding or unnecessary status-bar obstruction; shorten units or precision as needed. Both halves should deep-link to the same relevant app screen.

<a id="Minimal-presentation"></a>
### Minimal presentation

Preserve recognition while conveying current information instead of only a static logo.

<a id="Expanded-presentation"></a>
### Expanded presentation

Expand predictably from the smaller layout, retaining relative positions and fitting content close to the camera rather than leaving unused gaps.

<a id="Lock-Screen-presentation"></a>
### Lock Screen presentation

Create a distinct task layout rather than copying notification structure. Use restrained tint/background customization to fit personalized wallpapers. Verify contrast in both appearances and Always On, including the system-generated dismiss-button color; override its foreground if needed. Standard margins are 14 pt, with tighter spacing only when content grouping needs it.

<a id="StandBy-presentation"></a>
### StandBy presentation

Supply assets and, where useful, a custom layout for the larger scale. The default background blends with the bezel and surroundings and permits slightly more content scale. Preserve margins so expansion does not crop graphics, and test the red-tinted Night Mode.

<a id="CarPlay"></a>
## CarPlay

The default combines compact halves. A supplemental small family can support larger type and more information. Its custom layout is also used on watch, but CarPlay disables buttons and toggles; driving-oriented activities should prioritize timely content over those controls.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS or iPadOS rules are specified. Live Activities are unsupported in tvOS and visionOS.

<a id="macOS"></a>
### macOS

Paired Mac menu-bar presentations use compact/minimal/expanded styles. Activation opens the app through iPhone Mirroring.

<a id="watchOS"></a>
### watchOS

The activity appears atop the paired watch's Smart Stack, combining compact halves by default. Tap opens a watch app when available; otherwise it opens a full-screen view with a paired-iPhone launch button. A custom layout can improve essential progress, changes, and controls, but consider its shared use in CarPlay where interaction is disabled.

<a id="Specifications"></a>
## Specifications

These source dimensions are design guidance in points; system scaling and context can change final appearance.

<a id="CarPlay-dimensions"></a>
### CarPlay dimensions

Test all three activity sizes and listed Smart Display Zoom simulator configurations.

|Live Activity size (pt)|
|-----------------------|
|240x78                 |
|240x100                |
|170x78                 |

|Configuration|Resolution (pt)|
|-------------|---------------|
|Widescreen   |1920x720       |
|Portrait     |900x1200       |
|Standard     |800x480        |

<a id="iOS-dimensions"></a>
### iOS dimensions

|Screen dimensions (portrait)|Compact (leading and trailing)|Minimal (width given as a range)|Expanded (height given as a range)|Lock Screen (height given as a range)|Limited width|
|----------------------------|------------------------------|--------------------------------|----------------------------------|-------------------------------------|-------------|
|430x932                     |62.33x36.67                   |36.67–45x36.67                  |408x84–160                        |408x84–160                           |28x28        |
|393x852                     |52.33x36.67                   |36.67–45x36.67                  |371x84–160                        |371x84–160                           |28x28        |

<a id="iPadOS-dimensions"></a>
### iPadOS dimensions

|Screen dimensions (portrait)|Lock Screen (height given as a range)|
|----------------------------|-------------------------------------|
|1366x1024                   |500x84–160                           |
|1194x834                    |425x84–160                           |
|1012x834                    |425x84–160                           |
|1080x810                    |425x84–160                           |
|1024x768                    |425x84–160                           |

<a id="macOS-dimensions"></a>
### macOS dimensions

Use the iOS dimensions above.

<a id="watchOS-dimensions"></a>
### watchOS dimensions

Smart Stack activities use the same dimensions as watch widgets.

|Apple Watch size |Size of a Live Activity in the Smart Stack (pt)|
|-----------------|-----------------------------------------------|
|40mm             |152x69.5                                       |
|41mm             |165x72.5                                       |
|42mm             |176x72.5                                       |
|44mm             |173x76.5                                       |
|45mm             |184x80.5                                       |
|46mm             |194x80.5                                       |
|49mm (Ultra 3, 4)|198x81.5                                       |
|49mm (Ultra 1, 2)|191x81.5                                       |

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/ActivityKit>
<https://developer.apple.com/documentation/SwiftUI>
<https://developer.apple.com/documentation/WidgetKit>
<https://developer.apple.com/documentation/WidgetKit/Developing-a-WidgetKit-strategy> — WidgetKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2026/223>
  <https://developer.apple.com/videos/play/wwdc2025/216>
  <https://developer.apple.com/videos/play/wwdc2025/278>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: October 13, 2026, December 16, 2025, June 10, 2024, October 24, 2023, June 5, 2023, November 3, 2022, September 23, 2022.
