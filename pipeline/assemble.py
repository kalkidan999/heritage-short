import argparse
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from .storyboard import ROOT, load_storyboard


def timestamp(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},000"


def assemble(storyboard: dict, audio: Path, output: Path, vertical: bool = False) -> None:
    width, height = (720, 1280) if vertical else (1280, 720)
    framing = (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0x18120e,setsar=1"
        if vertical else
        "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1"
    )
    margin = 48 if vertical else 22
    font_size = 13 if vertical else 15
    if not audio.is_file():
        raise ValueError(f"Missing audio source: {audio}")
    if output.exists():
        raise ValueError(f"Output already exists: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory() as directory:
        scratch = Path(directory)
        manifest = []
        subtitles = []
        start = 0
        for index, shot in enumerate(storyboard["shots"]):
            duration = shot["duration_seconds"]
            end = start + duration
            shot_id = shot["id"]
            if shot_id == "end_card":
                source = ["-f", "lavfi", "-i", f"color=black:s={width}x{height}:r=24"]
                caption = storyboard["end_card"]
            else:
                image = ROOT / "outputs" / "keyframes" / f"{shot_id}.png"
                clip = ROOT / "outputs" / "shots" / f"{shot_id}.mp4"
                if clip.is_file():
                    source = ["-i", str(clip)]
                elif image.is_file():
                    source = ["-loop", "1", "-framerate", "24", "-i", str(image)]
                else:
                    raise ValueError(f"Missing keyframe: {image}")
                narration = shot["narration"]
                caption = narration["subtitle_en"] if narration else ""
            if caption:
                subtitles.append(
                    f"{len(subtitles) + 1}\n{timestamp(start)} --> {timestamp(end)}\n{caption}\n"
                )
            segment = f"shot-{index}.mp4"
            ffmpeg(
                [*source, "-t", str(duration), "-vf",
                 f"{framing},fps=24,tpad=stop_mode=clone:stop_duration={duration}",
                 "-an", "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", segment],
                scratch,
            )
            manifest.append(f"file '{segment}'")
            start = end
        (scratch / "shots.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8")
        (scratch / "captions.srt").write_text("\n".join(subtitles), encoding="utf-8")
        ffmpeg(
            ["-f", "concat", "-safe", "1", "-i", "shots.txt", "-i", str(audio),
             "-map", "0:v:0", "-map", "1:a:0",
             "-vf", f"subtitles=captions.srt:force_style='Alignment=2,MarginV={margin},FontSize={font_size}'",
             "-af", "apad", "-t", str(start), "-c:v", "libx264", "-preset", "veryfast",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", str(output)],
            scratch,
        )


def ffmpeg(arguments: list[str], directory: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-n", *arguments],
        cwd=directory,
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Assemble a stills rough cut.")
    parser.add_argument("audio", type=Path, help="Mixed narration and music")
    parser.add_argument("--vertical", action="store_true", help="Export in 9:16")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        filename = "rough-cut-vertical.mp4" if args.vertical else "rough-cut.mp4"
        output = args.output or ROOT / "outputs" / filename
        assemble(load_storyboard(ROOT / "storyboard.json"), args.audio.resolve(), output.resolve(), args.vertical)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Rough cut failed: {error}") from None
    print(f"Rough cut: {output}")


if __name__ == "__main__":
    main()
