# Next Task

REVIEW_RUN_ID: g2-runner-auth-v1-20260605

## G2 完成后

下一任务：**G3 — Submission Adapter (CDP Wrapper)**

## G3 范围

- 封装 Playwright CDP 连接、ZIP 上传、prompt 粘贴、发送
- 参数化 conversation ID、CDP host/port
- 不实际提交到 GPT（dry-run 模式）
- 不接入真实 Guard 或证据构建

## G3 禁止事项

- 不实际发送到 GPT
- 不修改 CURRENT_ROUTE.json
- 不含真实密钥
