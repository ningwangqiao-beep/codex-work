"""Read completed result files only; no data/test inference."""
import argparse,pathlib,json
p=argparse.ArgumentParser();p.add_argument('--root',default=str(pathlib.Path(__file__).resolve().parents[1]));p.add_argument('--output',required=True);a=p.parse_args();root=pathlib.Path(a.root)
r={'scope':'research_simulator_only','ablation':{},'reports':{},'limitations':['A-F here use constrained128-feature proxies; not requested complete ordered-history ablation','no human-player validation','old final tests never reopened for optimization','public counts may encode game progress; AUC gain does not prove history reading']}
for path in sorted((root/'experiments'/'round2_c').glob('*/validation.json')):r['ablation'][path.parent.name]=json.loads(path.read_text())
for path in sorted((root/'reports').glob('round2_c*calibration*.json')):r['reports'][path.name]=json.loads(path.read_text())
for path in sorted((root/'reports').glob('round2_c*final*.json')):r['reports'][path.name]=json.loads(path.read_text())
pathlib.Path(a.output).write_text(json.dumps(r,indent=2));print('Summary written:',a.output)
