# CareKit

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/carekit) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

CareKit supports care plans for chronic conditions, recovery, and wellness. CareKit 2.0 separates customizable task/chart/contact UI from an on-device Store of patients, plans, tasks, and contacts, with synchronized UI updates.

<a id="Data-and-privacy"></a>
## Data and privacy
Protect both entered and device-sourced sensitive information, obtain appropriate permissions, and provide a clear App Store privacy-policy URL.

<a id="HealthKit-integration"></a>
### HealthKit integration
Request relevant health data in the feature’s context, accounting for changed permissions whenever access is needed. Add concise purpose/benefit explanations to standard authorization UI without duplicating it. Manage sharing through system privacy settings, including designated caregivers, rather than conflicting custom controls.

<a id="Motion-data"></a>
### Motion data
With permission and clinical relevance, use activity state, steps, pace, stair flights, or custom physical-therapy motion data. ResearchKit tasks can measure range, flexibility, and walking capability.

<a id="Photos"></a>
### Photos
Permission-based photos/camera can document treatment progress and share it with the care team, such as periodic injury images.

<a id="ResearchKit-integration"></a>
### ResearchKit integration
Appropriate surveys, tasks, and charts can complement care plans, and ResearchKit’s consent module can request permission to collect/share information.

<a id="CareKit-views"></a>
## CareKit views
Use each category for its intended role: tasks for prescribed actions and symptom/data logging, charts for progress, and contacts for communication/location. Views have a header with optional text/symbol/disclosure/separator and an optional vertical stack. Let framework constraints organize added subviews.

<a id="Tasks"></a>
### Tasks
Every task requires a short title and schedule; optional instructions convey detail/warnings, and an optional group ID organizes related tasks. Simple style suits one step with completion button/checkmark and no default content stack. Instructions adds explanatory text to a simple task. Log records events with timestamps. Checklist gives separate descriptive steps/completion controls and optional instructions. Grid compresses short-labeled steps into buttons, optionally with instructions/custom collection UI; choose checklist if each step needs detail. Use category colors only with another signal. Keep wording accurate and concise using familiar names, and demonstrate complex actions with images/video where helpful.

<a id="Charts"></a>
### Charts
Bar, scatter, and line styles use titles/subtitles, axis markers, and current/historical datasets with automatic updates. Highlight meaningful narratives/trends without clutter. Keep labels brief, place shared units on axes, distinguish datasets with high-contrast colors and legends where needed, and explicitly name time units. Consolidate large data and restructure/offset extreme ranges so small values remain perceivable.

<a id="Contact-views"></a>
### Contact views
Choose simple or detailed styles to connect patients with care teams/trusted contacts by phone, message, email, or map. Category colors can help identify roles when combined with labels.

<a id="Notifications"></a>
## Notifications
Use timely reminders sparingly and coalesce when a plan has many tasks. Badges can signal unread caregiver messages. A detail view can expose pending tasks and completion actions without leaving current context; Watch can also display notifications.

<a id="Symbols-and-branding"></a>
## Symbols and branding
Prefer CareKit’s recognizable phone/message/mail/clock symbols. Custom grid content can use SF Symbols or coordinated custom symbols with actual care meaning, avoiding corporate logos or decoration as functional icons. Express brand subtly through color and voice so the care plan remains central; do not turn care UI into advertising.

<a id="Platform-considerations"></a>
## Platform considerations
No extra iOS/iPadOS rules; macOS/tvOS/visionOS/watchOS are unsupported.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/carekit) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Videos"></a>
#### Videos
Apple’s linked design sessions provide demonstrations and additional implementation context; no video review is implied here.

<a id="Change-log"></a>
## Change log
Source revision dates: May 2, 2023.
