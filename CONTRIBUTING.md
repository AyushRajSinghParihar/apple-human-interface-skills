# Contributing

Keep the router small and put source-specific guidance in its owning family.
Each current article has one primary owner; cross-topic links do not count as
additional source coverage.

1. Run `python3 scripts/hig.py check --live` to identify drift, or
   `python3 scripts/hig.py discover` to refresh an authoring snapshot.
2. Read the entire affected source, including platform sections, tables, notes,
   and meaningful media. Write original, actionable guidance and retain factual
   units, exceptions, and source qualifications.
3. Preserve the source-heading HTML anchors used by the coverage manifest.
   Link local dependencies relative to the installed package, never to a local
   checkout path or sibling installation.
4. Have another reviewer compare source and destination. Record the actual
   review evidence, source/destination hashes, and any media supporting-file
   hashes under `coverage/reviews/`. Do not approve your own authored guidance.
5. Run tests, strict coverage checks, and `python3 scripts/hig.py report`.
   Include the refreshed report and relevant review evidence in the pull request.

Do not commit raw Apple Markdown/JSON, downloaded media, private tooling caches,
or whole copied paragraphs. Resource links and change histories receive explicit
reference-only treatment; substantive guidance cannot be replaced by links.

When a source is unavailable or ambiguous, preserve its coverage record and
describe the limitation. Do not lower the denominator to make a report green.
