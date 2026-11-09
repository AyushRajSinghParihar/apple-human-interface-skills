---
type: llm
---

PASS if the reply does all of these:
1. Replaces "Are you sure?" with a title and message that name the project and say the deletion cannot be undone.
2. Replaces Yes and No with specific labels, such as Delete and Cancel.
3. Keeps or explains the Windows convention: the action button at the left (PrimaryButton) and Cancel at the right (CloseButton). If it keeps the macOS order, it must say that this conflicts with Windows conventions and what that costs users.
4. Does not show a second dialog on top of the first (Windows allows one ContentDialog at a time).
FAIL if any item is missing.
