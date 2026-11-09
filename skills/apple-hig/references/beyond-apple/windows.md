# Apple design guidance in a Windows app

**Not from Apple HIG.** Read [the procedure](README.md) first. Check the linked
host sources before you depend on a detail.

## Map the controls

| HIG topic | Windows (WinUI) equivalent | Keep from the HIG procedure |
|---|---|---|
| [Alerts](../../subskills/apple-hig-presentation/.topics/apple-hig-alerts/SKILL.md) | `ContentDialog` | interrupt only for a real decision; specific button labels; explain the consequence |
| [Toolbars](../../subskills/apple-hig-menus-and-actions/.topics/apple-hig-toolbars/SKILL.md) | `CommandBar` | the few actions that matter most; prefer symbols, and use text where a symbol cannot explain the action |
| [The menu bar](../../subskills/apple-hig-menus-and-actions/.topics/apple-hig-the-menu-bar/SKILL.md), [Context menus](../../subskills/apple-hig-menus-and-actions/.topics/apple-hig-context-menus/SKILL.md) | `MenuBar`, `MenuFlyout` and right-click context menus | complete, discoverable commands with keyboard shortcuts |
| [Sidebars](../../subskills/apple-hig-navigation-and-search/.topics/apple-hig-sidebars/SKILL.md), [Tab bars](../../subskills/apple-hig-navigation-and-search/.topics/apple-hig-tab-bars/SKILL.md) | `NavigationView` with a left or top pane | few, stable top-level destinations |
| [Undo and redo](../../subskills/apple-hig-patterns/.topics/apple-hig-undo-and-redo/SKILL.md) | Ctrl+Z and Ctrl+Y with Edit menu commands | prefer undo to a confirmation for routine, reversible work |

## Dialog buttons

Microsoft's [dialog guidance](https://learn.microsoft.com/en-us/windows/apps/design/controls/dialogs-and-flyouts/dialogs)
differs from the macOS layout:

- The "do it" buttons (`PrimaryButton`, `SecondaryButton`) are at the left. The
  safe button (`CloseButton`, for example Cancel) is at the right.
- Escape, system back and Gamepad B select the close button.
- A default button is optional; by default, no button is the default.
- Only one `ContentDialog` can be open in a window at a time.
- Use specific labels, for example Delete and Cancel, not Yes and No.

So keep the Windows order. Apply the HIG decision about whether to interrupt, what
the text says and which button is safe.

## The Windows convention wins

- Keep the caption controls (minimize, maximize, close) anchored to the right of
  the title bar ([title bar guidance](https://learn.microsoft.com/en-us/windows/apps/design/basics/titlebar-design)).
- Use Ctrl for shortcuts and show them in menus and tooltips.
- Use the system font, Segoe UI Variable
  ([typography](https://learn.microsoft.com/en-us/windows/apps/design/signature-experiences/typography)),
  and the system text-size setting.
- Make touch targets about 7.5 mm, which is 40 × 40 pixels at 1.0x scale
  ([targeting guidance](https://learn.microsoft.com/en-us/windows/apps/design/input/guidelines-for-targeting)).

## Checks

- Do the full task with the keyboard only, and with Narrator.
- Set a larger system text size and a contrast theme: no text clips and no
  function is lost.
- Press Escape in each dialog: the safe action happens.
