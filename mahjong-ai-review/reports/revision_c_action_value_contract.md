# Revision C shared state/candidate action-value interface

Implemented new files only; old frozen models/training sources untouched:

- models/revision_action_value.py:5970 parameters for state128/candidate12, shared32-wide state encoder,16-wide candidate encoder,32-wide concatenated candidate fusion,scalar action head and independent scalar state-value head.
- models/revision_candidate_schema.py: D BaselineBot analysis adapter, canonical27 candidate slots,12 explicit candidate features, legal mask. Missing seven-pairs and uncomputed secondary details have presence flags.
- evaluation/revision_action_value.py: exact/equivalent/top1/3/5, teacher target-value regret, masked regression error. Ties use declared tolerance and stable canonical tile ordering; illegal actions never count as topk success.
- scripts/revision_model_action_value.py: audited supervised streaming mini-batch trainer and separate --smoke path. No RL implementation or authorization implied.

Target contract:

    game_id, seed, source_group
    state_features[128]
    candidate_features[27,F]
    legal_mask[27] (binary, at least one legal)
    action_targets[27]
    optional state_target (only with state_target_definition)

D's current lexicographic(debt,structural,-effective,-two_draw,-one_draw,-fan,risk,tile) is NOT whole-game Q. Adapter excludes final tile tie when defining equivalent actions, maps unique preference groups to ordinal rank in[0,1], and declares target_semantics=lexicographic_preference_rank. Score spacing represents rank only; reported regret is in those teacher label units, not Mahjong net money. A state-return target is not invented: absent state_target_definition means no state-value loss and state_head_trained=false. Such a checkpoint must not be deployed as audited whole-game ValueNet.

Formal supervised manifest requires dataset_version, teacher_definition, target_semantics, state_dim, candidate_dim, candidate_feature_names, shards(train/validation), audit_path/audit_sha256 and source_fingerprints. Audit must bind dataset_fingerprint and source_fingerprints and explicitly attest observation_filter_audited. Data SHA=SHA256(json.dumps({str(shard_path):fileSHA256,...},sort_keys=True).encode()). Game IDs and(source_group,seed) cannot overlap splits; empty sets, missing fields, invalid values/masks rejected. No final-test shard is read.

Training losses recorded separately: action_value_mse, equivalent_ranking_ce, optional state_value_mse. Checkpoints include optimizer/RNG/data+source+schema binding/teacher semantics. STOP saves last and exits75; interrupted epoch restarts from its beginning. Completed outputs immutable, nonempty output needs --resume; every improved best is immutable best_epoch_N.pt, with BEST.json pointer, not an overwritten sole weight file.

Actual verification:

    .venv/Scripts/python.exe scripts/revision_model_action_value.py --smoke --output reports/revision_c_action_value_smoke.json

CPU2,seed42,2 legal Mahjong hand fixtures; one synthetic optimizer update only. Actual exit0. Tested shared/candidate/state head finite gradients,legal argmax,invalid all-false mask and NaN rejection,equal target-value tie semantics,checkpoint parameter roundtrip. state targets are synthetic fixture indices, not game returns. Evidence revision_c_action_value_smoke.json/.log/_exitcode.txt, checkpoint revision_c_action_value_smoke.pt. D adapter legal/same-preference fixture independently passed CPU. First smoke exposed torch argsort keyword mismatch, corrected then re-executed successfully.

No audited supervised candidate dataset available yet, so no formal Mahjong training, full trainer resume run or real state-value validation is claimed. Candidate CLI ready for scheduling after dataset audit:

    .venv/Scripts/python.exe scripts/revision_model_action_value.py --manifest PATH_TO_AUDITED_ACTION_MANIFEST --output checkpoints/revision_action_value_v1 --epochs 3 --resume

User's tightened gates remain: no new RL before rules,strong Bot,and value-network audit. Complete Claude S0-S12 source is unavailable; this implements the requested interface only, not a certified reconstruction.
