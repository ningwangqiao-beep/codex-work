import sys
import ctypes,json,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
start=time.perf_counter()
from rules.fast_hand_analysis import shanten,effective_draws
h=[0,1,2,3,4,5,6,7,8,9,9,9,10];r=shanten(h,0,2);e=effective_draws(h,0,2);elapsed=time.perf_counter()-start
class PMC(ctypes.Structure):
 _fields_=[('cb',ctypes.c_ulong),('faults',ctypes.c_ulong)]+[(k,ctypes.c_size_t) for k in ('peakworking','working','peakpaged','paged','peaknonpaged','nonpaged','pagefile','peakpagefile')]
p=PMC();p.cb=ctypes.sizeof(p)
k=ctypes.windll.kernel32;k.GetCurrentProcess.restype=ctypes.c_void_p
ok=ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.c_void_p(k.GetCurrentProcess()),ctypes.byref(p),p.cb)
assert ok
out=dict(process_cold_seconds=elapsed,working_set_bytes=p.working,peak_working_bytes=p.peakworking,result=r,effective=e,uses_gpu=False)
Path('reports/v3_b_fast_cold.json').write_text(json.dumps(out,indent=2));print(out)

