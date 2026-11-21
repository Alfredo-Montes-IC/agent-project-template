"""Check the portable template and basic secret hygiene using only the standard library."""
import argparse
import json
import posixpath
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    'README.md', 'AGENTS.md', 'CLAUDE.md', '.gemini/settings.json', '.agents/skill-mirrors.json',
    'docs/context/README.md', 'docs/product/project-brief.md', 'docs/architecture/README.md',
    'docs/standards/GUIDELINES.md', 'docs/standards/verification.md', 'docs/standards/GIT_WORKFLOW.md',
    'docs/workflows/multi-agent.md', 'docs/tasks/README.md', 'docs/templates/task.template.md',
    'docs/templates/handoff.template.md', 'docs/templates/adr.template.md', 'docs/templates/scoped-agents.template.md',
    'docs/agents/README.md', '.github/rulesets/main.json', '.github/rulesets/dev.json',
)
SECRET_PATTERNS = {
    'private key': re.compile(rb'-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----'),
    'GitHub token': re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{60,})\b'),
    'AWS access key identifier': re.compile(rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
}

def private_path(path):
    name = Path(path).name
    return (name == '.env' or name.startswith('.env.')) and name != '.env.example' or name in {'id_rsa', 'id_ed25519'} or name.endswith(('.pem', '.key'))

def collect(root=ROOT, staged=False):
    command = ['git', 'ls-files', '-z', '--cached']
    if not staged:
        command += ['--others', '--exclude-standard']
    names = subprocess.check_output(command, cwd=root).decode().split('\0')
    files = {}
    for name in dict.fromkeys(n for n in names if n):
        if staged:
            files[name] = subprocess.check_output(['git', 'show', ':' + name], cwd=root)
        elif (root / name).is_file():
            files[name] = (root / name).read_bytes()
    return files

def check_files(files):
    errors = []
    for path in REQUIRED:
        if path not in files:
            errors.append('Missing required file: ' + path)
    for path, data in files.items():
        if private_path(path):
            errors.append('Private configuration/key file must not be tracked: ' + path)
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(data):
                errors.append(f'Possible {label} in {path}; value redacted')
        if not path.endswith('.md'):
            continue
        text = data.decode('utf-8', errors='replace')
        for match in re.finditer(r'\[[^\]\r\n]+\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"\r\n]*")?\)', text):
            target = match[1].strip('<>')
            if urlsplit(target).scheme or target.startswith(('#', '//')):
                continue
            link = unquote(urlsplit(target).path)
            if not link:
                continue
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), link))
            if resolved.startswith('../') or resolved.startswith('/'):
                errors.append(f'Link leaves repository in {path}: {target}')
            elif resolved not in files and not any(p.startswith(resolved.rstrip('/') + '/') for p in files):
                errors.append(f'Broken local link in {path}: {target}')
    try:
        manifest = json.loads(files['.agents/skill-mirrors.json'])
        if manifest != {'source': '.agents/skills', 'mirrors': ['.claude/skills']}:
            errors.append('Unexpected managed skill roots')
        source = manifest['source'].rstrip('/') + '/'
        for path, data in files.items():
            if not path.startswith(source):
                continue
            relative = path[len(source):]
            if relative.endswith('/SKILL.md'):
                text = data.decode()
                parts = text.split('---', 2)
                if len(parts) != 3 or parts[0].strip():
                    errors.append('Invalid skill frontmatter: ' + path)
                    continue
                fields = dict(line.split(':', 1) for line in parts[1].strip().splitlines() if ':' in line)
                name = fields.get('name', '').strip()
                description = fields.get('description', '').strip()
                if set(fields) != {'name', 'description'} or not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64 or name != relative.split('/')[0] or not description:
                    errors.append('Invalid portable skill metadata: ' + path)
            for mirror in manifest['mirrors']:
                target = mirror.rstrip('/') + '/' + relative
                if files.get(target) != data:
                    errors.append('Skill mirror drift: ' + target)
        for mirror in manifest['mirrors']:
            prefix = mirror.rstrip('/') + '/'
            for path in files:
                if path.startswith(prefix) and source + path[len(prefix):] not in files:
                    errors.append('Unmanaged skill mirror file: ' + path)
        if not any(p.startswith(source) and p.endswith('/SKILL.md') for p in files):
            errors.append('No shared skills found')
    except (ValueError, KeyError, TypeError) as e:
        errors.append('Invalid skill manifest: ' + str(e))
    try:
        if files['CLAUDE.md'].decode().strip() != '@AGENTS.md':
            errors.append('CLAUDE.md must import the shared contract without duplicating it')
        if json.loads(files['.gemini/settings.json'])['context']['fileName'] != ['AGENTS.md']:
            errors.append('Gemini must load the shared AGENTS.md contract')
    except (ValueError, KeyError, TypeError) as e:
        errors.append('Invalid instruction adapter: ' + str(e))
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staged', action='store_true', help='Validate exact index content, not the working tree')
    args = parser.parse_args()
    errors = check_files(collect(staged=args.staged))
    for error in errors:
        print('ERROR:', error)
    if errors:
        return 1
    print('Context, shared skills, adapters, and basic secret hygiene passed' + (' for staged content.' if args.staged else '.'))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
