# Conversation Bootstrap

## T1 — Auto New Conversation Context Sync

Post-release feature for automating the Context Handoff Protocol flow.

## CLI

```bash
devframe handoff generate --target new-conversation > HANDOFF.md
devframe handoff validate HANDOFF.md
devframe handoff bootstrap --dry-run
```

## Flow

```
generate handoff → validate schema → CDP new conversation → submit handoff → capture reply → parse → handoff_verified?
```

## Current: Dry-Run Only

T1 implements the interface and safety layer. Live CDP bootstrap is deferred to T2.

## Safety

- Dry-run mode default
- handoff_verified=false → fail-closed
- No CDP in default path
