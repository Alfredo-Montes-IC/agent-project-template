"""Record and check a local review of the exact staged tree and parent."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def snapshot():
    merge_head = Path(git('rev-parse', '--git-path', 'MERGE_HEAD'))
    if not merge_head.is_absolute():
        merge_head = ROOT / merge_head
    if merge_head.exists():
        raise ValueError('Local merge commits require review of multiple parents and are not supported; use a PR.')
    tree = git('write-tree')
    parent = subprocess.run(['git', 'rev-parse', '--verify', 'HEAD'], cwd=ROOT,
                            text=True, capture_output=True)
    if parent.returncode not in (0, 128):
        raise RuntimeError('Cannot determine the current parent commit.')
    return {'tree': tree, 'parent': parent.stdout.strip() if parent.returncode == 0 else None}


def receipt_path():
    path = Path(git('rev-parse', '--git-path', 'adversarial-review.json'))
    return path if path.is_absolute() else ROOT / path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('snapshot', help='Print the staged tree and parent to give the reviewer')
    approve = sub.add_parser('record', help='Record a completed independent review')
    approve.add_argument('--tree', required=True)
    approve.add_argument('--parent', required=True, help='Reviewed parent SHA, or unborn')
    approve.add_argument('--reviewer', required=True, help='Independent reviewer/session identifier')
    approve.add_argument('--evidence', required=True, help='Review findings and disposition or durable reference')
    sub.add_parser('check', help='Require a matching completed review')
    args = parser.parse_args()
    try:
        current = snapshot()
        if args.action == 'snapshot':
            print(json.dumps(current))
        elif args.action == 'record':
            if args.tree != current['tree'] or args.parent != (current['parent'] or 'unborn'):
                raise ValueError('The staged tree or parent changed; review the new snapshot.')
            if not args.reviewer.strip() or not args.evidence.strip():
                raise ValueError('Reviewer and evidence are required.')
            receipt = {**current, 'reviewer': args.reviewer.strip(), 'evidence': args.evidence.strip()}
            receipt_path().write_text(json.dumps(receipt), encoding='utf-8')
            print('Local review recorded. This receipt does not authenticate its author.')
        else:
            try:
                receipt = json.loads(receipt_path().read_text(encoding='utf-8'))
            except (OSError, ValueError):
                raise ValueError('No valid independent review receipt; review the staged snapshot first.')
            if (not isinstance(receipt, dict) or receipt.get('tree') != current['tree']
                    or receipt.get('parent') != current['parent']
                    or not isinstance(receipt.get('reviewer'), str) or not receipt['reviewer'].strip()
                    or not isinstance(receipt.get('evidence'), str) or not receipt['evidence'].strip()):
                raise ValueError('Review does not match the staged tree and parent; obtain a new review.')
            print('Matching local review receipt found; reviewer independence is not authenticated.')
    except (OSError, subprocess.CalledProcessError, RuntimeError, ValueError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
