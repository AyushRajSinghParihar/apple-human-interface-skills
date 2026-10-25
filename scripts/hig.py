#!/usr/bin/env python3
"""Discover Apple's HIG and validate a versioned, independently reviewed package.

The skill itself is Markdown-only. This authoring utility uses the standard
library; PyYAML is optional for stricter frontmatter validation.
"""
import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
APPLE = "https://developer.apple.com"
PREFIX = "/design/human-interface-guidelines"
NAV = APPLE + "/tutorials/data/index/design--human-interface-guidelines"
NEWS = APPLE + "/design/whats-new/"
KNOWN = {"heading", "paragraph", "text", "strong", "emphasis", "reference",
         "image", "video", "row", "table", "unorderedList", "orderedList",
         "listItem", "links", "codeVoice", "aside", "tabNavigator", "small",
         "codeListing", "thematicBreak", "termList", "subscript", "superscript",
         "strikethrough", "lineBreak", "step", "tutorialSection"}
METADATA_HEADINGS = {"resources", "related", "see also", "change log", "changelog", "revision history"}


class SourceError(ValueError):
    """A source cannot be faithfully accounted for."""


def digest(value):
    if not isinstance(value, bytes):
        value = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    return hashlib.sha256(value).hexdigest()


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def read_json(path):
    return json.loads(pathlib.Path(path).read_text())


def write_json(path, value):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def media_representations(reference):
    """Freeze source asset identities and appearance/resolution traits."""
    representations = []
    variants = reference.get("variants", [])
    if not isinstance(variants, list):
        raise SourceError("Media variants must be an array")
    for variant in variants:
        if not isinstance(variant, dict):
            raise SourceError("Media variant must be an object")
        url, traits = variant.get("url"), variant.get("traits", [])
        if not isinstance(url, str) or not url or not isinstance(traits, list) or any(not isinstance(t, str) for t in traits):
            raise SourceError("Media variant requires a URL and an array of traits")
        if url.startswith(("/images/", "/videos/", "images/", "videos/")):
            url = APPLE + "/tutorials/" + url.lstrip("/")
        else:
            url = urllib.parse.urljoin(APPLE + "/tutorials/", url)
        representations.append({"url": url, "traits": list(traits)})
    return representations


def extract(doc):
    """Account for nested source units without publishing Apple's prose."""
    result = {"headings": [], "units": [], "media": [], "external_links": []}
    def visit(node, path, context=(), state=("overview", "guidance")):
        section, treatment = state
        if isinstance(node, list):
            for i, child in enumerate(node):
                state = visit(child, f"{path}/{i}", context, state)
            return state
        if not isinstance(node, dict):
            return state
        kind = node.get("type")
        if kind and kind not in KNOWN:
            raise SourceError(f"Unsupported DocC node {kind!r} at {path}")
        if kind == "heading":
            section = node.get("anchor") or node.get("text", "")
            if not section:
                raise SourceError(f"Heading without anchor or text at {path}")
            result["headings"].append({"anchor": section, "title": node.get("text", ""), "level": node.get("level", 2)})
            if node.get("level", 2) == 2:
                treatment = "metadata" if node.get("text", "").casefold() in METADATA_HEADINGS else "guidance"
        state = (section, treatment)
        if kind in {"paragraph", "table", "aside", "unorderedList", "orderedList", "tabNavigator", "codeListing", "termList", "image", "video"}:
            result["units"].append({"id": path, "kind": kind, "section": section,
                                    "context": list(context), "hash": digest(node), "treatment": treatment})
        if kind in {"image", "video"}:
            identifier = node.get("identifier", "")
            ref = doc.get("references", {}).get(identifier, {})
            result["media"].append({"id": path, "identifier": identifier, "kind": kind,
                                    "section": section, "context": list(context), "treatment": treatment,
                                    "reference_metadata_hash": digest(ref), "representations": media_representations(ref),
                                    "status": "pending"})
        if kind == "tabNavigator":
            for i, tab in enumerate(node.get("tabs", [])):
                visit(tab.get("content", []), f"{path}/tabs/{i}/content", context + (tab.get("title", ""),), state)
            return state
        for key, child in node.items():
            if isinstance(child, (dict, list)):
                visit(child, f"{path}/{key}", context, state)
        return state

    for i, content in enumerate(doc.get("primaryContentSections", [])):
        visit(content.get("content", []), f"primaryContentSections/{i}/content")
    for identifier, ref in doc.get("references", {}).items():
        url = ref.get("url", "")
        normalized = urllib.parse.urlparse(urllib.parse.urljoin(APPLE, url))
        internal = normalized.hostname == "developer.apple.com" and normalized.path.casefold().startswith(PREFIX)
        if url and not internal and not url.startswith("doc://com.apple.HIG/"):
            if url.startswith(("https://", "/documentation/", "/videos/", "/design/")):
                result["external_links"].append({"url": urllib.parse.urljoin(APPLE, url), "title": ref.get("title", identifier)})
    return result


