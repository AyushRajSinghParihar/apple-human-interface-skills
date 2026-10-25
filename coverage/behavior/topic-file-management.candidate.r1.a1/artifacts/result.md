# Decisions and patch summary

Updated interface.md in place from the four-sentence failure description to a concrete macOS document lifecycle contract. The patch defines independent document windows and identities, native save/autosave and draft recovery, separate PDF/interchange export, close/quit guards, explicit local/cloud deletion scope, and actionable recent-file recovery. It includes command placement, shortcuts, exact alert outcomes/defaults, cancellation, failure and asynchronous revision handling.

Open now preserves the current draft by opening another document window. Save retains the editable native identity and destination; Export As… creates an output snapshot without marking the original saved. Autosave is the default, with separate recovery for unnamed drafts and explicit protection when saving is unresolved. The actual native format, provider and framework remain implementation facts to establish.

Local eviction is available only when it can preserve acknowledged remote content. Shared deletion requires an explicit scope warning and confirmation. Recent references can be located, reauthorized, retried or removed without deleting content. Transactional writes and acknowledgment rules are product engineering decisions; they are not claims that HIG specifies a persistence algorithm.

# Worked before and after

**Before (scenario constructed from the supplied brief):** A writer types a new scene in Untitled, then opens Act Two. Open replaces the draft without warning. Saving Act Two asks for an export format again. Deleting a nominally local copy silently removes the shared original. A later recent-file entry is inaccessible and offers no recovery.

**After (specified behavior, not an executed demonstration):** The same Open creates an Act Two window while Untitled retains its scene, selection and history. Command-S in Untitled asks once for a native name/location; successful Save establishes that identity. Subsequent Command-S writes there without format selection. After another edit, Export As… to PDF includes the latest scene while the native document remains Edited until its native revision is saved. Canceling export changes neither document nor target.

For shared Act Two, Remove Download is available only after remote acknowledgment and only if supported; it leaves sharing intact. Delete Everywhere… names the cross-device and collaborator consequences and requires deliberate confirmation. If its recent reference later moves, Locate… validates the selected file and relinks after successful opening. Cancel at any point returns to the unchanged current screenplay.

# Acceptance checks

The following are acceptance scenarios for implementation, not test results. All runtime checks are **not executed**.

| Check | Required observable result |
| --- | --- |
| New/Open, including Finder and multiple selections | Untitled and existing edits survive; each valid identity opens independently; duplicate identity activates its window; individual errors preserve other work. |
| Open cancellation, unsupported/corrupt file | Existing text, selection and history remain; no empty replacement document masquerades as saved. |
| First Save and subsequent Save | First requests native name/location; reopen round-trips screenplay structure and metadata; subsequent saves retain URL/type without export prompts. Extension visibility preference persists. |
| Save failure and concurrent edits | Prior file remains valid; in-memory edits/history survive; only persisted revision clears its pending state; Retry/Save Elsewhere recover. |
| Autosave and recovery | Named edits persist periodically/on orderly exit; checkpointed unnamed work recovers after interruption; checkpoint/export never falsely establishes a native save. Dirty cues match autosave mode. |
| Export success/cancel/failure | Output reflects captured revision; original URL/type, history and unsaved state remain; no automatic output opening; failed/canceled replacement leaves old target intact; source aliases are rejected. |
| Close/quit and save-sheet cancellation | Save, Don’t Save, Cancel and save failure follow the guard; canceling Save prevents close/quit; export never bypasses it. Resolve multiple documents sequentially. |
| Local cache eviction | Eligible eviction preserves cloud identity/access and can redownload; offline, unsynced and conflicted documents cannot be evicted. Unsupported providers expose no false local action. |
| Shared deletion | Warning names service, devices, collaborators and recovery limits; Return alone does not commit; Cancel/Escape has no mutation; failed/partial acknowledgment never claims complete success. |
| Local-only deletion | Uses recoverable Trash, protects dirty edits, and does not mutate cloud content; text Undo does not falsely promise filesystem restoration. |
| Offline sync and conflict | Local work remains editable/durable; pending status differs from synchronized; reconnect preserves both divergent versions until meaningful resolution. |
| Recent-file recovery | Missing, denied and offline entries offer distinct recovery; successful resolution updates reference; Remove/Clear affect references only; cancel preserves active draft. |
| Keyboard, windows and sheets | With hidden toolbar and multiple windows, menu commands target active document; all tasks complete by keyboard; Escape/Command-Period restore context; sheet blocks only its parent; no stacked alerts. |
| Undo and activation | Undo/redo target meaningful edits in the active document, survive saves/exports, reveal restored content, and preserve work when switching apps. |
| Provider/preview integration, if present | Open/import filters accepted types; unsupported attachments preview through appropriate system integration; native previews and provider behavior need separate verification. No attachment/preview surface was supplied. |

# Evidence and limits

**Passed — static specification review:** Confirmed the original interface.md contained all four reported failures. Read the installed root SKILL.md explicitly, searched its complete topic index, and read each selected family, topic procedure and supporting reference in that order using separate single-file commands. Reviewed the revised specification for each reported failure and for success, cancellation and failure paths. Both requested Markdown files exist and the revised interface contains the command, persistence, exit, cloud and recents contracts.

**Failed:** No static acceptance failure identified in the revised document. The four original behaviors are defects reported by the supplied specification, not independently reproduced runtime failures.

**Not executed:** Application builds, tests, native save panels, disk durability, recovery after crashes, cloud propagation, provider permission changes, simultaneous collaboration, SDK/API availability, Mac keyboard behavior, GUI rendering, VoiceOver, Full Keyboard Access and other accessibility execution. This Linux task changed documentation only. No executable app, source implementation, screenshots, native format definition or provider contract was supplied as evidence. The acceptance table therefore makes no runtime pass claim.

Guidance was read only from `/tmp/hig-eval-zp9v32qm/.agents/skills/apple-hig/`. Route: root → Getting started / Designing for macOS; Patterns / File management, Modality, Undo and redo; Presentation / Alerts, Sheets; Technologies / iCloud; Menus and actions / The menu bar; Inputs / Keyboards. Each topic's supporting reference was read after its procedure. iCloud supplies relevant cloud-safety guidance without establishing an iCloud implementation. Local articles are dated 2026-10-25 snapshots of application guidance, not SDK references; no independent source/media review or live-source verification is claimed. No web browsing occurred.

Material source links and the distinction between source guidance and product choices are included in interface.md's Design basis. Particularly relevant are [File management](https://developer.apple.com/design/human-interface-guidelines/file-management#macOS), [File menu Save and Export](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#File-menu), [alert defaults](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons), and [cloud deletion/conflicts](https://developer.apple.com/design/human-interface-guidelines/icloud#Best-practices). These links identify the installed guidance's official sources; they were not fetched.
