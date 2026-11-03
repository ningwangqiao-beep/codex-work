"""V3 current GPU tensor evidence; never overwrites prior probes."""
import pathlib,json,time,hashlib,subprocess,platform,datetime,torch
root=pathlib.Path(__file__).resolve().parents[1];torch.set_num_threads(2)
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':platform.python_version(),'torch':torch.__version__,'cuda_build':torch.version.cuda,'cuda_available':torch.cuda.is_available(),'scope':'GPU_environment_probe_not_mahjong_training','script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}
r['nvidia_smi']=subprocess.check_output(['nvidia-smi','--query-gpu=name,driver_version,memory.total,memory.used,temperature.gpu','--format=csv,noheader'],text=True).strip()
if not r['cuda_available']:
 (root/'reports/v3_c_gpu_probe.json').write_text(json.dumps(r,indent=2));raise RuntimeError('CUDA unavailable')
torch.manual_seed(42);torch.cuda.reset_peak_memory_stats();a=torch.randn(1024,1024,device='cuda',requires_grad=True);start=time.perf_counter();loss=(a@a.T).square().mean();loss.backward();torch.cuda.synchronize();r.update(device=torch.cuda.get_device_name(0),forward_backward_finite=bool(torch.isfinite(loss) and torch.isfinite(a.grad).all()),loss=float(loss.detach()),seconds=time.perf_counter()-start,peak_allocated_bytes=torch.cuda.max_memory_allocated());(root/'reports/v3_c_gpu_probe.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));assert r['forward_backward_finite']
