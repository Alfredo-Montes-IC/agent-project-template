"""Shared policy for local Git hooks and pull-request routing."""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTECTED = {'main', 'dev'}
TASK = re.compile(r'^(feat|fix|docs|refactor|test|chore|security|hotfix)/[a-z0-9][a-z0-9._/-]*$')

def task_branch(name):
    return bool(TASK.fullmatch(name)) and '..' not in name and not name.endswith('/')

def validate_commit_branch(branch):
    if branch in PROTECTED:
        return f'Direct commits to {branch} are blocked. Use a task branch and pull request.'
    if not task_branch(branch):
        return 'Use an attached task branch such as feat/shared-skills; detached HEAD is blocked.'
    return None

def validate_pr(base, head):
    if base == 'main':
        return None if head == 'dev' else 'Pull requests to main must come from dev.'
    if base == 'dev':
        return None if task_branch(head) else 'Pull requests to dev must come from a named task branch.'
    return 'Integration pull requests must target dev or main.'

def validate_push(lines, root=ROOT):
    errors = []
    for line in lines:
        fields = line.split()
        if len(fields) != 4:
            errors.append('Malformed pre-push input; refusing push.')
            continue
        local_ref, local_sha, remote_ref, remote_sha = fields
        if not remote_ref.startswith('refs/heads/'):
            errors.append('This guard permits branch pushes only; handle tag publication through an explicit release process.')
            continue
        branch = remote_ref.removeprefix('refs/heads/')
        if branch in PROTECTED:
            errors.append(f'Direct pushes or deletion of {branch} are blocked; use a pull request.')
        elif not task_branch(branch):
            errors.append(f'Unapproved remote branch name: {branch}')
        elif set(local_sha) == {'0'}:
            errors.append(f'Branch deletion is blocked by this hook: {branch}')
        elif set(remote_sha) != {'0'}:
            result = subprocess.run(['git', 'merge-base', '--is-ancestor', remote_sha, local_sha], cwd=root, capture_output=True)
            if result.returncode:
                errors.append(f'Non-fast-forward or unverifiable history for {branch}; fetch and reconcile without force.')
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('event', choices=['commit', 'push', 'ci'])
    args = parser.parse_args()
    errors = []
    if args.event == 'commit':
        branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip()
        error = validate_commit_branch(branch)
        if error:
            errors.append(error)
    elif args.event == 'push':
        errors = validate_push(sys.stdin.read().splitlines())
    elif os.environ.get('GITHUB_EVENT_NAME') == 'pull_request':
        event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
        pr = event['pull_request']
        error = validate_pr(pr['base']['ref'], pr['head']['ref'])
        # Promotions must originate in the same repository, not a fork named dev.
        if pr['base']['ref'] == 'main' and pr['head']['repo']['full_name'] != pr['base']['repo']['full_name']:
            error = 'main promotion must originate in this repository dev branch.'
        if error:
            errors.append(error)
    for error in errors:
        print('ERROR:', error, file=sys.stderr)
    if errors:
        return 1
    print('Git branch policy passed.' if args.event != 'ci' else 'PR routing passed (routing applies to PR events).')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