def review_valid(review, source_hash, destination_hash):
    return bool(review and review.get("status") == "reviewed"
                and review.get("reviewer") and review.get("source_hash") == source_hash
                and review.get("destination_hash") == destination_hash)


def approval_record(root, page):
    path = pathlib.Path(root) / "coverage" / "reviews" / (page["slug"] + ".json")
    record = read_json(path) if path.is_file() else {"review": page.get("review", {}), "media": {}}
    for directory in ("media-reviews", "image-reviews"):
        media_path = pathlib.Path(root) / "coverage" / directory / (page["slug"] + ".json")
        if media_path.is_file():
            media = read_json(media_path)
            if media.get("source_hash") == page.get("source_hash"):
                record.setdefault("media", {}).update(media.get("media", {}))
    return record


def anchors(text):
    explicit = set(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)', text))
    for title in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        explicit.add(slug)
    return explicit


def link_errors(package):
    package = pathlib.Path(package).resolve()
    errors = []
    for path in package.rglob("*.md"):
        text = path.read_text()
        for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", text):
            if target.startswith(("http:", "https:", "mailto:", "data:")):
                continue
            target = target.strip("<>")
            filename, _, fragment = target.partition("#")
            dest = (path.parent / urllib.parse.unquote(filename)).resolve() if filename else path.resolve()
            if not dest.is_relative_to(package):
                errors.append(f"{path.relative_to(package)}: link outside package: {target}")
            elif not dest.is_file():
                errors.append(f"{path.relative_to(package)}: missing local file: {target}")
            elif fragment and urllib.parse.unquote(fragment) not in anchors(dest.read_text()):
                errors.append(f"{path.relative_to(package)}: missing anchor: {target}")
    return errors


def reachable_files(package):
    package = pathlib.Path(package).resolve()
    seen = set()
    pending = [package / "SKILL.md"]
    while pending:
        path = pending.pop()
        if path in seen or not path.is_file() or not path.is_relative_to(package):
            continue
        seen.add(path)
        if path.suffix != ".md":
            continue
        for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", path.read_text()):
            if target.startswith(("http:", "https:", "mailto:", "data:")):
                continue
            filename = urllib.parse.unquote(target.strip("<>").partition("#")[0])
            pending.append((path.parent / filename).resolve() if filename else path)
    return seen


def fetch(url):
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "apple-hig-skills/1.0 (source coverage verification)"})
            with urllib.request.urlopen(request, timeout=45) as response:
                return response.read(), response.url, dict(response.headers)
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def navigation(data):
    pages = {}

    def visit(node, family=None):
        path = node.get("path", "")
        slug = path.rsplit("/", 1)[-1]
        if node.get("type") == "collection" and slug != "components":
            family = slug
        if path.startswith(PREFIX):
            pages[path] = {"slug": slug, "title": node["title"], "type": node.get("type", "collection"),
                           "module": family, "path": path}
        for child in node.get("children", []):
            visit(child, family)

    for node in data["interfaceLanguages"]["swift"]:
        visit(node)
    if not any(p["type"] == "article" for p in pages.values()):
        raise SourceError("Empty or malformed HIG navigator: no articles discovered")
    return pages


