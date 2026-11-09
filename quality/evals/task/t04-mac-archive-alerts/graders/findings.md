---
type: llm
---

PASS if the reply finds at least four of these five problems, including problems 2, 3 and 5:
1. A routine successful save should not interrupt with an alert.
2. "Error" and "Something happened" hide the context and the consequence of the deletion.
3. Yes and No do not say what each button does (for example Delete versus Cancel).
4. A harmless acknowledgment should not make Cancel the default.
5. Alerts must not stack on top of each other.
FAIL otherwise, or if it invents a high-severity problem that the description does not support.
