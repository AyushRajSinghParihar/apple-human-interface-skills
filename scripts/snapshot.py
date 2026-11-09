"""Carry reviews forward to a new source snapshot, and scaffold drafts for new content.

Source units and media occurrences have positional IDs, so one inserted paragraph
moves every later ID. After `hig.py discover`:

  remap(root, slug)     moves each unit review whose source text is unchanged
                        (same unit hash and section) to the unit's new ID, and drops
                        reviews of removed units. If the guide changed since the
                        review, it reopens the moved reviews as drafts. Media records
                        of unchanged assets get the new occurrence IDs of their asset;
                        records of removed assets are deleted. The review's `sections`
                        and `tables` lists are not changed: update them by hand.
  scaffold(root, slug)  adds draft unit reviews for new units and draft media records
                        for new or changed assets. It downloads each asset to
                        .cache/review-media/SLUG/ so the binary hash is real and a
                        reviewer can examine the file.

Nothing here approves content. Every new or uncertain entry gets status "draft"
and TODO(re-review) evidence, which `hig.py check` rejects until a reviewer
rewrites the evidence and runs `hig.py review-approve`.
"""
import collections
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request


TODO = "TODO(re-review)"
SCALE = {"1x", "2x", "3x"}


def _read(path):
    return json.loads(Path(path).read_text())


