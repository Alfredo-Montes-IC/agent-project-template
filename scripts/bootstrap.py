"""Install repository-local Git hooks and synchronize skills."""
import subprocess
import sys
from pathlib import Path
from sync_skills import sync

ROOT = Path(__file__).resolve().parents[1]

def main():
    current = subprocess.run(['git', 'config', '--get', 'core.hooksPath'], cwd=ROOT, text=True, capture_output=True)
    if current.returncode not in (0, 1):
        print('Could not inspect local hook configuration.', file=sys.stderr)
        return 1
    if current.stdout.strip() not in ('', '.githooks'):
        print('Existing effective core.hooksPath differs; integrate existing hooks before installing these.', file=sys.stderr)
        return 1
    problems = sync()
    if problems:
        print('\n'.join(problems), file=sys.stderr)
        return 1
    subprocess.run(['git', 'config', '--local', 'core.hooksPath', '.githooks'], cwd=ROOT, check=True)
    for hook in (ROOT / '.githooks').iterdir():
        hook.chmod(hook.stat().st_mode | 0o111)
    print('Local hooks installed. Direct main/dev commits and pushes are blocked in this checkout.')
    print('Local hooks can be bypassed; server protections require separately activated GitHub rulesets.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
