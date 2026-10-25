# App Shortcuts

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/app-shortcuts)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

App Shortcuts expose important app actions and content through Siri, Spotlight, Shortcuts, the Action button, and Apple Pencil squeeze. They arrive with installation and can become personalized after use. App Intents define the actions, and each shortcut can combine steps into one task. An app can supply up to 10 App Shortcuts; people can also compose their own cross-app shortcuts from its intents.

<a id="Best-practices"></a>
## Best practices

Use app schemas for common domains when they can make content/actions discoverable to Apple Intelligence; App Shortcuts remain useful for distinctive features or content outside schemas. Favor common important tasks that finish in the current context, opening the app for more involved work when helpful. An App Shortcut can expose one optional parameter with predictable familiar options. If omitted, clarify with a likely default and a short alternative set. Keep spoken phrases simple rather than implying several parameters; ask for further required details in later steps. Teach availability with occasional contextual tips during relevant actions.

<a id="Responding-to-App-Shortcuts"></a>
### Responding to App Shortcuts

Use snippets for static results or confirmation options, and Live Activities for evolving progress such as a countdown. Spoken full dialogue must include all essential information for audio-only devices, including AirPods and HomePod.

<a id="Editorial-guidelines"></a>
## Editorial guidelines

Create brief memorable activation phrases with natural variants and the app name. Use title case and plural Shortcuts for App Shortcuts and the Shortcuts app. Use lowercase shortcut for an individual generic shortcut.

<a id="Platform-considerations"></a>
## Platform considerations

No additional visionOS or watchOS rules are specified. App Shortcuts are unsupported in tvOS.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Shortcuts can appear with an app's Spotlight Top Hit or below in the Shortcuts area. Supply an appropriate SF Symbol or linked-content preview. Put broadly useful tasks first initially; the system later prioritizes frequent use.

<a id="macOS"></a>
### macOS

App Shortcuts themselves are unsupported. App Intents actions remain available for people building custom shortcuts in the Mac Shortcuts app.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Siri](https://developer.apple.com/design/human-interface-guidelines/siri)
[Siri Style Guide](https://developer.apple.com/siri/style-guide/)
[Shortcuts User Guide](https://support.apple.com/guide/shortcuts/welcome/ios)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/AppIntents>
<https://developer.apple.com/documentation/SiriKit>
<https://developer.apple.com/documentation/AppIntents/getting-started-with-the-app-intents-framework> — App Intents
<https://developer.apple.com/documentation/AppIntents/defining-app-entities-for-your-custom-data-types> — App Intents

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2026/310>
  <https://developer.apple.com/videos/play/wwdc2025/281>
  <https://developer.apple.com/videos/play/wwdc2025/244>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: June 8, 2026, January 17, 2025, June 5, 2023.
