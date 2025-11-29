from pydantic import BaseModel


class Visit(BaseModel):
    imię: str
    rasa: str
    płec: str
    wiek: int
    maść: str
    waga: int
    opis_wywiadu: str
    opis_badania: str
    zastosowane_leki: str
    zalecenia: str

    def get_payload(self):
        return {
            "imię": self.imię,
            "rasa": self.rasa,
            "płec": self.płec,
            "wiek": self.wiek,
            "maść": self.maść,
            "waga": self.waga,
            "opis_wywiadu": self.opis_wywiadu,
            "opis_badania": self.opis_badania,
            "zastosowane_leki": self.zastosowane_leki,
            "zalecenia": self.zalecenia,
        }
