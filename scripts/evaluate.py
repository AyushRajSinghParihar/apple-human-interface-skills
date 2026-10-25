#!/usr/bin/env python3
"""Run artifact evaluations through the authenticated Codex CLI; never grade them.

Each attempt installs a copy outside this checkout, retains raw client evidence,
and binds artifacts and consumed instructions to SHA256 bytes. The workspace-write
sandbox and no-browsing prompt are recorded policies, not a claim of OS isolation.
"""
import argparse
import concurrent.futures
import difflib
import glob
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import selectors
import shlex
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import time

_spec = importlib.util.spec_from_file_location('hig', Path(__file__).with_name('hig.py'))
hig = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hig)
digest = hig.digest
HARNESS_HASH = digest(Path(__file__).read_bytes())
ROOT = Path(__file__).resolve().parents[1]
BASELINE = 'a748d07'
MODEL = 'gpt-6.1-sol'


def allocate_attempt(root, case_id, variant, repetition):
    parent = Path(root) / 'coverage/behavior'
    parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, 100000):
        path = parent / f'{case_id}.{variant}.r{repetition}.a{attempt}'
        try:
            path.mkdir()
            return path, attempt
        except FileExistsError:
            continue
    raise ValueError('Too many attempts')


def execution_status(returncode, events):
    started = any(e.get('type') == 'thread.started' and isinstance(e.get('thread_id'), str) and e['thread_id'] for e in events)
    return 'completed' if returncode == 0 and started and any(e.get('type') == 'turn.completed' for e in events) else 'infrastructure_error'


def safe_file(project, name):
    path = (project / name).resolve()
    if not path.is_relative_to(project.resolve()) or path == project.resolve():
        raise ValueError(f'Unsafe fixture/artifact path: {name}')
    return path


def artifact_checks(case, project):
    missing = [name for name in case.get('output_files', ['result.md'])
               if not safe_file(project, name).is_file() or not safe_file(project, name).read_bytes().strip()]
    changed = {name: safe_file(project, name).is_file() and
               safe_file(project, name).read_bytes() != value.encode()
               for name, value in case.get('input_files', {}).items()}
    adaptation = case.get('mode') == 'adapt'
    changed_required = not adaptation or changed.get('interface.md', False)
    return {'missing_artifacts': missing, 'changed_inputs': changed,
            'adaptation_changed': changed_required, 'passed': not missing and changed_required}


def fixture_diff(name, original, revised):
    lines = difflib.unified_diff(original.splitlines(True), revised.splitlines(True),
                                 fromfile='before/' + name, tofile='after/' + name)
    return ''.join(line if line.endswith('\n') else line + '\n\\ No newline at end of file\n'
                   for line in lines)


def task_prompt(case):
    prompt = case['prompt']
    if case.get('invoke', True):
        prompt += ('\n\nEvaluation audit: explicitly read the installed apple-hig root SKILL.md, '
                   'then follow its routing and read the selected family and any routed topic procedure '
                   'before the source guide. Resolve those paths from the installed package. '
                   'Read one file per command using cat, sed, head, tail or rg so instruction consumption '
                   'is auditable; file listings alone are insufficient.')
    else:
        prompt = prompt.replace('$apple-hig', 'Apple HIG')
    return prompt + ('\n\nWork only from the supplied local files and installed instructions. '
                     'Do not browse the web. Produce the requested files in this project. '
                     'Do not claim device, SDK, GUI or accessibility execution absent actual evidence.')


def _segments(command):
    try:
        tokens = shlex.split(command)
    except ValueError:
        return []
    if tokens and Path(tokens[0]).name in {'bash', 'sh', 'zsh'} and '-lc' in tokens:
        return _segments(tokens[tokens.index('-lc') + 1])
    # Punctuation separates commands; shlex.split above only unwraps a shell.
    lexer = shlex.shlex(command, posix=True, punctuation_chars=';&|<>\n')
    lexer.whitespace = ' \t\r'
    lexer.whitespace_split = True
    groups, group = [], []
    try:
        for token in lexer:
            if token and all(c in ';&|<>\n' for c in token):
                if group:
                    groups.append(group)
                group = []
            else:
                group.append(token)
    except ValueError:
        return []
    if group:
        groups.append(group)
    return groups


