import streamlit as st
import os
import datetime
from sql_db.client import get_visits
from sql_db.visit import Visit

st.title("Vet Assistant")

# Folder na nagrania
SAVE_DIR = "Recordings"
os.makedirs(SAVE_DIR, exist_ok=True)

# Nagrywanie
audio_file = st.audio_input("Nagraj wizyte")

if audio_file:
    st.audio(audio_file)

    # Generowanie unikalnej nazwy pliku
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recording_{timestamp}.wav"
    filepath = os.path.join(SAVE_DIR, filename)

    # Zapis do pliku
    with open(filepath, "wb") as f:
        f.write(audio_file.getvalue())

    st.success(f"Zapisano nagranie jako: {filename}")
    st.write("Ścieżka:", filepath)
