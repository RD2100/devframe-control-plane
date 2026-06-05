# Next Task

REVIEW_RUN_ID: g0-bootstrap-skeleton-v1-20260605

## G0 完成后

下一任务：**G1 — Pipeline Definition and State Machine Spec**

## G1 范围

只设计 YAML pipeline schema，不实现 Runner。

### G1 交付物

1. `schemas/pipeline.schema.json` — Pipeline 定义的 JSON Schema
2. `schemas/state_transition.schema.json` — 状态转换的 JSON Schema
3. `schemas/evidence_spec.schema.json` — 证据规格的 JSON Schema
4. `docs/pipeline-spec.md` — Pipeline 规格说明文档
5. 更新 `CURRENT_STATE.yaml` 为 G1_in_progress

### G1 禁止事项

- 不实现 `pipeline_runner.py`
- 不实现 CDP / Playwright 接入
- 不包含真实证据或用户数据
- 不实现 CLI 命令
