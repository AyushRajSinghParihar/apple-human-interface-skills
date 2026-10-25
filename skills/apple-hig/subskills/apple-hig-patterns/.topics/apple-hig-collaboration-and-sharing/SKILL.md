---
name: apple-hig-collaboration-and-sharing
description: Use when creating, reviewing, or adapting send-a-copy, collaborative sharing, participant permissions, management, and related updates.
---

# Separate sharing a copy from sharing access

Read [the collaboration guide](../../references/collaboration-and-sharing.md). This workflow is application advice; integration capability depends on infrastructure and platform.

Inspect object identity, sharing backend, participant/permission model, current UI, platform, and create/review/adapt intent. Distinguish copy transfer, ongoing collaboration, and synchronous SharePlay. Record existing access/link behavior; a Share button does not prove permissions or universal links work.

Use convenient standard Share entry/presentation and offer send-a-copy alongside collaboration. Explain a small logical set of who can access/edit/add participants. Once shared, expose Collaboration prominently with participants/communication, essential custom information, and management. Use system management where supplied; custom infrastructure needs appropriate representations, management UI, and universal links. Route updates to the relevant object rather than generic home. On visionOS explain that entering Full Space pauses Shared Space window streaming; on watch use supported ShareLink behavior. Do not claim this collaboration integration on tvOS.

Implement the authorized sharing UI/links/permission binding, specify access/representation/management contracts, or review concrete misleading-access defects. Do not actually send invitations or change live permissions without authorization; a design/build request can be satisfied with reviewable artifacts.

**Worked transformation:** Before: “Share” silently grants edit access to anyone with a link and offers no copy or management route. Decision: access and transfer have different consequences. After: expose explicit collaboration/copy choice, concise access/edit permissions, and a persistent Collaboration management route tied to the shared document.

Deliver the artifact, copy-versus-access model, permissions, participant management, and link destinations. Verify recipient scope, changed/revoked access, copied representation, and update links. Fail for access broader than described, copy mistaken for collaboration, or management unavailable after sharing. Separate mocked UI from actual backend enforcement/device integration.

Load [activity-views](../../../apple-hig-menus-and-actions/.topics/apple-hig-activity-views/SKILL.md) for share mechanics or [privacy](../../../apple-hig-foundations/.topics/apple-hig-privacy/SKILL.md) for exposure decisions.
