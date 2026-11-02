import json, pathlib, platform, time
import torch
out = pathlib.Path(__file__).resolve().parents[1] / 'reports' / 'gpu_probe.json'
r = dict(python=platform.python_version(), torch=torch.__version__, cuda_build=torch.version.cuda, cuda_available=torch.cuda.is_available())
if r['cuda_available']:
    torch.manual_seed(42)
    a=torch.randn(1024,1024,device='cuda',requires_grad=True)
    start=time.perf_counter()
    loss=(a@a.T).square().mean()
    loss.backward()
    torch.cuda.synchronize()
    r.update(device=torch.cuda.get_device_name(0),loss=loss.item(),finite=bool(torch.isfinite(a.grad).all()),seconds=time.perf_counter()-start,peak_bytes=torch.cuda.max_memory_allocated())
out.write_text(json.dumps(r,indent=2),encoding='utf-8')
print(out.read_text())
assert r['cuda_available'] and r['finite'], 'GPU test failed'
