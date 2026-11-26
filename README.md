# Heritage Short

First checkpoint: verify that Python can call FFmpeg and log the result.

Run `python3 smoke_test.py` from this directory. It requires Python 3 and
FFmpeg with libx264 on your PATH. It creates a one-second black MP4 in
`outputs/` and appends a status and latency record to `runs.jsonl`.
This checks local tooling only; it does not contact a model provider.

## Validate the storyboard

From the project directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pipeline.storyboard
```

The validator checks the JSON Schema first, then verifies total runtime,
unique IDs, and links from shots and music cues. It does not generate media.

## Rehearse the narration

Run `.venv/bin/python -m pipeline.rehearsal` to print each shot's time
window, Amharic line, and English subtitle from the validated storyboard.
Read each line at a natural pace and check that it fits its shot with
room for pauses. Shots marked `[No narration]` still have room for music
or sound effects. The printed windows are not measured speech timings.

## Build the radio cut

Record one Amharic narration track with the lines placed at their rehearsal
times. Use a recording you have permission to share and music you have
permission to use. Then run:

```sh
.venv/bin/python -m pipeline.radio_cut narration.wav placeholder-music.wav
```

This writes `outputs/radio-cut.mp4`: a black screen, narration, and quiet
looping music. It uses the storyboard runtime, but does not align speech
for you. To keep another draft, pass a new filename with `--output`.

Alternatively, record each line separately and put the WAV files in
`outputs/narration/`: `intro.wav`, `graze.wav`, `cherries.wav`, `leap.wav`,
`wonder.wav`, and `roast.wav`. Pass that folder instead of `narration.wav`.
The command places each clip at its shot's start and rejects any clip
that is too long. No recording is needed for Kaldi's jump.

If you don't have placeholder music, generate a short original loop and
use it with the per-shot recordings:

```sh
.venv/bin/python -m pipeline.placeholder_music
.venv/bin/python -m pipeline.radio_cut outputs/narration outputs/placeholder-music.wav
```

The loop is for the prototype only; it does not replace the final score
or the “ቡና፣ ቡና” refrain.

## Assemble a stills rough cut

Put scene PNGs named after their shot IDs in `outputs/keyframes/`.
Pass a mixed audio file (or a radio-cut MP4 with audio):

```sh
.venv/bin/python -m pipeline.assemble outputs/radio-cut-kaldi.mp4
```

This outputs a horizontal rough cut with burned-in English subtitles
and the AI disclosure card. FFmpeg must include the `subtitles` filter.

Add `--vertical` to export `outputs/rough-cut-vertical.mp4` in 9:16.
The vertical rough cut fits each still inside the frame without cropping,
so the goats and ceremony guests stay visible.

To use an animated shot, put its MP4 in `outputs/shots/`, named after
its shot ID (for example, `intro.mp4`). Assembly prefers that clip over
the PNG, trims it to the storyboard slot, or holds its final frame if it
is short. It keeps the supplied narration mix rather than the clip audio.

## Rebuild both layouts

With the keyframes, optional motion clips, and a prepared audio mix:

```sh
.venv/bin/python -m pipeline.rebuild /path/to/mixed-audio.wav
```

This validates the storyboard and writes both MP4s to `outputs/rebuild/`.
Use `--output-dir` to keep a separate version. This rebuilds the edit
from prepared assets; it does not generate missing assets from a clean clone.
# heritage-short
# heritage-short
