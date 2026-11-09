Keep React and web conventions. Apple’s clarity comes from hierarchy, readable labels, predictable behavior, and accessible controls—not proprietary assets.

Based on your description, make these changes in priority order. The principles below come from HIG; the HTML and interaction choices are web recommendations.

1. **Replace the mouse-only toggle.** This blocks keyboard users from changing settings. Use a native `<input type="checkbox">` with an associated `<label>`; add `role="switch"` when presenting it as an on/off switch. Style it without removing keyboard focusability. Tab must reach it, Space must toggle it, and focus must remain visible. Show state through thumb position or a checkmark as well as color. This follows HIG’s [accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) and [toggle](https://developer.apple.com/design/human-interface-guidelines/toggles) principles.

2. **Prevent silent loss of changes.** For independent preferences, I recommend saving each change automatically. Show “Saving…,” then “Saved” only after persistence succeeds. On failure, retain the attempted value and show an actionable error with Retry. This is a product recommendation, not a universal HIG requirement.
   
   If changes require a deliberate batch commit, retain Save but put **Save changes** and **Cancel** in a consistently accessible action area. For unsaved changes, intercept in-app navigation with **Save changes**, **Discard changes**, and **Keep editing**. Use the browser’s `beforeunload` warning for reload/close as a fallback; it is not reliable enough to be the sole protection. HIG’s relevant principle is [protecting work before dismissal](https://developer.apple.com/design/human-interface-guidelines/modality).

3. **Give every text input a persistent visible label.** Disappearing placeholders make populated fields ambiguous. Place a `<label htmlFor="…">` above each input and match its `id`. Reserve placeholders for examples, such as `name@example.com`. Connect help and errors with `aria-describedby`. Use readable text colors; grey alone does not prove a contrast failure, so measure the actual colors. Sources: [HIG text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields), [WCAG labels or instructions](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html).

4. **Organize the 30 settings into meaningful sections.** A flat list makes people scan everything to find one preference. Start with categories such as **Account**, **Notifications**, **Privacy**, and **Appearance**, adjusted to your actual inventory. Use an `h1` for Settings, `h2` headings for sections, and `<fieldset>`/`<legend>` for related control groups. Give each row a clear label and add supporting text only when its consequences need explanation. Keep frequently used task controls near the task itself. Group names and count are design recommendations; HIG supports [keeping settings focused and placing options according to scope](https://developer.apple.com/design/human-interface-guidelines/settings).

5. **Remove the proposal to bundle SF Pro and SF Symbols.** Apple’s downloadable fonts are not a general webfont licence; do not self-host SF Pro for this site. Use:
   
   ```css
   font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
   ```
   
   This uses the device’s installed system font without distributing Apple’s font files. SF Symbols also has platform and usage restrictions; use a web-licensed icon set such as Lucide instead. See [Apple Fonts](https://developer.apple.com/fonts/) and [SF Symbols](https://developer.apple.com/sf-symbols/) for their licence terms.

Before release, verify the entire flow by keyboard and screen reader, confirm saved values survive reload, simulate save failures, and check 200% text enlargement without clipping. Measure text contrast against WCAG AA requirements.

The keyboard barrier, disappearing labels, and silent data loss are established by your description. Runtime accessibility, contrast, and persistence checks remain **not done** because no implementation was supplied.