def validate_document(doc, path):
    if not isinstance(doc, dict):
        raise SourceError("DocC document must be a JSON object")
    identifier = doc.get("identifier")
    metadata = doc.get("metadata")
    content = doc.get("primaryContentSections")
    if not isinstance(identifier, dict) or not isinstance(identifier.get("url"), str):
        raise SourceError("DocC source is missing its document identifier")
    identity = urllib.parse.urlparse(identifier["url"])
    if identity.scheme != "doc" or identity.netloc.casefold() != "com.apple.hig" or identity.path.casefold().rstrip("/") != path.casefold().rstrip("/"):
        raise SourceError("DocC document identity does not match the requested HIG route")
    if not isinstance(metadata, dict) or not isinstance(metadata.get("title"), str) or not metadata["title"]:
        raise SourceError("DocC source is missing its title")
    if not isinstance(content, list) or any(not isinstance(c, dict) for c in content):
        raise SourceError("DocC primaryContentSections must be an array of content sections")
    if not isinstance(doc.get("references", {}), dict):
        raise SourceError("DocC references must be an object")


def source_links(doc):
    for ref in doc.get("references", {}).values():
        path = urllib.parse.urlparse(ref.get("url", "")).path.rstrip("/")
        if path.startswith(PREFIX) and ref.get("type") == "topic":
            yield path, ref.get("title", path.rsplit("/", 1)[-1])


