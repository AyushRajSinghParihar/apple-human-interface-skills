---
name: apple-hig-web-views
description: Use when choosing, reviewing, or adapting embedded web content and its in-app navigation boundary.
---

# Bound embedded browsing to its task

Read [the web-view guide](../../references/web-views.md). The navigation procedure below is application advice, not an assertion that controls appear automatically.

Inspect the target platform, embedded document/page, possible links, host navigation, and create/review/adapt request. Establish whether the task is displaying a single document or browsing multiple pages, what must remain in the app, and what can open externally. Trace actual navigation handlers when supplied; a visible Back icon does not establish browser history behavior.

Choose an embedded web view when web content serves the immediate app task. If the design expands into a general browser, return to the task and identify the bounded content and exit. On tvOS/watchOS, where the guide says web views are unsupported, propose a native summary or suitable supported destination rather than promising the same embed.

Implement the requested embed/navigation boundary or provide a page-flow specification. If multiple pages can be visited, explicitly enable history behavior and provide corresponding Back/Forward controls with accurate availability. Distinguish browser Back from dismissing the host screen. Decide how external links, failed navigation, and return to the task behave based on the supplied product requirements; these are application decisions, not extra HIG mandates. In reviews report specific paths that strand the user rather than generic browser feature requests.

**Worked transformation:** Before: an app displays help inside a web view; a related-article link replaces the page, while the only Back control closes Help. Decision: article history and host dismissal are different actions. After: help history has working Back/Forward states, and a separately named Close returns to the original app task without inventing Safari-like tabs.

Deliver the artifact and a compact host/page navigation map. Follow an internal link, return through history, reach the history boundary, and leave Help. Fail for unsupported platform claims, a dead-end linked page, or a Back control that unexpectedly discards the host task. Distinguish source/logic inspection from native WebKit execution and actual network results.

Load [modality](../../../apple-hig-patterns/.topics/apple-hig-modality/SKILL.md) if the host blocks a task, or [toolbars](../../../apple-hig-menus-and-actions/.topics/apple-hig-toolbars/SKILL.md) when browsing controls need placement work.
