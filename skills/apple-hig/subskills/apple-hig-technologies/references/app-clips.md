# App Clips

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/app-clips) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

An App Clip is a temporary, small native experience for an immediate finite task or a meaningful app/game demo without full installation. Discovery includes App Clip Codes, NFC/QR, permitted Siri location suggestions, Maps, website banners/cards, shared Messages links, and, since iOS 17, another app’s links/previews.

<a id="Designing-your-App-Clip"></a>
## Designing your App Clip
Let people finish the whole task/demo/level without installing. Include only essentials, with a short linear flow, few screens/forms, and no complex tabs/settings. Do not use it as advertising or show ads. Prefer native frameworks; a web-only experience should be a website link instead. Launch directly into relevant context without a splash, waiting, missing required assets, or avoidable downloads. Remove unused code/assets to keep startup fast under poor bandwidth. Support deep-link sharing, Apple Pay for quick checkout, and guest use; if identity is indispensable, minimize data with Sign in with Apple. After the full app replaces the Clip, invocations should open the familiar focused context without repeat login or extra steps.

<a id="Preserving-privacy"></a>
### Preserving privacy
App Clips cannot do background operations and may be deleted with all local data between uses. Minimize handled/stored information and securely retain required credentials off-device rather than relying on Clip storage. Sign in with Apple and Apple Pay can reduce privacy-sensitive handling.

<a id="Showcasing-your-app"></a>
### Showcasing your app
Clips do not live on Home Screen and the system removes inactive ones. Card and first-launch banner already link to the full app. If more promotion is useful, use SKOverlay after task completion or a natural pause, letting demo players experience the full demo first. Explain added value politely without repeated interruption or promotional push notifications.

<a id="Limiting-notifications"></a>
### Limiting notifications
Default limited notification scheduling/receipt lasts up to 8 hours after launch. Explicitly request extended permission only when the task truly needs it, such as a multiday rental. Send only task-related notifications responding to explicit action, never pure promotion; a task completed entirely inside the Clip may need none.

<a id="Creating-App-Clips-for-businesses"></a>
### Creating App Clips for businesses
A platform provider can configure many business/location experiences under one Clip. Match the business’s card branding inside the experience and subdue provider branding. Handle simultaneous use of several businesses/locations, verify launch context, and consider switching among recent locations.

<a id="Creating-content-for-an-App-Clip-card"></a>
## Creating content for an App Clip card
Choose imagery explaining the task, content, or location rather than a UI screenshot. Prefer photos/graphics without embedded unlocalizable text. Header art must be opaque PNG/JPEG, 1800 × 1200 px. Title maximum is 30 characters; subtitle maximum 56. Choose View for informational/media/educational Clips, Play for games, and Open otherwise.

<a id="App-Clip-Codes"></a>
## App Clip Codes
Use Apple-generated codes from App Store Connect or the command-line generator. A badge includes the App Clip logo below the code; a code-only option fits constrained contexts. Default/custom foreground/background pairs generate a third coordinated color.

<a id="Interacting-with-App-Clip-Codes"></a>
### Interacting with App Clip Codes
Scan-only codes have a camera center glyph and work with Camera or Control Center Code Scanner. NFC-integrated codes have an iPhone glyph and work by nearby holding/NFC Tag Reader or ordinary camera scanning.

<a id="Displaying-App-Clip-Codes"></a>
### Displaying App Clip Codes
Choose NFC-integrated when physically reachable, such as a table/register/card, and scan-only for distant signs or digital/email/social content. Include the logo badge if clear space permits; omit it for disposable paper/plastic and gambling/drinking-associated objects. Never use the logo alone.

Use flat or cylindrical surfaces only; on a cylinder the code width must not exceed one sixth of its circumference. Keep codes rigid, flat, well-adhered, lit, upright, unobstructed, undimmed, and unanimated, without extreme scanning angles. Attach a rigid card to flexible packaging rather than printing directly on crumpling material.

|Medium|Minimum|
|---|---|
|Print|0.75 in diameter (1.9 cm)|
|Digital PNG/SVG|256 × 256 px|
|Embedded NFC tag|35 mm diameter or equivalent; a matching code is at least 1.37 in / 3.48 cm|

Keep distance:diameter at most 20:1, preferably 10:1; at 40 in / 101 cm distance, prefer at least 4 in / 10.16 cm diameter. A code beside QR/other scannable content should be no smaller than that neighbor. Clear space must at least equal the gap between the center glyph and circular code; allow separate reliable targeting of adjacent codes.

<a id="Using-clear-messaging"></a>
### Using clear messaging
Place a short action explaining what scanning enables, especially without the logo. For scan-only, identify Camera on iPhone/iPad when useful; for NFC, explain holding iPhone near the named object. Avoid implying contact. Use App Clip/App Clip Code capitalization and Apple trademark rules.

<a id="Customizing-your-App-Clip-Code"></a>
### Customizing your App Clip Code
Do not redraw, filter, recolor after generation, add effects, distort proportions, or scale strokes independently. Choose sufficiently contrasting colors through the generator, which rejects unsafe pairs and can suggest a compatible foreground. Preserve the generated three-color relationship.

<a id="Printing-guidelines"></a>
## Printing guidelines
Test printed codes at multiple angles before distribution. Use high-quality untextured matte material/lamination, avoiding shiny, reflective, holographic, or thin laminate finishes. For outdoors use UV/weather-resistant materials/coatings. The source favors flexographic professional printing or inkjet desktop printing. Rasterize at least 600 ppi and print at least 300 dpi; calibrate for alignment, gamma, artifacts, and circular geometry. Use receipt paper’s available width.

Convert generated sRGB SVG to CMYK with media-relative colorimetric intent: Generic CMYK ICC for CMYK printers, Gracol 2013 ICC for CMYKOV, with CIELab Delta E tolerance 2.5. Generate grayscale codes for grayscale-only printers instead of converting colored ones. Use Type 5 NFC tags at least 35 mm or equivalent. Pilot large runs, track each SVG’s invocation URL/filename with version/change control, and print validation identifiers outside the code’s padded region.

<a id="Verifying-your-printers-calibration"></a>
### Verifying your printer’s calibration
Use Apple’s color-pair calibration sheet at its intended scale to verify the chosen pair. Use the two-grayscale-bar sheet to check gray levels; missing or overly light tones indicate calibration trouble or an unsuitable printer.

<a id="Legal-requirements"></a>
## Legal requirements
Use only approved generated designs following these rules and only for an active App Clip; remove codes when the Clip becomes inactive. Apple can revise the design and retains all rights. Do not register or incorporate code/mark/logo elements into company/product names or claim ownership. Avoid misleading source, damaging reputation/goodwill, or infringing others’ rights. Do not add symbols. Keep Apple trademarks untranslated; Apple-approved translations may apply to legal credit text, not the marks.

<a id="Platform-considerations"></a>
## Platform considerations
No extra iOS/iPadOS rules; macOS/tvOS/visionOS/watchOS are unsupported.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/app-clips) for linked Apple design assets and implementation resources.

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
Source revision dates: June 9, 2025, May 2, 2023.
