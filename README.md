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
# heritage-short
# heritage-short
