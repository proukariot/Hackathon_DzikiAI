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
        imię="1",
        rasa="rasa",
        płec="płec",
        wiek=0,
        maść="maść",
        waga=0,
        opis_wywiadu="opis_wywiadu",
        opis_badania="opis_badania",
        zastosowane_leki="zastosowane_leki",
        zalecenia="zalecenia",
    )

    return visit


def get_visits():
    r = requests.get(f"{SERVER_URL}/all_visits")
    print(f"visits: {r.json()}")
    print(f"status: {r.status_code}")

    return r.json()


# visit = get_test_visit()
get_visits()
# send_visit(visit)
