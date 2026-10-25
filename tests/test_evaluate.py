"""Evidence runner regressions: fabricated reads and stale/incomplete runs must fail."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/evaluate.py'
spec = importlib.util.spec_from_file_location('evaluate', SCRIPT)
evaluate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluate)


class EvaluationTests(unittest.TestCase):
    def test_only_successful_reader_commands_count_as_consumed_files(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            package = project / '.agents/skills/apple-hig'
            package.mkdir(parents=True)
            (package / 'SKILL.md').write_text('real instruction')
            def event(command, code=0, output=""):
                return {'type': 'item.completed', 'item': {'type': 'command_execution',
                        'command': command, 'exit_code': code, 'status': 'completed', 'aggregated_output': output}}
            for command, code in [('echo .agents/skills/apple-hig/SKILL.md', 0),
                                  ('cat .agents/skills/apple-hig/SKILL.md', 1),
                                  ('rg --files .agents/skills/apple-hig', 0),
                                  ('true || cat .agents/skills/apple-hig/SKILL.md', 0),
                                  ('head -n 0 .agents/skills/apple-hig/SKILL.md', 0),
                                  ('cat .agents/skills/apple-hig/SKILL.md >/dev/null', 0),
                                  ("cat > result.md <<'EOF'\ncat .agents/skills/apple-hig/SKILL.md\nEOF", 0)]:
                with self.subTest(command=command):
                    self.assertEqual(evaluate.consumed_reads([event(command, code)], project, package), ([], []))
            reads, outside = evaluate.consumed_reads([
                event("/bin/bash -lc 'cat .agents/skills/apple-hig/SKILL.md'", output="real instruction")], project, package)
            self.assertEqual(reads, ['SKILL.md'])
            self.assertEqual(outside, [])

    def test_failed_compound_requires_full_observed_file_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            package = project / '.agents/skills/apple-hig'
            package.mkdir(parents=True)
            (package / 'SKILL.md').write_text('complete instruction\nsecond line\n')
            item = {'type': 'command_execution', 'command': 'cat .agents/skills/apple-hig/SKILL.md; cat missing.md',
                    'exit_code': 1, 'status': 'failed'}
            for output, wanted in [('complete instruction', []), ('different file contents', []),
                                   ('complete instruction\nsecond line\ncat: missing.md: No such file', ['SKILL.md'])]:
                with self.subTest(output=output):
                    item['aggregated_output'] = output
                    self.assertEqual(evaluate.consumed_reads([{'type': 'item.completed', 'item': item}], project, package),
                                     (wanted, []))

    def test_partial_reference_reads_require_matching_substantive_source_content(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            package = project / '.agents/skills/apple-hig'
            reference = package / 'references/source.md'
            reference.parent.mkdir(parents=True)
            reference.write_text('A complete substantive recommendation supported by this source.\nA second paragraph not read.\n')
            item = {'type': 'command_execution', 'command': "sed -n '1p' .agents/skills/apple-hig/references/source.md", 'exit_code': 0}
            for output, wanted in [('unrelated output', []),
                                   ('A complete substantive recommendation supported by this source.\n', ['references/source.md'])]:
                item['aggregated_output'] = output
                self.assertEqual(evaluate.consumed_reads([{'type': 'item.completed', 'item': item}], project, package), (wanted, []))

    def test_newline_listing_does_not_hide_a_subsequent_real_read(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            package = project / '.agents/skills/apple-hig'
            package.mkdir(parents=True)
            (package / 'SKILL.md').write_text('instruction')
            events = [{'type': 'item.completed', 'item': {'type': 'command_execution',
                      'command': "/bin/bash -lc 'rg --files .agents\ncat .agents/skills/apple-hig/SKILL.md'",
                      'exit_code': 0, 'aggregated_output': 'instruction'}}]
            self.assertEqual(evaluate.consumed_reads(events, project, package), (['SKILL.md'], []))

    def test_zero_exit_without_completed_turn_is_infrastructure_failure(self):
        self.assertEqual(evaluate.execution_status(0, [{'type': 'thread.started'}]), 'infrastructure_error')
        self.assertEqual(evaluate.execution_status(0, [{'type': 'turn.completed'}]), 'infrastructure_error')
        self.assertEqual(evaluate.execution_status(0, [{'type': 'thread.started', 'thread_id': 'fresh-session'}, {'type': 'turn.completed'}]), 'completed')
        self.assertEqual(evaluate.execution_status(1, [{'type': 'turn.completed'}]), 'infrastructure_error')

    def test_adaptation_requires_artifact_and_changed_fixture(self):
        case = {'mode': 'adapt', 'input_files': {'interface.md': 'original'}, 'output_files': ['result.md']}
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / 'interface.md').write_text('original')
            self.assertEqual(evaluate.artifact_checks(case, project)['missing_artifacts'], ['result.md'])
            (project / 'result.md').write_text('decision')
            self.assertFalse(evaluate.artifact_checks(case, project)['passed'])
            (project / 'interface.md').write_text('revised specification')
            self.assertTrue(evaluate.artifact_checks(case, project)['passed'])

    def test_fixture_patch_replays_a_file_without_a_trailing_newline(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / 'interface.md').write_text('original without newline')
            patch = project / 'fixture.patch'
            patch.write_text(evaluate.fixture_diff('interface.md', 'original without newline', 'corrected\nspecification\n'))
            result = subprocess.run(['git', 'apply', str(patch)], cwd=project, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((project / 'interface.md').read_bytes(), b'corrected\nspecification\n')

    def test_attempt_allocation_never_overwrites_previous_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first, attempt = evaluate.allocate_attempt(root, 'topic-buttons', 'candidate', 1)
            (first / 'record.json').write_text('immutable')
            second, attempt = evaluate.allocate_attempt(root, 'topic-buttons', 'candidate', 1)
            self.assertNotEqual(first, second)
            self.assertEqual(attempt, 2)
            self.assertEqual((first / 'record.json').read_text(), 'immutable')

    def test_resume_rejects_changed_case_or_package(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / 'skills/apple-hig'
            package.mkdir(parents=True)
            (package / 'SKILL.md').write_text('instruction')
            record_dir, _ = evaluate.allocate_attempt(root, 'topic-buttons', 'candidate', 1)
            case = root / 'case.json'
            case.write_text('{"id":"topic-buttons"}')
            (record_dir / 'result.md').write_text('artifact')
            (record_dir / 'events.jsonl').write_text('{"type":"turn.completed"}\n')
            record = {'status': 'completed', 'case_hash': evaluate.digest(case.read_bytes()),
                      'harness_hash': evaluate.digest(SCRIPT.read_bytes()), 'model': 'gpt-6.1-sol',
                      'package_dependencies': {'SKILL.md': evaluate.digest(b'instruction')},
                      'artifacts': {'result.md': {'path': str((record_dir / 'result.md').relative_to(root)), 'hash': evaluate.digest(b'artifact')}},
                      'transcript': {'path': str((record_dir / 'events.jsonl').relative_to(root)),
                                     'hash': evaluate.digest((record_dir / 'events.jsonl').read_bytes())}}
            (record_dir / 'record.json').write_text(json.dumps(record))
            self.assertTrue(evaluate.resumable(root, case, 'topic-buttons', 'candidate', 1, 'gpt-6.1-sol'))
            record['artifacts'] = {}
            (record_dir / 'record.json').write_text(json.dumps(record))
            self.assertFalse(evaluate.resumable(root, case, 'topic-buttons', 'candidate', 1, 'gpt-6.1-sol'))
            record['artifacts'] = {'result.md': {'path': str((record_dir / 'result.md').relative_to(root)), 'hash': evaluate.digest(b'artifact')}}
            (record_dir / 'record.json').write_text(json.dumps(record))
            case.write_text('{"id":"topic-buttons","prompt":"changed"}')
            self.assertFalse(evaluate.resumable(root, case, 'topic-buttons', 'candidate', 1, 'gpt-6.1-sol'))
            case.write_text('{"id":"topic-buttons"}')
            (package / 'SKILL.md').write_text('new instruction')
            self.assertFalse(evaluate.resumable(root, case, 'topic-buttons', 'candidate', 1, 'gpt-6.1-sol'))

    def test_negative_resume_tracks_visible_discovery_instruction_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / 'skills/apple-hig'
            package.mkdir(parents=True)
            (package / 'SKILL.md').write_text('original discovery description')
            case = root / 'negative.json'
            case.write_text('{"id":"negative","invoke":false}')
            run, _ = evaluate.allocate_attempt(root, 'negative', 'candidate', 1)
            (run / 'result.md').write_text('result')
            (run / 'events.jsonl').write_text('events')
            record = {'status': 'completed', 'case_hash': evaluate.digest(case.read_bytes()),
                      'harness_hash': evaluate.HARNESS_HASH, 'model': 'gpt-6.1-sol',
                      'package_dependencies': {}, 'discovery_dependencies': {
                          'SKILL.md': evaluate.digest(b'original discovery description')},
                      'artifacts': {'result.md': {'path': str((run / 'result.md').relative_to(root)),
                                               'hash': evaluate.digest(b'result')}},
                      'transcript': {'path': str((run / 'events.jsonl').relative_to(root)), 'hash': evaluate.digest(b'events')}}
            (run / 'record.json').write_text(json.dumps(record))
            self.assertTrue(evaluate.resumable(root, case, 'negative', 'candidate', 1, 'gpt-6.1-sol'))
            (package / 'SKILL.md').write_text('changed discovery scope')
            self.assertFalse(evaluate.resumable(root, case, 'negative', 'candidate', 1, 'gpt-6.1-sol'))

    def test_stress_routes_bind_each_expected_topic_instead_of_null_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'coverage').mkdir()
            (root / 'coverage/capabilities.json').write_text(json.dumps({'topics': [
                {'topic': 'buttons', 'family': 'menus-and-actions'},
                {'topic': 'accessibility', 'family': 'foundations'}]}))
            case = {'kind': 'stress', 'topic': None, 'family': None,
                    'expected_topics': ['buttons', 'accessibility'], 'invoke': True}
            reads = evaluate.required_reads(case, 'candidate', root)
            self.assertEqual(len(reads), 7)
            self.assertIn('subskills/apple-hig-foundations/.topics/apple-hig-accessibility/SKILL.md', reads)
            self.assertIn('subskills/apple-hig-menus-and-actions/references/buttons.md', reads)
            case['invoke'] = False
            self.assertEqual(evaluate.required_reads(case, 'candidate', root), [])

    def test_negative_prompt_does_not_instruct_hig_reads_or_leak_rubric(self):
        case = {'invoke': False, 'prompt': 'Repair CSV parsing.', 'rubric': {'secret': 'hidden'}}
        prompt = evaluate.task_prompt(case)
        self.assertNotIn('$apple-hig', prompt)
        self.assertNotIn('SKILL.md', prompt)
        self.assertNotIn('hidden', prompt)


if __name__ == '__main__':
    unittest.main()
