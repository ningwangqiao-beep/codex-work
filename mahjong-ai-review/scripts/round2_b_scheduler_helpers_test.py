import json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scheduler.audit_helpers import source_fingerprints,append_event
class Helpers(unittest.TestCase):
 def test_recursive_relative_cycle(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/'pkg').mkdir();(p/'pkg/__init__.py').write_text('');(p/'main.py').write_text('from pkg import a\nimport os\n');(p/'pkg/a.py').write_text('from . import b\n');(p/'pkg/b.py').write_text('from . import a\n')
   r=source_fingerprints(p,['main.py']);self.assertEqual(set(r['fingerprints']),{'main.py','pkg/__init__.py','pkg/a.py','pkg/b.py'})
 def test_escape(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(ValueError):source_fingerprints(d,['../outside.py'])
 def test_dynamic_report(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/'a.py').write_text('__import__("x")');self.assertEqual(source_fingerprints(p,['a.py'])['dynamic_imports'][0]['line'],1)
 def test_append_preserves(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'events.jsonl';append_event(p,{'type':'stopped','code':75});before=p.read_bytes();append_event(p,{'type':'resumed'});self.assertTrue(p.read_bytes().startswith(before));self.assertEqual(len([json.loads(s) for s in p.read_text().splitlines()]),2)
if __name__=='__main__':unittest.main()