def discover(root=ROOT, offline=False, output=None):
    root = pathlib.Path(root)
    cache = root / ".cache" / "apple"
    research = root / ".cache" / "research"
    cache.mkdir(parents=True, exist_ok=True)
    research.mkdir(parents=True, exist_ok=True)
    if offline:
        nav = read_json(research / "navigator.json")
        news = (research / "whats-new.html").read_text()
    else:
        raw, _, _ = fetch(NAV)
        (research / "navigator.json").write_bytes(raw)
        nav = json.loads(raw)
        raw, _, _ = fetch(NEWS)
        (research / "whats-new.html").write_bytes(raw)
        news = raw.decode()
    pages = navigation(nav)
    old_path = root / "coverage" / "manifest.json"
    old = read_json(old_path) if old_path.exists() else {}
    previous = {p["path"]: p for p in old.get("pages", [])}
    observed = {}

    def load(page):
        page = dict(page)
        try:
            file = cache / (page["slug"] + ".json")
            if offline:
                raw = file.read_bytes()
                headers = {}
            else:
                raw, _, headers = fetch(APPLE + "/tutorials/data" + page["path"] + ".json")
                file.write_bytes(raw)
            doc = json.loads(raw)
            validate_document(doc, page["path"])
            extraction = extract(doc)
            if page["type"] == "article" and not any(u["treatment"] == "guidance" for u in extraction["units"]):
                raise SourceError("Article source contains no substantive content")
            headers = {key.casefold(): value for key, value in headers.items()}
            page.update({"status": "fetched", "source_hash": digest(doc), "retrieved_at": now(),
                         "source_url": APPLE + page["path"], "etag": headers.get("etag"),
                         "last_modified": headers.get("last-modified"), "extraction": extraction})
            page["platforms"] = doc.get("metadata", {}).get("customMetadata", {}).get("supported-platforms", "")
            if page["type"] == "article":
                if not page.get("module"):
                    raise SourceError("New article has no assigned family")
                page["destination"] = f'skills/apple-hig/subskills/apple-hig-{page["module"]}/references/{page["slug"]}.md'
            else:
                page["destination"] = "skills/apple-hig/references/topic-index.md"
            prior = previous.get(page["path"], {})
            page["review"] = prior.get("review", {"status": "pending"})
            prior_media = {m["id"]: m for m in prior.get("extraction", {}).get("media", [])}
            for media in page["extraction"]["media"]:
                earlier = prior_media.get(media["id"], {})
                if earlier.get("reference_metadata_hash") == media["reference_metadata_hash"] and prior.get("source_hash") == page["source_hash"]:
                    for key in ("status", "reviewer", "evidence", "treatment", "review_method", "binary_hash"):
                        if key in earlier:
                            media[key] = earlier[key]
            return page, list(source_links(doc))
        except (OSError, ValueError, SourceError) as error:
            page.update({"status": "error", "error": str(error)})
            return page, []

    pending = list(pages.values())
    while pending:
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(load, pending))
        pending = []
        for page, links in results:
            observed[page["path"]] = page
            for path, title in links:
                if path not in pages:
                    item = {"path": path, "slug": path.rsplit("/", 1)[-1], "title": title,
                            "type": "article", "module": None}
                    pages[path] = item
                    pending.append(item)
    for path, prior in previous.items():
        if path not in observed:
            missing = dict(prior)
            missing.update({"status": "missing-from-discovery", "error": "Prior route absent from discovery; explicit removal reconciliation required"})
            observed[path] = missing
    history = []
    for path in sorted(set(re.findall(PREFIX + r"/[a-z0-9-]+", news)) - pages.keys()):
        record = {"requested_url": APPLE + path}
        if offline:
            cached = read_json(research / "inventory.json") if (research / "inventory.json").exists() else {}
            record.update(next((h for h in cached.get("historical", []) if h.get("requested_url") == record["requested_url"]), {"status": "unverified"}))
            if record.get("canonical_url") and record.get("status") == 200:
                record["status"] = "redirect"
            elif "404" in record.get("error", ""):
                record.update({"status": "unavailable", "http_status": 404})
        else:
            try:
                _, canonical, _ = fetch(record["requested_url"])
                record.update({"canonical_url": canonical, "status": "redirect" if canonical != record["requested_url"] else "live-unindexed"})
                if urllib.parse.urlparse(canonical).path not in pages:
                    record["needs_review"] = True
            except urllib.error.HTTPError as error:
                record.update({"status": "unavailable" if error.code == 404 else "error", "http_status": error.code})
            except OSError as error:
                record.update({"status": "error", "error": str(error)})
        history.append(record)
    result = {"schema_version": 1, "snapshot_at": now(), "scope": "Current English Apple Human Interface Guidelines",
              "discovery_seeds": [NAV, APPLE + PREFIX, NEWS],
              "pages": sorted(observed.values(), key=lambda p: p["path"]), "historical": history}
    result["discovery_hash"] = digest([p["path"] for p in result["pages"]])
    output = pathlib.Path(output) if output else old_path
    write_json(output, result)
    return result


def live_media_errors(root, manifest):
    """Verify the exact independently inspected representations, including variants."""
    assets = {}
    errors = []

    def collect(node):
        if isinstance(node, list):
            for child in node:
                collect(child)
        elif isinstance(node, dict):
            url, fingerprint = node.get("asset_url"), node.get("binary_hash")
            if url and fingerprint:
                if isinstance(fingerprint, str):
                    fingerprint = fingerprint.lower()
                if url in assets and assets[url] != fingerprint:
                    errors.append(f"Conflicting reviewed media fingerprints: {url}")
                assets[url] = fingerprint
            for child in node.values():
                if isinstance(child, (dict, list)):
                    collect(child)

    for page in manifest["pages"]:
        collect(approval_record(root, page).get("media", {}))

    def verify(item):
        url, expected = item
        try:
            raw, _, _ = fetch(url)
            return f"Live media drift requires review: {url}" if digest(raw) != expected else None
        except OSError as error:
            return f"Live media fetch failed: {url}: {error}"

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        errors.extend(error for error in pool.map(verify, assets.items()) if error)
    return errors


