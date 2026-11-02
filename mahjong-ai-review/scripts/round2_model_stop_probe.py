import sys,pathlib,os,json,torch
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from models.round2 import AblationBrain
from training.streaming import train
m=json.load(open(root/'datasets/simulation_v2/manifest.json'));out=root/'experiments/round2_c/stop_probe';out.mkdir(parents=True,exist_ok=True);stop=out/'STOP';stop.write_text('test');os.environ['MAHJONG_STOP_FILE']=str(stop)
try:train(AblationBrain('A',loss_bins=m['loss_bins']).cuda(),m,out,epochs=1)
except SystemExit as e:assert e.code==75
else:raise AssertionError('stop ignored')
stop.unlink();del os.environ['MAHJONG_STOP_FILE'];s=torch.load(out/'last.pt',weights_only=False);assert s['interrupted_epoch']==0 and s['batches_completed']==0
print('STOP checkpoint exit75 PASS')
