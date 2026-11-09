Keep the React implementation, but adopt Apple’s clarity, hierarchy, and predictable feedback. Here’s what to change:

| Current issue | Exact change |
|---|---|
| **30 toggles in one list** | Divide them into meaningful sections such as **Account**, **Notifications**, **Privacy**, and **Appearance**. Give each section a visible heading and group related settings together. Put frequently used settings first; move advanced settings to a separate section or page. |
| **Labels disappear when typing** | Give every field a persistent, visible label. In React, connect `<label htmlFor="…">` to the input’s `id`. Use placeholders only for optional examples, and place instructions beneath the field. Use readable text contrast: at least **4.5:1** for normal-sized text. |
| **Save is distant and leaving silently discards edits** | Prefer **automatic saving for independent, reversible settings**. Show saving, success, and failure feedback, and preserve the person’s input if saving fails. For changes that need explicit submission, use a clearly visible Save/Cancel action area, show when changes are unsaved, and warn before navigation would discard them. |
| **Mouse-only custom toggle** | Replace the clickable `<div>` with a native checkbox styled as a switch, or an accessible switch component. It needs an accessible name, checked state, visible keyboard focus, and **Tab + Space** support. Make the label clickable and provide a generous hit area—ideally **44 × 44 CSS pixels**. |
| **Bundled SF Pro and SF Symbols** | **Do not bundle Apple’s downloaded assets for a general-purpose website.** Their licenses restrict permitted uses; availability to download does not grant general web redistribution rights. Use a system font stack and an icon library licensed for web use, such as Lucide. Review the applicable Apple licenses before any exceptional use. |

For typography, use the visitor’s platform font without distributing font files:

```css
font-family: system-ui, -apple-system, BlinkMacSystemFont,
  "Segoe UI", sans-serif;
```

For each setting, use a consistent row: a clear label, optional short explanatory text, and the control. Avoid relying on color alone to communicate state.

Prioritize the inaccessible toggle, disappearing labels, and silent data loss first. Then improve grouping, spacing, and typography. The result should feel polished while following familiar web behavior.