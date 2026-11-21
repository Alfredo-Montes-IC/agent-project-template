import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from git_guard import validate_commit_branch, validate_pr, validate_push
from project_checks import check_files, collect, private_path
from sync_skills import sync
from apply_rulesets import verify_rules, verify_definition
from sync_workflows import render
import bootstrap

class PolicyTests(unittest.TestCase):
    def test_commit_branch(self):
        for name in ['main','dev','','Main','feature/unsafe','feat/../bad']:
            self.assertIsNotNone(validate_commit_branch(name), name)
        for name in ['feat/invoices','security/authz','fix/42-regression','docs/agent-setup']:
            self.assertIsNone(validate_commit_branch(name), name)

    def test_pr_routing(self):
        self.assertIsNone(validate_pr('dev','feat/task'))
        self.assertIsNone(validate_pr('main','dev'))
        for base, head in [('main','feat/task'),('main','hotfix/task'),('dev','main'),('dev','dev'),('dev',''),('release','feat/task')]:
            self.assertIsNotNone(validate_pr(base,head))

    def test_destination_refs_deletion_and_force(self):
        zero='0'*40; one='1'*40; two='2'*40
        self.assertTrue(validate_push([f'refs/heads/feat/task {one} refs/heads/main {zero}']))
        self.assertTrue(validate_push([f'refs/heads/feat/task {zero} refs/heads/feat/task {one}']))
        self.assertTrue(validate_push(['not a valid ref line']))
        self.assertFalse(validate_push([f'refs/heads/feat/task {one} refs/heads/feat/task {zero}']))
        with patch('git_guard.subprocess.run', return_value=subprocess.CompletedProcess([],1)):
            self.assertTrue(validate_push([f'refs/heads/feat/task {one} refs/heads/feat/task {two}']))
        with patch('git_guard.subprocess.run', return_value=subprocess.CompletedProcess([],0)):
            self.assertFalse(validate_push([f'refs/heads/feat/task {one} refs/heads/feat/task {two}']))

    def test_mirrors_and_secret_hygiene(self):
        files=collect(ROOT)
        self.assertEqual(check_files(files), [])
        broken=dict(files); broken['.claude/skills/security-review/SKILL.md']=b'changed'
        self.assertTrue(any('mirror drift' in e for e in check_files(broken)))
        broken=dict(files); broken['.env.local']=b'VALUE=not-a-real-secret'
        self.assertTrue(any('Private configuration' in e for e in check_files(broken)))
        token=('gh'+'p_')+'a'*36
        broken=dict(files);broken['fixture.txt']=token.encode()
        errors=check_files(broken)
        self.assertTrue(any('GitHub token' in e for e in errors))
        self.assertNotIn(token,'\n'.join(errors))
        self.assertFalse(private_path('nested/.env.example'))
        self.assertTrue(private_path('nested/.env.prod'))

    def test_sync_detects_drift_without_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/'.agents/skills/example').mkdir(parents=True)
            (root/'.agents/skills/example/SKILL.md').write_text('---\nname: example\ndescription: Example\n---\n')
            (root/'.agents/skill-mirrors.json').write_text(json.dumps({'source':'.agents/skills','mirrors':['.claude/skills']}))
            self.assertTrue(sync(root,check=True))
            self.assertFalse((root/'.claude').exists())
            self.assertEqual(sync(root),[])
            self.assertEqual(sync(root,check=True),[])
            (root/'.claude/skills/example/foreign.txt').write_text('preserve')
            self.assertTrue(sync(root))
            self.assertTrue((root/'.claude/skills/example/foreign.txt').exists())

    def test_sync_rejects_destination_symlink_without_touching_target(self):
        with tempfile.TemporaryDirectory() as folder, tempfile.TemporaryDirectory() as outside:
            root=Path(folder);external=Path(outside)
            (root/'.agents/skills/example').mkdir(parents=True)
            (root/'.agents/skills/example/SKILL.md').write_text('safe')
            (root/'.agents/skill-mirrors.json').write_text(json.dumps({'source':'.agents/skills','mirrors':['.claude/skills']}))
            (root/'.claude/skills').mkdir(parents=True)
            try:(root/'.claude/skills/example').symlink_to(external,target_is_directory=True)
            except OSError:self.skipTest('Symlink creation unavailable on this platform/account')
            self.assertTrue(sync(root))
            self.assertEqual(list(external.iterdir()),[])

    def test_sync_rejects_path_escape_before_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/'.agents').mkdir()
            (root/'.agents/skill-mirrors.json').write_text(json.dumps({'source':'../private','mirrors':['../../outside']}))
            self.assertTrue(sync(root))

    def test_ruleset_verification_does_not_accept_files_as_active_protection(self):
        for branch in ['main','dev']:
            definition=json.loads((ROOT/f'.github/rulesets/{branch}.json').read_text())
            verify_rules(branch,definition['rules'])
        with self.assertRaises(RuntimeError):verify_rules('main',[])

    def test_cross_platform_and_secret_checks_are_required_for_solo_rules(self):
        for branch in ['main','dev']:
            definition=json.loads((ROOT/f'.github/rulesets/{branch}.json').read_text())
            pr=next(rule for rule in definition['rules'] if rule['type']=='pull_request')
            self.assertEqual(pr['parameters']['required_approving_review_count'],0)
            for name in ['windows-checks','python-minimum-checks','secret-scan']:
                changed=json.loads(json.dumps(definition['rules']))
                status=next(rule for rule in changed if rule['type']=='required_status_checks')
                status['parameters']['required_status_checks']=[c for c in status['parameters']['required_status_checks'] if c['context']!=name]
                with self.subTest(branch=branch,check=name),self.assertRaises(RuntimeError):
                    verify_rules(branch,changed)

    def test_server_bypass_and_weakened_parameters_are_rejected(self):
        expected=json.loads((ROOT/'.github/rulesets/main.json').read_text())
        verify_definition(expected,expected)
        normalized=json.loads(json.dumps(expected))
        for check in normalized['rules'][-1]['parameters']['required_status_checks']:check['integration_id']=None
        verify_definition(expected,normalized)
        changed=json.loads(json.dumps(expected));changed['bypass_actors']=[{'actor_id':1}]
        with self.assertRaises(RuntimeError):verify_definition(expected,changed)
        changed=json.loads(json.dumps(expected));changed['enforcement']='disabled'
        with self.assertRaises(RuntimeError):verify_definition(expected,changed)
        changed=json.loads(json.dumps(expected));changed['rules'][-1]['parameters']['strict_required_status_checks_policy']=False
        with self.assertRaises(RuntimeError):verify_definition(expected,changed)

    def test_trusted_routing_workflow_no_pr_checkout_and_matches_source(self):
        workflow=(ROOT/'.github/workflows/branch-policy.yml').read_text()
        self.assertEqual(workflow,render())
        self.assertNotIn('actions/checkout',workflow)
        self.assertNotIn('secrets.',workflow)
        # Execute the exact embedded policy, independent of a PR's changed git_guard.py.
        marker="python3 - <<'PYTHON'\n"
        body=workflow.split(marker,1)[1].rsplit('          PYTHON',1)[0]
        body='\n'.join(line[10:] if line.startswith('          ') else line for line in body.splitlines())
        for base,head,repo,expected in [('dev','feat/task','owner/project',0),('main','dev','owner/project',0),('main','feat/task','owner/project',1),('main','dev','fork/project',1)]:
            env={**os.environ,'PR_BASE':base,'PR_HEAD':head,'PR_HEAD_REPO':repo,'PR_BASE_REPO':'owner/project'}
            result=subprocess.run([sys.executable,'-c',body],env=env,capture_output=True)
            self.assertEqual(result.returncode,expected)

    def test_fork_cannot_impersonate_dev_promotion(self):
        with tempfile.TemporaryDirectory() as folder:
            event=Path(folder)/'event.json'
            event.write_text(json.dumps({'pull_request':{'base':{'ref':'main','repo':{'full_name':'owner/project'}},'head':{'ref':'dev','repo':{'full_name':'other/project'}}}}))
            env={**os.environ,'GITHUB_EVENT_NAME':'pull_request','GITHUB_EVENT_PATH':str(event)}
            result=subprocess.run([sys.executable,str(ROOT/'scripts/git_guard.py'),'ci'],env=env,capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('same repository', result.stderr.replace('this repository','same repository'))

class GitIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.git('init','-b','feat/test')
        self.git('config','user.name','Fixture')
        self.git('config','user.email','fixture@example.invalid')
        # A disposable minimal repository checks actual hook execution, not just helper calls.
        (self.root/'scripts').mkdir()
        for name in ['git_guard.py','project_checks.py','review_gate.py']:
            shutil.copyfile(ROOT/'scripts'/name,self.root/'scripts'/name)
        shutil.copytree(ROOT/'.githooks',self.root/'.githooks')
        for hook in (self.root/'.githooks').iterdir():hook.chmod(0o755)
        (self.root/'value.txt').write_text('baseline')
        self.git('add','.')
        self.git('commit','-m','fixture baseline')
        self.git('config','core.hooksPath','.githooks')

    def tearDown(self):self.temp.cleanup()

    def git(self,*args,check=True):
        return subprocess.run(['git',*args],cwd=self.root,capture_output=True,text=True,check=check)

    def test_bootstrap_preserves_inherited_hooks(self):
        self.git('config','--local','--unset','core.hooksPath')
        config=self.root/'global.config'
        config.write_text('[core]\n    hooksPath = /organization/security-hooks\n')
        with patch.dict(os.environ,{'GIT_CONFIG_GLOBAL':str(config)}),patch.object(bootstrap,'ROOT',self.root),patch.object(bootstrap,'sync',return_value=[]):
            self.assertEqual(bootstrap.main(),1)
            local=self.git('config','--local','--get','core.hooksPath',check=False)
            self.assertEqual(local.returncode,1)

    def test_actual_commit_hooks_block_main_and_dev(self):
        for branch in ['main','dev']:
            self.git('checkout','-b',branch)
            (self.root/'value.txt').write_text(branch)
            self.git('add','value.txt')
            result=self.git('commit','-m','should be blocked',check=False)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('Direct commits',result.stderr)
            self.git('restore','--staged','value.txt')
            self.git('restore','value.txt')

    def test_actual_push_hook_blocks_feature_to_main_refspec(self):
        bare=self.root/'remote.git'
        self.git('init','--bare',str(bare))
        self.git('remote','add','origin',str(bare))
        result=self.git('push','origin','HEAD:refs/heads/main',check=False)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('Direct pushes',result.stderr)

    def test_review_receipt_blocks_missing_and_changed_snapshots(self):
        # This fixture does not contain the full template context checked by this hook.
        (self.root/'scripts/project_checks.py').write_text('print("fixture checks passed")\n')
        (self.root/'value.txt').write_text('reviewed change')
        self.git('add','value.txt')
        blocked=self.git('commit','-m','missing review',check=False)
        self.assertNotEqual(blocked.returncode,0)
        self.assertIn('review receipt',blocked.stderr)
        gate=self.root/'scripts/review_gate.py'
        snapshot=json.loads(subprocess.check_output([sys.executable,str(gate),'snapshot'],cwd=self.root,text=True))
        record=subprocess.run([sys.executable,str(gate),'record','--tree',snapshot['tree'],
                               '--parent',snapshot['parent'],'--reviewer','independent-test-session',
                               '--evidence','No findings'],cwd=self.root,capture_output=True,text=True)
        self.assertEqual(record.returncode,0,record.stderr)
        (self.root/'value.txt').write_text('changed after review')
        self.git('add','value.txt')
        stale=self.git('commit','-m','stale review',check=False)
        self.assertNotEqual(stale.returncode,0)
        self.assertIn('does not match',stale.stderr)
        (self.root/'value.txt').write_text('reviewed change')
        self.git('add','value.txt')
        self.assertEqual(self.git('commit','-m','reviewed',check=False).returncode,0)

    def test_merge_commit_is_blocked(self):
        self.git('checkout','-b','feat/other')
        (self.root/'other.txt').write_text('other')
        self.git('add','other.txt')
        # Build a separate commit before enabling the hook in this disposable fixture.
        self.git('config','--local','--unset','core.hooksPath')
        self.git('commit','-m','other')
        self.git('checkout','feat/test')
        (self.root/'local.txt').write_text('local')
        self.git('add','local.txt')
        self.git('commit','-m','local')
        self.git('config','core.hooksPath','.githooks')
        result=self.git('merge','--no-ff','feat/other','-m','merge',check=False)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('Local merge commits are blocked',result.stderr)

    def test_cherry_pick_without_review_is_blocked(self):
        self.git('checkout','-b','feat/other')
        (self.root/'other.txt').write_text('other')
        self.git('add','other.txt')
        self.git('config','--local','--unset','core.hooksPath')
        self.git('commit','-m','other')
        other=self.git('rev-parse','HEAD').stdout.strip()
        self.git('checkout','feat/test')
        self.git('config','core.hooksPath','.githooks')
        result=self.git('cherry-pick',other,check=False)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('review receipt',result.stderr)

    def test_index_scan_cannot_be_hidden_by_clean_worktree(self):
        token=('gh'+'p_')+'b'*36
        (self.root/'value.txt').write_text(token)
        self.git('add','value.txt')
        (self.root/'value.txt').write_text('clean working copy')
        snapshot=collect(self.root,staged=True)
        self.assertEqual(snapshot['value.txt'],token.encode())
        self.assertTrue(any('GitHub token' in e for e in check_files(snapshot)))

if __name__ == '__main__':unittest.main()
