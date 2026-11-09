"""Find stale review hashes, then draft or approve the affected review records.

Each review record binds a reviewer's judgement to exact file bytes. These
helpers only recompute hashes and mark records for another review. They never
approve content by themselves: `approve` needs a named reviewer and refuses a
record that still contains the re-review marker.
"""
import datetime as dt
import hashlib
import json
from pathlib import Path


TODO_MARK = "TODO(re-review)"
REVIEW_DIRS = ("reviews", "skill-reviews", "media-reviews", "image-reviews")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def _read(path):
    return json.loads(Path(path).read_text())


def _write(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def _actual(root, relative):
    target = (root / relative).resolve()
    if not target.is_relative_to(root) or not target.is_file():
        return None
    return digest(target)


def _record_paths(root):
    coverage = root / "coverage"
    paths = [coverage / "routing-review.json"]
    for directory in REVIEW_DIRS:
        paths.extend(sorted((coverage / directory).glob("*.json")))
    return [path for path in paths if path.is_file()]


def _sources(root):
    manifest = root / "coverage/manifest.json"
    if not manifest.is_file():
        return {}
    return {page["slug"]: page for page in _read(manifest).get("pages", []) if "slug" in page}


def _topic_rows(root):
    inventory = root / "coverage/capabilities.json"
    if not inventory.is_file():
        return {}
    return {row["topic"]: row for row in _read(inventory).get("topics", []) if isinstance(row, dict) and "topic" in row}


def _walk(node, pointer, owner, found):
    """Yield every generic (path, hash) binding with its nearest status-bearing owner."""
    if isinstance(node, dict):
        if "status" in node:
            owner = node
        if isinstance(node.get("path"), str) and isinstance(node.get("hash"), str):
            found.append((pointer + "/hash", node, "hash", node["path"], owner))
        if isinstance(node.get("destination"), str) and isinstance(node.get("destination_hash"), str) and pointer:
            found.append((pointer + "/destination_hash", node, "destination_hash", node["destination"], owner))
        for key, value in node.items():
            _walk(value, f"{pointer}/{key}", owner, found)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            _walk(value, f"{pointer}/{index}", owner, found)


def _bindings(root, path, record):
    """Return (pointer, holder, key, target, expected_hash, owner) for one record."""
    root = root.resolve()
    relative = path.relative_to(root / "coverage").as_posix()
    slug = path.stem
    sources, rows = _sources(root), _topic_rows(root)
    package = "skills/apple-hig/"
    result = []

    def add(pointer, holder, key, target, expected, owner):
        result.append((pointer, holder, key, target, expected, owner))

    if relative == "routing-review.json":
        for key, target in (("root_hash", package + "SKILL.md"),
                            ("topic_index_hash", package + "references/topic-index.md"),
                            ("platform_routes_hash", package + "references/platforms-and-tasks.md")):
            add("/" + key, record, key, target, _actual(root, target), record)
        for family in sorted(record.get("family_hashes", {})):
            target = f"{package}subskills/apple-hig-{family}/SKILL.md"
            add("/family_hashes/" + family, record["family_hashes"], family, target, _actual(root, target), record)
    elif relative.startswith("skill-reviews/"):
        row, page = rows.get(slug, {}), sources.get(slug, {})
        for key, field in (("skill_hash", "skill_path"), ("reference_hash", "reference_path")):
            if field in row:
                add("/" + key, record, key, row[field], _actual(root, row[field]), record)
        if "source_hash" in page:
            add("/source_hash", record, "source_hash", "coverage/manifest.json#" + slug, page["source_hash"], record)
    elif relative.startswith("reviews/") and isinstance(record.get("review"), dict):
        review, page = record["review"], sources.get(slug, {})
        if "destination" in page:
            add("/review/destination_hash", review, "destination_hash", page["destination"],
                _actual(root, page["destination"]), review)
        if "source_hash" in page:
            add("/review/source_hash", review, "source_hash", "coverage/manifest.json#" + slug, page["source_hash"], review)
    found = []
    _walk(record, "", None, found)
    for pointer, holder, key, target, owner in found:
        if pointer in {"/review/destination_hash"}:
            continue
        add(pointer, holder, key, target, _actual(root, target), owner)
    return result


def stale(root):
    """List every recorded hash that no longer matches its bound file or source."""
    root = Path(root).resolve()
    issues = []
    for path in _record_paths(root):
        record = _read(path)
        for pointer, holder, key, target, expected, _owner in _bindings(root, path, record):
            if holder.get(key) != expected:
                issues.append({"record": path.relative_to(root).as_posix(), "field": pointer,
                               "target": target, "recorded": holder.get(key), "current": expected})
    return issues


def _mark(value):
    if isinstance(value, str):
        return value if value.startswith(TODO_MARK) else f"{TODO_MARK} {value}".strip()
    if isinstance(value, dict):
        return {key: _mark(item) for key, item in value.items()}
    return value


def draft(root, relative):
    """Write current hashes into one record and mark each affected owner as a draft."""
    root = Path(root).resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root / "coverage") or not path.is_file():
        raise ValueError(f"not a review record: {relative}")
    record = _read(path)
    changed, owners = [], []
    for pointer, holder, key, _target, expected, owner in _bindings(root, path, record):
        if holder.get(key) == expected:
            continue
        if expected is None:
            raise ValueError(f"{relative}{pointer}: bound file is missing; fix the route before a review")
        holder[key] = expected
        changed.append(pointer)
        if owner is not None and all(owner is not item for item in owners):
            owners.append(owner)
    for owner in owners:
        if owner.get("status") != "draft":
            owner["previous_review"] = {"reviewer": owner.get("reviewer", ""), "reviewed_at": owner.get("reviewed_at", "")}
        owner["status"] = "draft"
        owner["reviewer"] = ""
        owner["reviewed_at"] = ""
        if "evidence" in owner:
            owner["evidence"] = _mark(owner["evidence"])
    if changed:
        _write(path, record)
    return changed


