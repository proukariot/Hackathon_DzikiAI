import requests
from pypdf import PdfReader
import json

API_URL = "http://127.0.0.1:8000/extract"
PDF_PATH = "data/Walker.pdf"


def read_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def send_to_api(text):
    payload = {"text": text}
    response = requests.post(API_URL, json=payload)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    print("✔ Reading PDF...")
    pdf_text = read_pdf(PDF_PATH)

    print("✔ Sending to API...")
    result = send_to_api(pdf_text)

    print("\n✔ Result JSON:")
    print(json.dumps(result, indent=4, ensure_ascii=False))
