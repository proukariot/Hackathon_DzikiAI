import streamlit as st
import os
import datetime
from sql_db.client import get_animals
from llm.transcription import save_transcription


st.title("Vet Assistant")

# --- Pobranie danych o zwierzętach ---
animals_data = get_animals()

if not animals_data:
    st.error("Brak danych o zwierzętach z serwera.")
else:
    # --- SELECT: Właściciel ---
    owner_names = sorted(list({row["owner_name"] for row in animals_data}))
    selected_owner = st.selectbox("Wybierz właściciela", owner_names)

    # Zwierzęta właściciela
    animals_for_owner = [
        row for row in animals_data if row["owner_name"] == selected_owner
    ]

    # --- SELECT: Zwierzę ---
    animal_name_to_obj = {row["pet_name"]: row for row in animals_for_owner}
    selected_animal_name = st.selectbox(
        "Wybierz zwierzę", list(animal_name_to_obj.keys())
    )

    selected_animal = animal_name_to_obj.get(selected_animal_name)

    # --- Wyświetlanie danych pacjenta w formie karty ---
    if selected_animal:
        st.subheader("📋 Karta pacjenta")

        # Obliczanie wieku
        current_year = datetime.datetime.now().year
        birth_year = int(selected_animal["birth_year"])
        age = current_year - birth_year

        # User-friendly karta
        st.markdown(
            f"""
            <div style="padding: 15px; border-radius: 10px; background-color: #f5f5f5; border: 1px solid #ddd;">
                <h3 style="margin-bottom: 10px;">🐾 {selected_animal['pet_name']}</h3>
                <p><strong>Gatunek:</strong> {selected_animal['species'].capitalize()}</p>
                <p><strong>Rasa:</strong> {selected_animal['breed']}</p>
                <p><strong>Płeć:</strong> {selected_animal['sex'].capitalize()}</p>
                <p><strong>Wiek:</strong> {age} lat</p>
                <p><strong>Rok urodzenia:</strong> {birth_year}</p>
                <p><strong>Umaszczenie:</strong> {selected_animal['coat']}</p>
                <p><strong>Waga:</strong> {selected_animal['waga']} kg</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --- Nagrywanie wizyty ---
    SAVE_DIR = "Recordings"
    os.makedirs(SAVE_DIR, exist_ok=True)

    audio_file = st.audio_input("🎙️ Nagraj wizytę")

    if audio_file:
        st.audio(audio_file)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        animal_id = selected_animal["id_animal"] if selected_animal else "unknown"
        filename = f"recording_{animal_id}_{timestamp}.wav"
        filepath = os.path.join(SAVE_DIR, filename)

        with open(filepath, "wb") as f:
            f.write(audio_file.getvalue())

        st.success(f"Nagranie zapisane jako **{filename}**")
        st.write("📁 Ścieżka:", filepath)
