import logging
import random
import subprocess

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from TikTokApi import TikTokApi

from utils import config

GCLOUD_JSON = config["gcloud"]["json-file"]
GCLOUD_PROJECT = config["gcloud"]["project"]

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)

logger.addHandler(ch)


def videos_location(id):
    return f"../data/videos/{id}.mp4"


def audio_location(id):
    return f"../data/audio/{id}.wav"


def transcriptions_location(id):
    return f"../data/transcripts/{id}.txt"


def download_videos(urls):
    v_ids = [x.strip().split("/")[-1] for x in urls.split(",")]

    # Avoid scraping protection
    d_id = str(random.randint(10000, 999999999))

    with TikTokApi(custom_device_id=d_id) as api:
        for v_id in v_ids:
            logger.info(f"Downloading video with id: {v_id}")
            try:
                video_bytes = api.video(id=v_id).bytes()

                with open(videos_location(v_id), "wb") as output:
                    output.write(video_bytes)
            except:
                logger.error("Error downloading video. Skipping...")

    logger.info("Downloading finished!\n")

    return v_ids


def convert_videos_to_audio_files(v_ids):
    for v_id in v_ids:
        logger.info(f"Converting {v_id}.mp4")

        command = f"ffmpeg -y -loglevel quiet -i {videos_location(v_id)} -vn {audio_location(v_id)}"
        subprocess.call(command, shell=True)

    logger.info("Conversion finished!\n")

    return v_ids


def transcribe_audio(v_ids):
    # Initialize client
    client = SpeechClient().from_service_account_json(GCLOUD_JSON)
    config = cloud_speech.RecognitionConfig(auto_decoding_config={})

    recognizer_id = "omnirecogniser51"

    # Get/Create Recognizer
    try:
        request = cloud_speech.GetRecognizerRequest(
            name=f"projects/{GCLOUD_PROJECT}/locations/global/recognizers/{recognizer_id}"
        )
        recognizer = client.get_recognizer(request=request)
    except:
        request = cloud_speech.CreateRecognizerRequest(
            parent=f"projects/{GCLOUD_PROJECT}/locations/global",
            recognizer_id=recognizer_id,
            recognizer=cloud_speech.Recognizer(
                language_codes=["en-US"], model="latest_long"
            ),
        )

        operation = client.create_recognizer(request=request)
        recognizer = operation.result()

    transcriptions = []
    for v_id in v_ids:
        logger.info(f"Transcribing {v_id}.wav")

        with open(audio_location(v_id), "rb") as f:
            content = f.read()

        try:
            request = cloud_speech.RecognizeRequest(
                recognizer=recognizer.name, config=config, content=content
            )

            response = client.recognize(request=request)
            results = [result.alternatives[0].transcript for result in response.results]

            with open(transcriptions_location(v_id), "w") as output:
                text = "".join(results)

                transcriptions.append(text)
                output.write(text)
        except:
            logger.error("File too big. Skipping...")

    logger.info("Transcription finished!\n")

    return transcriptions
