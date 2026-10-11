# Agent Skill Governance V4

把“模型建议”和“业务授权”分开的 Python 工程。模型可以解释和提出 Skill 补丁，但不能替代权限、审批、校验器（Validator）或比较并交换（CAS）。

版本：`4.0.0.dev5`。本包是公开展示审核候选版，不是正式 RC1。**源码许可待权利人确认，确认前不要公开发布。** 见 [NOTICE](NOTICE.md)。

## 三分钟运行

需要 Python 3.11+，在解压目录执行：

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS / Linux：source .venv/bin/activate
python -m pip install -e ".[dev]" build
python -m agent_governance_portfolio verify
python -m agent_governance_portfolio demo generic_change_request
```

预期校验返回 `REGISTRY_V3=PASS`、`REGISTRY_LEGACY=PASS`，配置示例返回 `executed: true` 和合成回执。无真实数据库、设备或模型调用；审批标识每次可能不同。

## 各部分怎样协作

```text
宿主 Agent / 工具调用
        │ ActionRequest：主体、资源、动作、参数、Trace
        ▼
通用治理内核 GovernanceRuntime
        ├─ 权限与策略 → 参数绑定审批 → 激活前复核
        └─ DomainAdapter → 权威事实 → CAS 提交 → 执行回执
              ├─ 通用配置 / 科研参数（内存合成示例）
              └─ SAC 储能适配器（接口 + 冻结策略；非企业完整系统）

通用 Skill：action-risk-gate / action-review
专业 Skill：sac-plan-review
        └─ 只读解释，不能改变上面的授权或执行结果

前向反馈 → 经验归因与家族去重 → 受限 Candidate 补丁
        → 配对评测 → EvolutionQualityGate → 独立审批
        → 隔离 staging 注册表 / 回滚（不是正式 Registry 晋升）
```

Skill 是能力与解释方式的文件包，不是业务写权限。`skill_packs/` 是中文展示入口；`skills/` 保存冻结运行资产；`src/agent_governance_assets/` 是安装资源副本，由同步脚本逐字节检查。

## 可以直接验证什么

```bash
python -m pytest -q
python scripts/validate_skills.py
python scripts/sync_assets.py --check
python -m agent_governance_portfolio demo research_workflow
python -m agent_governance_portfolio demo sac_dispatch
python -m agent_governance_portfolio demo skill_evolution
python examples/custom_domain.py
python -m build
```

公开回归为 330 项。四个示例分别演示通用配置、科研参数、SAC 合成后台和受控自进化；后者明确标记 `SYNTHETIC_INFRASTRUCTURE_ONLY`，不代表真实候选晋升。额外配额适配器演示越权拒绝与重复执行拒绝。

## 实验成果与限制

历史 Benchmark112 在 56 个合成物理家族、14 类机制上完成 112 对真实模型 Review。模型建议的经济解释覆盖率为 50.89% → 94.64%，SOC 解释覆盖率为 55.36% → 95.54%；回答更长，P95 从 13.58 秒升至 18.56 秒。换序一致性仅 17/28，存在未人工确认的事实和执行声明风险。这些是**历史模型建议，不是本轮重新测得、人工验收或正式晋升成绩**。

见 [评测口径](docs/07_evaluation.md) 与 [本轮测试收据](TEST_RECEIPT.json)。公开回归不能替代企业 HTTP、数据库或设备验收。历史私有 SAC 回归与原始模型回答不在本包内。

## 继续阅读

- [一页概览](PORTFOLIO_ONE_PAGER.md) · [安装](INSTALL.md)
- [架构](docs/01_architecture.md) · [通用治理](docs/02_generic.md)
- [SAC 专业适配](docs/03_sac.md) · [适配接口](docs/04_adapters.md)
- [自进化](docs/05_evolution.md) · [安全边界](docs/06_security.md)
- [新增领域](docs/09_new_domain.md) · [研究引用](docs/references.md)
- [版本可追溯性](docs/08_history.md) · [文件保留规则](03_PUBLIC_FILE_SELECTION.md)

旧 V1 源码副本和内部迁移流水账移出本包，旧 ZIP 和 Git 历史未改写。本包不会覆盖旧仓库。MIT 文本原样保留；依赖许可见 [依赖清单](docs/dependency_licenses.md)。
