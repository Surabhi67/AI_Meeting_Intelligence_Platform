import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("../.env")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def generate_summary(transcript):

    prompt = f"""
    Summarize this meeting transcript.

    Give:
    - Main topics discussed
    - Important points
    - Action items

    Important:
    - Do not use Markdown formatting.
    - Do not use #, *, **, or bullet symbols.
    - Return plain text only.
    - Use simple headings and numbered lists.

    Transcript:

    {transcript}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You summarize meeting transcripts clearly and concisely."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content