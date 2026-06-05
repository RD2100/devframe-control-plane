"Playwright Bridge — optional import, safety flag, live CDP behind flag. No real GPT submit in tests."
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from .submission_result import SubmissionRequest, SubmissionResult


class BridgeMode(str, Enum):
    DISABLED = "disabled"
    DRY_RUN = "dry_run"
    LIVE = "live"


@dataclass
class BridgeConfig:
    cdp_host: str = "localhost"
    cdp_port: int = 9222
    conversation_id: str = ""
    mode: BridgeMode = BridgeMode.DISABLED
    safety_flag: bool = False


def _try_import_playwright() -> bool:
    try:
        __import__("playwright")
        return True
    except ImportError:
        return False


def health_check(config: BridgeConfig) -> tuple[bool, str]:
    if config.mode == BridgeMode.DISABLED:
        return False, "bridge_disabled"
    if config.mode == BridgeMode.DRY_RUN:
        return True, "dry_run_ready"
    if not config.safety_flag:
        return False, "safety_flag_required_for_live_mode"
    if not config.conversation_id:
        return False, "conversation_id_required"
    if not _try_import_playwright():
        return False, "playwright_not_installed"
    return True, "live_ready"


def submit_via_bridge(
    request: SubmissionRequest,
    config: BridgeConfig,
) -> SubmissionResult:
    ok, reason = health_check(config)
    if not ok:
        return SubmissionResult(
            success=False,
            review_run_id=request.review_run_id,
            mode=config.mode.value,
            detail=f"Blocked: {reason}",
        )
    if config.mode in (BridgeMode.DISABLED, BridgeMode.DRY_RUN):
        return SubmissionResult(
            success=True,
            review_run_id=request.review_run_id,
            mode=config.mode.value,
            detail="Dry-run submission — no real CDP",
            captured_reply_sha256="dry_run_no_capture",
        )
    # LIVE mode: placeholder for G7 real CDP
    return SubmissionResult(
        success=False,
        review_run_id=request.review_run_id,
        mode="live_placeholder",
        detail="Live CDP submission not yet implemented (G7 pilot)",
    )


def safety_attestation(config: BridgeConfig) -> dict:
    return {
        "playwright_imported": _try_import_playwright(),
        "mode": config.mode.value,
        "safety_flag": config.safety_flag,
        "no_real_gpt_submit_in_tests": True,
        "no_state_mutation": True,
    }
