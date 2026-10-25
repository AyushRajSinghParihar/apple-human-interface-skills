"""Behavioral contracts for source accounting and portable package checks."""
import copy
import importlib.util
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "hig.py"
spec = importlib.util.spec_from_file_location("hig", SCRIPT)
hig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hig)


class ExtractionTests(unittest.TestCase):
    def test_media_representations_freeze_source_urls_and_traits(self):
        doc = {"references": {
            "example.png": {"type": "image", "variants": [
                {"url": "/images/light.png", "traits": ["2x", "light"]},
                {"url": "https://cdn.example.com/dark.png", "traits": ["2x", "dark"]}]},
            "clip.mp4": {"type": "video", "variants": [
                {"url": "/videos/clip.mp4", "traits": ["1x", "light"]}]}},
            "primaryContentSections": [{"content": [
                {"type": "image", "identifier": "example.png"},
                {"type": "video", "identifier": "clip.mp4"}]}]}
        media = hig.extract(doc)["media"]
        self.assertEqual(media[0].get("representations"), [
            {"url": "https://developer.apple.com/tutorials/images/light.png", "traits": ["2x", "light"]},
            {"url": "https://cdn.example.com/dark.png", "traits": ["2x", "dark"]}])
        self.assertEqual(media[1].get("representations"), [
            {"url": "https://developer.apple.com/tutorials/videos/clip.mp4", "traits": ["1x", "light"]}])

    def test_nested_platform_tab_table_and_media_are_accounted_for(self):
        doc = {"references": {"example.png": {"type": "image", "alt": "Two controls", "variants": []}},
               "primaryContentSections": [{"kind": "content", "content": [
                   {"type": "heading", "text": "watchOS", "anchor": "watchOS", "level": 2},
                   {"type": "tabNavigator", "tabs": [{"title": "Small", "content": [
                       {"type": "table", "rows": [[[{
                           "type": "paragraph", "inlineContent": [{"type": "text", "text": "44 pt"}]
                       }]]]},
                       {"type": "aside", "content": [{"type": "paragraph", "inlineContent": [
                           {"type": "text", "text": "Retain an alternate input."}]}]},
                       {"type": "paragraph", "inlineContent": [{"type": "image", "identifier": "example.png"}]}
                   ]}]}]}]}
        result = hig.extract(doc)
        self.assertEqual(result["headings"], [{"anchor": "watchOS", "title": "watchOS", "level": 2}])
        self.assertTrue(any(u["kind"] == "table" for u in result["units"]))
        self.assertTrue(any(u["kind"] == "aside" for u in result["units"]))
        self.assertEqual(result["media"][0]["identifier"], "example.png")
        self.assertTrue(all(u["section"] == "watchOS" for u in result["units"]))
        self.assertTrue(any("Small" in u["context"] for u in result["units"]))

    def test_unknown_content_is_an_explicit_error(self):
        with self.assertRaisesRegex(hig.SourceError, "newInteractiveDiagram"):
            hig.extract({"primaryContentSections": [{"content": [{"type": "newInteractiveDiagram"}]}]})

    def test_changed_numeric_fact_invalidates_content_fingerprint(self):
        original = {"primaryContentSections": [{"content": [{"type": "table", "rows": [[[{
            "type": "paragraph", "inlineContent": [{"type": "text", "text": "44 pt"}]}]]]}]}]}
        changed = copy.deepcopy(original)
        changed["primaryContentSections"][0]["content"][0]["rows"][0][0][0]["inlineContent"][0]["text"] = "44 px"
        self.assertNotEqual(hig.extract(original)["units"][0]["hash"], hig.extract(changed)["units"][0]["hash"])

    def test_resource_links_are_distinguished_from_substantive_guidance(self):
        result = hig.extract({"primaryContentSections": [{"content": [
            {"type": "heading", "text": "Resources", "anchor": "Resources", "level": 2},
            {"type": "paragraph", "inlineContent": [{"type": "text", "text": "Related API documentation"}]}
        ]}]})
        self.assertTrue(all(u["treatment"] == "metadata" for u in result["units"]))

    def test_absolute_hig_links_are_internal_and_external_dependencies_survive(self):
        result = hig.extract({"references": {
            "one": {"url": "https://developer.apple.com/design/human-interface-guidelines/buttons#iOS", "title": "Buttons"},
            "two": {"url": "/design/human-interface-guidelines/icons", "title": "Icons"},
            "three": {"url": "/documentation/swiftui/button", "title": "Button API"}
        }})
        self.assertEqual(result["external_links"], [{"url": "https://developer.apple.com/documentation/swiftui/button", "title": "Button API"}])

    def test_nested_column_headings_do_not_leak_into_sibling_columns(self):
        result = hig.extract({"primaryContentSections": [{"content": [
            {"type": "heading", "text": "Shared", "anchor": "Shared", "level": 2},
            {"type": "row", "columns": [
                {"content": [{"type": "heading", "text": "First", "anchor": "First", "level": 3},
                             {"type": "paragraph", "inlineContent": [{"type": "text", "text": "A"}]}]},
                {"content": [{"type": "paragraph", "inlineContent": [{"type": "text", "text": "B"}]}]}
            ]},
            {"type": "paragraph", "inlineContent": [{"type": "text", "text": "After row"}]}
        ]}]})
        sections = [u["section"] for u in result["units"] if u["kind"] == "paragraph"]
        self.assertEqual(sections, ["First", "Shared", "Shared"])


