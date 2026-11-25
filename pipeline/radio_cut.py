import argparse
import subprocess
from pathlib import Path

from .storyboard import ROOT, load_storyboard


def narration_inputs(source: Path, shots: list) -> tuple[list, list, int]:
    if not source.is_dir():
        if not source.is_file():
            raise ValueError(f"Audio file not found: {source}")
        return ["-i", str(source)], ["[1:a:0]volume=0.8[n]"], 2

    inputs = []
    filters = []
    labels = []
    start = 0
    for shot in shots:
        if shot["narration"] is not None:
            clip = source / f"{shot['id']}.wav"
            if not clip.is_file():
                raise ValueError(f"Missing narration clip: {clip}")
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "a:0",
                 "-show_entries", "stream=duration", "-of", "csv=p=0", str(clip)],
                capture_output=True, text=True, check=True,
            )
            try:
                duration = float(result.stdout.strip())
            except ValueError:
                raise ValueError(f"Could not read audio duration: {clip}") from None
            if not 0 < duration <= shot["duration_seconds"]:
                raise ValueError(f"{clip.name} is {duration:.2f}s; it must fit its {shot['duration_seconds']}s shot.")
            index = len(labels) + 1
            label = f"[line{index}]"
            filters.append(f"[{index}:a:0]asetpts=PTS-STARTPTS,adelay={start * 1000}:all=1{label}")
            labels.append(label)
            inputs.extend(("-i", str(clip)))
        start += shot["duration_seconds"]
    if not labels:
        raise ValueError("The storyboard contains no narration lines.")
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,volume=0.8[n]")
    return inputs, filters, len(labels) + 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a black-screen radio cut.")
    parser.add_argument("narration", type=Path, help="Timed narration file or folder of shot-ID WAV files")
    parser.add_argument("music", type=Path, help="Placeholder music you have permission to use")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs" / "radio-cut.mp4")
    args = parser.parse_args()
    try:
        storyboard = load_storyboard(ROOT / "storyboard.json")
        duration = sum(shot["duration_seconds"] for shot in storyboard["shots"])
        for source in (args.narration, args.music):
            if args.output.resolve() == source.resolve():
                raise ValueError("Output must not overwrite an audio input.")
        if not args.music.is_file():
            raise ValueError(f"Audio file not found: {args.music}")
        inputs, filters, music_index = narration_inputs(args.narration, storyboard["shots"])
        filters.extend((
            f"[{music_index}:a:0]volume=0.12[m]",
            "[n][m]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95:level=0[a]",
        ))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-n",
                "-f", "lavfi", "-i", "color=black:s=640x360:r=24",
                *inputs,
                "-stream_loop", "-1", "-i", str(args.music),
                "-filter_complex", ";".join(filters),
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
