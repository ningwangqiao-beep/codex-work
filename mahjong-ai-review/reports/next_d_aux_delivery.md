# 独立辅助验证准备

新增next_aux_validation.py，未改冻结next_data_scale。仅2或主审批准100局；独立7110000..7110099范围，绝不混入train/固定val/dev/final。调用冻结producer.work逐局原子records/game/commit，aux RUN与manifest另绑定10主源+6间接/producer/本脚本source，resume核seed/seat/split/contentSHA，2worker、1536MiB free RAM门槛，STOP安全保存提交后exit75。

真实2局smoke：31状态、2结构听牌阳性、0合法风险阳性，2.435秒exit0。输入191/fullseq重编码与隐藏未来poison隔离独立审计通过；resume exit0，未批准100拒绝exit1。正式100尚未启动，无训练/校准。

冻结work记录source_group保留next-history100；这不是数据角色定义，独立manifest明确auxiliary_validation_only_NOT_fixed_validation/no_training/no_calibration_yet，不可凭该旧字段混并数据。风险阳性不足问题本2局无法回答，正式100若获准仍需真实统计。

最终脚本SHA210a3c70890943b55bbee9488bf52de17fc90974078da636dc06d517ad55894f。

正式命令（待主审绑定批准）：

    .venv/Scripts/python.exe scripts/next_aux_validation.py --games 100 --out datasets/next_aux_validation100 --approval reports/next_aux_validation_approval.json

approval需approved:true/games:100/source_hashes完整16源。resume加--resume。未使用付费API。
