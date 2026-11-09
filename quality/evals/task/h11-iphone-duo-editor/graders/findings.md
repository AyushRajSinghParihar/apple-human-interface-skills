---
type: llm
---

PASS if the reply makes at least four of these corrections, including 2 and 3:
1. Treat the device as one iPhone whose layout resizes continuously: use size classes, safe areas and layout margins instead of fixed 375 pt widths.
2. On the outer display, keep the toolbars and tab bar in their system placement along the side (vertical controls), not moved to the top edge.
3. Keep side controls on the same physical side in right-to-left languages, because they align with the hardware.
4. Give toolbar items both a title and a symbol, because the system uses the title for overflow and expanded forms.
5. Keep content and controls out of the reserved regions: the central folding region when partly folded, and the inner camera region while that camera is active (move the UI aside).
FAIL otherwise.
