Use a standard visionOS confirmation alert with this specification:

| Element | Corrected specification |
|---|---|
| Title | **Delete “[Album Name]”?** |
| Message | Briefly explain the actual consequences, including the effect on other participants and whether deletion can be undone. |
| Thumbnail accessory | Include only if it helps identify the album. Maximum height **154 pt**, with a **16 pt corner radius**. |
| Shared Space placement | Present in front of the album window, slightly forward along the z-axis. Keep the alert anchored to the window when it moves. |
| Full Space placement | Present centered in the wearer’s field of view. |
| Buttons | **Delete Album**, using the destructive role, and **Cancel**, using the cancel role. Cancel dismisses without deleting. |

These dimensions and placement behaviors follow [Apple’s alert guidelines](https://developer.apple.com/design/human-interface-guidelines/alerts).