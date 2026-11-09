# Apple design guidance in an Android app

**Not from Apple HIG.** Read [the procedure](README.md) first. Check the linked
host sources before you depend on a detail.

## Map the controls

Use the [Material 3 components](https://m3.material.io/components) for the host
controls. Keep the decision of the HIG procedure.

| HIG topic | Android equivalent | Keep from the HIG procedure |
|---|---|---|
| [Alerts](../../subskills/apple-hig-presentation/.topics/apple-hig-alerts/SKILL.md) | Material dialog | interrupt only for a real decision; specific button labels; never stack dialogs |
| [Undo and redo](../../subskills/apple-hig-patterns/.topics/apple-hig-undo-and-redo/SKILL.md) | a snackbar with an Undo action | prefer undo to a confirmation for a routine, reversible deletion |
| [Action sheets](../../subskills/apple-hig-presentation/.topics/apple-hig-action-sheets/SKILL.md) | a bottom sheet or a menu | short, specific choices after a deliberate action |
| [Tab bars](../../subskills/apple-hig-navigation-and-search/.topics/apple-hig-tab-bars/SKILL.md) | navigation bar | few, stable top-level destinations |
| [Sidebars](../../subskills/apple-hig-navigation-and-search/.topics/apple-hig-sidebars/SKILL.md) | navigation rail or navigation drawer on large screens | the same destinations as on a phone |
| [Toolbars](../../subskills/apple-hig-menus-and-actions/.topics/apple-hig-toolbars/SKILL.md) | top app bar | the few actions that matter most on this screen |
| [Activity views](../../subskills/apple-hig-menus-and-actions/.topics/apple-hig-activity-views/SKILL.md) | the Android Sharesheet | use the system share flow, not a custom copy |
| [Typography](../../subskills/apple-hig-foundations/.topics/apple-hig-typography/SKILL.md) | Material type scale in `sp` units | hierarchy that stays clear at a large font scale |

## The Android convention wins

- System back must work on every screen, also inside sheets and dialogs. Do not
  depend on an edge-swipe gesture from iOS
  ([predictive back](https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture)).
- Use the Material dialog and its button placement, not the Apple layout.
- Each interactive element has a target of at least 48 × 48 dp
  ([Android accessibility](https://developer.android.com/guide/topics/ui/accessibility/apps)).
- Use the system font and `sp` units for text.
- Give each control a purpose description (`contentDescription`) and its role, so
  that TalkBack announces it correctly.

## Checks

- Do the full task with TalkBack.
- Set the largest font scale: no text clips and no function is lost.
- Use system back on each screen and in each dialog.
- Check text contrast: at least 4.5:1 below 18sp (14sp bold), else 3:1
  ([Android accessibility](https://developer.android.com/guide/topics/ui/accessibility/apps)).
- Run the [Accessibility Scanner](https://play.google.com/store/apps/details?id=com.google.android.apps.accessibility.auditor).
