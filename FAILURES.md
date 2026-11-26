# Failures

| What happened | Response and outcome |
| --- | --- |
| First FFmpeg smoke test timed out after 30 seconds | A direct encode and subsequent Python run succeeded. The original cause was not established. |
| Kaggle interactive GPU session stayed queued | No Wan render was verified. Used stills for the other scenes and local SadTalker for the opening. |
| SadTalker dependency build failed on Python 3.8 | Pinned LMDB to 1.5.1 in the isolated environment; dependencies then installed. |
| SadTalker checkpoint download timed out and the sandbox blocked an automatic model fetch | Retried the checkpoint download and fetched the face-model weights separately. The preview and full opening rendered locally. |
| Music masked narration | Measured the quiet source voice, normalized the six clips, lowered the music, and added speech-triggered ducking. |
