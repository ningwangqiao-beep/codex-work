# Round 2 independent rules audit

Actual rules suite: 38 tests passed in 0.005s. Command: py -3.13 -m unittest discover -s tests -p "test_rules*.py". Log round2_b_tests.txt. Current/frozen hashes and exact diffs preserved in round2_b_fingerprints.json and round2_b_*_diff.txt; frozen dataset untouched.

Frozen-vs-current behavior: stricter win-before-meld priority; exited winner cardinality; removal of wrapper layering; explicit dragon-pair bonus (default zero); public action API otherwise compatible. Existing generator already resolved wins first, so priority fix should not change its intended games; D must nevertheless re-audit fingerprints.

Round 2 fixes: rejected negative/noninteger score/fee parameters, which previously could mutate a kong before negative payment rejection; concealed kong metadata now tracked as (player, meld_index). D notified to mask opponent concealed-kong tile identities and not publish draw tile identities. Frozen selfplay did not perform concealed kongs, so new leak concern does not invalidate those specific old observations. Masking and future dataset audit belong to D.

Reviewed potential discard labels: union is exact three-seat bitmask, total liability sums configured actual winning payments, not marginal probabilities; candidate_mask gates discard legality separately. Hidden full state remains labels only. Active-player and missing-suit conditions checked by winning. Tenpai labels are structural current waits, not future win labels. No evidence of future input in current observation source; broader history schema audits remain D's responsibility.

Covered: multiple winners physically share one tile; frozen winner hands remain archived; zero-sum transfers; concealed/exposed/added gang fees and refund path; robbery has no gang fee; empty wall kong refuses without changing state; malformed win/claim refuses without changing state; strict full deck/phase cardinality; seven pairs/dragon option; flower-pig/cha-jiao idempotence and switch.

Limitations remain explicitly simulated: no passed-win/passed-peng lock, root/last-tile/gang-win bonus; gang fees disabled default; no self-draw surcharge; fixed exchange direction; structural readiness ignores exhausted external copies; discard multiwin continuation follows discarder next active. Not certified Weile adaptation. Full game re-audit by D is required after current metadata/config validation hash changes.
