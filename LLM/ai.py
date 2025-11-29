import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


def summarize_vet_visit(transcription_json: dict) -> dict:
    system_prompt = (
        "Jestes asystentem weterynarza. "
        "Na podstawie transkrypcji przygotuj zwięzłe podsumowanie. "
        "Jeśli brakuje informacji, wpisz 'nie podano'."
    )

    user_prompt = (
        "Oto transkrypcja wizyty w formacie JSON. "
        "Wyciągnij objawy, czas trwania, leki oraz inne informacje. "
        "Zwróć odpowiedź jako poprawny JSON zgodny ze schematem.\n\n"
        f"{json.dumps(transcription_json, ensure_ascii=False, indent=2)}"
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "podsumowanie_wizyty_wet",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "objawy": {"type": "array", "items": {"type": "string"}},
                        "od_kiedy_sie_dzieje": {"type": "string"},
                        "przyjmowane_leki": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "nazwa": {"type": "string"},
                                    "dawka": {"type": "string"},
                                    "czestotliwosc": {"type": "string"},
                                    "droga_podania": {"type": "string"},
                                    "dodatkowe_uwagi": {"type": "string"},
                                },
                                "required": ["nazwa"],
                                "additionalProperties": False,
                            },
                        },
                        "dodatkowe_informacje": {"type": "string"},
                    },
                    "required": [
                        "objawy",
                        "od_kiedy_sie_dzieje",
                        "przyjmowane_leki",
                        "dodatkowe_informacje",
                    ],
                    "additionalProperties": False,
                },
            },
        },
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    # ✔️ poprawny dostęp do odpowiedzi w formacie JSON Schema
    return response.choices[0].message.parsed
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


def summarize_vet_visit(transcription_json: dict) -> dict:
    """
    transcription_json – słownik wczytany z pliku z transkrypcją (np. {'text': '...'}).
    Zwraca podsumowanie jako dict zgodny ze schematem.
    """
    system_prompt = (
        "Jesteś asystentem weterynarza. "
        "Na podstawie transkrypcji rozmowy z opiekunem zwierzęcia "
        "przygotowujesz zwięzłe, ustrukturyzowane podsumowanie w języku polskim. "
        "Skupiasz się wyłącznie na informacjach obecnych w transkrypcji. "
        "Jeśli czegoś nie ma w tekście, wpisz 'nie podano' zamiast zgadywać."
    )

    user_prompt = (
        "Oto transkrypcja wizyty w formacie JSON. "
        "Wyodrębnij z niej:\n"
        "- objawy,\n"
        "- od kiedy się dzieje (czas trwania / charakter początku),\n"
        "- przyjmowane leki,\n"
        "- dodatkowe ważne informacje.\n\n"
        "Zwróć odpowiedź w formacie JSON zgodnym ze schematem.\n\n"
        f"```json\n{json.dumps(transcription_json, ensure_ascii=False, indent=2)}\n```"
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "podsumowanie_wizyty_wet",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "objawy": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "od_kiedy_sie_dzieje": {
                            "type": "string"
                        },
                        "przyjmowane_leki": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "nazwa": {"type": "string"},
                                    "dawka": {"type": "string"},
                                    "czestotliwosc": {"type": "string"},
                                    "droga_podania": {"type": "string"},
                                    "dodatkowe_uwagi": {"type": "string"}
                                },
                                # 🟢 PRZYGOTUJ WSZYSTKIE KLUCZE JAKO REQUIRED (wymóg strict=True)
                                "required": [
                                    "nazwa",
                                    "dawka",
                                    "czestotliwosc",
                                    "droga_podania",
                                    "dodatkowe_uwagi"
                                ],
                                "additionalProperties": False
                            }
                        },
                        "dodatkowe_informacje": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "objawy",
                        "od_kiedy_sie_dzieje",
                        "przyjmowane_leki",
                        "dodatkowe_informacje"
                    ],
                    "additionalProperties": False
                }
            }
        },
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    # ⬇️ przy response_format=json_schema to już jest dict, nie string
    return response.choices[0].message.parsed
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


def summarize_vet_visit(transcription_json: dict) -> dict:
    """
    transcription_json – słownik wczytany z pliku z transkrypcją (JSON).
    Zwraca podsumowanie jako dict zgodny ze schematem.
    """
    system_prompt = (
        "Jesteś asystentem weterynarza. "
        "Na podstawie transkrypcji rozmowy z opiekunem zwierzęcia "
        "przygotowujesz zwięzłe, ustrukturyzowane podsumowanie w języku polskim. "
        "Skupiasz się wyłącznie na informacjach obecnych w transkrypcji. "
        "Jeśli czegoś nie ma w tekście, wpisz 'nie podano' zamiast zgadywać."
    )

    # Uproszczony prompt – bez ```json```, żeby nic nie mieszać
    user_prompt = (
        "Oto transkrypcja wizyty w formacie JSON.\n"
        "Na jej podstawie wyodrębnij:\n"
        "- objawy,\n"
        "- od kiedy się dzieje (czas trwania / charakter początku),\n"
        "- przyjmowane leki,\n"
        "- dodatkowe ważne informacje.\n\n"
        "Zwróć odpowiedź jako POPRAWNY JSON zgodny z podanym schematem.\n\n"
        f"{json.dumps(transcription_json, ensure_ascii=False, indent=2)}"
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "podsumowanie_wizyty_wet",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "objawy": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "od_kiedy_sie_dzieje": {
                            "type": "string"
                        },
                        "przyjmowane_leki": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "nazwa": {"type": "string"},
                                    "dawka": {"type": "string"},
                                    "czestotliwosc": {"type": "string"},
                                    "droga_podania": {"type": "string"},
                                    "dodatkowe_uwagi": {"type": "string"}
                                },
                                # strict=True → required musi zawierać WSZYSTKIE klucze z properties
                                "required": [
                                    "nazwa",
                                    "dawka",
                                    "czestotliwosc",
                                    "droga_podania",
                                    "dodatkowe_uwagi"
                                ],
                                "additionalProperties": False
                            }
                        },
                        "dodatkowe_informacje": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "objawy",
                        "od_kiedy_sie_dzieje",
                        "przyjmowane_leki",
                        "dodatkowe_informacje"
                    ],
                    "additionalProperties": False
                }
            }
        },
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",  "content": user_prompt},
        ],
    )

    # ⭐ Obsługa zarówno nowych, jak i starszych wersji biblioteki
    msg = response.choices[0].message

    # Jeśli kiedyś zaktualizujesz bibliotekę i pojawi się .parsed:
    if hasattr(msg, "parsed") and msg.parsed is not None:
        return msg.parsed

    # W Twojej wersji: message.content to string z czystym JSON-em → parsujemy ręcznie
    raw = msg.content
    return json.loads(raw)