def consumed_reads(events, project, package):
    """Conservative trace: explicit existing file operands of successful readers.

    Reader output is not synthesized from metadata. Failed compound commands
    count a file only when its complete bytes appear in captured stdout; listings,
    echo and unexecuted heredoc bodies never count as instruction consumption.
    """
    reads, outside = set(), set()
    project, package = project.resolve(), package.resolve()
    for event in events:
        item = event.get('item', {})
        if event.get('type') != 'item.completed' or item.get('type') != 'command_execution':
            continue
        command = item.get('command', '')
        if '<<' in command or '||' in command:
            continue
        successful = item.get('exit_code') == 0 and item.get('status') != 'failed'
        cwd = project
        for tokens in _segments(command):
            if not tokens:
                continue
            executable = Path(tokens[0]).name
            if executable == 'cd' and len(tokens) == 2:
                cwd = (cwd / tokens[1]).resolve()
                continue
            if executable not in {'cat', 'sed', 'head', 'tail', 'rg'} or '--files' in tokens:
                continue
            if executable == 'sed' and any(t == '-i' or t.startswith('--in-place') for t in tokens):
                continue
            for token in tokens[1:]:
                if token.startswith('-'):
                    continue
                operand = Path(token).expanduser()
                if not operand.is_absolute():
                    operand = cwd / operand
                candidates = [Path(p) for p in glob.glob(str(operand))] if any(c in str(operand) for c in '*?[') else [operand]
                for path in candidates:
                    path = path.resolve()
                    if not path.is_file():
                        continue
                    raw = path.read_bytes()
                    output = item.get('aggregated_output', '').encode()
                    observed = bool(raw.strip()) and raw in output
                    # Procedures require their whole body. Source references may
                    # be consulted in excerpts, but must expose actual prose.
                    if not observed and successful and path.is_relative_to(package):
                        relative = path.relative_to(package)
                        if 'references' in relative.parts and path.suffix == '.md':
                            observed = any(len(line.strip()) >= 48 and len(line.split()) >= 6
                                           and not line.lstrip().startswith((b'#', b'<a ', b'Source:', b'Snapshot:', b'Retrieved:'))
                                           and line in output for line in raw.splitlines())
                    if not observed:
                        continue
                    if path.is_relative_to(package):
                        reads.add(path.relative_to(package).as_posix())
                    elif not path.is_relative_to(project):
                        outside.add(str(path))
    return sorted(reads), sorted(outside)


def required_reads(case, variant, root=ROOT):
    if not case.get('invoke', True):
        return []
    if case.get('topic') and case.get('family'):
        routes = [(case['topic'], case['family'])]
    else:
        inventory = json.loads((root / 'coverage/capabilities.json').read_text())
        families = {row['topic']: row['family'] for row in inventory['topics']}
        routes = [(topic, families[topic]) for topic in case['expected_topics']]
    paths = ['SKILL.md']
    for topic, family_name in routes:
        family = f'subskills/apple-hig-{family_name}'
        paths.append(f'{family}/SKILL.md')
        if variant == 'candidate':
            paths.append(f'{family}/.topics/apple-hig-{topic}/SKILL.md')
        paths.append(f'{family}/references/{topic}.md')
    return list(dict.fromkeys(paths))


def install(root, project, variant):
    package = project / '.agents/skills/apple-hig'
    package.parent.mkdir(parents=True)
    if variant == 'candidate':
        shutil.copytree(root / 'skills/apple-hig', package)
    else:
        archive = subprocess.run(['git', '-C', str(root), 'archive', BASELINE, 'skills/apple-hig'],
                                 check=True, capture_output=True).stdout
        with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
            tar.extractall(project / 'baseline-export', filter='data')
        shutil.move(str(project / 'baseline-export/skills/apple-hig'), package)
        shutil.rmtree(project / 'baseline-export')
    subprocess.run(['git', 'init', '-q', str(project)], check=True, capture_output=True)
    return package


