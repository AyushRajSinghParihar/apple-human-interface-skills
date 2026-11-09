Keep the native WinUI 3 dialog, but make the consequences explicit and remove the stacked warning.

1. **Replace “Are you sure?” and Yes/No with concrete copy.**

   > **Delete project “Atlas”?**  
   > This permanently deletes the project and its 40 files. This action cannot be undone.  
   > **Delete** · **Cancel**

   Specify whether deletion also affects synced copies if that is part of the actual behavior. Confirmation is justified for this irreversible action.

2. **Use Windows button ordering.**  
   Let `ContentDialog` arrange its standard buttons: use `PrimaryButtonText="Delete"` and `CloseButtonText="Cancel"`. Don’t manually copy macOS’s Cancel-left/Delete-right layout. Borrow Apple’s clarity while preserving Windows conventions.

3. **Choose the default deliberately.**  
   For this irreversible, 40-file deletion, I recommend `DefaultButton="None"` and initial focus on Cancel. Enter on opening should not delete; after someone explicitly focuses Delete, keyboard activation should work.

   This is a risk-based recommendation, **not an Apple prohibition**: Apple explicitly allows a normal destructive default when confirming deletion the person deliberately requested. Its guidance also permits no default when deliberate reading matters. See [Apple HIG: Alerts—Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons).

4. **Remove the second dialog.**  
   Include any sync warning that changes the deletion decision in the original confirmation. If sync state changes while it’s open, update that dialog and require a fresh decision when necessary. Put routine sync status inline. WinUI supports only one `ContentDialog` per window at a time; serialize any truly separate decisions. See [Microsoft’s dialog guidance](https://learn.microsoft.com/windows/apps/design/controls/dialogs-and-flyouts/dialogs).

Before shipping, verify that Escape and Cancel preserve everything, opening the dialog then pressing Enter does not delete, deliberate Delete activation deletes exactly the disclosed scope, and sync updates never stack dialogs. These are review recommendations; runtime behavior hasn’t been tested.