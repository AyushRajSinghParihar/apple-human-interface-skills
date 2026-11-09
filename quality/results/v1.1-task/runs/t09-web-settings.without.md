Keep the clarity of Apple’s settings design, while using standard web patterns. I’d make these five changes:

| Current issue | Exactly what to change |
|---|---|
| **30 toggles in one list** | Group settings into clearly named sections, such as **Account**, **Notifications**, **Privacy**, and **Appearance**. Use headings and short descriptions where needed. Put common settings first; move rarely used or advanced options into expandable sections or separate pages. |
| **Labels disappear during typing** | Give every control a persistent, visible label. For text fields, put the label above or beside the input and connect it with `<label htmlFor="…">`. Use placeholders only for optional examples. Make label text readable with sufficient contrast; associate help text using `aria-describedby`. |
| **Save button at the bottom; silent loss of edits** | Prefer saving independent toggles immediately, with a clear saving/error state and a way to retry if saving fails. For settings that need to be submitted together, use an explicit Save flow with a readily visible action bar, mark unsaved changes, and warn before navigation would discard them. Don’t report success until the save succeeds. |
| **Mouse-only custom toggle** | Replace the clickable `<div>` with a native `<input type="checkbox">`, styled as a switch if desired. Give it an associated label, a visible keyboard focus indicator, and a comfortably sized clickable label area. Verify that **Tab** reaches it, **Space** changes it, and a screen reader announces its name and state. Don’t communicate its state through color alone. |
| **Bundling SF Pro and SF Symbols** | **Don’t bundle Apple’s downloads into the website without a license that explicitly permits that use.** Apple’s downloadable font and symbol assets have usage restrictions; downloading them doesn’t grant general web redistribution rights. Use a system font stack and a web-licensed icon set such as Lucide, checking its license. |

For typography, use the visitor’s existing system font:

```css
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif;
}
```

This lets Apple devices use their installed system font without shipping Apple’s font files.

Before release, verify the entire page using only a keyboard, check accessible names and contrast, and test failed saves and navigation with unsaved edits. Those checks address the biggest usability risks here.