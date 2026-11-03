"""Freeze rule champion and evidence; no re-evaluation or weight replacement."""
import dataclasses,hashlib,json,pathlib,platform,shutil,sys
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from scheduler.audit_helpers import source_fingerprints
from rules.v3 import V3Config
out=root/'champions/v3_rules_20261103'
if (out/'MANIFEST.json').exists():raise RuntimeError('Champion snapshot already frozen')
out.mkdir(parents=True,exist_ok=True)
report=json.loads((root/'reports/v3_chief_final_evaluation_summary.json').read_text())
if report['status']!='completed' or report['complete_seed_groups']!=5000:raise ValueError('Final evaluation not completed')
dependency=source_fingerprints(root,['baselines/v3_bot.py','simulator/v3_selfplay.py','scripts/v3_data_resumable_compare.py'])
files=[]
for relative,digest in dependency['fingerprints'].items():
    p=root/relative;dest=out/'source'/relative;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    if hashlib.sha256(dest.read_bytes()).hexdigest()!=digest:raise ValueError('Source changed during snapshot')
    files.append({'path':relative,'sha256':digest})
evidence=[]
for relative in ['reports/v3_d_compare_5000000_mixed.json','reports/v3_d_compare_5000000_mixed.jsonl','reports/v3_chief_final_evaluation_summary.json','reports/v3_final_preregistration.json','reports/v3_chief_ready.json','reports/v3_chief_batch_recheck.json','reports/v3_chief_gate_tests.log']:
    p=root/relative;h=hashlib.sha256(p.read_bytes()).hexdigest();evidence.append({'path':relative,'sha256':h,'bytes':p.stat().st_size})
    if p.suffix!='.jsonl':
        dest=out/'evidence'/p.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
manifest={'champion_id':'v3-rules-20261103','ability_type':'deterministic_rule_program_not_trained_network','learned_weights':[],'bot_configuration':{'two_step_draw_limit':2},'rule_configuration':dataclasses.asdict(V3Config()),'sources':files,'evaluation_data_and_evidence':evidence,'source_dependency_limits':dependency['coverage'],'dynamic_imports':dependency['dynamic_imports'],'evaluation_scope':'registered V3 simulation and fixed mixed opponents; no real-player certification','mean_net':report['summary']['new_baseline']['net'],'primary_comparison':report['comparisons']['new_baseline'],'python':platform.python_version(),'old_models_retained':True}
(out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2));(root/'reports/next_chief_champion_freeze.json').write_text(json.dumps(manifest,indent=2));print(json.dumps({'champion':manifest['champion_id'],'files':len(files),'evidence':len(evidence),'mean_net':manifest['mean_net'],'weights':'none - rule program'}))
