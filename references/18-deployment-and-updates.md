# 18. Skill 的安装、会话触发与可审查更新

## 运行方式

- GitHub 是源代码和版本库，不会自动成为所有聊天的默认知识。使用 Skill 的助手必须有能力读取 `SKILL.md` 和相关 `references/`。
- 研究任务开始时优先读取 `memory/accepted_rules.md`；之后只选任务需要的模块，避免无谓加载。
- 会话结束时，只对**用户明确纠错、可跨项目复用且非敏感**的经验生成单个 JSON 反馈；无新增则不提交。

## GitHub 自动 PR 链路

研究助手填写 `templates/feedback.json` → 审核 `safe_to_upload` → 用授权账户创建标题以 `[FR feedback]` 开头的 Issue → `.github/workflows/feedback-to-pr.yml` 提取、校验、运行测试 → 建立候选分支和 PR → **人工审核合并** → 下次执行读新规则。

不需要预先创建 `fr-feedback` 标签。若使用 `workflow_dispatch`，由有权限的维护者提供已经存在的 Issue 编号。**不能把 GitHub Issues 当成原始聊天备份。**

## 一次性仓库设置

1. 确保 Actions 允许工作流运行。
2. 在 `Settings → Actions → General → Workflow permissions` 中检查是否允许工作流写入仓库，以及是否允许 Actions 创建 Pull Request。如果组织政策禁用，则工作流只能生成本地候选/报错，维护者需要手动提 PR。
3. 保持仓库为 Private，或在转为 Public 前逐个核查历史提交、敏感信息、代码、许可。
4. 对 `main` 配置人工审查规则；不要为了省步骤开启无需复核的自动合并。
5. 在 `Actions` 查看 `FR quality checks` 的最近运行结果；GitHub UI 成功不等于财务事实已经核实。

## 什么算一次学习

- **可沉淀**：将产能与销量混用的纠错、限定需求章节范围、价税口径标准、先改结构后润色、术语误写的复核方法。
- **不可直接沉淀**：某家公司未经核实的报价、保密访谈全文、客户姓名、偶然得到的目标价、一次性日期变化。
- 若规则互相冲突，维护者在 PR 中解释适用边界，不添加自相矛盾的规则。

## 发布和更新是两件事

研究 Skill 的 GitHub 更新只会更新工作规则，不会自动发布投资研报。任何发给客户、媒体或平台的研究报告仍必须取得明确授权，并通过研究质量和所属机构合规审批。
