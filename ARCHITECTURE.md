# Architecture

`storyboard.json` is the shared contract. The validator checks the schema,
runtime, unique IDs, and references. The rehearsal and radio-cut tools use
shot durations to place narration. Assembly prefers a shot-ID MP4 over its
matching PNG, keeps the supplied audio mix, and renders captions and the
disclosure card in both aspect ratios.

Image generation and SadTalker currently run outside the Python CLI. The
current assembly command starts from prepared assets, not a clean clone.
Provider adapters, per-shot cache keys, retries, and model-call logging
are not implemented end to end.
