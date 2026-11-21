"""Delete only unchanged task heads belonging to verified, merged PRs into dev.

Runs as trusted embedded code without checking out PR code. Git's force-with-lease
makes deletion conditional on the exact reviewed head, including concurrent updates.
"""
import base64
import json
import os
import re
import subprocess
import tempfile
import urllib.request
from urllib.parse import quote

TASK = re.compile(r'^(feat|fix|docs|refactor|test|chore|security|hotfix)/[a-z0-9][a-z0-9._/-]*$')

def candidate(pr, repo):
    head = pr.get('head') or {}
    base = pr.get('base') or {}
    branch = head.get('ref', '')
    if not (pr.get('merged') and pr.get('merge_commit_sha') and base.get('ref') == 'dev'
            and (base.get('repo') or {}).get('full_name') == repo
            and (head.get('repo') or {}).get('full_name') == repo
            and TASK.fullmatch(branch) and '..' not in branch and not branch.endswith('/')
            and re.fullmatch('[0-9a-f]{40}', head.get('sha', ''))):
        return None
    return branch, head['sha']

def delete_with_lease(repo, branch, sha, token):
    # No token in argv, URL, source files, or logs. No repository code is loaded.
    env = os.environ.copy()
    env.update(GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='http.https://github.com/.extraheader',
               GIT_CONFIG_VALUE_0='AUTHORIZATION: basic ' + base64.b64encode(('x-access-token:'+token).encode()).decode(),
               GIT_TERMINAL_PROMPT='0')
    with tempfile.TemporaryDirectory() as directory:
        subprocess.run(['git', 'init', '--bare', directory], check=True, capture_output=True, env=env)
        result = subprocess.run(['git', '-C', directory, 'push',
            '--force-with-lease=refs/heads/'+branch+':'+sha,
            'https://github.com/'+repo+'.git', ':refs/heads/'+branch], env=env, capture_output=True)
        if result.returncode:
            raise RuntimeError('Deletion refused or failed; branch retained. Inspect permissions, protection, or concurrent updates.')

def main():
    repo = os.environ['GITHUB_REPOSITORY']
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
        raise ValueError('Invalid repository')
    token = os.environ['GH_TOKEN']
    def api(path):
        request = urllib.request.Request('https://api.github.com/repos/'+repo+path,
            headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json',
                     'X-GitHub-Api-Version':'2022-11-28'})
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    # Bound the backlog; newest 100 closed dev PRs cover initial installation.
    # Each list item is re-read because the list response does not prove merged=true.
    for item in api('/pulls?state=closed&base=dev&sort=updated&direction=desc&per_page=100'):
        pr = api('/pulls/'+str(item['number']))
        selected = candidate(pr, repo)
        if not selected:
            continue
        branch, sha = selected
        # Ensure the merged result still exists in dev (works with merge/squash/rebase).
        comparison = api('/compare/'+quote(pr['merge_commit_sha'], safe='')+'...dev')
        if comparison['status'] not in ('identical', 'ahead'):
            continue
        # Retain the task head until the full dev -> main promotion is merged.
        # Concurrent administrator rewrites of both branches remain outside scope.
        stable = api('/compare/'+quote(pr['merge_commit_sha'], safe='')+'...main')
        if stable['status'] not in ('identical', 'ahead'):
            continue
        refs = api('/git/matching-refs/heads/'+quote(branch, safe=''))
        exact = next((ref for ref in refs if ref['ref']=='refs/heads/'+branch), None)
        if exact is None or exact['object']['sha'] != sha:
            continue
        delete_with_lease(repo, branch, sha, token)
        print('Deleted merged task branch:', branch)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
