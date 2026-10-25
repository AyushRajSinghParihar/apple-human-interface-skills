# Siri

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/siri) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Siri supports information and quick actions through voice and system entry points, including the Siri app and Dynamic Island interactions. On supported devices, Siri AI uses Apple Intelligence for natural-language/contextual actions across apps and onscreen content.

<a id="Getting-your-app-to-work-with-Siri"></a>
## Getting your app to work with Siri
Expose app actions as intents and content as entities through App Intents; the system otherwise lacks specific awareness of the app’s capabilities. Siri, Spotlight, and Shortcuts can then surface appropriate actions/content. Adopt existing domain schemas, such as email/music/photos, to use built-in natural-language and contextual logic.

<a id="Sharing-contextual-information"></a>
### Sharing contextual information
Annotate views/content with app entities so Siri understands references to onscreen objects. Donate relevant entities to the on-device Spotlight index for search and Siri. Donate actual user actions/interests as intents to inform appropriate future suggestions.

<a id="Best-practices"></a>
## Best practices
Prioritize popular actions and the device/location/hands-free contexts where people need them. Use the audience’s familiar nouns and verbs. Index personally relevant content such as favorites, searches, bookmarks, and wishlists instead of indiscriminately donating everything; whole catalogs can be justified for email/messages. Keep advertisements, marketing, and purchase pitches out of Siri-delivered content. Prefer built-in responses unless they cannot meet the need.

<a id="Customizing-your-apps-experience-with-Siri"></a>
## Customizing your app’s experience with Siri
Use App Shortcuts for custom functions beyond existing schema domains. Optional intent/entity properties can improve schema responses with static or interactive snippets, such as playback controls. The system may omit optional visual properties in some contexts, so essential information cannot depend on their appearance.

Write clear, brief response dialogue and specific follow-up questions that identify the object being requested. Remove repeated detail and humor that become irritating. Provide both audible and visual forms; spoken output must stand alone. Avoid unnecessary gender assumptions, use open-ended narrowing when options are too numerous to read, and keep wording device-independent unless a specific device is verified. Omit the app name because the system supplies attribution. Respect parental controls, avoid offensive speech, and remember bystanders can hear responses. Replace generic failures with a precise explanation of the current problem.

<a id="Editorial-guidelines"></a>
## Editorial guidelines
Call Siri by name rather than gendered pronouns. Do not impersonate Siri or Apple, reproduce reserved system behavior, or claim reserved phrases such as emergency calls. Siri remains untranslated; only the greeting in the invocation localizes. The source’s approved groupings are:

|Locales|Invocation|
|---|---|
|ar_AE, ar_SA|يا Siri|
|da_DK, sv_SE|Hej Siri|
|de_AT, de_CH, de_DE; en_AU, en_CA, en_GB, en_IE, en_IN, en_NZ, en_SG, en_US, en_ZA; ja_JP, tr_TR|Hey Siri|
|es_CL, es_ES, es_MX, es_US|Oye Siri|
|fi_FI, nb_NO, no_NO|Hei Siri|
|fr_BE, fr_CA, fr_CH, fr_FR|Dis Siri|
|it_CH, it_IT|Ehi Siri|
|ko_KR|Siri야|
|ms_MY|Hai Siri|
|nl_BE|Hé, Siri|
|nl_NL|Hé Siri|
|pt_BR|E aí Siri|
|ru_RU|привет Siri|
|th_TH|หวัดดี Siri|
|zh_CN|嘿Siri|
|zh_HK|喂 Siri|
|zh_TW|嘿 Siri|

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/siri) for linked Apple design assets and implementation resources.

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
Source revision dates: June 8, 2026, June 5, 2023, May 2, 2023.
