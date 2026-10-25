# Pickers

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/pickers)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Pickers offer scrollable, ordered choices for single or multipart values. Language and locale affect displayed values and order. Date pickers can also use calendars and numeric entry.

<a id="Best-practices"></a>
## Best practices

Use a picker for a medium or longer list. A short list may work better in a pull-down; a very large dataset may need a resizable list or indexed table. Arrange values logically so hidden choices are predictable, for example alphabetically. Present the picker near the edited field, commonly at the bottom of the window or in a popover, instead of forcing a separate navigation step.

Minute wheels default to 0–59. A coarser interval is allowed if it divides 60 evenly; 15-minute steps produce 0, 15, 30, and 45.

<a id="Platform-considerations"></a>
## Platform considerations

visionOS has no additional rules in this source.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Date entry supports touch, hardware keyboards, and pointers. Choose among these styles:

| Style | Presentation |
| --- | --- |
| Compact | Current value in an accent-colored button; activation opens a modal calendar/time editor |
| Inline | Calendar for dates and dates with time; a time-only button reveals wheels |
| Wheels | Scrolling value wheels with built-in or hardware keyboard entry |
| Automatic | The system chooses for the platform and mode |

Modes are date (month/day/year), time (hour/minute and optional AM/PM), date with time, and countdown (hours/minutes, maximum 23 hours 59 minutes). Countdown is unavailable with inline and compact styles. The exact ordering follows device location. Compact is useful for tight space and permits multiple date/time edits before tapping outside to confirm.

<a id="macOS"></a>
### macOS

A textual picker saves space and supports precise entry. A graphical picker suits calendar browsing, date-range selection, or a clock-face presentation.

<a id="tvOS"></a>
### tvOS

SwiftUI Picker provides picker support.

<a id="watchOS"></a>
### watchOS

The Digital Crown enables precise movement through choices. Wheel styles support ordinary values and dates/times; configure outlines, captions, and scroll indicators as needed. For longer lists, a navigation-link picker displays a button that opens the list, and also allows crown scrubbing without opening it.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Pull-down buttons](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons)
[Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/Picker> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UIDatePicker> — UIKit
<https://developer.apple.com/documentation/UIKit/UIPickerView> — UIKit
<https://developer.apple.com/documentation/AppKit/NSDatePicker> — AppKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 5, 2023.
