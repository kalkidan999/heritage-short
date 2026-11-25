import argparse
import subprocess
from pathlib import Path

from .storyboard import ROOT, load_storyboard


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a black-screen radio cut.")
    parser.add_argument("narration", type=Path, help="Narration pre-timed to the storyboard")
    parser.add_argument("music", type=Path, help="Placeholder music you have permission to use")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs" / "radio-cut.mp4")
    args = parser.parse_args()
    try:
        storyboard = load_storyboard(ROOT / "storyboard.json")
        duration = sum(shot["duration_seconds"] for shot in storyboard["shots"])
        for source in (args.narration, args.music):
            if not source.is_file():
                raise ValueError(f"Audio file not found: {source}")
            if args.output.resolve() == source.resolve():
                raise ValueError("Output must not overwrite an audio input.")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-n",
                "-f", "lavfi", "-i", "color=black:s=640x360:r=24",
                "-i", str(args.narration),
                "-stream_loop", "-1", "-i", str(args.music),
                "-filter_complex",
                "[1:a:0]volume=0.8[n];[2:a:0]volume=0.12[m];"
                "[n][m]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95:level=0[a]",
                "-map", "0:v:0", "-map", "[a]", "-t", str(duration),
                "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-movflags", "+faststart", str(args.output),
            ],
            check=True,
        )
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Radio cut failed: {error}") from None
    print(f"Radio cut: {args.output} ({duration}s)")


if __name__ == "__main__":
    main()
