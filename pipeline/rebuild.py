import argparse
import subprocess
from pathlib import Path

from .assemble import assemble
from .storyboard import ROOT, load_storyboard


def main() -> None:
    parser = argparse.ArgumentParser(description="Build both film layouts from prepared assets.")
    parser.add_argument("audio", type=Path, help="Prepared narration and music mix")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs" / "rebuild")
    args = parser.parse_args()
    destinations = [
        (args.output_dir.resolve() / "khalid-horizontal.mp4", False),
        (args.output_dir.resolve() / "khalid-vertical.mp4", True),
    ]
    try:
        storyboard = load_storyboard(ROOT / "storyboard.json")
        for output, _ in destinations:
            if output.exists():
                raise ValueError(f"Output already exists: {output}; choose a new --output-dir.")
        for output, vertical in destinations:
            assemble(storyboard, args.audio.resolve(), output, vertical=vertical)
            print(output)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Rebuild failed: {error}") from None


if __name__ == "__main__":
    main()
