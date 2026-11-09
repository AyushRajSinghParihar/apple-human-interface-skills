Use an **alert** for the confirmation. On macOS, you can present that alert as a window-modal sheet using `NSAlert`; these aren’t mutually exclusive. A custom sheet is useful only if deletion requires a more involved task.

Make the consequence explicit:

> **Delete project “Atlas”?**  
> This permanently deletes the project and its 40 files. This action cannot be undone.

Offer **Cancel** and **Delete Project**.

If the user explicitly chose to delete the project, **Delete Project can be the normal default**, activated by Return. Apple’s guidance says **Cancel shouldn’t be the default**. If the consequences warrant deliberate reading, consider **no default button**, with Escape canceling.

If deletion is readily undoable, consider skipping confirmation and offering Undo. The file count alone doesn’t determine whether confirmation is needed.

Sources: Apple HIG [Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts) and [Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets).