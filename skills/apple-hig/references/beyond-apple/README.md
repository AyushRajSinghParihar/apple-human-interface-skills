# Apple design guidance outside Apple platforms

**Not from Apple HIG.** This file is original guidance of this package. It tells
you how to apply the HIG procedures to a product that runs on the web, Android
or Windows. A fact from a host platform links its source; a statement without a
link is this package's own advice. Check the current host documentation before
you depend on a detail.

Use this file when the product, or one build of it, runs outside Apple platforms:
a web app, an Android app, a Windows app, or a React Native, Flutter, Electron,
.NET MAUI or Kotlin Multiplatform build for these platforms.

## Procedure

1. Find the host platform of each build. For a cross-platform app, use the Apple
   procedures for the Apple builds and this file for the other builds.
2. Find the HIG topic of each decision in the [topic index](../topic-index.md),
   and read its procedure for the decision itself.
3. Map each Apple control to its host equivalent with [web](web.md),
   [Android](android.md) or [Windows](windows.md).
4. Apply the conflict rule below to each difference.
5. Check the result with the host's own accessibility tools and standards.

## Conflict rule

Apple's principles control these areas, because they do not depend on the
platform:

- clarity of hierarchy and content, and the purpose of each screen
- feedback, progress and error recovery
- when to interrupt (modality), and how to protect unsaved work
- writing: specific labels, plain language, no blame
- accessibility: text that grows, meaning that does not depend on color alone,
  a name for each control, simple alternatives to complex gestures

The host convention wins where people depend on the platform's behavior:

- system back navigation and browser history
- the order and placement of dialog buttons
- keyboard modifiers and shortcuts of the person's system (Ctrl on Windows; on
  the web, Command on a Mac and Ctrl on other systems)
- window controls, title bars and system menus
- the system font, the system share sheet, notifications and settings screens
- the host's minimum target size and its accessibility APIs

If the user asks for an Apple look on every platform, apply it. Then list each
conflict with the host convention and its cost to the people who use the product.

## Topics that do not transfer

- **Apple-only system features:** CarPlay, Digital Crown, complications, watch
  faces, Activity rings, Always On, Top Shelf, Action button, Camera Control,
  Apple Pencil and Scribble, Siri, App Shortcuts, Live Activities, widgets on
  Apple surfaces, App Clips, iMessage apps, Game Center, HealthKit, CareKit,
  ResearchKit, HomeKit, iCloud, SharePlay, ID Verifier, Tap to Pay on iPhone,
  and the visionOS spatial topics. Use only their general
  lessons, for example about glanceable content or privacy.
- **Partly portable:** Apple Pay and Sign in with Apple also work on the web, and
  a website can add passes to Apple Wallet (see the Wallet guide). ShazamKit also
  has an SDK for Android ([ShazamKit](https://developer.apple.com/shazamkit/)).
  When you use these, follow their HIG procedures for the button, the wording
  and the flow.
- **All other topics** transfer as principles. Apply the decision of the
  procedure, then use the host control.

## Licence limits

- Do not bundle SF Pro, SF Compact or SF Mono in a product for another
  platform. Apple's font licence permits the San Francisco fonts only "for
  creating mock-ups of user interfaces to be used in software products running
  on Apple's" operating systems, and it does not permit embedding
  ([Apple Fonts](https://developer.apple.com/fonts/)). Use the host system font.
- This package found no permission to use New York or SF Symbols outside Apple
  platforms. Check their licences before any use, or use a font and an icon set
  with a suitable licence.
- Use Apple trademarks and badges, for example the Apple Pay button, only as
  Apple's own guidelines for them permit.

## Units and sizes

As a starting point, this package treats 1 pt (Apple) as about 1 CSS px, 1 dp
(Android) and 1 effective pixel (Windows) at standard zoom. Then use the host's
own minimum, not Apple's.

| Item | Apple (iOS) | Web | Android | Windows |
|---|---|---|---|---|
| Control or target size | 44 × 44 pt default, 28 × 28 pt minimum ([Accessibility](../../subskills/apple-hig-foundations/references/accessibility.md)) | 24 × 24 CSS px minimum, WCAG 2.2 SC 2.5.8 ([W3C](https://www.w3.org/TR/WCAG22/#target-size-minimum)) | at least 48 × 48 dp ([Android](https://developer.android.com/guide/topics/ui/accessibility/apps)) | about 7.5 mm, 40 × 40 px at 1.0x ([Microsoft](https://learn.microsoft.com/en-us/windows/apps/design/input/guidelines-for-targeting)) |
| Body text | 17 pt default, 11 pt minimum | relative units (`rem`) that follow the browser text size | `sp` units that follow the font scale | the system text-size setting |
| Text contrast | see [Color](../../subskills/apple-hig-foundations/references/color.md) and [Accessibility](../../subskills/apple-hig-foundations/references/accessibility.md) | 4.5:1, or 3:1 for large text, WCAG SC 1.4.3 ([W3C](https://www.w3.org/TR/WCAG22/#contrast-minimum)) | 4.5:1 below 18sp (14sp bold), else 3:1 ([Android](https://developer.android.com/guide/topics/ui/accessibility/apps)) | use the system contrast themes |

## Accessibility map

| Apple | Web | Android | Windows |
|---|---|---|---|
| VoiceOver | screen readers with semantic HTML and ARIA | TalkBack, `contentDescription`, `Role` semantics | Narrator, UI Automation names |
| Dynamic Type | browser text size and zoom to 200%, WCAG SC 1.4.4 | font scale with `sp` | system text size |
| Reduce Motion | `prefers-reduced-motion` media query | the system animation settings | the system animation effects setting |
| Dark Mode | `prefers-color-scheme` media query | dark theme | light and dark app themes |
