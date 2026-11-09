Use Apple’s emphasis on clarity, but follow Windows conventions for the interaction.

- **Name the action and its consequence.** Replace “Are you sure?” with **“Delete ‘Project name’?”** and body text: **“This will permanently delete the project and its 40 files. This action can’t be undone.”** Make clear whether synced copies are also deleted.
- **Use explicit buttons:** **Delete** and **Cancel**, not Yes and No. People should understand each choice without rereading the question.
- **Keep the Windows button order.** In a WinUI 3 `ContentDialog`, use `PrimaryButtonText="Delete"` and `CloseButtonText="Cancel"`. Let the platform place them; don’t copy the macOS order.
- **Make Cancel the default.** Set `DefaultButton="Close"` so an incidental Enter doesn’t permanently delete 40 files. Keep initial focus on Cancel and let Escape cancel. Delete should require a deliberate choice.
- **Remove the stacked dialog.** A `ContentDialog` doesn’t support another open `ContentDialog` in the same window. Include any relevant sync warning in the confirmation before the person commits. If a separate step is necessary, close the first dialog before showing the next.

The proposed Delete default is the most important change to reject: an irreversible action should not be the easiest one to trigger accidentally.