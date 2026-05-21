import os
import tempfile
import ffmpeg
from google.cloud import storage

BUCKET_NAME = "meeting-summarizer-audio"


def upload_file(file, meeting_id: str) -> str:
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    ext = os.path.splitext(file.filename)[1]

    blob_name = f"meetings/{meeting_id}/audio.wav"

    # 1. save incoming upload temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_input:
        tmp_input.write(file.file.read())
        input_path = tmp_input.name

    # 2. create temp output file (normalized audio)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_output:
        output_path = tmp_output.name

    # 3. convert to mono + 16kHz
    ffmpeg.input(input_path).output(
        output_path,
        ac=1,        # mono
        ar=16000,    # 16kHz
        format="wav"
    ).run(overwrite_output=True)

    # 4. upload cleaned file
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(output_path)

    # cleanup
    os.remove(input_path)
    os.remove(output_path)

    return f"gs://{BUCKET_NAME}/{blob_name}"