# Apple design guidance in a web app

**Not from Apple HIG.** Read [the procedure](README.md) first. Check the linked
host sources before you depend on a detail.

## Map the controls

| HIG topic | Web equivalent | Keep from the HIG procedure |
|---|---|---|
| [Alerts](../../subskills/apple-hig-presentation/.topics/apple-hig-alerts/SKILL.md) | `<dialog>` that follows the [WAI-ARIA dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/): focus moves in, Escape closes, focus returns to the trigger | interrupt only for a real decision; specific button labels; never stack dialogs |
| [Sheets](../../subskills/apple-hig-presentation/.topics/apple-hig-sheets/SKILL.md), [Modality](../../subskills/apple-hig-patterns/.topics/apple-hig-modality/SKILL.md) | a modal `<dialog>` or a separate page with its own URL | one focused task; a clear exit; protect unsaved work, also when the person leaves the page |
| [Toggles](../../subskills/apple-hig-selection-and-input/.topics/apple-hig-toggles/SKILL.md) | `<input type="checkbox" role="switch">` with a `<label>` | the label says what the setting does; apply the change at once or with an explicit commit, as the procedure decides |
| [Text fields](../../subskills/apple-hig-selection-and-input/.topics/apple-hig-text-fields/SKILL.md) | `<input>` with a visible `<label>` ([WCAG SC 3.3.2](https://www.w3.org/TR/WCAG22/#labels-or-instructions)), `autocomplete` and `inputmode` | a clear hint of what to enter; clear errors next to the field |
| [Tab bars](../../subskills/apple-hig-navigation-and-search/.topics/apple-hig-tab-bars/SKILL.md), [Sidebars](../../subskills/apple-hig-navigation-and-search/.topics/apple-hig-sidebars/SKILL.md) | `<nav>` with links and `aria-current="page"` | few, stable top-level destinations |
| [Menus](../../subskills/apple-hig-menus-and-actions/.topics/apple-hig-menus/SKILL.md), [Action sheets](../../subskills/apple-hig-presentation/.topics/apple-hig-action-sheets/SKILL.md) | the [WAI-ARIA menu button pattern](https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/) or the `popover` attribute | short, grouped, specific commands |
| [Typography](../../subskills/apple-hig-foundations/.topics/apple-hig-typography/SKILL.md) | a `system-ui` font stack and `rem` units | hierarchy that stays clear when text grows |
| [Dark Mode](../../subskills/apple-hig-foundations/.topics/apple-hig-dark-mode/SKILL.md), [Motion](../../subskills/apple-hig-foundations/.topics/apple-hig-motion/SKILL.md) | `prefers-color-scheme` and `prefers-reduced-motion` | follow the person's system setting |

## The web convention wins

- The browser back button, the address bar and links must work. Each main view
  has its own URL.
- Use a link for navigation and a button for an action.
- Give each field a visible label. A placeholder alone disappears when the person
  types ([WCAG SC 3.3.2](https://www.w3.org/TR/WCAG22/#labels-or-instructions)).
- Support the keyboard: Tab, Shift-Tab, Enter, Space and Escape. Keep a visible
  focus indicator ([WCAG SC 2.4.7](https://www.w3.org/TR/WCAG22/#focus-visible)).
- Do not block text selection, the browser context menu or browser zoom.
- Do not copy iOS controls pixel for pixel. A web form that looks like an iPhone
  screen feels wrong in a desktop browser.

## Checks

- Do the full task with the keyboard only.
- Do the task with a screen reader (for example VoiceOver on macOS or NVDA on
  Windows).
- Zoom the text to 200% ([WCAG SC 1.4.4](https://www.w3.org/TR/WCAG22/#resize-text)): no content
  or function is lost.
- Turn on reduced motion and dark appearance in the operating system.
- Measure text contrast ([WCAG SC 1.4.3](https://www.w3.org/TR/WCAG22/#contrast-minimum)) and target size
  ([WCAG SC 2.5.8](https://www.w3.org/TR/WCAG22/#target-size-minimum)).