def publication_errors(root):
    """Inspect publishable source-tree files; raw-source caches are excluded."""
    root = pathlib.Path(root)
    errors = []
    ignored = {".git", ".cache", ".venv", "__pycache__", ".superpowers"}
    media = {".mp4", ".mov", ".png", ".jpg", ".jpeg", ".webp", ".heic", ".gif", ".wav", ".mp3", ".aiff",
             ".svg", ".tif", ".tiff", ".pdf"}
    for directory, folders, files in os.walk(root):
        folders[:] = [name for name in folders if name not in ignored]
        for filename in files:
            path = pathlib.Path(directory) / filename
            if path.suffix.casefold() in media:
                errors.append(f"Downloaded media cannot be published: {path.relative_to(root)}")
            elif path.suffix == ".json":
                try:
                    data = read_json(path)
                except (OSError, ValueError):
                    continue
                if isinstance(data, dict) and "primaryContentSections" in data and "identifier" in data:
                    errors.append(f"Raw DocC source cannot be published: {path.relative_to(root)}")
    return errors


def media_review_issues(root, package, reachable, media, observed):
    """Bind inspected assets and every appearance to their frozen source uses."""
    errors, pending = [], []
    label = f'media {media["identifier"]}'

    def text_present(value):
        return isinstance(value, str) and bool(value.strip())

    def fingerprint_valid(value):
        return isinstance(value, str) and re.fullmatch(r"[0-9a-fA-F]{64}", value) is not None

    representations = media.get("representations")
    groups_by_url = {}
    if not isinstance(representations, list) or not representations:
        pending.append(f"{label}: frozen source media representations missing")
        representations = []
    for representation in representations:
        if not isinstance(representation, dict):
            pending.append(f"{label}: invalid frozen source media representation")
            continue
        url, traits = representation.get("url"), representation.get("traits")
        if not text_present(url) or not isinstance(traits, list) or any(not isinstance(t, str) for t in traits):
            pending.append(f"{label}: invalid frozen source media representation")
            continue
        group = tuple(sorted(t for t in traits if t not in {"1x", "2x", "3x"}))
        groups_by_url.setdefault(url, set()).add(group)

    def inspected(record, kind):
        valid = isinstance(record, dict)
        if not valid:
            pending.append(f"{label}: {kind} inspection record missing")
            return False
        for field in ("review_method", "reviewer", "evidence"):
            if not text_present(record.get(field)):
                pending.append(f"{label}: {kind} {field} missing")
                valid = False
        if record.get("status") != "reviewed":
            pending.append(f"{label}: {kind} review pending")
            valid = False
        url = record.get("asset_url")
        if not text_present(url) or url not in groups_by_url or urllib.parse.urlparse(url).scheme not in {"http", "https"}:
            pending.append(f"{label}: {kind} asset URL missing or outside frozen source representations")
            valid = False
        if not fingerprint_valid(record.get("binary_hash")):
            pending.append(f"{label}: {kind} binary hash missing or invalid")
            valid = False
        return valid

    covered = set()
    if inspected(observed, "primary media"):
        covered.update(groups_by_url[observed["asset_url"]])
    occurrences = observed.get("reviewed_occurrence_ids")
    if not isinstance(occurrences, list) or media["id"] not in occurrences:
        pending.append(f'{label}: substantive media occurrence review missing: {media["id"]}')

    variants = observed.get("appearance_variants", [])
    if not isinstance(variants, list):
        pending.append(f"{label}: appearance inspection records must be an array")
        variants = []
    for variant in variants:
        if inspected(variant, "appearance media"):
            covered.update(groups_by_url[variant["asset_url"]])
    expected = set().union(*groups_by_url.values()) if groups_by_url else set()
    disposition = observed.get("appearance_variant_disposition")
    reasoned = text_present(disposition) or (isinstance(disposition, dict) and any(text_present(v) for v in disposition.values()))
    decorative = observed.get("classification") == "decorative" and reasoned
    if expected - covered and not decorative:
        pending.append(f"{label}: expected appearance review missing: {sorted(expected - covered)}")

    supports = observed.get("supporting_files")
    if not isinstance(supports, list) or not supports:
        pending.append(f"{label}: media supporting files missing")
        supports = []
    for support in supports:
        if not isinstance(support, dict) or not text_present(support.get("path")) or not fingerprint_valid(support.get("hash")):
            pending.append(f"{label}: media supporting file path/hash missing or invalid")
            continue
        target = (root / support["path"]).resolve()
        if not target.is_relative_to(package.resolve()) or not target.is_file() or digest(target.read_bytes()) != support["hash"].lower():
            pending.append(f'{label}: media supporting file review missing or stale: {support["path"]}')
        elif target not in reachable:
            errors.append(f'{label}: media supporting file unreachable: {support["path"]}')
    return errors, pending