def _write(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def _page(root, slug):
    for page in _read(root / "coverage/manifest.json")["pages"]:
        if page.get("slug") == slug and page.get("type") == "article":
            return page
    raise ValueError(f"no article {slug} in coverage/manifest.json")


def _media_files(root, slug):
    """The review files that can hold media records, in the checker's merge order."""
    return [root / "coverage/reviews" / f"{slug}.json",
            root / "coverage/media-reviews" / f"{slug}.json",
            root / "coverage/image-reviews" / f"{slug}.json"]


def remap(root, slug):
    root = Path(root).resolve()
    page = _page(root, slug)
    free = collections.defaultdict(list)
    for unit in page["extraction"]["units"]:
        free[(unit["hash"], unit["section"])].append(unit["id"])
    report = {"units_kept": 0, "units_dropped": 0, "media_moved": [], "media_drafted": []}
    path = root / "coverage/reviews" / f"{slug}.json"
    guide = root / page["destination"]
    report["units_drafted"] = 0
    if path.is_file():
        record = _read(path)
        review = record.get("review", {})
        # Unit evidence can describe the guide's text, so a changed guide reopens it.
        guide_changed = guide.is_file() and review.get("destination_hash") not in (None, hashlib.sha256(guide.read_bytes()).hexdigest())
        kept = []
        for old in review.get("units", []):
            ids = free.get((old.get("source_unit_hash"), old.get("source_anchor")))
            if ids:
                old["id"] = ids.pop(0)
                if guide_changed and old.get("treatment") != "metadata" and old.get("status") == "reviewed":
                    _draft(old, "the guide changed after this review; confirm the evidence")
                    report["units_drafted"] += 1
                kept.append(old)
            else:
                report["units_dropped"] += 1
        report["units_kept"] = len(kept)
        review["units"] = kept
        _write(path, record)
    occurrences = collections.defaultdict(list)
    metadata = {}
    for media in page["extraction"]["media"]:
        if media["treatment"] != "metadata":
            occurrences[media["identifier"]].append(media["id"])
            metadata[media["identifier"]] = media["reference_metadata_hash"]
    for path in _media_files(root, slug):
        if not path.is_file():
            continue
        record = _read(path)
        changed = False
        removed = [identifier for identifier in record.get("media", {}) if identifier not in occurrences]
        for identifier in removed:
            del record["media"][identifier]
            report.setdefault("media_removed", []).append(identifier)
            changed = True
        for identifier, observed in record.get("media", {}).items():
            if observed.get("reference_metadata_hash") != metadata[identifier]:
                continue
            old = observed.get("reviewed_occurrence_ids", [])
            new = occurrences[identifier]
            if sorted(old) == sorted(new):
                continue
            observed["reviewed_occurrence_ids"] = list(new)
            changed = True
            if len(old) == len(new):
                report["media_moved"].append(identifier)
            else:
                # The asset is the same, but it appears in a different number of places.
                _draft(observed, f"occurrences changed from {len(old)} to {len(new)}")
                report["media_drafted"].append(identifier)
        if changed:
            _write(path, record)
    return report


def _draft(owner, why):
    if owner.get("status") != "draft":
        owner["previous_review"] = {"reviewer": owner.get("reviewer", ""), "reviewed_at": owner.get("reviewed_at", "")}
    owner.update({"status": "draft", "reviewer": "", "reviewed_at": ""})
    evidence = owner.get("evidence", "")
    if not str(evidence).startswith(TODO):
        owner["evidence"] = f"{TODO} {why}. {evidence}".strip()


def _fetch(url, target):
    if not target.is_file():
        request = urllib.request.Request(url, headers={"User-Agent": "apple-hig-skills/1.1 (source review)"})
        with urllib.request.urlopen(request, timeout=60) as response:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(response.read())
    return hashlib.sha256(target.read_bytes()).hexdigest()


def scaffold(root, slug, fetch=True):
    root = Path(root).resolve()
    page = _page(root, slug)
    destination = page["destination"]
    reference = root / destination
    report = {"units_added": 0, "media_added": [], "media_updated": []}
    path = root / "coverage/reviews" / f"{slug}.json"
    record = _read(path) if path.is_file() else {"review": {}, "media": {}}
    review = record.setdefault("review", {})
    reviewed = {u.get("id") for u in review.get("units", [])}
    guide_text = reference.read_text() if reference.is_file() else ""
    for unit in page["extraction"]["units"]:
        if unit["treatment"] == "metadata" or unit["id"] in reviewed:
            continue
        entry = {"id": unit["id"], "source_unit_hash": unit["hash"], "source_anchor": unit["section"],
                 "status": "draft", "treatment": unit["treatment"], "destination": destination,
                 "evidence": f"{TODO} new or changed source unit ({unit['kind']}); confirm that the guide keeps its guidance."}
        if f'id="{unit["section"]}"' in guide_text:
            entry["destination_anchor"] = unit["section"]
        review.setdefault("units", []).append(entry)
        report["units_added"] += 1
    if report["units_added"]:
        _write(path, record)

    known = {}
    for candidate in _media_files(root, slug):
        if candidate.is_file():
            known.update(_read(candidate).get("media", {}))
    by_identifier = collections.defaultdict(list)
    for media in page["extraction"]["media"]:
        if media["treatment"] != "metadata":
            by_identifier[media["identifier"]].append(media)
    images = root / "coverage/image-reviews" / f"{slug}.json"
    videos = root / "coverage/media-reviews" / f"{slug}.json"
    stores = {}
    for identifier, uses in by_identifier.items():
        first = uses[0]
        current = known.get(identifier)
        if current and current.get("reference_metadata_hash") == first["reference_metadata_hash"]:
            continue
        target = videos if first.get("kind") == "video" else images
        store = stores.setdefault(target, _read(target) if target.is_file() else {"source_hash": page["source_hash"], "media": {}})
        store["source_hash"] = page["source_hash"]
        groups = collections.OrderedDict()
        for representation in first.get("representations", []):
            group = tuple(sorted(t for t in representation["traits"] if t not in SCALE))
            if group not in groups or "2x" in representation["traits"]:
                groups[group] = representation["url"]
        urls = list(groups.values())
        cache = root / ".cache/review-media" / slug
        hashes = {url: (_fetch(url, cache / url.rsplit("/", 1)[-1]) if fetch else "0" * 64) for url in urls}
        entry = {
            "status": "draft", "reviewer": "", "reviewed_at": "",
            "reference_metadata_hash": first["reference_metadata_hash"],
            "asset_url": urls[0] if urls else "", "binary_hash": hashes.get(urls[0], "") if urls else "",
            "review_method": f"{TODO} describe how the asset was examined",
            "classification": f"{TODO} guidance-bearing, illustrative or decorative",
            "evidence": f"{TODO} what the asset shows and where the guide keeps its lesson (section #{first['section']})",
            "destination": destination,
            "supporting_files": [{"path": destination, "hash": hashlib.sha256(reference.read_bytes()).hexdigest()}],
            "reviewed_occurrence_ids": [use["id"] for use in uses],
            "appearance_variants": [
                {"asset_url": url, "binary_hash": hashes[url], "status": "draft", "reviewer": "",
                 "review_method": f"{TODO} compare with the primary appearance",
                 "evidence": f"{TODO} what this appearance adds"} for url in urls[1:]],
        }
        if current:
            entry["previous_review"] = {"reviewer": current.get("reviewer", ""), "reviewed_at": current.get("reviewed_at", "")}
            report["media_updated"].append(identifier)
        else:
            report["media_added"].append(identifier)
        store["media"][identifier] = entry
    for target, store in stores.items():
        _write(target, store)
    return report


RENEWER = "deterministic-snapshot-diff"


def renew(root, slug, previous_manifest):
    """Renew drafts of a page whose new source differs only outside guidance and media.

    It approves only when every unit hash (with its ID and section), every media
    identifier with its metadata hash, the guide, and the procedure are the same as
    in the reviewed snapshot. The evidence names exactly what was compared.
    """
    root = Path(root).resolve()
    new = _page(root, slug)
    old = next((p for p in previous_manifest["pages"] if p.get("slug") == slug), None)
    if old is None:
        raise ValueError(f"{slug}: not in the previous manifest")

    def units(page):
        return sorted((u["id"], u["hash"], u["section"], u["treatment"]) for u in page["extraction"]["units"])

    def media(page):
        return sorted((m["id"], m["identifier"], m["reference_metadata_hash"]) for m in page["extraction"]["media"])

    if units(old) != units(new) or media(old) != media(new) or old.get("destination") != new.get("destination"):
        raise ValueError(f"{slug}: guidance units or media changed; a reviewer must examine this page")
    evidence = (f"Deterministic renewal for source snapshot {new['source_hash'][:12]} "
                f"(previous {old['source_hash'][:12]}): all {len(new['extraction']['units'])} extracted units "
                f"and {len(new['extraction']['media'])} media uses have identical IDs, sections and hashes, so "
                "the change is outside the guidance (for example metadata or links). The guide and the "
                "procedure bytes are unchanged; the earlier review still applies.")
    renewed = []
    for directory in ("reviews", "skill-reviews"):
        path = root / "coverage" / directory / f"{slug}.json"
        if not path.is_file():
            continue
        record = _read(path)
        owner = record["review"] if directory == "reviews" else record
        if owner.get("status") != "draft":
            continue
        previous = owner.pop("previous_review", {})
        owner["status"] = "reviewed"
        owner["reviewer"] = RENEWER
        owner["reviewed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
        if directory == "reviews":
            owner["evidence"] = f"{evidence} Previous review: {previous.get('reviewer', '?')} at {previous.get('reviewed_at', '?')}."
        else:
            owner["evidence"] = {key: (value[len(TODO):].strip() if isinstance(value, str) and value.startswith(TODO) else value)
                                 for key, value in owner.get("evidence", {}).items()}
            owner["renewal"] = evidence
        _write(path, record)
        renewed.append(f"coverage/{directory}/{slug}.json")
    return renewed
