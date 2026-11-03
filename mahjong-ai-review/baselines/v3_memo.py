"""V3 memoized exact existing calculator. Cache does not change formula."""
from functools import lru_cache
from rules.hand_analysis import shanten as _shanten,effective_draws as _effective
@lru_cache(maxsize=30000)
def _s(h,opened,missing,public):return _shanten(h,opened,missing,public)
@lru_cache(maxsize=10000)
def _e(h,opened,missing,public):return tuple((x['tile'],x['remaining'],x['shanten']) for x in _effective(h,opened,missing,public))
def shanten(hand,opened=0,missing=None,public=()):return dict(_s(tuple(sorted(hand)),opened,missing,tuple(sorted(public))))
def effective_draws(hand,opened=0,missing=None,public=()):return [dict(tile=t,remaining=n,shanten=s) for t,n,s in _e(tuple(sorted(hand)),opened,missing,tuple(sorted(public)))]
