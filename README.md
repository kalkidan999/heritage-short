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
# heritage-short
# heritage-short
