Keep the clarity of an Apple app, but follow Windows interaction conventions.

- **Replace “Are you sure?” with a specific title:** “Delete ‘Project name’?”
- **State the consequence:** “This will permanently delete this project and its 40 files. This can’t be undone.” If deletion also affects synced copies or collaborators, say so explicitly.
- **Use “Delete” and “Cancel,” not “Yes” and “No.”** The buttons should make sense without rereading the question.
- **Keep WinUI’s native button order.** Set `PrimaryButtonText="Delete"` and `CloseButtonText="Cancel"`. Let `ContentDialog` arrange them; don’t copy macOS’s layout.
- **Make Cancel the default:** `DefaultButton="Close"`. For an irreversible action, Enter shouldn’t delete merely because the dialog appeared. Keep Delete available through deliberate focus or a click. Escape should cancel.
- **Remove stacked dialogs.** Put a relevant sync warning in the confirmation itself. If it needs a separate decision, close the first dialog before presenting the next; WinUI permits only one `ContentDialog` per window at a time.

Suggested content:

> **Delete ‘Project name’?**  
> This will permanently delete this project and its 40 files. This can’t be undone.
>
> **Delete** · **Cancel** *(default)*

The key improvement is specific language, clear consequences, and a safe default—not matching another platform’s button placement.