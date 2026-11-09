Keep React. Apply Apple’s principles of clear hierarchy, persistent meaning, and predictable behavior, with standard web semantics. Based on your description, make these five changes:

1. **Group the 30 settings by purpose.**  
   The flat list makes people scan everything to find one option. Introduce named sections such as Notifications, Privacy, and Appearance, based on your actual inventory. Use an `<h1>` for Settings, `<h2>` section headings, and `<fieldset>`/`<legend>` for related controls. Put common settings first; move frequent task-specific options beside the task they affect. These grouping choices are my proposed web adaptation of [Apple’s settings guidance](https://developer.apple.com/design/human-interface-guidelines/settings).

2. **Give every input a permanent visible label.**  
   Disappearing placeholders remove context while people type or review values. Use `<label htmlFor="…">` connected to the input’s `id`. Reserve placeholders for optional examples, and connect helper text with `aria-describedby`. Keep toggle labels stable and specific, such as “Email notifications.” Grey text is not automatically a contrast failure, but your actual colors need measurement. See [Apple’s text-field guidance](https://developer.apple.com/design/human-interface-guidelines/text-fields).

3. **Fix silent data loss before visual polish.**  
   My recommendation: save independent, reversible settings immediately. Show “Saving…” and only show “Saved” after the server confirms. On failure, explain the error beside the setting and provide Retry; clearly distinguish an unsaved value from an applied one.

   If settings must be committed together, retain explicit saving: use a persistent action bar with **Save changes**, **Cancel**, and an unsaved indicator. Guard in-app navigation while dirty and add a browser unload warning as a fallback; browser warnings cannot guarantee preservation. Apple’s [toggle guidance](https://developer.apple.com/design/human-interface-guidelines/toggles) supports truthful state representation; this particular saving model is a product recommendation, not a universal HIG requirement.

4. **Replace the clickable `div` with a native control.**  
   This is a functional accessibility blocker. Use `<input type="checkbox">`; add `role="switch"` when its meaning and appearance are on/off. Bind React’s `checked` and `onChange`, associate a visible label, and preserve a visible `:focus-visible` outline. Tab must reach it, Space must toggle it, and assistive technology must announce its name and state. Styling must preserve focusability; do not hide the input with `display: none`. See the [W3C switch pattern](https://www.w3.org/WAI/ARIA/apg/patterns/switch/).

5. **Remove downloaded SF Pro and SF Symbols from the web bundle plan.**  
   Apple’s published font license does not grant general website embedding, and its system-image license restricts use to specified Apple-platform applications. Use this system-font stack instead:

   ```css
   font-family: system-ui, -apple-system, BlinkMacSystemFont,
                "Segoe UI", sans-serif;
   ```

   This uses fonts supplied by the visitor’s device without distributing Apple’s files. Use independently licensed web icons or original SVGs. Sources: [Apple font license](https://developer.apple.com/fonts/) and [Xcode agreement, §2.10](https://www.apple.com/legal/sla/docs/xcode.pdf).

**Review status:** Your description establishes failures in organization, persistent labels, change preservation, and keyboard access. No runtime checks passed or were executed. Before release, verify keyboard-only completion, screen-reader names and states, failed saves, navigation with pending edits, reload persistence, contrast, and usable layout at 200% zoom.