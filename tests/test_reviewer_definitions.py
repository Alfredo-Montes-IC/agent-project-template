"""Check the project reviewer definitions required by supported clients."""
import re
import unittest
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10 can still run the other checks.
    tomllib = None

ROOT = Path(__file__).resolve().parents[1]
ROLES = {
    'adversarial-reviewer': 'adversarial-code-reviewer',
    'code-standards-reviewer': 'code-standards-review',
    'security-reviewer': 'security-review',
    'migration-reviewer': 'data-migration',
    'accessibility-reviewer': 'accessibility-review',
}


class ReviewerDefinitionTests(unittest.TestCase):
    def test_markdown_reviewer_definitions_have_valid_scoped_metadata(self):
        for directory in ['.agents/agents', '.claude/agents', '.gemini/agents']:
            for name, skill in ROLES.items():
                with self.subTest(client=directory, role=name):
                    text = (ROOT / directory / (name + '.md')).read_text(encoding='utf-8')
                    self.assertTrue(text.startswith('---\n'))
                    frontmatter, body = text[4:].split('\n---\n', 1)
                    self.assertRegex(frontmatter, rf'(?m)^name: {re.escape(name)}$')
                    self.assertRegex(frontmatter, r'(?m)^description: .+')
                    if directory == '.agents/agents':
                        self.assertRegex(frontmatter, r'(?m)^subagent: true$')
                    if directory == '.gemini/agents':
                        self.assertRegex(frontmatter, r'(?m)^kind: local$')
                    self.assertIn(f'.agents/skills/{skill}/SKILL.md', body)
                    self.assertIn('docs/workflows/adversarial-review.md', body)
                    self.assertIn('Do not edit files.', body)

    @unittest.skipIf(tomllib is None, 'TOML parsing requires Python 3.11+')
    def test_codex_reviewer_toml_is_valid(self):
        for name, skill in ROLES.items():
            with self.subTest(role=name):
                path = ROOT / '.codex/agents' / (name + '.toml')
                data = tomllib.loads(path.read_text(encoding='utf-8'))
                self.assertEqual(data['name'], name)
                self.assertTrue(data['description'])
                self.assertIn(f'.agents/skills/{skill}/SKILL.md', data['developer_instructions'])
                self.assertIn('Do not edit files.', data['developer_instructions'])


if __name__ == '__main__':
    unittest.main()
