"""Generate context handoff documents from project state.

HANDOFF AUTHORSHIP MODEL (T3):
- The generator provides the STRUCTURE (template with sections).
- A GPT/Agent with full project context fills in the SUBSTANCE.
- The generated file is a skeleton — it MUST be reviewed and augmented
  by a GPT that has full session context before transfer to a new conversation.
"""
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent.parent


def generate_handoff(target: str = "new-conversation") -> str:
    """Generate a HANDOFF.md skeleton. Must be reviewed by a GPT with full context before transfer."""

    lines = []
    lines.append("")
    lines.append("# HANDOFF — DevFrame Control Plane")
    lines.append("")
    lines.append("> GENERATED SKELETON — MUST BE REVIEWED AND AUGMENTED BY GPT WITH FULL CONTEXT")
    lines.append(f"> Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    lines.append(f"> Target: {target}")
    lines.append("")
    lines.append("## IMPORTANT — Handoff Authorship Model")
    lines.append("")
    lines.append("This template provides the STRUCTURE. The SUBSTANCE must be written by a GPT/Agent")
    lines.append("that has full project context. Before transferring to a new conversation:")
    lines.append("")
    lines.append("1. A GPT with full session context MUST fill in ALL sections below")
    lines.append("2. The authoring GPT MUST include: project identity, architecture, completed phases,")
    lines.append("   current state, safety boundaries, lessons learned, and next steps")
    lines.append("3. Placeholders like `{{FIELD}}` must be replaced with actual content")
    lines.append("4. The resulting HANDOFF.md should be 10,000+ characters of self-contained context")
    lines.append("5. The transfer Agent MUST upload HANDOFF.md as a .md FILE ATTACHMENT (not inline text)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Project Identity")
    lines.append("{{PROJECT_IDENTITY}}")
    lines.append("")
    lines.append("## 2. Architecture")
    lines.append("{{ARCHITECTURE}}")
    lines.append("")
    lines.append("## 3. Completed Work")
    lines.append("{{COMPLETED_PHASES}}")
    lines.append("")
    lines.append("## 4. Current State")
    lines.append("{{CURRENT_STATE}}")
    lines.append("")
    lines.append("## 5. Safety Boundaries")
    lines.append("{{SAFETY_BOUNDARIES}}")
    lines.append("")
    lines.append("## 6. Key Decisions and Lessons Learned")
    lines.append("{{LESSONS_LEARNED}}")
    lines.append("")
    lines.append("## 7. Next Steps")
    lines.append("{{NEXT_STEPS}}")
    lines.append("")
    lines.append("## 8. Expected Response Schema")
    lines.append("```yaml")
    lines.append("overall_judgment: accepted | blocked | review_unverified")
    lines.append("handoff_understood: yes | no")
    lines.append("project_identity_understood: yes | no")
    lines.append("architecture_understood: yes | no")
    lines.append("completed_phases_understood: yes | no")
    lines.append("current_state_understood: yes | no")
    lines.append("safety_boundaries_understood: yes | no")
    lines.append("next_steps_understood: yes | no")
    lines.append("ready_for_next_authorization: yes | no")
    lines.append("rationale: brief")
    lines.append("```")
    lines.append("")
    lines.append("## 9. Transfer Protocol (for Agent)")
    lines.append("")
    lines.append("The Agent transferring this handoff MUST:")
    lines.append("1. Upload HANDOFF.md as a .md FILE ATTACHMENT (not inline text paste)")
    lines.append("2. Include a brief bootstrap prompt asking the new conversation to read the file")
    lines.append("3. Capture the reply and verify handoff_understood=yes")
    lines.append("4. Fail-closed if handoff_verified=false")
    lines.append("")

    return "\n".join(lines)


def save_handoff(output_path: str | Path, target: str = "new-conversation") -> Path:
    content = generate_handoff(target)
    path = Path(output_path)
    path.write_text(content, encoding="utf-8")
    return path
