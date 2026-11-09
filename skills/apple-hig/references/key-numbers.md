# Key numbers

These values come from the source guides of this package. Each row gives the
platform scope and the guide that has the full rule and its exceptions. A
minimum is a limit, not a comfortable default. Read the linked guide before you
apply a number outside its scope.

## Text and controls

From [Accessibility](../subskills/apple-hig-foundations/references/accessibility.md):

| Platform | Default text | Minimum text | Default control | Minimum control |
|---|---:|---:|---:|---:|
| iOS, iPadOS | 17 pt | 11 pt | 44 × 44 pt | 28 × 28 pt |
| macOS | 13 pt | 10 pt | 28 × 28 pt | 20 × 20 pt |
| tvOS | 29 pt | 23 pt | 66 × 66 pt | 56 × 56 pt |
| visionOS | 17 pt | 12 pt | 60 × 60 pt | 28 × 28 pt |
| watchOS | 16 pt | 12 pt | 44 × 44 pt | 28 × 28 pt |

- Text enlargement: support at least 200%; 140% on watchOS
  ([Accessibility](../subskills/apple-hig-foundations/references/accessibility.md)).
- Contrast values in Apple's Accessibility Inspector: 4.5:1 for text up to
  17 pt, 3:1 for 18 pt and larger, and 3:1 for bold text
  ([Accessibility](../subskills/apple-hig-foundations/references/accessibility.md)).
- Dynamic Type sizes for each text style:
  [Typography](../subskills/apple-hig-foundations/references/typography.md).

## System surfaces

| Value | Scope | Guide |
|---|---|---|
| Ideally no more than 8 hours of activity | Live Activities | [Live Activities](../subskills/apple-hig-system-experiences/references/live-activities.md) |
| Up to 4 hours on Lock Screen, Mac and watch after the end; summary lifetime commonly 15–30 minutes | Live Activities | [Live Activities](../subskills/apple-hig-system-experiences/references/live-activities.md) |
| Compact or minimal content in a 28 pt circle | Live Activities in limited-width Dynamic Island contexts | [Live Activities](../subskills/apple-hig-system-experiences/references/live-activities.md) |
| Transitions of up to 2 seconds | Widgets | [Widgets](../subskills/apple-hig-system-experiences/references/widgets.md) |
| Accessory view no taller than 154 pt, 16 pt corner radius | Alerts in visionOS | [Alerts](../subskills/apple-hig-presentation/references/alerts.md) |
| Up to three buttons | Alerts | [Alerts](../subskills/apple-hig-presentation/references/alerts.md) |

## App icons

From [App icons](../subskills/apple-hig-foundations/references/app-icons.md):

| Platform | Canvas | Result | Pixels |
|---|---|---|---:|
| iOS, iPadOS, macOS | square | rounded square | 1024 × 1024 |
| tvOS | landscape rectangle | rounded rectangle | 800 × 480 |
| visionOS | square | circle | 1024 × 1024 |
| watchOS | square | circle | 1088 × 1088 |

Widget, complication and Live Activity dimensions for each device are in the
size tables of their guides.
