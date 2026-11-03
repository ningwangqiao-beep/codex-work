# V3 rules audit

Executed: py -3.13 -m unittest discover -s tests -p "test_rules*.py". Exit0; 61 test methods passed in6.937s; reports/v3_b_tests.log and v3_b_exitcode.txt. Tests cover base/selfdraw no duplicate fan/cap, seven/dragon/pure seven target levels, active-only selfdraw, all gang matrices, zero-sum ledger reconstruction, legacy multiwin/rob/terminal cases and mathematical audit regressions.

New V3 implementation rules/v3.py; existing core.score dispatches only when explicit config.rule_version matches. Legacy default remains legacy. simulator/table.py consumes V3 config, self draw and direct-gang relationship; ledger records all mutually exclusive transfers. Initial desired fan/matrix behavior ready for D small integration, NOT 1000/10000 audit pass and NOT new-rule training admission.

No Claude source received. No new RL or large training started by B. Rule uncertainties documented RULES_V3.md and RULES_PENDING.md; not Weile official compatibility certification. Big/small cha-jiao separate modes not yet implemented, terminal payout config granularization remains work.

Main-review corrections: immutable pattern_levels and explicit combination/dai-yao/jiang policies in V3Config; unsupported version/fees/policies rejected. score returns rule_source=user_specification, room_verified=False and assumed_components. Ledger checked against score reconstruction on every Table.check; refunds carry reversal=True. Updated actual test result:63 methods passed6.923s exit0, same command/log.

Final revision supersedes prior statement of missing big/small implementation: three explicit cha_jiao_mode values now implemented and tested; big=max wait payment, small=min wait payment are SIMULATION ASSUMPTIONS, not room certification. Latest full command same; actual68 rules methods passed6.974s exit0. Matrix tests enumerate concealed/added eight active subsets, direct four subsets, ten patterns with basefan1..4 and selfdraw cap, refund signals and each terminal mode. Sources now frozen for chief independent tests and D small integration; no1000/10000 pass claimed by B.