def discovery(project, config=(), timeout=45):
    # app-server has no ignore-user-config/ignore-rules flags; exec below does.
    # Discovery is read-only and its only config changes are process overrides.
    command = ['codex', 'app-server', '--disable', 'plugins', *config, '--stdio']
    process = subprocess.Popen(command, cwd=project, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL, text=True, bufsize=1, start_new_session=True)
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)
    transcript = []
    def send(message):
        process.stdin.write(json.dumps(message) + '\n')
        process.stdin.flush()
    def response(identifier):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if not selector.select(max(0, deadline - time.monotonic())):
                break
            line = process.stdout.readline()
            if not line:
                raise RuntimeError('app-server exited before discovery response')
            message = json.loads(line)
            transcript.append(message)
            if message.get('id') == identifier:
                if 'error' in message:
                    raise RuntimeError(str(message['error']))
                return message['result']
        raise TimeoutError('app-server skills/list timeout')
    try:
        send({'id': 1, 'method': 'initialize', 'params': {'clientInfo': {'name': 'hig-evaluation', 'version': '1.0'}}})
        response(1)
        send({'method': 'initialized', 'params': {}})
        send({'id': 2, 'method': 'skills/list', 'params': {'cwds': [str(project)], 'forceReload': True}})
        result = response(2)
        skills = [skill for entry in result.get('data', []) for skill in entry.get('skills', [])]
        if not skills:
            raise RuntimeError('skills/list returned no skills')
        return skills
    finally:
        selector.close()
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
        process.communicate(timeout=10)


def skill_overrides(skills, package):
    disabled = []
    for skill in skills:
        path = Path(skill['path']).resolve()
        if not path.is_relative_to(package.resolve()):
            disabled.append('{path=' + json.dumps(str(path)) + ',enabled=false}')
    return ['-c', 'skills.config=[' + ','.join(disabled) + ']']


def dependency_bytes(root, variant, relative):
    if variant == 'candidate':
        return (root / 'skills/apple-hig' / relative).read_bytes()
    return subprocess.run(['git', '-C', str(root), 'show', f'{BASELINE}:skills/apple-hig/{relative}'],
                          check=True, capture_output=True).stdout


def resumable(root, case_path, case_id, variant, repetition, model):
    pattern = f'{case_id}.{variant}.r{repetition}.a*/record.json'
    for path in sorted((root / 'coverage/behavior').glob(pattern), reverse=True):
        try:
            record = json.loads(path.read_text())
            if (record['status'] != 'completed' or record['case_hash'] != digest(case_path.read_bytes())
                    or record['harness_hash'] != HARNESS_HASH or record['model'] != model):
                continue
            dependencies = {**record['package_dependencies'], **record.get('discovery_dependencies', {})}
            if any(digest(dependency_bytes(root, variant, name)) != fingerprint
                   for name, fingerprint in dependencies.items()):
                continue
            case = json.loads(case_path.read_text())
            if not record['transcript'] or any(name not in record['artifacts'] for name in case.get('output_files', ['result.md'])):
                continue
            bound = list(record['artifacts'].values()) + ([record['transcript']] if record['transcript'] else [])
            if any(digest((root / item['path']).read_bytes()) != item['hash'] for item in bound):
                continue
            return True
        except (OSError, ValueError, KeyError, subprocess.CalledProcessError):
            continue
    return False


