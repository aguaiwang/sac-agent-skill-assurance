# 架构：执行治理与 Skill 自进化

治理运行时（GovernanceRuntime）接收结构化请求，读取领域适配器（DomainAdapter）的权威快照，进行权限、策略、审批绑定和提交复核。后台通过比较并交换（CAS）返回回执。只读审查（Review）提供解释，不拥有写权限。

通用内核位于 `src/agent_governance/`，通用 Skill 位于 `skills/action-risk-gate/versions/3.0.1/` 与 `skills/action-review/versions/3.0.1/`。SAC 专业 Skill 位于 `skills/sac-plan-review/`，历史冻结策略与注册表位于 `src/agent_governance/sac_policy/`，具体文件以冻结 Registry 为准。包装入口只负责资源定位、校验和合成演示，不参与风险判断。

自进化复用反馈、经验、候选补丁、配对评测与质量门控；发布与回滚各自审批。候选只能改善解释，不能修改安全核心或自授权执行。

V1 轨迹证据与 V4 执行治理不是无缝替换 API。本包移出旧源码副本，原始归档和 Git 历史保留。见 [版本范围](08_history.md)。
