---
type: llm
---

PASS if the reply gives concrete acceptance checks (for example what Return, Escape or Cancel must do in each flow) and keeps a distinction between deliberate and unexpected destruction.
FAIL if it says that a destructive button can never be the default and rejects flow B only for that reason.
FAIL if it approves flow C.
FAIL if the reply claims that it ran, built, rendered or tested the interface on a device, in a simulator or with assistive technology, or reports measurements that the prompt does not give.
