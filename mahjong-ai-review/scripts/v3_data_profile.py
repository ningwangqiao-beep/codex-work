import sys,time,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from simulator.v3_selfplay import play
from baselines.v3_bot import BaselineV3
from baselines.v3_memo import _s,_e
captured=[]
def capture(o,legal):
 if not captured:captured.append((o,legal))
 return legal[0]
play(3500000,policy=capture,policy_seat=0)
o,legal=captured[0];bot=BaselineV3();start=time.perf_counter();a=bot(o,legal);cold=time.perf_counter()-start;details=bot.last_analysis;start=time.perf_counter();b=bot(o,legal);warm=time.perf_counter()-start;assert a==b and details==bot.last_analysis
r=dict(seed=3500000,cold_seconds=cold,warm_seconds=warm,legal_count=len(legal),chosen=a,exact_repeat=True,shanten_cache=str(_s.cache_info()),effective_cache=str(_e.cache_info()),details=details,limits={'shanten_cache':30000,'effective_cache':10000,'draw_branch':2,'discard_branch':2},not_game_strength_evaluation=True)
Path('reports/v3_d_baseline_profile.json').write_text(json.dumps(r,indent=2));print({k:v for k,v in r.items() if k!='details'})
