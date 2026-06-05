"Generate context handoff documents from project state."
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import yaml

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = ROOT / "templates" / "context_handoff" / "HANDOFF_TEMPLATE.md"


def load_state() -> dict:
    with open(ROOT / "CURRENT_STATE.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def generate_handoff(target: str = "new-conversation") -> str:
    state = load_state()
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    replacements = {
        "{{PROJECT_NAME}}": state.get("project", "devframe-control-plane"),
        "{{PROJECT_TYPE}}": "Workflow Integration Layer",
        "{{PROJECT_GOAL}}": "Declarative pipeline engine for AI agent workflows",
        "{{CURRENT_STATUS}}": f"{state.get('current_stage', 'unknown')} ({state.get('status', 'unknown')})",
        "{{NEXT_STAGE}}": state.get("next_stage", "unknown"),
        "{{NEXT_STAGE_DESCRIPTION}}": state.get("next_stage_description", ""),
        "{{ACCEPTED_PHASES}}": _format_accepted_phases(),
        "{{KNOWN_LIMITATIONS}}": "G5/G6 accepted with evidence limitation. H5 deferred optional.",
        "{{ALLOWED_ACTIONS}}": "- Read-only operations\n- Dry-run execution\n- Schema validation",
        "{{PROHIBITED_ACTIONS}}": "- No live CDP without authorization\n- No guard removal\n- No evidence cleanup",
    }

    for key, value in replacements.items():
        template = template.replace(key, value)

    header = f"# HANDOFF — Generated {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n\n"
    return header + template


def _format_accepted_phases() -> str:
    phases = [
        ("G0", "accepted"), ("G1", "accepted"), ("G2", "accepted"),
        ("G3", "accepted"), ("G4", "accepted"), ("G5", "accepted*"),
        ("G6", "accepted*"), ("G7", "accepted"), ("G8A", "accepted"),
        ("G8", "accepted"), ("H1", "accepted"), ("H2", "accepted"),
        ("H3", "accepted"), ("H4", "accepted"), ("H6", "accepted"),
    ]
    return "\n".join(f"| {p} | {s} |" for p, s in phases)


def save_handoff(output_path: str | Path, target: str = "new-conversation") -> Path:
    content = generate_handoff(target)
    path = Path(output_path)
    path.write_text(content, encoding="utf-8")
    return path
