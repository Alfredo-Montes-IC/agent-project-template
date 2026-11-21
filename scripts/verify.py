"""Run repository checks; application checks must be added by each project."""
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
commands = [
    [sys.executable, 'scripts/project_checks.py'],
    [sys.executable, 'scripts/sync_skills.py', '--check'],
    [sys.executable, 'scripts/sync_workflows.py', '--check'],
    [sys.executable, 'scripts/sync_cleanup_workflow.py', '--check'],
    [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
    ['git', 'diff', '--check'],
]
for command in commands:
    result = subprocess.run(command, cwd=root)
    if result.returncode:
        raise SystemExit(result.returncode)
print('Repository verification passed. Application behavior is outside these template checks.')
