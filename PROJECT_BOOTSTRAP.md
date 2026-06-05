# Project Bootstrap

REVIEW_RUN_ID: g0-bootstrap-skeleton-v1-20260605

## 仓库目标

DevFrame Control Plane 是 dev-frame-opencode 生态的工作流整合层。它将散落的 Agent 组件（证据构建、Guard、CDP 通信、状态机）整合成声明式流水线引擎。

## 当前阶段

**G0 — Bootstrap Skeleton**

只做项目结构、文档、模板和安全边界。不实现任何可执行代码。

## 下一阶段

**G1 — Pipeline Schema Design**

定义 YAML pipeline schema、状态转换规格、证据规格。仍不实现 Runner。

## 禁止事项

- 不实现 Runner / 执行引擎
- 不接入 CDP / Playwright
- 不迁移旧项目 evidence
- 不含真实密钥、cookie、session
- 不含用户私有材料
- 不含真实论文内容

## 关键文件

| 文件 | 用途 |
|------|------|
| README.md | 项目概述 |
| QUICKSTART.md | 用户快速开始指南 |
| PROJECT_BOOTSTRAP.md | 本文档 |
| CURRENT_STATE.yaml | 当前阶段状态 |
| NEXT_TASK.md | 下一步任务 |
| SAFETY_BOUNDARIES.md | 安全边界 |
| PHASE_LEDGER.md | 阶段记录 |
| EVIDENCE_INDEX.md | 证据索引 |
| .gitignore | 排除规则 |
| .env.example | 环境变量模板 |

## 模板目录

| 目录 | 用途 |
|------|------|
| templates/code_project/ | 软件工程项目模板 |
| templates/paper_iteration/ | 论文迭代审查模板 |
| examples/ | 示例工作流说明 |
| docs/ | 架构与概念文档 |
