import json
from google.cloud import storage

BUCKET_NAME = "meeting-summarizer-audio"


def get_transcript(gcs_uri: str):

    # remove gs://
    path = gcs_uri.replace(
        f"gs://{BUCKET_NAME}/",
        ""
    )

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    blob = bucket.blob(path)

    data = json.loads(
        blob.download_as_text()
    )

    transcript = ""

    for result in data["results"]:
        transcript += result["alternatives"][0]["transcript"] + " "

    return transcript