def check(root=ROOT, live=False, allow_pending=False):
    root = pathlib.Path(root)
    manifest = read_json(root / "coverage" / "manifest.json")
    package = root / "skills" / "apple-hig"
    errors = link_errors(package) + publication_errors(root)
    if not manifest.get("pages") or not any(p.get("type") == "article" for p in manifest["pages"]):
        errors.append("Empty HIG source inventory cannot establish coverage")
    expected_fingerprint = digest(sorted(p["path"] for p in manifest.get("pages", [])))
    if manifest.get("pages") and manifest.get("discovery_hash") != expected_fingerprint:
        errors.append("Recorded discovery fingerprint does not match the source route inventory")
    reachable = reachable_files(package)
    if not (package / "SKILL.md").is_file():
        errors.append("Missing package root SKILL.md")
    pending = []
    for skill in package.rglob("SKILL.md"):
        text = skill.read_text()
        match = re.match(r"---\n(.*?)\n---\n", text, re.S)
        if not match:
            errors.append(f"{skill.relative_to(root)}: missing YAML frontmatter")
            continue
        try:
            import yaml
        except ImportError:
            front = dict(re.findall(r"^(name|description):\s*(.+)$", match.group(1), re.M))
        else:
            try:
                front = yaml.safe_load(match.group(1))
            except yaml.YAMLError as error:
                errors.append(f"{skill.relative_to(root)}: invalid YAML: {error}")
                continue
        if not isinstance(front, dict):
            errors.append(f"{skill.relative_to(root)}: frontmatter must be a mapping")
            continue
        name = front.get("name", "")
        description = front.get("description", "")
        if name != skill.parent.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            errors.append(f"{skill.relative_to(root)}: invalid/mismatched skill name")
        if not isinstance(description, str) or not 1 <= len(description) <= 1024:
            errors.append(f"{skill.relative_to(root)}: invalid description")
        if len(text.splitlines()) >= 500:
            errors.append(f"{skill.relative_to(root)}: entrypoint must stay under 500 lines")
        if re.search(r"\[TODO:|\bTBD\b", text):
            errors.append(f"{skill.relative_to(root)}: unfinished scaffold")
    for page in manifest["pages"]:
        if page.get("status") != "fetched":
            errors.append(f'{page["slug"]}: source fetch failed: {page.get("error")}')
            continue
        dest = root / page["destination"]
        if not dest.is_file():
            errors.append(f'{page["slug"]}: missing destination {page["destination"]}')
            continue
        if dest.resolve() not in reachable:
            errors.append(f'{page["slug"]}: destination unreachable from package router')
        text = dest.read_text()
        if page["type"] == "article":
            family_skill = dest.parent.parent / "SKILL.md"
            if family_skill.resolve() not in reachable:
                errors.append(f'{page["slug"]}: family SKILL.md missing or unreachable')
            local_anchors = anchors(text)
            for heading in page["extraction"]["headings"]:
                if heading["anchor"] not in local_anchors:
                    errors.append(f'{page["slug"]}: source heading not mapped: {heading["anchor"]}')
            record = approval_record(root, page)
            review = record.get("review", {})
            approved = review_valid(review, page["source_hash"], digest(dest.read_bytes()))
            if not approved:
                pending.append(f'{page["slug"]}: independent semantic review pending or stale')
            reviewed_units = {u["id"]: u for u in review.get("units", [])}
            for unit in page["extraction"].get("units", []):
                if unit["treatment"] == "metadata":
                    continue
                reviewed = reviewed_units.get(unit["id"], {})
                if reviewed.get("status") != "reviewed" or reviewed.get("source_unit_hash") != unit["hash"] or reviewed.get("source_anchor") != unit["section"] or not reviewed.get("evidence"):
                    pending.append(f'{page["slug"]}: substantive unit review missing or stale: {unit["id"]}')
                    continue
                target = (root / reviewed.get("destination", page["destination"])).resolve()
                if not target.is_relative_to(package.resolve()) or not target.is_file():
                    errors.append(f'{page["slug"]}: invalid unit destination: {unit["id"]}')
                elif reviewed.get("destination_anchor") and reviewed["destination_anchor"] not in anchors(target.read_text()):
                    errors.append(f'{page["slug"]}: unit destination anchor missing: {unit["id"]}')
                elif target != dest.resolve() and reviewed.get("destination_hash") != digest(target.read_bytes()):
                    pending.append(f'{page["slug"]}: supplementary unit destination review missing or stale: {unit["id"]}')
            for media in page["extraction"]["media"]:
                if media["treatment"] == "metadata":
                    continue
                observed = record.get("media", {}).get(media["identifier"], media)
                if not approved or observed.get("status") != "reviewed" or not observed.get("reviewer") or not observed.get("evidence") or observed.get("reference_metadata_hash") != media.get("reference_metadata_hash"):
                    pending.append(f'{page["slug"]}: media review pending: {media["identifier"]}')
                media_errors, media_pending = media_review_issues(root, package, reachable, media, observed)
                errors.extend(f'{page["slug"]}: {error}' for error in media_errors)
                pending.extend(f'{page["slug"]}: {issue}' for issue in media_pending)
    for historical in manifest.get("historical", []):
        if historical.get("needs_review") or historical.get("status") in {"error", "unverified", "live-unindexed"}:
            errors.append(f'Unresolved historical source: {historical["requested_url"]}')
    if live:
        latest = discover(root, output=root / ".cache" / "live-manifest.json")
        old = {p["path"]: p for p in manifest["pages"]}
        new = {p["path"]: p for p in latest["pages"]}
        for path in sorted(old.keys() | new.keys()):
            if path not in old or path not in new or old[path].get("source_hash") != new[path].get("source_hash") or new.get(path, {}).get("status") != "fetched":
                errors.append(f"Live source drift requires review: {path}")
        def history_state(records):
            return sorted((h["requested_url"], h.get("status"), h.get("canonical_url"), h.get("http_status")) for h in records)
        if history_state(manifest.get("historical", [])) != history_state(latest.get("historical", [])):
            errors.append("Live historical source/redirect drift requires review")
        errors.extend(live_media_errors(root, manifest))
    if not allow_pending:
        errors.extend(pending)
    return {"errors": errors, "pending": pending, "pages": len(manifest["pages"]),
            "articles": sum(p["type"] == "article" for p in manifest["pages"])}


