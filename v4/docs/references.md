# 研究参考与没有实现的范围

这些资料只作方法定位，不是测试成绩或认证。

| 来源 | 本项目借鉴 | 不得宣称 |
| --- | --- | --- |
| [Agent Skills](https://agentskills.io/specification) | 描述触发、SKILL.md 与按需参考资料 | manifest.json 是官方强制格式 |
| [GEPA](https://arxiv.org/abs/2507.19457) | 用失败解释提出局部提示补丁 | 已实现完整 Genetic-Pareto 搜索或 SOTA |
| [DSPy MIPROv2](https://github.com/stanfordnlp/dspy/blob/main/docs/docs/api/optimizers/MIPROv2.md) | 与提示及示例优化方法比较 | 本项目用了贝叶斯优化 |
| [SkillsBench](https://arxiv.org/abs/2602.12670) | Skill 增强也要检查负迁移 | 已运行其基准测试集 |
| [AgentDojo](https://arxiv.org/abs/2406.13352) | 区分间接提示注入与真实工具风险 | A14 显式用户注入等于完整工具环境防御 |
| [OWASP Agentic 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | 威胁模型中考虑工具权限及供应链 | 获得 OWASP 安全认证 |

查阅日期：2026-10-11。项目自己的证据以冻结源码和本包测试收据为准。
