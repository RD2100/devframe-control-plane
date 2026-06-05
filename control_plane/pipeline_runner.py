"Pipeline Runner — parse YAML, validate, dry-run stage sequence."
from __future__ import annotations
import sys
from pathlib import Path
from .pipeline_spec import load_pipeline, validate_pipeline, get_stage_sequence


def dry_run(pipeline_path: str | Path) -> int:
    try:
        pipeline = load_pipeline(pipeline_path)
    except Exception as e:
        print(f"ERROR: Cannot load pipeline: {e}")
        return 1

    errors = validate_pipeline(pipeline)
    if errors:
        print("VALIDATION ERRORS:")
        for err in errors:
            print(f"  - {err}")
        return 1

    stages = get_stage_sequence(pipeline)
    pipeline_id = pipeline.get("pipeline_id", "unknown")
    print(f"Pipeline: {pipeline_id}")
    print(f"Stages: {len(stages)}")
    for i, sid in enumerate(stages):
        stage = pipeline["stages"][i]
        stype = stage.get("type", "unknown")
        depends = stage.get("depends_on", "none")
        gpt = "GPT" if stage.get("requires_gpt_acceptance") else "no-review"
        print(f"  {i+1}. {sid} [{stype}] depends={depends} review={gpt}")
    print("DRY-RUN COMPLETE — all stages valid.")
    return 0


def run_cli():
    if len(sys.argv) < 3 or "--pipeline" not in sys.argv:
        print("Usage: python -m control_plane.run --pipeline <path> [--dry-run]")
        sys.exit(1)
    idx = sys.argv.index("--pipeline")
    path = sys.argv[idx + 1]
    return dry_run(path)


if __name__ == "__main__":
    sys.exit(run_cli())