def run_case(root, case_path, variant, repetition, model, timeout, smoke=False):
    case = json.loads(case_path.read_text())
    directory, attempt = allocate_attempt(root, case['id'], variant, repetition)
    record = {'schema_version': 1, 'run_id': directory.name, 'case_id': case['id'],
              'variant': variant, 'repetition': repetition, 'attempt': attempt,
              'status': 'infrastructure_error', 'case_path': case_path.relative_to(root).as_posix(),
              'case_hash': digest(case_path.read_bytes()), 'harness_hash': HARNESS_HASH,
              'model': model, 'cli_version': '', 'started_at': hig.now(), 'finished_at': None,
              'package_dependencies': {}, 'discovery_dependencies': {}, 'thread_id': None, 'reads': [], 'required_reads': required_reads(case, variant, root),
              'routing': {'missing': [], 'passed': False}, 'artifacts': {}, 'transcript': {}, 'checks': {},
              'baseline_commit': BASELINE if variant == 'baseline' else None}
    def bound(path):
        return {'path': path.relative_to(root).as_posix(), 'hash': digest(path.read_bytes())}
    try:
        record['cli_version'] = subprocess.run(['codex', '--version'], check=True, capture_output=True, text=True).stdout.strip()
        with tempfile.TemporaryDirectory(prefix='hig-eval-') as temporary:
            project = Path(temporary)
            package = install(root, project, variant)
            snapshot = {p.relative_to(package).as_posix(): p.read_bytes() for p in package.rglob('*') if p.is_file()}
            for name, content in case.get('input_files', {}).items():
                path = safe_file(project, name)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
                saved = directory / 'fixtures' / name
                saved.parent.mkdir(parents=True, exist_ok=True)
                saved.write_bytes(path.read_bytes())
            skills = discovery(project)
            overrides = skill_overrides(skills, package)
            isolated = discovery(project, overrides)
            visible = [s for s in isolated if s.get('enabled', True)]
            hig_visible = [s for s in visible if Path(s['path']).resolve().is_relative_to(package)]
            unrelated = [s['path'] for s in visible if s not in hig_visible]
            hidden = [s['path'] for s in hig_visible if '.topics' in Path(s['path']).parts]
            expected = 14
            checks = {'visible_hig_count': len(hig_visible), 'expected_visible_hig_count': expected,
                      'unrelated_enabled': unrelated, 'hidden_topics_visible': hidden,
                      'disabled_unrelated_count': len(skills) - len(hig_visible)}
            record['discovery_dependencies'] = {Path(skill['path']).resolve().relative_to(package).as_posix():
                                                digest(snapshot[Path(skill['path']).resolve().relative_to(package).as_posix()])
                                                for skill in hig_visible}
            record['checks']['discovery'] = checks
            hig.write_json(directory / 'discovery.json', {'checks': checks,
                           'visible_hig': [{'name': s['name'], 'path': s['path']} for s in hig_visible]})
            if len(hig_visible) != expected or unrelated or hidden:
                raise RuntimeError('Installed discovery did not expose exactly 14 HIG entries with unrelated skills disabled')
            command = ['codex', 'exec', '--disable', 'plugins', '--ignore-user-config', '--ignore-rules', '--ephemeral', '--json',
                       '--sandbox', 'workspace-write', '-c', 'approval_policy="never"',
                       *overrides, '--model', model, '--cd', str(project),
                       '--output-last-message', str(project / 'final-message.txt'), '-']
            prompt = task_prompt(case)
            (directory / 'prompt.txt').write_text(prompt)
            hig.write_json(directory / 'command.json', {'argv': command, 'cwd': str(project), 'smoke': smoke,
                           'policy': {'web': 'prompt prohibition', 'filesystem': 'Codex workspace-write sandbox; no stronger isolation asserted'}})
            events_file = directory / 'events.jsonl'
            with events_file.open('w') as stdout, (directory / 'stderr.txt').open('w') as stderr:
                process = subprocess.Popen(command, cwd=project, stdin=subprocess.PIPE, stdout=stdout,
                                           stderr=stderr, text=True, start_new_session=True)
                timed_out = False
                try:
                    process.communicate(prompt, timeout=timeout)
                except subprocess.TimeoutExpired:
                    timed_out = True
                    os.killpg(process.pid, signal.SIGTERM)
                    try:
                        process.communicate(timeout=10)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.communicate()
            events, malformed = [], []
            for line in events_file.read_text().splitlines():
                try:
                    events.append(json.loads(line))
                except ValueError:
                    malformed.append(line)
            record['transcript'] = bound(events_file)
            record['thread_id'] = next((event['thread_id'] for event in events
                                        if event.get('type') == 'thread.started' and event.get('thread_id')), None)
            record['reads'], forbidden = consumed_reads(events, project, package)
            required = record['required_reads']
            missing = sorted(set(required) - set(record['reads']))
            negative_violation = not case.get('invoke', True) and bool(record['reads'])
            record['routing'] = {'missing': missing, 'passed': not missing and not negative_violation,
                                 'unexpected_hig_reads': negative_violation}
            record['package_dependencies'] = {name: digest(snapshot[name]) for name in sorted(set(required + record['reads'])) if name in snapshot}
            package_changed = [name for name, value in snapshot.items()
                               if not (package / name).is_file() or (package / name).read_bytes() != value]
            record['checks'].update(artifact_checks(case, project))
            record['checks'].update({'exit_code': process.returncode, 'turn_completed': any(e.get('type') == 'turn.completed' for e in events),
                                     'malformed_event_count': len(malformed), 'forbidden_reads': forbidden,
                                     'package_changed': package_changed})
            for name in case.get('output_files', ['result.md']):
                source = safe_file(project, name)
                if source.is_file():
                    destination = directory / 'artifacts' / name
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(source, destination)
                    record['artifacts'][name] = bound(destination)
            patches = []
            for name, original in case.get('input_files', {}).items():
                source = safe_file(project, name)
                if source.is_file() and source.read_bytes() != original.encode():
                    destination = directory / 'artifacts' / name
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(source, destination)
                    record['artifacts'][name] = bound(destination)
                    patches.append(fixture_diff(name, original, source.read_text()))
            if patches:
                patch = directory / 'artifacts/fixture.patch'
                patch.write_text(''.join(patches))
                record['artifacts']['fixture.patch'] = bound(patch)
            if (project / 'final-message.txt').is_file():
                shutil.copyfile(project / 'final-message.txt', directory / 'final-message.txt')
                record['final_message'] = bound(directory / 'final-message.txt')
            record['status'] = 'timed_out' if timed_out else execution_status(process.returncode, events)
            if record['status'] == 'completed':
                if malformed or package_changed or forbidden:
                    record['status'] = 'infrastructure_error'
                elif not record['checks']['passed']:
                    record['status'] = 'artifact_error'
                elif not record['routing']['passed']:
                    record['status'] = 'routing_error'
    except (OSError, ValueError, RuntimeError, TimeoutError, subprocess.SubprocessError) as error:
        record['checks']['infrastructure_error'] = str(error)
    finally:
        record['finished_at'] = hig.now()
        with (directory / 'record.json').open('x') as stream:
            json.dump(record, stream, indent=2, ensure_ascii=False)
            stream.write('\n')
    print(json.dumps({'run_id': record['run_id'], 'status': record['status'], 'reads': len(record['reads'])}), flush=True)
    return record


