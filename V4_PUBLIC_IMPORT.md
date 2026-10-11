# V4 公开精修版导入记录

## 来源与授权

源包：`Agent_Skill_Governance_V4_PUBLIC_REFINED_20261011.zip`。

ZIP SHA256：`134b4c50a0193a061a160601dd13bbba86bec1a43e8bafe5e18501254cbdd87d`。

2026-10-11，提交请求方明确确认该源码已获准公开，并授权使用 GitHub 账号 `aguaiwang` fork、提交 PR，等待仓库维护者审核合并。该记录不新增或转让版权，不修改现有 LICENSE、归属及依赖许可。`v4/` 内保留原审核包文件，包括其生成时的“授权待确认”说明；本记录补充后续用户授权事实，不把历史报告重写为当时已获授权。

## 最小破坏的版本共存

- 根目录保留 V1 的安装入口、`skill_assurance` 命名空间、源码、测试、Skill 包及 CI。
- `v4/` 完整导入精修 ZIP，使用独立的 `agent-action-governance` 分发名和 `agent_governance` 命名空间。
- V4 不是 V1 的原位升级，不承诺旧 API 无修改即可迁移；安装和测试分别在两个环境执行。
- 新增独立 V4 CI，根目录原 CI 不修改。
- 不删除、重写 Git 历史，不生成新 Candidate，不改变审批、安全门控、正式 Registry 或冻结 Prompt。

## 评测口径

V4 的 330 项公开回归、四个合成示例和两套 Registry 在 PR 提交前重新运行；具体结果见本文件后续收据。历史 SAC 私有回归、HTTP 及 Benchmark112 不在本次复跑范围，公开工程内的历史摘要不能当作本次新成绩。

正式发布、RC1 和业务生产准入仍按项目原有规则，公开授权不等于质量门控通过。合并由目标仓库维护者决定，本次只提交 PR。

## 本次提交前复验（2026-10-11）

两个独立的新建 Python 3.11 虚拟环境分别安装 V1/V4；安装依赖镜像超时后改用官方 PyPI。初次无隔离构建因新环境 setuptools 65.5.0 不满足 `>=68` 失败，补齐 setuptools/wheel 后构建成功，不修改源码或测试。

| 项目 | 实际结果 |
| --- | --- |
| V1 `python -m pytest -q` | 8 passed |
| V1 security evaluation | 52/52 |
| V1 offline trigger evaluation | 80/80；Host selector runtime未评测 |
| V4 `python -m pytest -q` | 330 passed，pytest报告8.29秒 |
| V4 Registry V3 / Legacy | PASS / PASS |
| V4 Skill入口校验 | 3个入口通过 |
| V4安装资源副本 | 14文件逐字节一致 |
| V4合成示例 | SAC、通用变更、科研、自进化4/4通过 |
| 额外领域适配示例 | PASS |
| V4 wheel / sdist | 构建成功 |
| 源ZIP内容 | 141个文件逐字节一致 |
| Git暂存导出后的内部checksum | 140/140，校验清单自身由源ZIP SHA覆盖 |
| 本次新增内容密钥/真实开发者路径格式扫描 | 未发现命中；不是完整法律或隐私审计 |

测试产生的缓存、egg-info、构建产物及临时合成Candidate未提交；V1测试生成的结果文件恢复到原Git版本，不覆盖历史收据。

冻结源包 `risk_models.py` 自带一个文件末尾空行，默认 `git diff --check` 提示该既有格式问题；为保持源包字节与冻结哈希，不修改该文件。排除 `blank-at-eof` 后的差异检查通过，无其他空白问题。V4公开包原有技术扫描的精确负向测试例外原样保留。

不申请正式Candidate晋升，不执行生产操作，不生成新的真实模型回答。远程GitHub Actions由PR触发，其结果与上述本地结果分开看待。
