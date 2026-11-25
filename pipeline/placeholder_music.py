import argparse
import math
import wave
from array import array
from pathlib import Path
from sys import byteorder

from .storyboard import ROOT


SAMPLE_RATE = 24_000
NOTES = (261.63, 329.63, 392.00, 329.63, 220.00, 261.63, 329.63, 261.63)


def make_loop() -> bytes:
    samples = array("h")
    for frequency in NOTES:
        for index in range(SAMPLE_RATE):
            time = index / SAMPLE_RATE
            envelope = min(1, time / 0.03, (1 - time) / 0.15) * math.exp(-3 * time)
            phase = math.tau * frequency * time
            tone = math.sin(phase) + 0.18 * math.sin(2 * phase)
            samples.append(round(9000 * envelope * tone))
    if byteorder == "big":
        samples.byteswap()
    return samples.tobytes()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an original placeholder music loop.")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs" / "placeholder-music.wav")
    args = parser.parse_args()
    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("xb") as file, wave.open(file, "wb") as track:
            track.setparams((1, 2, SAMPLE_RATE, 0, "NONE", "not compressed"))
            track.writeframes(make_loop())
    except OSError as error:
        raise SystemExit(f"Could not write placeholder music: {error}") from None
    print(args.output)


if __name__ == "__main__":
    main()