def select_cases(root, requested, suite):
    cases = sorted((root / 'evals/cases').glob('*.json'))
    if requested:
        paths = []
        for value in requested:
            path = Path(value)
            if not path.is_file():
                path = root / 'evals/cases' / (value.removesuffix('.json') + '.json')
            if not path.is_file():
                raise ValueError(f'Unknown case: {value}')
            paths.append(path.resolve())
        return paths
    if suite:
        return cases
    raise ValueError('Specify --case (repeatable) or --suite')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', action='append', default=[])
    parser.add_argument('--variant', choices=['candidate', 'baseline'], default='candidate')
    parser.add_argument('--suite', action='store_true')
    parser.add_argument('--workers', type=int, choices=[1, 2, 3], default=1)
    parser.add_argument('--timeout', type=int, default=600)
    parser.add_argument('--repetition', type=int, default=1)
    parser.add_argument('--model', default=MODEL)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--smoke', action='store_true')
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if args.timeout <= 0 or args.repetition <= 0:
        parser.error('timeout and repetition must be positive')
    try:
        paths = select_cases(root, args.case, args.suite)
        tasks = []
        for path in paths:
            case = json.loads(path.read_text())
            repetitions = range(1, 4) if args.suite and case.get('kind') == 'stress' else [args.repetition]
            tasks.extend((path, 'candidate' if args.suite else args.variant, rep) for rep in repetitions)
            if args.suite and case.get('baseline_control'):
                tasks.append((path, 'baseline', 1))
        if args.smoke:
            tasks = tasks[:1]
        if args.resume:
            tasks = [(path, variant, rep) for path, variant, rep in tasks
                     if not resumable(root, path, json.loads(path.read_text())['id'], variant, rep, args.model)]
        def execute(task):
            path, variant, rep = task
            record = run_case(root, path, variant, rep, args.model, args.timeout, args.smoke)
            if record['status'] in {'infrastructure_error', 'timed_out'}:
                record = run_case(root, path, variant, rep, args.model, args.timeout, args.smoke)
            return record
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            records = list(pool.map(execute, tasks))
        return int(any(record['status'] != 'completed' for record in records))
    except (OSError, ValueError, KeyError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    sys.exit(main())
