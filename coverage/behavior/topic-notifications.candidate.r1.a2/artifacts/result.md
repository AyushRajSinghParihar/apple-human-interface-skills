# Result

Patched `interface.md` in place with an implementable iPhone reminder contract. Replaced diagnosis disclosure with exact generic title/body and hidden-preview copy; removed every-minute repeats; specified appointment-specific activation; separated acknowledgment from booking cancellation; and added permission-denied recovery, event identity, foreground behavior, badge policy, and acceptance checks.

## Decisions and support

- Keep notification content generic even when unlocked. [Notifications — Best practices and Content](https://developer.apple.com/design/human-interface-guidelines/notifications#Content) supports protecting confidential content and generic hidden previews. Omitting appointment time and provider is this specification's conservative privacy choice.
- Send one reminder per occurrence; dismissal and nonresponse never trigger another. [Notifications — Best practices](https://developer.apple.com/design/human-interface-guidelines/notifications#Best-practices) advises against repeating the same event for nonresponse. A 24-hour lead time and no second reminder after rescheduling an issued occurrence are explicit product choices.
- Activation resolves the correct appointment; `Acknowledge` changes reminder state only. [Notification actions](https://developer.apple.com/design/human-interface-guidelines/notifications#Notification-actions) supports useful, clearly labeled, preferably nondestructive actions without redundant Open App. Authentication before acknowledgment is an added product safeguard.
- Request permission in context, preserve appointment access when denied, and use Active urgency. [Managing notifications](https://developer.apple.com/design/human-interface-guidelines/managing-notifications#Integrating-with-Focus) supports consent and honest interruption levels; no evidence justifies Critical delivery. [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission) supports contextual permission requests and minimized access.
- Use explicit success/failure wording and a recovery action, following [Writing](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices). Quiet foreground updates and no new badge follow the notification guidance; badges are optional, not required.

## Worked before/after

Illustrative fixture, not an observed payload: appointment A is tomorrow at 10:00; appointment B is next week. A has a confidential diagnosis in its authenticated record.

| Step | Before, based on supplied brief | Revised specification |
| --- | --- | --- |
| A's reminder appears | Full diagnosis visible on Lock Screen; exact original text not supplied | `Appointment Reminder` / `You have an upcoming appointment.` Hidden-preview description: `Appointment reminder`. |
| Person dismisses it | Reappears every minute | No repeat for A, including after retry or restart. |
| Person activates it | Opens generic Home | Authenticate if needed, then open A's current details, never B. |
| Person chooses acknowledgment | Cancels A | Marks A's reminder acknowledged; booking remains scheduled. Feedback: `Reminder acknowledged. Your appointment is unchanged.` |
| Permission denied | Failure behavior unspecified | No prompt loop; upcoming appointments remain accessible, with an optional Settings route. |

## Acceptance audit

Passed — static specification review: all four supplied defects have explicit replacements in `interface.md`; denied/revoked permission has a usable fallback; exact strings, identity and duplicate rules, stale/account states, action failure, foreground handling, and badge policy are defined. The worked fixture traces the intended outcomes, not executed behavior.

Failed — no static specification checks remain failed. This does not establish that an implementation passes.

Not executed — actual notification generation, delivery, deduplication under concurrency, persistence failure, deep-link routing, account authorization, system permission prompts, Focus/summary/silent behavior, hidden-preview rendering, SDK compilation, device/GUI testing, localization, truncation, and VoiceOver. The numbered acceptance contract in `interface.md` defines checks for an implementation before release.

## Evidence and routing limits

Explicitly read the installed root `.agents/skills/apple-hig/SKILL.md`, then the System experiences family and Notifications procedure; searched the complete topic index for notification, privacy, and writing concepts. Read the Patterns family and Managing notifications procedure, and Foundations family with Privacy and Writing procedures, before reading their respective source guides. Each file was consumed by its own `cat` command; the index search used its own `rg` command. All paths were resolved within this installed package.

Sources were supplied `interface.md` and the installed local guidance only. The original artifact was a single prose brief, with no app code, payloads, screenshots, OS target version, SDK, tests, or authentication implementation. Official links above are attribution from the local snapshot; no web browsing or current-source verification occurred. This is appointment reminder design, with no treatment-plan, health-data-sharing, or research-consent feature introduced. No framework adoption, device execution, security certification, or accessibility execution is claimed. API feasibility and native rendering remain implementation verification work.
