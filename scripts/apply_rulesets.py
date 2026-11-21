"""Preview or apply the named GitHub rulesets using an independently authenticated gh CLI."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def gh(args, body=None):
    result = subprocess.run(['gh', 'api', *args], input=body, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or 'GitHub rejected the request')
    return json.loads(result.stdout) if result.stdout.strip() else None

def verify_rules(branch, rules):
    types = {rule['type'] for rule in rules}
    expected = {'deletion', 'non_fast_forward', 'pull_request', 'required_status_checks'}
    if not expected.issubset(types):
        raise RuntimeError(f'{branch}: active protections missing: {sorted(expected-types)}')
    checks = {c['context'] for r in rules if r['type'] == 'required_status_checks' for c in r['parameters']['required_status_checks']}
    if not {'repository-checks', 'branch-policy', 'windows-checks', 'python-minimum-checks', 'secret-scan'}.issubset(checks):
        raise RuntimeError(f'{branch}: required check contexts missing')

def verify_definition(expected, actual):
    for key in ['name', 'target', 'enforcement', 'conditions']:
        if expected[key] != actual.get(key):
            raise RuntimeError(f"{expected['name']}: unexpected server {key}")
    if actual.get('bypass_actors'):
        raise RuntimeError(f"{expected['name']}: server bypass actors are not permitted")
    actual_rules = {rule['type']:rule for rule in actual.get('rules',[])}
    for wanted in expected['rules']:
        current = actual_rules.get(wanted['type'])
        if current is None:
            raise RuntimeError(f"{expected['name']}: missing server rule {wanted['type']}")
        for key, value in wanted.get('parameters',{}).items():
            actual_value = current.get('parameters',{}).get(key)
            if key == 'required_status_checks':
                normalize = lambda checks: sorted((c['context'], c.get('integration_id')) for c in checks)
                matches = isinstance(actual_value, list) and normalize(actual_value) == normalize(value)
            else:
                matches = actual_value == value
            if not matches:
                raise RuntimeError(f"{expected['name']}: weakened/changed parameter {wanted['type']}.{key}")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True, help='owner/repository')
    parser.add_argument('--apply', action='store_true', help='Apply/update only template-main and template-dev')
    parser.add_argument('--check', action='store_true', help='Read effective rules; do not change settings')
    args = parser.parse_args()
    if args.apply and args.check:
        parser.error('--apply and --check are mutually exclusive')
    if len(args.repo.split('/')) != 2 or any(not part or part.startswith('-') for part in args.repo.split('/')):
        parser.error('Expected owner/repository')
    definitions = [json.loads((ROOT / f'.github/rulesets/{b}.json').read_text()) for b in ['main','dev']]
    if not args.apply and not args.check:
        print('PREVIEW ONLY. No GitHub settings were changed.')
        print(json.dumps({'repository':args.repo,'rulesets':definitions}, indent=2))
        return 0
    try:
        if args.apply:
            existing = gh([f'repos/{args.repo}/rulesets?includes_parents=false'])
            ids = {r['name']: r['id'] for r in existing if r.get('source_type') in (None,'Repository')}
            for definition in definitions:
                endpoint = f'repos/{args.repo}/rulesets'
                method = 'POST'
                if definition['name'] in ids:
                    endpoint += '/' + str(ids[definition['name']])
                    method = 'PUT'
                gh([endpoint, '--method', method, '--input', '-'], json.dumps(definition))
        active = gh([f'repos/{args.repo}/rulesets?includes_parents=false'])
        by_name = {r['name']:r['id'] for r in active if r.get('source_type') in (None,'Repository')}
        for definition in definitions:
            if definition['name'] not in by_name:
                raise RuntimeError('Named server ruleset missing: ' + definition['name'])
            actual = gh([f"repos/{args.repo}/rulesets/{by_name[definition['name']]}"])
            verify_definition(definition, actual)
        for branch in ['main','dev']:
            rules = gh([f'repos/{args.repo}/rules/branches/{branch}'])
            verify_rules(branch, rules)
            print(f'{branch}: active PR, status-check, deletion, and non-fast-forward protections verified.')
    except (OSError, RuntimeError, ValueError) as e:
        print('Protection not verified. Private repositories may require GitHub Pro and administration permission.\n' + str(e), file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
