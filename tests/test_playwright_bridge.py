import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from control_plane.playwright_bridge import (
    BridgeMode, BridgeConfig, health_check, submit_via_bridge, safety_attestation,
)
from control_plane.submission_result import SubmissionRequest


def make_config(mode=BridgeMode.DISABLED, safety=False, conv=""):
    return BridgeConfig(mode=mode, safety_flag=safety, conversation_id=conv)


def test_disabled_mode_health_check_fails():
    ok, reason = health_check(make_config(BridgeMode.DISABLED))
    assert ok is False
    assert "disabled" in reason


def test_dry_run_health_check_passes():
    ok, reason = health_check(make_config(BridgeMode.DRY_RUN))
    assert ok is True


def test_live_without_safety_flag_blocked():
    ok, reason = health_check(make_config(BridgeMode.LIVE, safety=False, conv="id"))
    assert ok is False
    assert "safety_flag" in reason


def test_live_without_conversation_id_blocked():
    ok, reason = health_check(make_config(BridgeMode.LIVE, safety=True, conv=""))
    assert ok is False
    assert "conversation_id" in reason


def test_disabled_submit_returns_blocked():
    req = SubmissionRequest(review_run_id="test")
    result = submit_via_bridge(req, make_config(BridgeMode.DISABLED))
    assert result.success is False


def test_dry_run_submit_returns_success():
    req = SubmissionRequest(review_run_id="test")
    result = submit_via_bridge(req, make_config(BridgeMode.DRY_RUN))
    assert result.success is True
    assert result.mode == "dry_run"


def test_live_placeholder_returns_not_implemented():
    req = SubmissionRequest(review_run_id="test")
    cfg = make_config(BridgeMode.LIVE)
    cfg.safety_flag = True
    cfg.conversation_id = "6a223019"
    result = submit_via_bridge(req, cfg)
    assert "not yet implemented" in result.detail.lower() or result.success is False


def test_safety_attestation_no_state_mutation():
    attest = safety_attestation(make_config(BridgeMode.DRY_RUN))
    assert attest["no_state_mutation"] is True
    assert attest["no_real_gpt_submit_in_tests"] is True