def report(root=ROOT):
    root = pathlib.Path(root)
    manifest = read_json(root / "coverage" / "manifest.json")
    media_dir = root / "skills" / "apple-hig" / "references" / "media"
    media_dir.mkdir(parents=True, exist_ok=True)
    sources = {p["slug"]: p for p in manifest["pages"]}
    media_index = ["# Original explanations of HIG visual examples", "",
                   "Read the relevant article guide first. These original supplementary notes",
                   "preserve lessons from inspected source demonstrations. Apple assets are not",
                   "bundled. The coverage report records actual review status and limitations.", "",
                   "| Topic | Visual explanation | Article guide |", "|---|---|---|"]
    for note in sorted(media_dir.glob("*.md")):
        slug = note.stem if note.stem in sources else note.stem.removesuffix("-images")
        if note.name == "index.md" or slug not in sources:
            continue
        source = sources[slug]
        local = f'../../subskills/apple-hig-{source["module"]}/references/{slug}.md'
        media_index.append(f'| {source["title"]} | [Examples]({note.name}) | [Guide]({local}) |')
    (media_dir / "index.md").write_text("\n".join(media_index) + "\n")
    result = check(root, allow_pending=True)
    articles = [p for p in manifest["pages"] if p["type"] == "article"]
    reviewed = sum(review_valid(approval_record(root, p).get("review"), p.get("source_hash"), digest((root / p["destination"]).read_bytes()))
                   for p in articles if (root / p["destination"]).is_file())
    lines = ["# Coverage report", "", f'Source snapshot: **{manifest["snapshot_at"]}**.', "",
             f'Current corpus: **{len(manifest["pages"])} pages; {len(articles)} articles**.',
             f'Independent article reviews valid: **{reviewed}/{len(articles)}**.',
             f'Outstanding review items (including media): **{len(result["pending"])}**.',
             f'Structural/source errors: **{len(result["errors"])}**.', "",
             "Completeness: **complete for this snapshot**." if not result["pending"] and not result["errors"] else "Completeness: **review in progress; do not claim full substantive coverage**.", "",
             "## Article treatment", "", "| Article | Family | Local guide | Review |", "|---|---|---|---|"]
    for p in articles:
        dest = root / p["destination"]
        valid = dest.exists() and review_valid(approval_record(root, p).get("review"), p["source_hash"], digest(dest.read_bytes()))
        lines.append(f'| [{p["title"]}]({p["source_url"]}) | {p["module"]} | [Guide](../{p["destination"]}) | {"Reviewed" if valid else "Pending"} |')
    lines += ["", "## Historical links", ""]
    for h in manifest.get("historical", []):
        lines.append(f'- {h["requested_url"]}: {h.get("status", h.get("error", "unknown"))}' + (f' → {h["canonical_url"]}' if h.get("canonical_url") else ""))
    lines += ["", "## Review boundaries", "", "Counts prove source accounting, not semantic fidelity. Article and media review must be independently recorded. Historical and external sources are outside the current-article denominator. See [audit method](audit.md).", ""]
    (root / "coverage" / "REPORT.md").write_text("\n".join(lines))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["discover", "check", "check-skills", "report"])
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument("--offline", action="store_true", help="Discover from previously fetched source cache")
    parser.add_argument("--output", type=pathlib.Path)
    parser.add_argument("--live", action="store_true", help="Verify current source content without changing the tracked manifest")
    parser.add_argument("--allow-pending", action="store_true", help="Development check: permit explicitly pending semantic/media review")
    args = parser.parse_args()
    try:
        if args.command == "check-skills":
            from capabilities import check as check_capabilities
            result = check_capabilities(args.root, allow_pending=args.allow_pending)
            print(json.dumps(result, indent=2))
            return int(bool(result["errors"]))
        if args.command == "discover":
            result = discover(args.root, args.offline, args.output)
            print(json.dumps({"pages": len(result["pages"]), "errors": [p["slug"] for p in result["pages"] if p.get("status") != "fetched"]}, indent=2))
            return int(any(p.get("status") != "fetched" for p in result["pages"]))
        result = check(args.root, args.live, args.allow_pending) if args.command == "check" else report(args.root)
        summary = dict(result)
        summary["pending_count"] = len(result["pending"])
        summary["pending"] = result["pending"][:20]
        if len(result["errors"]) > 30:
            summary["error_count"] = len(result["errors"])
            summary["errors"] = result["errors"][:30]
        print(json.dumps(summary, indent=2))
        return int(bool(result["errors"])) if args.command == "check" else 0
    except (OSError, ValueError, KeyError) as error:
        print(f"hig: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
