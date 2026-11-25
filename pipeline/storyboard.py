import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def load_storyboard(path: Path) -> dict:
    storyboard = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads(
        (ROOT / "schema" / "storyboard.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)
    for error in validator.iter_errors(storyboard):
        raise ValueError(f"{error.json_path}: {error.message}")

    shots = storyboard["shots"]
    shot_ids = {shot["id"] for shot in shots}
    references = storyboard["references"]
    reference_ids = {reference["id"] for reference in references}
    if len(shot_ids) != len(shots):
        raise ValueError("Shot IDs must be unique.")
    if len(reference_ids) != len(references):
        raise ValueError("Reference IDs must be unique.")
    duration = sum(shot["duration_seconds"] for shot in shots)
    if not 60 <= duration <= 90:
        raise ValueError(f"Runtime must be 60–90 seconds; got {duration}.")
    for shot in shots:
        unknown = set(shot["reference_ids"]) - reference_ids
        if unknown:
            raise ValueError(f"Shot {shot['id']} has unknown references: {', '.join(sorted(unknown))}")
    for cue in storyboard["music_cues"]:
        if cue["start_at_shot"] not in shot_ids:
            raise ValueError(f"Music cue points to an unknown shot: {cue['start_at_shot']}")
    return storyboard


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a Heritage Short storyboard.")
    parser.add_argument("path", nargs="?", type=Path, default=ROOT / "storyboard.json")
    args = parser.parse_args()
    try:
        storyboard = load_storyboard(args.path)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Invalid storyboard: {error}\n")
    shots = storyboard["shots"]
    seconds = sum(shot["duration_seconds"] for shot in shots)
    print(f"Valid storyboard: {len(shots)} shots, {seconds} seconds.")


if __name__ == "__main__":
    main()
