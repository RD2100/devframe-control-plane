# Install

## Requirements

- Python >= 3.10
- Git

## One-Command Install

```bash
git clone https://github.com/RD2100/devframe-control-plane.git
cd devframe-control-plane
pip install -e .
```

## Verify

```bash
devframe doctor
```

Expected: `Doctor: 9/9 checks passed`

## Initialize a Project

```bash
devframe init code_project my-project
cd my-project
devframe doctor
devframe run --pipeline PIPELINE.yaml
```

## Templates

| Template | Purpose |
|----------|---------|
| code_project | Software engineering pipeline |
| paper_iteration | Paper review iteration |
| context_handoff | New conversation bootstrap |