def _drafts(node, found):
    if isinstance(node, dict):
        if node.get("status") == "draft":
            found.append(node)
        for value in node.values():
            _drafts(value, found)
    elif isinstance(node, list):
        for value in node:
            _drafts(value, found)
    return found


def approve(root, relative, reviewer):
    """Approve every draft owner in one record after a named reviewer checks it."""
    if not isinstance(reviewer, str) or not reviewer.strip():
        raise ValueError("a named reviewer is required")
    root = Path(root).resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root / "coverage") or not path.is_file():
        raise ValueError(f"not a review record: {relative}")
    text = path.read_text()
    if TODO_MARK in text:
        raise ValueError(f"{relative}: replace each {TODO_MARK} marker with current review evidence first")
    record = json.loads(text)
    left = [pointer for pointer, holder, key, _t, expected, _o in _bindings(root, path, record) if holder.get(key) != expected]
    if left:
        raise ValueError(f"{relative}: stale bindings remain: {', '.join(left)}")
    owners = _drafts(record, [])
    if not owners:
        raise ValueError(f"{relative}: no draft review to approve")
    for owner in owners:
        owner.pop("previous_review", None)
        owner["status"] = "reviewed"
        owner["reviewer"] = reviewer.strip()
        owner["reviewed_at"] = _now()
    _write(path, record)
    return len(owners)


def marker_errors(root):
    """A re-review marker or a draft must never pass a release check."""
    root = Path(root).resolve()
    errors = []
    for path in _record_paths(root):
        text = path.read_text()
        label = path.relative_to(root).as_posix()
        if TODO_MARK in text:
            errors.append(f"{label}: unfinished re-review marker {TODO_MARK}")
        if _drafts(json.loads(text), []):
            errors.append(f"{label}: draft review awaits approval")
    return errors
