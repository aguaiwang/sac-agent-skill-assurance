# SAC 专业适配的边界

src/agent_governance/adapters/sac_dispatch.py 中 SACBackendAuthority 定义 read_candidate 与 activate_compare_and_set。SACDispatchAdapter 不接受任意重规划参数，只治理已有 dispatch_plan 的 activate_dispatch_plan。assess 将权威 replan_result、active_plan_id 等交给冻结确定性风险策略。

公开 examples/sac_dispatch/demo.py 用合成 Backend 实现协议。没有 SAC Actor、真实设备、MySQL 或模型权重。skills/sac-plan-review 是解释能力说明，src/agent_governance/sac_policy 是内部冻结策略资产，两者不能混成一个 Skill ID。历史真实 HTTP 验收只是摘要，不能本地重演企业服务。
