# DevFrame Control Plane

**工作流整合与编排层** — 将散落的 Agent 工作流组件整合成可冷启动、可迁移、可审核的声明式流水线框架。

## 解决什么问题

在 dev-frame-opencode 项目中，我们验证了一条完整的 GPT 治理 + Agent 执行流水线（P0-P15），但各组件散落：

- `review_pack_flow.py` 生成证据包
- `submission_guard.py` 做提交去重
- CDP/Playwright 做 GPT 通信
- `DECISION_LEDGER.jsonl` 做审计
- `CURRENT_ROUTE.json` 做状态跟踪

每次新任务都需要手动串联这些组件。DevFrame Control Plane 将这些整合成一个 **声明式流水线引擎**：

1. 用 YAML 定义流水线（阶段、依赖、证据要求）
2. Runner 自动执行（授权 → 证据包 → CDP 提交 → GPT 审查 → 闭合 → 下一阶段）
3. 状态机强制执行 CURRENT_ROUTE 不变式
4. 恢复管理器处理 CDP/GPT/测试异常

## 当前阶段

**G0 — Bootstrap 骨架**。只有项目结构、文档、模板和安全边界。尚未实现 Runner。

## 首批模板

| 模板 | 用途 |
|------|------|
| `code_project` | 软件工程项目的流水线模板（授权 → 执行 → 证据 → 审查 → 闭合） |
| `paper_iteration` | 论文迭代的审查模板（版本追踪 → 差异对比 → 审查规范） |

## 快速开始（设计版，命令暂不可运行）

```bash
git clone https://github.com/RD2100/devframe-control-plane.git
cd devframe-control-plane
python -m control_plane init --template code_project my-project
cd my-project
python -m control_plane doctor
python -m control_plane run pipeline.yaml
```

## 许可证

MIT
