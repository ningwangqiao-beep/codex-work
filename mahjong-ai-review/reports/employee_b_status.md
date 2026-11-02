# Employee B: first checkpoint

Actual verification: 6 unit tests passed, Python 3.13, 0.001s. See employee_b_tests.txt.

Implemented only: deterministic 108-tile dealing; basic decomposition and seven-pairs winning predicate; missing-suit gate; waits enumeration; forced missing-suit discards; multiple-winner payment conservation.

NOT a complete audited engine. Exchange, peng/kong action state machine, exposed-meld validation, scoring patterns/cap, gang settlement, cha-jiao/hua-zhu, passed-win restrictions, observation interface and full-game invariants remain incomplete. No training or large simulation authorized by this checkpoint.

No Weile-specific assumptions approved. Code is a reviewable foundation, not production rules. In particular meld_count is caller-supplied and is not a replacement for validating public meld tiles.

Test command from project directory: py -3.13 -m unittest discover -s tests -p test_rules_core.py

Checkpoint updated: Table now supports draw/advance/self-win/added-kong robbery/exhaustion/cha-jiao/flower-pig, optional gang ledger with unready refund. Strict full-game mode enforces initial 108 tiles, hand sizes and active player phase cardinality. B-only test suite: 29 passed (0.004s). Added rob-kong fixture initially had a fifth copy and correctly failed; fixture repaired without weakening invariants. Caller-supplied win payments are rejected unless equal to configured score. No large simulation run by B; D owns integration/selfplay audit. Full game acceptance depends on D/chief results, not this unit suite.

Boundary audit update: win priority is now enforced inside claim(), not solely caller arbitration. Strict mode validates exited winners' concealed counts (self-draw 14-3m; discard/rob 13-3m). Rule core wrapper layers removed. dragon_pair_quad_fan defaults to 0 (four equal tiles count as two pairs but add no bonus); explicit positive values add per-quad dragon-pair bonus under cap. All remain simulation assumptions. Five boundary transaction/rotation cases and dragon-pair config added. B suite 35 passed in 0.004s. D notified to regenerate fingerprints/re-audit; previous data remains bound to frozen source snapshot.

Remaining limitations: no passed-win lock; no passed-peng lock; no concealed-kong robbery; no root/gang-win/last-tile bonus; self draw has no surcharge; three exchange direction is configured rather than room-random; readiness uses legal structural waits irrespective of all external copies already visible (explicit interpretation); constructor accepts fixtures unless strict=True. No claim that these match a specific Weile room. Turn after discard multiwin proceeds from discarder to next active seat; external room evidence may require different convention.
