# Kaldi and the Red Berries

## Intent and audience

I wanted to retell the Ethiopian legend of Kaldi in first-person
Amharic, with English subtitles for viewers who need them. The short
aims to connect Kaldi's curiosity to the warmth of a present-day
Ethiopian coffee ceremony without presenting the legend as fact.

## What I built

A validated, ten-shot storyboard sets the timing, narration, visual
prompts, and music cues. The edit rebuilds from prepared assets in
one command. Both 76-second exports were verified: 1280×720 horizontal
and 720×1280 vertical. The pipeline does not yet regenerate all assets
from a clean clone.

## Feedback and changes

The planned three-viewer radio-cut test and near-final audience test
were not completed. Creator review found that synthetic ambience
sounded like rain and the backing masked the narration. I removed the
ambience, raised the narration clips, and ducked the music during speech.
The approved comparison mix uses a Pixabay track, not an original score.

## Hardest problem

The Kaggle GPU session remained queued, so I could not verify a Wan
image-to-video run. Instead, I tested SadTalker locally on the CPU with
an opening still and a three-second excerpt of the Amharic recording.
After confirming that Kaldi's mouth followed the speech, I rendered
the full opening and rebuilt both layouts. The other scenes use stills.

## What helped and what did not

The storyboard contract helped most: the same shot IDs and durations
linked narration, stills, and video. I could replace just the opening
image with a motion clip without changing the rest of the timeline.
Relying on hosted GPU availability did not work in this run; I should
have verified an available runtime before planning around it.

## Extension and next steps

The audio-driven opening and speech-triggered music ducking extend the
stills cut. Next I would make an original score, complete both audience
tests, and test motion on the goat-and-cherry shot. To make the pipeline
fully reproducible, I would add provider adapters, per-shot caching,
and model-call logs with actual timing and cost measurements.
