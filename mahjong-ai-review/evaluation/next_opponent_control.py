"""Stable within-sample event-multiset permutation for history negative control."""
import hashlib,torch

def shuffle_history(tokens,mask,sample_keys,seed=42):
 if tokens.shape[:2]!=mask.shape or len(sample_keys)!=len(tokens) or mask.dtype!=torch.bool or (mask[:,1:]&~mask[:,:-1]).any():raise ValueError('Bad history control batch')
 shuffled=tokens.clone()
 for i,key in enumerate(sample_keys):
  n=int(mask[i].sum());value=int.from_bytes(hashlib.sha256((str(seed)+':'+str(key)).encode()).digest()[:8],'little')%(2**63);generator=torch.Generator(device='cpu').manual_seed(value);order=torch.randperm(n,generator=generator).to(tokens.device);shuffled[i,:n]=tokens[i,:n][order]
 return shuffled
