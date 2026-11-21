"""Metadata-only routing policy, also used as the generated trusted workflow body."""
import os
import re
import sys

base = os.environ.get('PR_BASE', '')
head = os.environ.get('PR_HEAD', '')
same_repo = os.environ.get('PR_HEAD_REPO', '') == os.environ.get('PR_BASE_REPO', '')
task = bool(re.fullmatch(r'(feat|fix|docs|refactor|test|chore|security|hotfix)/[a-z0-9][a-z0-9._/-]*', head)) and '..' not in head and not head.endswith('/')
allowed = (base == 'main' and head == 'dev' and same_repo) or (base == 'dev' and task)
if not allowed:
    print('Invalid PR routing. Use task branch -> dev -> main; promotions must use this repository dev branch.', file=sys.stderr)
    raise SystemExit(1)
print('Trusted metadata-only PR routing passed.')
