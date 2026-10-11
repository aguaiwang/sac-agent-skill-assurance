# 受控补丁而非自授权上线

Observation 保存脱敏来源与分区，Experience 聚合可修复失败。candidate.propose 只接收允许分区，拒绝 tool_calls；apply_bound_patch 校验原文件哈希和唯一 before 文本；build_candidate 限制路径、大小及只读工作流。路径限制不是 OS 沙箱，不能运行不可信生成器 Python。

EvolutionQualityGate 要求完整 target/regression/heldout 与安全计数、无负迁移和最小目标增益；结果为 NEEDS_REVIEW 或 REJECTED。SkillPromotionAdapter 注入可信 evaluator，审批绑定报告与 expected_champion，在本地锁中原子更新独立 Registry；回滚也需要新审批。真实候选未晋升，本包演示是 SYNTHETIC_INFRASTRUCTURE_ONLY。
