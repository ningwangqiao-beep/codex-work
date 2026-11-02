# Experiments

Only synthetic interface experiments completed: GPU tensor probe, MLP forward/backward, metric tie handling, temperature calibration and streaming checkpoint resume. No claim of reading opponents or beating statistical baseline.

Known limitations: score prediction is categorical over configured loss bins; supplied bins should cover exact configured loss values to prevent quantization ambiguity. Joint-risk and conditional-wait heads are independently supervised and can disagree; outputs expose marginal_disagreement and HEADS_NOT_PROBABILISTICALLY_CONSTRAINED. Calibration currently binary-temperature helper, not applied to untrained joint output. No real held-out accuracy or calibrated deal-in claims.

Pending: D's audited data, per-target active/candidate masks, complete independent test comparison and empirical frequency baseline, confidence intervals, trained calibration and deploy export.

�ڶ����Զ�ʵ�����½���ѳ־û���ROUND2_REPORT.md��reports/round2_automatic_results.json���������޸������������Ϊ׼�����ܽ�ѵ����ɵ����ɹ���


## ģ�»������Ժ��Զ���ʵ��
{
  "imitation": {
    "means": {
      "heuristic": 0.445,
      "old_reading_risk": -0.8525,
      "trained_policy_value": -0.4675
    },
    "comparison": {
      "mean_difference": -0.9125,
      "paired_seed_cluster_bootstrap_95ci": [
        -1.225,
        -0.625
      ]
    },
    "clear_improvement": false,
    "scope": "configured_simulator_only"
  },
  "imitation_then_rl": {
    "means": {
      "heuristic": 0.5525,
      "old_reading_risk": -0.6975,
      "trained_policy_value": -0.32
    },
    "comparison": {
      "mean_difference": -0.8725,
      "paired_seed_cluster_bootstrap_95ci": [
        -1.27,
        -0.4775
      ]
    },
    "clear_improvement": false,
    "scope": "configured_simulator_only"
  }
}
ֻ�ж�����������½����0�ű���ȷ���ƣ�ʧ�ܷ�������¼�������������齫AI�ɹ���

ģ��ѧϰ����ʧ���ѱ�������֤�ݣ�round2_warmstart_results.json����Ҫ����ä���Զ��ľ���������ת��Ϸ���ѡ�����ṹ����������/��Ч���Ų��ԡ�

����������������160��mean��+.15/CI[-.3125,+.6125]��δȷ�ϸĽ�����ѡ����teacher������ɣ�utility����100%�����ڻ������Ը��֡��²в��Զ��Ĵ�ð�̺���ƣ�������ǰ���Ƴɹ���


## ��ѡ�ṹ�в��Զ���ʵ�ʽ��
{
  "mean_difference": 0.0125,
  "paired_seed_bootstrap_95ci": [
    -0.3475,
    0.3675
  ],
  "simulation_only": true,
  "checkpoint_sha256": "a022c3df22b947da72d589753616c00b54b17df36867334493816d890303ad17",
  "flags": [
    "PAIRED_INITIAL_SEED_NOT_IDENTICAL_FUTURE",
    "RESIDUAL_EVAL_GREEDY_TRAIN_SOFTMAX"
  ],
  "clear_improvement": false
}
����1000��ѵ�������100�����������������������齫AI��ֻѧϰ���ƣ�����������ʽ������ȷ�����䲻��ɹ���
