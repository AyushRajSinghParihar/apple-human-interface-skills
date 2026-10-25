# Sign in with Apple

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Sign in with Apple authenticates or registers using an existing Apple Account, system biometrics, and built-in two-factor protection across Apple/non-Apple apps and websites. A person can share a private relay email. Apple does not use the service to profile app activity.

<a id="Offering-Sign-in-with-Apple"></a>
## Offering Sign in with Apple
Explain the actual value of signing in and defer it until necessary. If a separate app account is required, explain/setup that account before offering its sign-in methods. Support linking an existing account, for example after matching the voluntarily shared address or through account settings. Commerce should prefer guest purchase and optional registration afterward without reasking name/email already supplied to Apple Pay. Welcome successful sign-in immediately and indicate the current authentication method in account/settings.

<a id="Collecting-data"></a>
## Collecting data
Minimize extra requests and distinguish legally/contractually required fields from optional beneficial ones. Never demand an extra password while the person uses Sign in with Apple. Respect relay-email choice instead of asking for the underlying address; show the relay address for support or use an order/phone identifier where appropriate. The source also gives Settings > Apple Account > Password & Security > Apps using Apple Account as a route for retrieving the private relay address. Ask optional information after useful engagement and do not block account/features when declined. Display how collected data is used so requests are understandable.

<a id="Displaying-buttons"></a>
## Displaying buttons
Make the option at least as prominent/large as other sign-in methods and visible without scrolling.

<a id="Using-the-system-provided-buttons"></a>
### Using the system-provided buttons
Prefer APIs for approved proportional/localized appearance, VoiceOver, and supported corner adjustment. Available titles include Sign in with Apple, Sign up with Apple, and Continue with Apple; use one suitable terminology consistently. Watch has the shorter Apple-logo Sign in title.

<a id="White"></a>
#### White
Available across platforms/web; suits dark backgrounds with sufficient contrast.

<a id="White-with-outline"></a>
#### White with outline
Available on iOS/macOS/web for light backgrounds that need definition. Avoid dark/saturated backgrounds.

<a id="Black"></a>
#### Black
Available across platforms/web for light backgrounds. Watch uses a dark-gray fill rather than pure black to remain distinct from the display.

<a id="Button-size-and-corner-radius"></a>
#### Button size and corner radius
On iOS/macOS/web, adjust corners to match neighboring buttons, including square/capsule shapes. Minimum size is 140 × 30 pt (140 × 30 px @1x or 280 × 60 px @2x), with clear margin at least one tenth of height; account for localized text length.

<a id="Creating-a-custom-Sign-in-with-Apple-button"></a>
### Creating a custom Sign in with Apple button
Custom designs for iOS/macOS/web are subject to App Review and must remain instantly recognizable. Use only Apple-supplied padded PNG/SVG/PDF logo art, black or white, matching file height to button height without cropping or added vertical padding. The logo itself is not the whole button. Text variants must remain rectangular; logo-only can be circular/rectangular. Use approved titles and only black or white logo/title. Font, weight, size, uppercase to match an all-caps design, overall black/white background with subtle texture/gradient, corners, bezel, and shadow may be adapted within guidelines.

<a id="Custom-buttons-with-a-logo-and-text"></a>
#### Custom buttons with a logo and text
SVG/PDF scale to any height; PNG is for 44 pt-high buttons. Choose small/medium/large logo assets to align with other sign-in logos. Prefer system type with title size approximately 43% of button height (button about 233% of type size). Preserve normal capitalization unless the interface is all caps. Center the title vertically and use the full-height padded logo file. Horizontal leading inset can align authentication logos; preserve at least 8% of button width between title and trailing edge. Keep 140 × 30 pt minimum size and one-tenth-height outside margins.

<a id="Custom-logo-only-buttons"></a>
#### Custom logo-only buttons
Use SVG/PDF at any size or PNG only at 44 × 44 pt. Keep the 1:1 ratio and built-in padding with no added horizontal/vertical padding or cropping. Mask the complete art to circle/rounded rectangle if needed. Keep clear space at least one tenth of height.

<a id="Platform-considerations"></a>
## Platform considerations
No extra platform-specific rules are provided.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple) for linked Apple design assets and implementation resources.

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
Source revision dates: September 14, 2022.
