# TikTalk Transcriber

Transcribes TikTok videos into text format.

## Requirements:

- python
- pip
- ffmpeg [https://ffmpeg.org/]
- gcloud service account key [https://cloud.google.com/iam/docs/keys-create-delete#iam-service-account-keys-create-gcloud]

## How to run

### Virtual environment

- `bash /> python -m venv .venv`
- `bash /> source .venv/bin/activate`
- `bash /> python -m pip install -r requirements.txt

### Config

- In data/config.yaml:
  - project
  - path to service account key json file

### Packages setup

Gradio doesn't run without this modification but you can still manually call the functions in `src/transcriber`.

- /Users/maximekiriakov/Documents/Omnithink/dev/scripts/tiktok_audio_transcription/.venv/lib/python3.11/site-packages/TikTokApi/tiktok.py:205 add:

```
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
```

### Run

- `bash src/> gradio app.py
