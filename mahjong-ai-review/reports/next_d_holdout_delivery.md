# 独立读牌holdout200准备

正式范围7120000..7120199未生成；smoke只用7120900..7120901。真实2局32状态2.607秒exit0；8结构听牌阳性、7合法risk阳性、0multi。独立ledger/编码/poison/seed-seat/实际文件与16源审计通过。未批准正式200拒绝exit1。

版本next-opponent-holdout200-v1；no_training/no_calibration/no_selection全部true，旧aux100已开发使用不能当本轮final。冻结producer原始record source_group保持legacy，独立manifest定义holdout角色，不能混train/aux。

主控在候选权重冻结后签许可，绑定完整16源及每份候选绝对路径SHA；脚本--checkpoint参数可重复，起止核权重不变。2worker、1536MiB可用RAM门槛、逐局原子commit、完整seed/seat/split恢复。

待批准生成：

    .venv/Scripts/python.exe scripts/next_data_holdout200.py --games 200 --out datasets/next_opponent_holdout200 --approval reports/next_opponent_holdout200_approval.json --checkpoint ABSOLUTE_FROZEN_WEIGHT_PATH

独立审计：

    .venv/Scripts/python.exe scripts/next_data_holdout_audit.py --manifest datasets/next_opponent_holdout200/manifest.json --out reports/next_d_holdout200_audit.json

生成器SHA256 2cac3a8424f13aa46e9161cd3ff6f6af8d277eb1b140788eae613f92338847c4。小smoke与正式范围不重叠，不能据smoke风险7正例调整候选。未付费API、未训练/RL。
