Use an **alert** for the confirmation. On macOS, you can present an `NSAlert` as a sheet attached to the project’s window—“alert” describes the content; “sheet” describes its presentation.

If the user explicitly chose Delete Project, **Delete can be the default**, so Return confirms their intent. Always include **Cancel**, but don’t make Cancel the default. If the 40-file loss needs deliberate attention, consider **no default button**.

For permanent deletion, use copy like:

> **Delete project “Orion”?**  
> This permanently deletes the project and its 40 files. This action cannot be undone.  
> **Cancel** · **Delete**

If deletion is easily undoable, consider skipping confirmation and offering Undo. The consequences and reversibility matter more than the file count.

Sources: Apple’s [Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts) and [Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets) guidance.