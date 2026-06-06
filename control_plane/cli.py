"CLI entry: devframe init, doctor, run."
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def cmd_init(template: str = "code_project", target: str = "."):
    tpl_dir = ROOT / "templates" / template
    if not tpl_dir.exists():
        print(f"Unknown template: {template}")
        print(f"Available: {[d.name for d in (ROOT/'templates').iterdir() if d.is_dir()]}")
        return 1
    target_dir = Path(target).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    for src in tpl_dir.rglob("*"):
        if src.is_file():
            rel = src.relative_to(tpl_dir)
            dst = target_dir / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"  created: {rel}")
    print(f"Project initialized from template '{template}' in {target_dir}")
    return 0


def cmd_doctor():
    checks = {
        "CURRENT_STATE.yaml": (ROOT / "CURRENT_STATE.yaml").exists(),
        "schemas/pipeline.schema.json": (ROOT / "schemas" / "pipeline.schema.json").exists(),
        "schemas/state_transition.schema.json": (ROOT / "schemas" / "state_transition.schema.json").exists(),
        "schemas/evidence_spec.schema.json": (ROOT / "schemas" / "evidence_spec.schema.json").exists(),
        "schemas/context_handoff.schema.json": (ROOT / "schemas" / "context_handoff.schema.json").exists(),
        "templates/code_project": (ROOT / "templates" / "code_project").is_dir(),
        "templates/paper_iteration": (ROOT / "templates" / "paper_iteration").is_dir(),
        "templates/context_handoff": (ROOT / "templates" / "context_handoff").is_dir(),
        ".gitignore covers .env": ".env" in (ROOT / ".gitignore").read_text(encoding="utf-8"),
    }
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    for name, ok in checks.items():
        print(f"  {'PASS' if ok else 'FAIL'}: {name}")
    print(f"Doctor: {passed}/{total} checks passed")
    return 0 if passed == total else 1


def cmd_run(pipeline_path: str, dry_run: bool = True, with_submission: bool = False):
    from .pipeline_runner import dry_run as runner_dry_run
    return runner_dry_run(pipeline_path, with_submission=with_submission)


def cmd_handoff_generate(target: str = "new-conversation"):
    from .handoff_generator import generate_handoff
    print(generate_handoff(target))
    return 0


def cmd_handoff_validate(path: str):
    from .handoff_verifier import validate_handoff
    text = Path(path).read_text(encoding="utf-8")
    ok, errors = validate_handoff(text)
    if ok:
        print("Handoff validation: PASSED")
        return 0
    for e in errors:
        print(f"  FAIL: {e}")
    return 1


def cmd_handoff_bootstrap(target: str = "new-conversation", dry_run: bool = True):
    from .conversation_bootstrap import run_bootstrap
    result = run_bootstrap(target, dry_run=dry_run)
    print(f"Mode: {result.mode}")
    print(f"Handoff generated: {result.handoff_generated} ({result.handoff_length} chars)")
    print(f"Submitted: {result.submitted}")
    print(f"Reply received: {result.reply_received}")
    print(f"Handoff verified: {result.handoff_verified}")
    return 0 if result.handoff_verified else 1


def cmd_handoff_transfer():
    """Transfer handoff document. Dry-run by default; --live requires safety flag."""
    import argparse

    parser = argparse.ArgumentParser(prog="devframe handoff transfer")
    parser.add_argument("--to", dest="target_url", default=None,
                        help="Target conversation URL or ID")
    parser.add_argument("--file", dest="handoff_file", default="HANDOFF.md",
                        help="Handoff file to transfer (default: HANDOFF.md)")
    parser.add_argument("--live", dest="live", action="store_true", default=False,
                        help="Execute live CDP transfer (default: dry-run)")
    parser.add_argument("--safety-flag", dest="safety_flag", action="store_true", default=False,
                        help="Required for live mode")

    # Reconstruct args from sys.argv after 'transfer'
    args_list = sys.argv[sys.argv.index("transfer") + 1:]
    try:
        parsed = parser.parse_args(args_list)
    except SystemExit:
        return 1

    target = parsed.target_url or "new-conversation"
    handoff_file = parsed.handoff_file

    if not parsed.live:
        # Dry-run
        print(f"Handoff transfer (dry-run): would upload {handoff_file} to {target}")
        print("  Step 1: Verify HANDOFF.md exists")
        print("  Step 2: CDP connect and navigate to target")
        print("  Step 3: Upload HANDOFF.md as .md file attachment")
        print("  Step 4: Include bootstrap prompt")
        print("  Step 5: Click send")
        print("  Step 6: Capture reply and verify handoff_verified")
        return 0

    # Live mode
    if not parsed.safety_flag:
        print("ERROR: --safety-flag required for live CDP transfer")
        return 1

    from .playwright_bridge import BridgeConfig, BridgeMode, submit_via_bridge, health_check as bridge_health
    from .submission_result import SubmissionRequest

    config = BridgeConfig(
        mode=BridgeMode.LIVE,
        safety_flag=True,
        conversation_id=target,
    )

    ok, reason = bridge_health(config)
    if not ok:
        print(f"ERROR: Health check failed: {reason}")
        return 1

    req = SubmissionRequest(review_run_id=handoff_file)
    result = submit_via_bridge(req, config)
    print(f"Transfer result: success={result.success}, mode={result.mode}")
    print(f"Detail: {result.detail}")
    return 0 if result.success else 1


def main():
    if len(sys.argv) < 2:
        print("DevFrame Control Plane CLI")
        print("  devframe init [template] [target]  — initialize project")
        print("  devframe doctor                    — check project health")
        print("  devframe run --pipeline <path>     — dry-run pipeline")
        print("  devframe handoff generate           — generate handoff doc")
        print("  devframe handoff validate <file>    — validate handoff")
        print("  devframe handoff bootstrap          — dry-run bootstrap")
        print("  devframe handoff transfer --to <url> [--live --safety-flag] — transfer handoff")
        return 0
    cmd = sys.argv[1]
    if cmd == "handoff":
        sub = sys.argv[2] if len(sys.argv) > 2 else "generate"
        if sub == "generate":
            return cmd_handoff_generate()
        elif sub == "validate":
            return cmd_handoff_validate(sys.argv[3]) if len(sys.argv) > 3 else 1
        elif sub == "bootstrap":
            return cmd_handoff_bootstrap()
        elif sub == "transfer":
            return cmd_handoff_transfer()
        else:
            print(f"Unknown handoff subcommand: {sub}")
            return 1
    elif cmd == "init":
        tpl = sys.argv[2] if len(sys.argv) > 2 else "code_project"
        tgt = sys.argv[3] if len(sys.argv) > 3 else "."
        return cmd_init(tpl, tgt)
    elif cmd == "doctor":
        return cmd_doctor()
    elif cmd == "run":
        if "--pipeline" not in sys.argv:
            print("Usage: devframe run --pipeline <path>")
            return 1
        idx = sys.argv.index("--pipeline")
        path = sys.argv[idx + 1]
        with_sub = "--with-submission" in sys.argv
        return cmd_run(path, with_submission=with_sub)
    else:
        print(f"Unknown command: {cmd}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
