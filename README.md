# TikTalk Transcriber

Transcribes TikTok videos into text format.

## Requirements:

- python
- pip
- ffmpeg [https://ffmpeg.org/]
- gcloud service account key [https://cloud.google.com/iam/docs/keys-create-delete#iam-service-account-keys-create-gcloud]

## How to run

### Virtual environment

- `/> python -m venv .venv`
- `/> source .venv/bin/activate`
- `/> python -m pip install -r requirements.txt`

### Config

- In data/config.yaml add:
  - path to service account key json file
  - project

### Packages setup

Gradio doesn't run without this modification but you can still manually call the functions in `src/transcriber`.

- at /Users/maximekiriakov/Documents/Omnithink/dev/scripts/tiktok_audio_transcription/.venv/lib/python3.11/site-packages/TikTokApi/tiktok.py:205 add:

```
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
```

### Run

- `src/> gradio app.py`
