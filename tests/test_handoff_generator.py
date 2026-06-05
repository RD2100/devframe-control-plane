import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from control_plane.handoff_generator import generate_handoff, save_handoff, load_state


def test_generate_handoff_returns_string():
    text = generate_handoff("new-conversation")
    assert isinstance(text, str)
    assert len(text) > 500


def test_generate_handoff_contains_required_sections():
    text = generate_handoff("new-conversation")
    for section in ["Project Identity", "Current Status", "Safety Boundaries", "Failure Policy"]:
        assert section in text, f"Missing: {section}"


def test_load_state_returns_dict():
    state = load_state()
    assert isinstance(state, dict)
    assert "project" in state


def test_save_handoff_writes_file(tmp_path):
    path = save_handoff(tmp_path / "test_handoff.md", "new-conversation")
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "devframe-control-plane" in content
