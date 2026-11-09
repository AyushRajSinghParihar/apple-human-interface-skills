---
description: Review an interface against Apple's Human Interface Guidelines and rank the findings
argument-hint: "[file, folder, screenshot or description]"
---

Use the apple-hig skill in review mode. The target is: $ARGUMENTS

If no target is given, review the interface files that the current branch changes.

1. Find the platform and the user task. Examine the supplied code, screenshot or
   specification before you decide what is wrong.
2. Map each control and each material decision to its topic procedure in the
   skill's topic index, and read those procedures.
3. Rank the findings. For each one, give the observed problem, its effect, the HIG
   rule with its link, and a concrete correction.
4. Keep source-backed findings apart from your own suggestions. Do not invent a
   violation without evidence.
5. List the checks as passed, failed or not done.
