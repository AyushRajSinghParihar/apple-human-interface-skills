Use a native visionOS confirmation alert with this specification:

| Element | Corrected specification |
|---|---|
| Title | **Delete “[Album Name]”?** |
| Message | Briefly explain the actual consequences for participants and photos, including whether deletion can be undone. |
| Thumbnail accessory | Maximum **154 pt tall**, with a **16 pt corner radius**. |
| Shared Space | Present slightly in front of the album’s parent window. Keep the alert attached as the window moves. |
| Full Space | Present centered in the person’s field of view. |
| Buttons | **Delete Album** and **Cancel**. Delete Album commits deletion; Cancel dismisses without changes. |

Because this confirms an explicitly requested deletion, **Delete Album may be the normal default action**, allowing Return to confirm. If deliberate reading is necessary, use no default. Don’t make Cancel the default. Support Escape and Command-Period to cancel when a keyboard is attached.

These corrections follow [Apple’s Alerts guidance](https://developer.apple.com/design/human-interface-guidelines/alerts). The consequence message needs to match your app’s deletion behavior; runtime presentation and keyboard behavior remain untested.