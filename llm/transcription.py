import os
import json
import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


def transcribe_audio(file_path: str) -> str:
    """Wysyła nagranie do Whisper i zwraca tekst."""
    with open(file_path, "rb") as f:
        transcription = client.audio.transcriptions.create(model="whisper-1", file=f)
    return transcription.text


def save_transcription(text: str, output_dir: str = "Transcriptions") -> str:
    """Zapisuje transkrypcję do folderu Transcriptions jako JSON."""
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"transcription_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({"text": text}, f, ensure_ascii=False, indent=2)

    return filepath
