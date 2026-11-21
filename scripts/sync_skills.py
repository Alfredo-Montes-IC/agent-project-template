"""Synchronize managed skill mirrors; never remove foreign files."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def sync(root=ROOT, check=False):
    manifest = json.loads((root / '.agents/skill-mirrors.json').read_text())
    if manifest != {'source': '.agents/skills', 'mirrors': ['.claude/skills']}:
        return ['Unexpected skill roots; review sync policy before changing managed locations']
    source = root / manifest['source']
    errors = []
    if source.is_symlink() or any(p.is_symlink() for p in source.rglob('*')):
        return ['Symlinks are not allowed inside shared skill bundles']
    mirror_root = root / '.claude/skills'
    if (root / '.claude').is_symlink() or mirror_root.is_symlink() or (mirror_root.exists() and any(p.is_symlink() for p in mirror_root.rglob('*'))):
        return ['Symlinks are not allowed in managed skill destinations']
    skills = sorted(p for p in source.iterdir() if p.is_dir())
    for skill in skills:
        if not (skill / 'SKILL.md').is_file():
            errors.append(f'Missing SKILL.md: {skill.relative_to(root)}')
            continue
        expected = {p.relative_to(skill): p.read_bytes() for p in skill.rglob('*') if p.is_file()}
        for mirror in manifest['mirrors']:
            target = root / mirror / skill.name
            for relative, content in expected.items():
                dest = target / relative
                if check:
                    if not dest.is_file() or dest.read_bytes() != content:
                        errors.append(f'Skill mirror drift: {dest.relative_to(root)}')
                else:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(content)
            if target.exists():
                for p in target.rglob('*'):
                    if p.is_file() and p.relative_to(target) not in expected:
                        errors.append(f'Unmanaged extra mirror file; review manually: {p.relative_to(root)}')
    return errors

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail on drift without writing')
    args = parser.parse_args()
    problems = sync(check=args.check)
    for problem in problems:
        print('ERROR:', problem)
    if problems:
        raise SystemExit(1)
    print('Shared skills and managed mirrors match.' if args.check else 'Managed skill mirrors synchronized.')
