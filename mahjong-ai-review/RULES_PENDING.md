# Proposed simulation rule configuration, not verified Weile room rules

Version: simulation-v1. Basic win 0 fan; all triplets +1; seven pairs +2; pure suit +2; additive cap 4 fan, payment 2^fan. No roots, kong-win bonus or self-draw bonus. Active players alone pay self draw. Discard allows multiple simultaneous winners and physical tile recorded once. Added kong may be robbed, concealed kong may not. Missing suit tiles must all be discarded before claiming melds. Exchange three same-suit tiles, fixed configurable direction. No passed-win restrictions in this configuration. Public wall count derives from initial wall and draws.

Terminal settlement: active flower-pig players pay 16 to each active non-pig; active non-pig non-ready players pay active ready players their maximum achievable configured win payment; flower pigs excluded from cha-jiao to avoid double penalty. Earlier winners excluded. No gang fees or refunds in this initial isolated configuration (explicitly disabled); thus not an implementation of a room requiring gang payments. All uncertainties require actual room evidence before official compatibility claim.

State constructor supports partial-inventory unit fixtures; full game audit must additionally require 108 tiles, 13 each at deal and stable total inventory. Engine does not arbitrate claim priority automatically: selfplay must evaluate all legal wins first, then kong/peng by seat order, otherwise advance. Player style must never inspect other hidden hands.

Optional gang proposal now implemented: gang_payments_enabled=False by default; enabled concealed kong charges each active opponent 2, exposed kong charges discard payer 2, added kong charges each active opponent 1. Successfully robbed added kong has no fee. refund_unready_gangs=True reverses original gang transfers for receivers still active and not ready at exhaustion (including flower pigs), to original payers. These are simulation assumptions, not verified room facts.

Dragon seven pairs: dragon_pair_quad_fan is configurable, default 0. At positive value each four-copy group in seven-pairs adds that many fan, still capped at four. Claim API rejects any peng/kong when an active opponent can win the pending tile; this isolated configuration assumes all legal discard wins are taken rather than voluntary pass. This avoids an unmodelled passed-win state. Advancing without claims remains an explicit caller operation; selfplay must resolve wins before advance.

Round 2 privacy interpretation: concealed-kong identity is private to its owner; Table.concealed_kongs stores owner/meld-index so observation exporter can mask opponent identities. Tile count four and kong action remain public. This conservative information policy is a simulation assumption pending room evidence.

V3 assumptions now supersede legacy only under explicit V3Config. See RULES_V3.md. Dai-yao/jiang-triplet interpretation, unlisted combo max target, terminal flower-pig/max cha-jiao/refund relations remain unconfirmed. Big/small cha-jiao distinct payout modes remain not implemented, don't imply full room support.

V3 now implements explicit max_wait_payment/min_wait_payment/disabled cha-jiao modes. Naming max=big/min=small is a simulation interpretation requiring room evidence, not official confirmation. Supersedes earlier 'not implemented' status.
