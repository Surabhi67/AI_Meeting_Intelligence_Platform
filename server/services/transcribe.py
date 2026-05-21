from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

BUCKET_NAME = "meeting-summarizer-audio"
MAX_AUDIO_LENGTH_SECS = 8 * 60 * 60


def run_batch_recognize(meeting_id: str, audio_ext: str):
    client = SpeechClient()

    audio_gcs_uri = f"gs://{BUCKET_NAME}/meetings/{meeting_id}/audio{audio_ext}"
    gcs_output_folder = f"gs://{BUCKET_NAME}/meetings/{meeting_id}/transcription"

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config={},
        features=cloud_speech.RecognitionFeatures(
            enable_word_confidence=False,        # keep OFF (saves cost)
            enable_word_time_offsets=False,      # keep OFF (saves cost)
            enable_automatic_punctuation=True,   # keep ON (useful, low cost impact)
        ),
        model="telephony",  
        language_codes=["en-US"],
    )

    output_config = cloud_speech.RecognitionOutputConfig(
        gcs_output_config=cloud_speech.GcsOutputConfig(uri=gcs_output_folder),
    )

    files = [
        cloud_speech.BatchRecognizeFileMetadata(uri=audio_gcs_uri)
    ]

    request = cloud_speech.BatchRecognizeRequest(
        recognizer="projects/project-1fbd9291-46f9-4e56-897/locations/global/recognizers/_",
        config=config,
        files=files,
        recognition_output_config=output_config,
    )

    operation = client.batch_recognize(request=request)

    print("Waiting for transcription...")
    result = operation.result(timeout=MAX_AUDIO_LENGTH_SECS * 3)

    return result