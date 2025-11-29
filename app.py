import streamlit as st
import os
import json
import datetime
from sql_db.client import get_animals
from llm.transcription import transcribe_audio, save_transcription
from llm.ai import summarize_vet_visit

# -----------------------------------------------------------
# 🌟 Wyróżniony nagłówek aplikacji
# -----------------------------------------------------------

st.markdown(
    """
    <h1 style="
        text-align: center; 
        color: #2458a6;
        font-size: 48px;
        margin-bottom: 10px;">
        🐾 Vet Assistant 💙
    </h1>
    <p style="text-align:center; color:#4a4a4a; margin-top:-10px;">
        Inteligentny asystent gabinetu weterynaryjnego
    </p>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------
# 🐾 Dane o pacjencie
# -----------------------------------------------------------

animals_data = get_animals()
selected_animal = None
selected_owner = None
birth_year = None
age = None

if not animals_data:
    st.error("Brak danych o zwierzętach z serwera.")
else:
    # Wybór właściciela
    owner_names = sorted(list({row["owner_name"] for row in animals_data}))
    selected_owner = st.selectbox("Wybierz właściciela", owner_names)

    # Zwierzęta danego właściciela
    animals_for_owner = [row for row in animals_data if row["owner_name"] == selected_owner]

    # Wybór zwierzęcia
    animal_name_to_obj = {row["pet_name"]: row for row in animals_for_owner}
    selected_animal_name = st.selectbox("Wybierz zwierzę", list(animal_name_to_obj.keys()))

    selected_animal = animal_name_to_obj.get(selected_animal_name)

    # --- Karta pacjenta ---
    if selected_animal:
        st.subheader("📋 Karta pacjenta")

        current_year = datetime.datetime.now().year
        birth_year = int(selected_animal["birth_year"])
        age = current_year - birth_year

        st.markdown(f"### 🐾 {selected_animal['pet_name']}")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Opiekun:**", selected_owner)
            st.write("**Gatunek:**", selected_animal["species"].capitalize())
            st.write("**Rasa:**", selected_animal["breed"])
            st.write("**Płeć:**", selected_animal["sex"].capitalize())

        with col2:
            st.write("**Wiek:**", f"{age} lat")
            st.write("**Rok urodzenia:**", f"{birth_year}")
            st.write("**Umaszczenie:**", selected_animal["coat"])
            st.write("**Waga:**", f"{selected_animal['waga']} kg")

# -----------------------------------------------------------
# 🎙️ Wyróżniona sekcja nagrywania
# -----------------------------------------------------------

st.markdown(
    """
    <div style="
        margin-top: 25px;
        padding: 18px;
        border-radius: 12px;
        border: 2px solid #6ab0ff;
        background-color: #eef6ff;">
        <h3 style="margin-top: 0;">🎙️ Nagrywanie wizyty</h3>
    </div>
    """,
    unsafe_allow_html=True
)

SAVE_DIR = "Recordings"
TRANS_DIR = "Transcriptions"
os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(TRANS_DIR, exist_ok=True)

audio_file = st.audio_input("Kliknij, aby rozpocząć nagrywanie")

if audio_file:
    # Podgląd nagrania
    st.audio(audio_file)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    animal_id = selected_animal["id_animal"] if selected_animal else "unknown"
    audio_filename = f"recording_{animal_id}_{timestamp}.wav"
    audio_path = os.path.join(SAVE_DIR, audio_filename)

    # Zapis nagrania (bez komunikatu o nazwie pliku)
    with open(audio_path, "wb") as f:
        f.write(audio_file.getvalue())

    summary = None

    # -----------------------------------------------------------
    # 🔄 Transkrypcja + AI
    # -----------------------------------------------------------
    with st.spinner("Przetwarzam nagranie..."):
        try:
            # Transkrypcja w formacie JSON (dict)
            transcription_json = transcribe_audio(audio_path)

            # Zapis transkrypcji do katalogu Transcriptions
            save_transcription(transcription_json, output_dir=TRANS_DIR)

            st.info("📝 Transkrypcja została zapisana.")

            # Podsumowanie wizyty z LLM
            summary = summarize_vet_visit(transcription_json)

        except Exception:
            st.error("Wystąpił problem podczas transkrypcji lub generowania podsumowania.")
            summary = None

    # -----------------------------------------------------------
    # 🧾 Ładnie sformatowane podsumowanie wizyty
    # -----------------------------------------------------------

    if summary:
        st.markdown("## 🧾 Podsumowanie wizyty")

        col_left, col_right = st.columns(2)

        # Lewa kolumna: objawy + czas trwania
        with col_left:
            st.markdown("### 🩺 Objawy")
            objawy = summary.get("objawy", [])
            if objawy:
                st.markdown(
                    "<ul>" + "".join([f"<li>{o}</li>" for o in objawy]) + "</ul>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown("_nie podano_")

            st.markdown("### ⏱️ Od kiedy się dzieje")
            st.markdown(f"**{summary.get('od_kiedy_sie_dzieje', 'nie podano')}**")

        # Prawa kolumna: leki + dodatkowe informacje
        with col_right:
            st.markdown("### 💊 Przyjmowane leki")

            leki = summary.get("przyjmowane_leki", [])
            if leki:
                for med in leki:
                    st.markdown(
                        f"""
                        <div style="padding: 8px 12px; background:#f7f7f7; border-radius:8px; margin-bottom:8px;">
                        <strong>{med.get('nazwa', 'nie podano')}</strong><br>
                        • dawka: {med.get('dawka', 'nie podano')}<br>
                        • częstotliwość: {med.get('czestotliwosc', 'nie podano')}<br>
                        • droga podania: {med.get('droga_podania', 'nie podano')}<br>
                        • uwagi: {med.get('dodatkowe_uwagi', 'nie podano')}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.markdown("_nie podano_")

            st.markdown("### 📝 Dodatkowe informacje")
            st.markdown(f"**{summary.get('dodatkowe_informacje', 'nie podano')}**")

        st.caption("Automatycznie wygenerowane na podstawie nagranej rozmowy.")
