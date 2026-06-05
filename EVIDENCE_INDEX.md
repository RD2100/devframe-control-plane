# Evidence Index

REVIEW_RUN_ID: g0-bootstrap-skeleton-v1-20260605

## 当前状态

G0 阶段尚未生成 evidence packs。此索引初始化为空。

## Evidence Pack 登记规范（Future）

当流水线运行时，每个阶段的 evidence pack 应按以下格式登记：

```markdown
| REVIEW_RUN_ID | 阶段 | 类型 | 状态 | 文件数 | SHA256 |
|---------------|------|------|------|--------|--------|
| g0-bootstrap-v1 | G0 | bootstrap | completed | 14 | — |
```

## 证据目录

```
evidence_packs/
  g0-bootstrap-skeleton-v1-20260605/
    PACK_MANIFEST.md
    VALIDATION_RESULT.json
    ...
```

## 规则

- 所有 evidence packs 必须包含 PACK_MANIFEST.md 和 VALIDATION_RESULT.json
- SHA256 必须覆盖 pack 中所有文件（排除自引用文件）
- 证据包不得包含敏感信息
- 历史证据只追加，不删除