class ReviewTests(unittest.TestCase):
    def package_fixture(self, root):
        package = root / "skills" / "apple-hig"
        family = package / "subskills" / "apple-hig-content"
        (family / "references").mkdir(parents=True)
        (package / "SKILL.md").write_text('---\nname: apple-hig\ndescription: Design Apple interfaces.\n---\n[Family](subskills/apple-hig-content/SKILL.md)\n')
        (family / "SKILL.md").write_text('---\nname: apple-hig-content\ndescription: Design content.\n---\n[Guide](references/charts.md)\n')
        guide = family / "references" / "charts.md"
        guide.write_text('# Charts\nExplain the underlying data clearly.\n')
        page = {"path": "/design/human-interface-guidelines/charts", "slug": "charts", "type": "article", "status": "fetched", "module": "content", "source_hash": "source", "destination": str(guide.relative_to(root)), "extraction": {"headings": [], "units": [], "media": []}, "review": {"status": "reviewed", "reviewer": "independent", "source_hash": "source", "destination_hash": hig.digest(guide.read_bytes())}}
        (root / "coverage").mkdir()
        hig.write_json(root / "coverage" / "manifest.json", {"pages": [page], "historical": [], "discovery_hash": hig.digest([page['path']])})
        return guide, package

    def media_fixture(self, root):
        _, package = self.package_fixture(root)
        note = package / 'visual.md'
        note.write_text('# Visual example\nExplains the motion in both appearances.\n')
        with (package / 'SKILL.md').open('a') as stream:
            stream.write('[Visual explanation](visual.md)\n')
        manifest = hig.read_json(root / 'coverage' / 'manifest.json')
        media = {'identifier': 'clip.mp4', 'id': 'video-1', 'kind': 'video', 'section': 'overview',
                 'treatment': 'guidance', 'reference_metadata_hash': 'metadata', 'representations': [
                     {'url': 'https://developer.apple.com/tutorials/videos/clip-1x.mp4', 'traits': ['1x', 'light']},
                     {'url': 'https://developer.apple.com/tutorials/videos/clip-2x.mp4', 'traits': ['2x', 'light']},
                     {'url': 'https://developer.apple.com/tutorials/videos/clip-dark.mp4', 'traits': ['2x', 'dark']}]}
        manifest['pages'][0]['extraction']['media'] = [media, dict(media, id='video-2')]
        approval = {'status': 'reviewed', 'reviewer': 'independent', 'evidence': 'Viewed the actual sequence.',
                    'reference_metadata_hash': 'metadata', 'review_method': 'Actual chronological frame inspection',
                    'asset_url': 'https://developer.apple.com/tutorials/videos/clip-2x.mp4', 'binary_hash': 'a' * 64,
                    'classification': 'guidance-bearing', 'reviewed_occurrence_ids': ['video-1', 'video-2'],
                    'supporting_files': [{'path': str(note.relative_to(root)), 'hash': hig.digest(note.read_bytes())}],
                    'appearance_variants': [{'status': 'reviewed', 'reviewer': 'independent',
                        'evidence': 'Compared the actual alternate sequence.', 'review_method': 'Actual alternate frame inspection',
                        'asset_url': 'https://developer.apple.com/tutorials/videos/clip-dark.mp4', 'binary_hash': 'b' * 64}]}
        hig.write_json(root / 'coverage' / 'manifest.json', manifest)
        self.write_media_approval(root, manifest, approval)
        return note, manifest, approval

    def write_media_approval(self, root, manifest, approval):
        hig.write_json(root / 'coverage' / 'reviews' / 'charts.json', {
            'review': manifest['pages'][0]['review'], 'media': {'clip.mp4': approval}})

    def test_media_provenance_cannot_be_deleted_or_replaced_with_placeholders(self):
        mutations = [('missing-' + field, lambda record, field=field: record.pop(field)) for field in (
            'review_method', 'asset_url', 'binary_hash', 'supporting_files', 'reviewed_occurrence_ids')]
        mutations += [
            ('invalid-hash', lambda record: record.update(binary_hash='g' * 64)),
            ('empty-method', lambda record: record.update(review_method='  ')),
            ('wrong-asset', lambda record: record.update(asset_url='https://example.com/unrelated.mp4')),
            ('empty-support', lambda record: record.update(supporting_files=[])),
            ('missing-support-hash', lambda record: record['supporting_files'][0].pop('hash')),
            ('missing-support-path', lambda record: record['supporting_files'][0].pop('path'))]
        for name, mutate in mutations:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = pathlib.Path(tmp)
                _, manifest, approval = self.media_fixture(root)
                self.assertEqual(hig.check(root)['errors'], [])
                mutate(approval)
                self.write_media_approval(root, manifest, approval)
                result = hig.check(root)
                self.assertTrue(any('media' in error.lower() for error in result['errors']), result)

    def test_media_approval_accounts_for_every_substantive_occurrence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            _, manifest, approval = self.media_fixture(root)
            self.assertEqual(hig.check(root)['errors'], [])
            approval['reviewed_occurrence_ids'].remove('video-2')
            self.write_media_approval(root, manifest, approval)
            self.assertTrue(any('occurrence' in error.lower() for error in hig.check(root)['errors']))

    def test_expected_appearance_cannot_be_hidden_by_removing_variant_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            _, manifest, approval = self.media_fixture(root)
            self.assertEqual(hig.check(root)['errors'], [])
            approval.pop('appearance_variants')
            self.write_media_approval(root, manifest, approval)
            self.assertTrue(any('appearance' in error.lower() for error in hig.check(root)['errors']))

    def test_each_appearance_requires_its_own_inspection_provenance(self):
        for field in ('asset_url', 'binary_hash', 'review_method', 'reviewer', 'evidence'):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as tmp:
                root = pathlib.Path(tmp)
                _, manifest, approval = self.media_fixture(root)
                self.assertEqual(hig.check(root)['errors'], [])
                approval['appearance_variants'][0].pop(field)
                self.write_media_approval(root, manifest, approval)
                self.assertTrue(any('appearance' in error.lower() for error in hig.check(root)['errors']))

    def test_resolution_variants_share_one_reviewed_appearance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            _, manifest, _ = self.media_fixture(root)
            manifest['pages'][0]['extraction']['media'][0]['representations'].append({
                'url': 'https://developer.apple.com/tutorials/videos/clip-3x.mp4', 'traits': ['3x', 'light']})
            hig.write_json(root / 'coverage' / 'manifest.json', manifest)
            self.assertEqual(hig.check(root)['errors'], [])

    def test_only_decorative_alternate_can_receive_a_reasoned_disposition(self):
        for classification, disposition, accepted in (
                ('decorative', 'Theme decoration adds no guidance.', True),
                ('decorative', {'reason': 'Theme decoration adds no guidance.'}, True),
                ('decorative', '', False),
                ('guidance-bearing', 'Both themes look similar.', False)):
            with self.subTest(classification=classification, disposition=disposition), tempfile.TemporaryDirectory() as tmp:
                root = pathlib.Path(tmp)
                _, manifest, approval = self.media_fixture(root)
                approval.pop('appearance_variants')
                approval.update(classification=classification, appearance_variant_disposition=disposition)
                self.write_media_approval(root, manifest, approval)
                result = hig.check(root)
                self.assertEqual(not result['errors'], accepted, result)

    def test_vector_print_and_tiff_assets_cannot_be_published(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.package_fixture(root)
            for extension in ('.svg', '.tif', '.tiff', '.pdf'):
                with self.subTest(extension=extension):
                    asset = root / ('downloaded' + extension)
                    asset.write_bytes(b'downloaded source asset')
                    self.assertTrue(any(asset.name in error for error in hig.publication_errors(root)))
                    asset.unlink()

    def test_package_gate_catches_modified_guidance_and_pending_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            guide, _ = self.package_fixture(root)
            self.assertEqual(hig.check(root)["errors"], [])
            guide.write_text('# Charts\nRead the official source.\n')
            self.assertTrue(hig.check(root)["errors"])
            self.assertEqual(hig.check(root, allow_pending=True)["errors"], [])
            self.assertTrue(hig.check(root, allow_pending=True)["pending"])

    def test_article_cannot_be_disconnected_from_router(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            _, package = self.package_fixture(root)
            (package / "SKILL.md").write_text('---\nname: apple-hig\ndescription: Design Apple interfaces.\n---\nNo routes.\n')
            self.assertTrue(any('unreachable' in e for e in hig.check(root)["errors"]))

    def test_malformed_frontmatter_is_reported_without_crashing_the_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            _, package = self.package_fixture(root)
            (package / "SKILL.md").write_text('---\nname: apple-hig\ndescription: "unterminated\n---\n')
            self.assertTrue(any('YAML' in e for e in hig.check(root)["errors"]))

    def test_source_access_failure_stays_in_coverage_denominator(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.package_fixture(root)
            file = root / "coverage" / "manifest.json"
            manifest = hig.read_json(file)
            manifest["pages"][0].update(status="error", error="HTTP 403")
            hig.write_json(file, manifest)
            result = hig.check(root)
            self.assertEqual(result["articles"], 1)
            self.assertTrue(any('HTTP 403' in e for e in result["errors"]))

    def test_empty_inventory_cannot_pass_strict_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.package_fixture(root)
            hig.write_json(root / 'coverage' / 'manifest.json', {'pages': [], 'historical': []})
            self.assertTrue(any('empty' in e.lower() for e in hig.check(root)['errors']))

    def test_raw_docc_source_cannot_be_published_outside_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.package_fixture(root)
            hig.write_json(root / 'accidental-apple-export.json', {'identifier': {'url': 'doc://com.apple.HIG/design/human-interface-guidelines/charts'}, 'primaryContentSections': []})
            self.assertTrue(any('raw' in e.lower() for e in hig.check(root)['errors']))

    def test_alternate_unit_destination_is_bound_to_its_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            _, package = self.package_fixture(root)
            note = package / 'additional.md'
            note.write_text('# Additional\nA material platform exception.\n')
            with (package / 'SKILL.md').open('a') as f:
                f.write('[Additional guidance](additional.md)\n')
            file = root / 'coverage' / 'manifest.json'
            manifest = hig.read_json(file)
            page = manifest['pages'][0]
            page['extraction']['units'] = [{'id': 'one', 'kind': 'paragraph', 'hash': 'fact', 'section': 'overview', 'treatment': 'guidance'}]
            page['review']['units'] = [{'id': 'one', 'source_unit_hash': 'fact', 'source_anchor': 'overview', 'status': 'reviewed', 'evidence': 'Reviewed exception', 'destination': str(note.relative_to(root)), 'destination_anchor': 'additional', 'destination_hash': hig.digest(note.read_bytes())}]
            hig.write_json(file, manifest)
            self.assertEqual(hig.check(root)['errors'], [])
            note.write_text('# Additional\nThe exception has disappeared.\n')
            self.assertTrue(any('destination' in e for e in hig.check(root)['errors']))

    def test_article_approval_cannot_hide_unreviewed_substantive_unit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.package_fixture(root)
            file = root / "coverage" / "manifest.json"
            manifest = hig.read_json(file)
            manifest["pages"][0]["extraction"]["units"] = [{"id": "unit-1", "kind": "paragraph", "section": "overview", "hash": "fact", "treatment": "guidance"}]
            hig.write_json(file, manifest)
            self.assertTrue(any('unit' in e for e in hig.check(root)["errors"]))

    def test_changed_supplementary_media_explanation_invalidates_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            note, _, _ = self.media_fixture(root)
            self.assertEqual(hig.check(root)["errors"], [])
            note.write_text('# Visual example\nDifferent meaning.\n')
            self.assertTrue(any('supporting' in e for e in hig.check(root)["errors"]))

    def test_review_must_preserve_source_section_association(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.package_fixture(root)
            file = root / "coverage" / "manifest.json"
            manifest = hig.read_json(file)
            page = manifest["pages"][0]
            page["extraction"]["units"] = [{"id": "one", "kind": "paragraph", "hash": "fact", "section": "watchOS", "treatment": "guidance"}]
            page["review"]["units"] = [{"id": "one", "source_unit_hash": "fact", "source_anchor": "overview", "status": "reviewed", "evidence": "Reviewed in a different section"}]
            hig.write_json(file, manifest)
            self.assertTrue(any('unit' in e for e in hig.check(root)["errors"]))

    def test_live_media_change_is_detected_even_when_document_url_is_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            _, manifest, _ = self.media_fixture(root)
            with patch.object(hig, 'fetch', return_value=(b'changed visual demonstration', 'https://developer.apple.com/tutorials/videos/clip-2x.mp4', {})):
                self.assertTrue(any('media drift' in e.lower() for e in hig.live_media_errors(root, manifest)))

    def test_live_media_accepts_hex_case_without_reporting_content_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            _, manifest, approval = self.media_fixture(root)
            # Independently known SHA-256 of the bytes b'abc', written in uppercase.
            fingerprint = 'BA7816BF8F01CFEA414140DE5DAE2223B00361A396177A9CB410FF61F20015AD'
            approval['binary_hash'] = fingerprint
            approval['appearance_variants'][0]['binary_hash'] = fingerprint
            self.write_media_approval(root, manifest, approval)
            with patch.object(hig, 'fetch', return_value=(b'abc', '', {})):
                self.assertEqual(hig.live_media_errors(root, manifest), [])

    def test_pending_appearance_cannot_be_hidden_by_primary_media_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            _, _, approval = self.media_fixture(root)
            approval['appearance_variants'][0]['status'] = 'pending'
            hig.write_json(root / 'coverage' / 'media-reviews' / 'charts.json', {
                'source_hash': 'source', 'media': {'clip.mp4': approval}
            })
            self.assertTrue(any('appearance' in e.lower() for e in hig.check(root)['errors']))

    def test_separate_media_reviews_merge_without_overwriting_textual_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.package_fixture(root)
            page = hig.read_json(root / 'coverage' / 'manifest.json')['pages'][0]
            hig.write_json(root / 'coverage' / 'media-reviews' / 'charts.json', {
                'source_hash': 'source', 'media': {'example.png': {'status': 'reviewed', 'evidence': 'Actual image inspected'}}
            })
            record = hig.approval_record(root, page)
            self.assertEqual(record['review']['reviewer'], 'independent')
            self.assertEqual(record['media']['example.png']['status'], 'reviewed')
            hig.write_json(root / 'coverage' / 'image-reviews' / 'charts.json', {
                'source_hash': 'source', 'media': {'other.png': {'status': 'reviewed', 'evidence': 'Actual other image inspected'}}
            })
            self.assertIn('other.png', hig.approval_record(root, page)['media'])

    def test_live_historical_redirect_change_requires_reconciliation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.package_fixture(root)
            file = root / 'coverage' / 'manifest.json'
            manifest = hig.read_json(file)
            manifest['historical'] = [{'requested_url': 'https://developer.apple.com/old', 'status': 'redirect', 'canonical_url': 'https://developer.apple.com/current'}]
            hig.write_json(file, manifest)
            changed = copy.deepcopy(manifest)
            changed['historical'][0]['canonical_url'] = 'https://developer.apple.com/different'
            with patch.object(hig, 'discover', return_value=changed):
                self.assertTrue(any('historical' in e.lower() for e in hig.check(root, live=True)['errors']))

    def test_approval_is_bound_to_source_and_destination(self):
        review = {"status": "reviewed", "source_hash": "source", "destination_hash": "guide", "reviewer": "independent"}
        self.assertTrue(hig.review_valid(review, "source", "guide"))
        self.assertFalse(hig.review_valid(review, "new-source", "guide"))
        self.assertFalse(hig.review_valid(review, "source", "new-guide"))
        self.assertFalse(hig.review_valid(dict(review, status="pending"), "source", "guide"))

    def test_relative_links_resolve_after_package_is_relocated(self):
        with tempfile.TemporaryDirectory() as tmp:
            package = pathlib.Path(tmp) / "anywhere" / "apple-hig"
            (package / "subskills").mkdir(parents=True)
            (package / "SKILL.md").write_text("Read [topic](subskills/topic.md#rules).\n")
            target = package / "subskills" / "topic.md"
            target.write_text('<a id="rules"></a>\n# Guidance\n')
            self.assertEqual(hig.link_errors(package), [])
            target.unlink()
            self.assertTrue(hig.link_errors(package))

    def test_link_escape_and_missing_anchor_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            package = pathlib.Path(tmp) / "apple-hig"
            package.mkdir()
            (pathlib.Path(tmp) / "outside.md").write_text("secret")
            (package / "SKILL.md").write_text("[escape](../outside.md) [missing](SKILL.md#absent)\n")
            errors = hig.link_errors(package)
            self.assertTrue(any("outside package" in e for e in errors))
            self.assertTrue(any("anchor" in e for e in errors))


class DiscoveryTests(unittest.TestCase):
    def sources(self, root):
        research = root / '.cache' / 'research'
        research.mkdir(parents=True)
        nodes = [{'path': hig.PREFIX + '/content', 'title': 'Content', 'type': 'collection', 'children': [
            {'path': hig.PREFIX + '/' + slug, 'title': slug, 'type': 'article'} for slug in ('charts', 'text-views')]}]
        hig.write_json(research / 'navigator.json', {'interfaceLanguages': {'swift': nodes}})
        (research / 'whats-new.html').write_text('')
        for slug in ('content', 'charts', 'text-views'):
            hig.write_json(root / '.cache' / 'apple' / (slug + '.json'), {
                'identifier': {'url': 'doc://com.apple.HIG' + hig.PREFIX + '/' + slug},
                'metadata': {'title': slug}, 'references': {},
                'primaryContentSections': [{'content': [{'type': 'paragraph', 'inlineContent': [{'type': 'text', 'text': 'Meaningful source guidance.'}]}]}]
            })
        return research

    def test_removed_seed_route_remains_unresolved_in_discovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            research = self.sources(root)
            hig.discover(root, offline=True)
            nav = hig.read_json(research / 'navigator.json')
            nav['interfaceLanguages']['swift'][0]['children'].pop()
            hig.write_json(research / 'navigator.json', nav)
            result = hig.discover(root, offline=True)
            removed = next(p for p in result['pages'] if p['slug'] == 'text-views')
            self.assertNotEqual(removed['status'], 'fetched')
            self.assertIn('remov', removed['error'].lower())

    def test_malformed_document_shape_is_retained_as_failed_route(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.sources(root)
            for body in ([], {}):
                with self.subTest(body=body):
                    hig.write_json(root / '.cache' / 'apple' / 'charts.json', body)
                    result = hig.discover(root, offline=True)
                    page = next(p for p in result['pages'] if p['slug'] == 'charts')
                    self.assertEqual(page['status'], 'error')


if __name__ == "__main__":
    unittest.main()
