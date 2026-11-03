# History audit: confirmed old-source gaps

Read-only inspected simulator/v3_selfplay.py and observations/v3_public.py; no champion source modifications. Missing public history events: setup dealer initial draw, exposed-kong replacement draw, successful rob_kong_win (present in win_events but absent public_history), passes. Exchange and missing declarations present; missing suit available in state although declaration event lacks suit. Concealed kong masks tile; draw events carry no private tile, appropriate. Exchange view gives observer own sent/received only with explicit historical scope, not current holding guarantee.

D notified to implement separate v3_history_v2 source with monotonic causal event indices, public/private boundaries and synthetic helper fixtures so rare robbery/multiwin paths can be tested independently. No training and no frozen-source writes by B.
