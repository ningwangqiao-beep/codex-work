# SICHUAN-XUEZHAN-4FAN-V3

User-provided target levels, not additive: basic1; all-triplets/pure-suit/dai-yao/seven-pairs2; dragon-pairs/pure-triplets/jiang-triplets3; pure-seven/pure-dragon4. Highest matching target wins; basic never added again. Self draw exactly once min(4,base+1). Ordinary payment 2^fan. Current active nonwinner pay self draw.

Gang payments outside win cap: concealed active others2; added active others1; direct discarder2 plus other active opponents1. Robbed added kong produces no gang fees. Original zero-sum transfer ledger kept; refunds reverse original payments. Table defaults remain legacy unless explicitly passed V3Config. Frozen source snapshots unchanged. Mathematic fifth-copy fixes retained.

Explicit ambiguities: dai-yao means every meld and pair contains terminal, sequences123/789 only, terminal triplets/pair; jiang-triplets uses ranks2/5/8 only. Mixed unlisted combinations select max named target rather than add. Extra roots/last-tile/gang-win bonuses disabled. These room details remain assumptions, not Weile certification.

Terminal assumptions inherited and explicitly isolated: active flower-pigs pay16 to each active nonpig; nonpig nonready pay ready maximum V3 base-hand payment (no self-draw bonus); big/small cha-jiao not separately confirmed, currently single cha_jiao_enabled maximum-payment mode; gang refund for active unready receivers to original payers. Earlier winners excluded. No passed-win lock. These assumptions require further configuration before claiming arbitrary-room support.

Ledger categories mutually exclusive transfer events: discard_win, self_draw, rob_kong_win, direct_kong, concealed_kong, added_kong, cha_jiao, flower_pig, gang_refund. Every event has payer/receiver/amount and sums zero. No separate repeated other-loss charge.

V3 terminal-mode implementation supersedes earlier incomplete notice: V3Config.cha_jiao_mode supports max_wait_payment (default), min_wait_payment, disabled. As explicit simulation assumptions, max is named big cha-jiao and min small cha-jiao; both use configured base-hand discard payments over structurally legal waits, exclude flower pigs and earlier winners, and keep same ready membership for gang refunds. Ledger categories are cha_jiao_big/cha_jiao_small, no double charging both modes. Disabled skips cha-jiao transfers. cha_jiao_enabled=False remains master legacy-compatible off switch. Actual room meanings unverified. Earlier winner gang/selfdraw payments and extra gang-win bonuses remain disabled/active-only assumptions.
