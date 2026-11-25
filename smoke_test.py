import json
import subprocess
from pathlib import Path
from time import perf_counter


def main():
    root = Path(__file__).resolve().parent
    output = root / "outputs" / "smoke-test.mp4"
    output.parent.mkdir(exist_ok=True)
    started = perf_counter()
    status = "failed"
    try:
        subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-f", "lavfi", "-i", "color=black:s=320x180:r=24",
                "-t", "1", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                str(output),
            ],
            check=True,
            timeout=30,
        )
        status = "ok"
    finally:
        with (root / "runs.jsonl").open("a", encoding="utf-8") as log:
            log.write(json.dumps({
                "event": "local_smoke_test",
                "tool": "ffmpeg",
                "status": status,
                "latency_ms": round((perf_counter() - started) * 1000),
            }) + "\n")
    print(output)


if __name__ == "__main__":
    main()
