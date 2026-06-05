# DevFrame Control Plane

DevFrame Control Plane 是 dev-frame-opencode 生态的工作流控制平面，用声明式 pipeline、runner、state machine、evidence pack、submission/CDP adapter、CLI 和 context handoff protocol，把多阶段 Agent/GPT 工作流变成可冷启动、可迁移、可审核、可交接的 evidence-first 框架。

## 当前状态

| 项目 | 值 |
|------|-----|
| release | v0.1.0-rc |
| feature_complete | true |
| context_handoff_protocol | standardized |
| T3 handoff flow | accepted |
| tests | 55/55 PASS |
| doctor | 9/9 PASS |

## 已完成的流水线能力

- YAML pipeline spec — 声明式定义阶段、依赖、证据要求
- runner dry-run execution — 解析流水线、验证结构、打印阶段序列
- state machine / safety checks — 强制授权→执行→闭合不变式
- submission adapter — 提交抽象，dry-run 模式
- CDP adapter / Playwright bridge — 受控 CDP 接口，live 默认禁用，需显式安全标志
- CLI — `devframe init/doctor/run/handoff` 命令组
- context handoff generator / verifier — 生成、验证、交接上下文的标准化协议
- `devframe handoff transfer --to` — dry-run 文件附件传输协议
- paper_iteration 模板基础

## 快速开始

```bash
git clone https://github.com/RD2100/devframe-control-plane.git
cd devframe-control-plane

# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python -m venv .venv
source .venv/bin/activate

pip install -e .

# 检查项目健康状态
devframe doctor

# 基于模板初始化新项目
devframe init code_project my-project

# 干运行流水线（不改变状态）
devframe run --pipeline pipelines/minimal.yaml

# 生成交接文档骨架（GPT 填充实质内容）
devframe handoff generate

# 验证交接文档
devframe handoff validate HANDOFF.md

# 干运行交接传输（文件附件协议）
devframe handoff transfer --to https://chatgpt.com/c/<id>
```

## Safety Boundaries

- live CDP 默认禁用
- live CDP / GPT submission / state mutation 需要单独授权
- 禁止直接移除 guard
- 禁止清理 evidence
- 不导出 cookie / session / browser profile
- 不确定时 fail-closed

## 模板

| 模板 | 用途 |
|------|------|
| `code_project` | 软件工程项目流水线（授权 → 执行 → 证据 → 审查 → 闭合） |
| `paper_iteration` | 论文迭代审查模板（版本追踪 → 差异对比 → 审查规范） |
| `context_handoff` | 跨会话上下文交接模板 |

## 许可证

MIT
