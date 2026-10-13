# FR | Financial Research Skill

研究业务的可复用 Skill。目标不是代写字句，而是把**问题定义、原始证据、供需机制、财务映射、估值、研报表达和事后复盘**连成一套工作流。

> **当前版本：v0.1.0（基础版）**。依据当前项目可读取的《行业研究指导框架》以及本项目内已有研究任务沉淀。用户提供的 ChatGPT 分享链接 **未能读取正文**，故暂未覆盖链接中独有的全部内容。等待用户导出文本再进行差异补全。见 `SOURCE_COVERAGE.md`。

## 一分钟使用
1. 将 `FR/` 放入能读取本地 Skills 的工作目录，或在会话中附上 `SKILL.md` 与对应 references。
2. 告诉助手「使用 FR 研究 XX 行业／公司，先做需求与供给、核查来源、再写报告」。
3. 助手读 `SKILL.md` 和所需引用文档，建立证据清单，再形成观点、模型、交付物。
4. 结束后复盘，把当次确认的研究经验形成结构化反馈，追加到 `memory/accepted_rules.md` 或创建 GitHub 更新 PR。

**注意**：仅上传 GitHub 并不会自动使 ChatGPT 以此为全局 Skill。会话需要访问仓库文件，或在支持安装 Skill 的环境中安装。`FR` 也不能自动读取未来所有 ChatGPT 对话；必须由运行它的助手在任务结束时触发反馈上传。

## 文件说明
| 路径 | 作用 |
|---|---|
| `SKILL.md` | 调用入口、原则、任务路由 |
| `references/` | 研究方法、证据、需求供给、财务模型、估值、写作、质控 |
| `templates/` | 框架、证据台账、预测假设、复盘表 |
| `memory/accepted_rules.md` | 后续使用已确认的抽象规则 |
| `memory/lessons.jsonl` | 可追溯复盘记录（无原始私聊） |
| `scripts/ingest_feedback.py` | 结构化反馈校验、去重、追加规则 |
| `.github/workflows/feedback-to-pr.yml` | 收到反馈 Issue 后自动生成修改 PR |
| `.github/workflows/quality.yml` | 对代码与结构执行基础检查 |

## 自动演进的真实边界
**对话结束→助手提炼纠错规则→向仓库提交 `fr-feedback` Issue→GitHub Actions 生成 PR→审核合并→下次读取新规则**。

这是可接入的**事件式迭代**，不是脱离对话自行监听；GitHub 看不到未主动提交的 ChatGPT 会话。默认采取 PR 审核，保护研究规范不因单次错误自动漂移。对已经明确确认、可撤销且非敏感的小改动，未来可以在独立配置后选择自动合并，但本版不默认开启。

## 部署
1. 在 GitHub 创建名为 `FR` 的 **Private** 仓库，默认分支 `main`，不要预先生成冲突文件。
2. 将本目录的内容全部推送到 `main`。
3. GitHub 仓库 Settings → Actions → General，允许工作流获得按需的 Contents/PR 权限；如果工作流无法开 PR，检查仓库是否允许 Actions 创建 PR。
4. 建立 Issue：附 `fr-feedback` 标签及**单个 JSON 反馈**（见 `templates/feedback.json`），Actions 会开 PR。
5. 下一次使用时读取 `memory/accepted_rules.md` 及 CHANGELOG，避免同类错误重复。

## 原则
- 证据先于表达；一手资料先于转述；可追溯性先于表面精确。
- 研究问题优先于信息堆砌；下游真实需求优先于供给侧愿景。
- 不是一旦提出规则就自动升格为共识；对话中的假设和测算必须经检验。
- 未经授权不得把私聊、完整会议纪要、内网资料、客户名单或保密文档送到公开仓库。

### 本地终端快捷命令

下载并解压 ZIP 后，进入 `FR` 目录。已安装 GitHub CLI 且完成 `gh auth login` 时：

```bash
bash scripts/publish-to-github.sh
```

脚本将创建私有 `FR` 仓库、推送全部文件和建立 `fr-feedback` 标签；仓库已存在则停止，避免覆盖。复盘 JSON 验证后可用 `bash scripts/submit-feedback.sh path/to/feedback.json` 创建反馈 Issue 并触发 PR 工作流。

**仓库首次部署与自动更新权限**见 `references/18-deployment-and-updates.md`。
