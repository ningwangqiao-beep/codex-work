import torch
from models.networks import MahjongBrain
from models.round2_structured import StructuredBrain

def load_checkpoint(path,device='cpu'):
    s=torch.load(path,map_location=device,weights_only=False);config=dict(s['model_config']);architecture=config.pop('architecture',None)
    model=StructuredBrain(**config) if architecture=='structured-v1' else MahjongBrain(**config)
    model=model.to(device);model.load_state_dict(s['model']);return model,s
