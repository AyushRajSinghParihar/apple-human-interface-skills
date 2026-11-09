---
type: llm
---

PASS if the reply judges flows A, B and C separately and all three of these are true:
1. Flow A: it removes or avoids the alert for the routine, undoable removal and relies on Undo.
2. Flow B: it accepts that Empty Archive can stay the default (Return) action because the person deliberately asked for the irreversible action, as long as Cancel is present and the consequence is clear. Small wording improvements are fine.
3. Flow C: it treats the unexpected destructive default as a serious problem, and it removes Delete All as the default (a safe default, no default, or no dialog at all).
FAIL if any flow is missing or wrongly judged.
