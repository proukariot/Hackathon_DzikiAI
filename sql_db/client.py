import requests
from visit import Visit

SERVER_URL = "http://localhost:8000"


def send_visit(visit):
    payload = visit.get_payload()
    print(payload)
    r = requests.post(f"{SERVER_URL}/add_visit", json=payload)
    print("Response:", r.json())
    print("Response code:", r.status_code)


def get_messages():
    r = requests.get(f"{SERVER_URL}/all")
    print("Messages:", r.json())


def get_test_visit():
    visit = Visit(
        id_visit = 1,
        id_animal = 1,
        owner_name ="Jan Nowak",
        pet_name = "Burek",
        breed = "mieszany",
        species = "pies",
        age = 7,
        sex = "samiec",
        coat = "rudy",
        weight = "10",
        interview_description = "opis_wywiadu",
        treatment_description = "opis_badania",
        applied_medicines = "zastosowane leki",
        "recommendation" = "zalecenia",
    )

    return visit


visit = get_test_visit()
send_visit(visit)
