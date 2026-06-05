# Quickstart（设计版）

> 当前 G0 阶段，下方命令为设计预览，不可真实运行。G1 完成后逐步实现。

## 用户流程

### 1. 获取仓库

```bash
git clone https://github.com/RD2100/devframe-control-plane.git
cd devframe-control-plane
```

### 2. 选择模板

```bash
# 列出可用模板
python -m control_plane templates list

# 当前可用：
#   code_project      — 软件工程项目流水线
#   paper_iteration   — 论文迭代审查流水线
```

### 3. 生成项目骨架

```bash
# 基于模板创建新项目
python -m control_plane init --template code_project my-project

# 生成内容：
#   my-project/
#     PROJECT_BOOTSTRAP.md
#     CURRENT_STATE.yaml
#     NEXT_TASK.md
#     SAFETY_BOUNDARIES.md
#     PIPELINE.yaml
#     EVIDENCE_SPEC.yaml
#     .gitignore
#     .env.example
```

### 4. Doctor 检查

```bash
cd my-project
python -m control_plane doctor

# 检查项：
#   - 所有必需文件存在
#   - CURRENT_STATE.yaml 格式正确
#   - SAFETY_BOUNDARIES.md 覆盖必要条目
#   - .gitignore 排除敏感文件
#   - .env 未包含真实值（如有）
#   - 无 CDP / Playwright 代码（当前阶段）
```

### 5. 运行工作流（未来）

```bash
python -m control_plane run PIPELINE.yaml --mode execute
```

## 当前限制

- 所有命令为设计预览，不可执行
- Runner 将在 G2+ 实现
- CDP 接入将在 G3+ 实现
