import copy
import io
from unittest.mock import patch
import json
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
def module(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/f'{name}.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
cleanup=module('cleanup_merged_branches')
sync=module('sync_cleanup_workflow')

class CleanupTests(unittest.TestCase):
    def setUp(self):
        self.pr={'merged':True,'merge_commit_sha':'b'*40,
            'base':{'ref':'dev','repo':{'full_name':'owner/project'}},
            'head':{'ref':'feat/test','sha':'a'*40,'repo':{'full_name':'owner/project'}}}
    def test_only_merged_task_into_same_repo_dev(self):
        self.assertEqual(cleanup.candidate(self.pr,'owner/project'),('feat/test','a'*40))
        for key,value in [('merged',False),('merge_commit_sha',None)]:
            p=copy.deepcopy(self.pr);p[key]=value;self.assertIsNone(cleanup.candidate(p,'owner/project'))
        for part,key,value in [('base','ref','main'),('head','ref','dev'),('head','ref','main'),
                               ('head','ref','feat/../main'),('head','ref','feat/'),
                               ('head','repo',{'full_name':'fork/project'}),('head','sha','oops')]:
            p=copy.deepcopy(self.pr);p[part][key]=value;self.assertIsNone(cleanup.candidate(p,'owner/project'))
    def test_main_retention_and_changed_head(self):
        for stable_status, head_sha, expected in [('behind','a'*40,False),('ahead','a'*40,True),('ahead','c'*40,False)]:
            def open_api(request, timeout):
                url=request.full_url
                if '/pulls?' in url: data=[{'number':7}]
                elif url.endswith('/pulls/7'): data=self.pr
                elif url.endswith('...dev'): data={'status':'ahead'}
                elif url.endswith('...main'): data={'status':stable_status}
                elif '/git/matching-refs/' in url: data=[{'ref':'refs/heads/feat/test','object':{'sha':head_sha}}]
                else: raise AssertionError(url)
                return io.BytesIO(json.dumps(data).encode())
            with patch.dict(os.environ,{'GITHUB_REPOSITORY':'owner/project','GH_TOKEN':'synthetic'}), patch.object(cleanup.urllib.request,'urlopen',side_effect=open_api), patch.object(cleanup,'delete_with_lease') as delete:
                cleanup.main()
                self.assertEqual(delete.called,expected)

    def test_generated_workflow_is_trusted_and_current(self):
        text=sync.render();self.assertEqual(text,(ROOT/'.github/workflows/cleanup-branches.yml').read_text())
        self.assertNotIn('actions/checkout',text)
        self.assertNotIn('github.event.pull_request.head.ref }}',text)
        self.assertIn('contents: write',text)
        self.assertIn('--force-with-lease=refs/heads/',text)
    def test_real_git_lease_preserves_changed_head(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); remote=root/'remote.git';work=root/'work'
            def git(*args, cwd=None, check=True):
                return subprocess.run(['git',*args],cwd=cwd,text=True,capture_output=True,check=check)
            git('init','--bare',str(remote));git('init',str(work))
            git('config','user.name','Test',cwd=work);git('config','user.email','test@example.invalid',cwd=work)
            git('checkout','-b','feat/test',cwd=work);git('commit','--allow-empty','-m','first',cwd=work)
            old=git('rev-parse','HEAD',cwd=work).stdout.strip();git('push',str(remote),'HEAD',cwd=work)
            git('commit','--allow-empty','-m','new work',cwd=work);git('push',str(remote),'HEAD',cwd=work)
            new=git('rev-parse','HEAD',cwd=work).stdout.strip()
            args=['push','--force-with-lease=refs/heads/feat/test:'+old,str(remote),':refs/heads/feat/test']
            self.assertNotEqual(git(*args,cwd=work,check=False).returncode,0)
            self.assertIn(new,git('ls-remote',str(remote),'refs/heads/feat/test',cwd=work).stdout)
            args[1]='--force-with-lease=refs/heads/feat/test:'+new
            git(*args,cwd=work)
            self.assertFalse(git('ls-remote',str(remote),'refs/heads/feat/test',cwd=work).stdout)

if __name__=='__main__':unittest.main()
