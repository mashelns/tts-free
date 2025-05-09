import streamlit as st
import requests

st.set_page_config(page_title="ElevenLabs Multilingual TTS", layout="centered")
st.title("🗣️ ElevenLabs Multilingual TTS")

# Load API key
api_key = st.secrets["api_key"] if "api_key" in st.secrets else ""

# User input fallback
if not api_key:
    api_key = st.text_input("🔑 Masukkan API Key kamu", type="password")

# Pilihan voice multibahasa resmi dari ElevenLabs
multilang_voices = {
    "Rachel (EN/ES/FR)": "21m00Tcm4TlvDq8ikWAM",
    "Antoni (EN/ES)": "ErXwobaYiN019PkySvjV",
    "Elli (EN/DE)": "MF3mGyEYCl7XYWbV9V6O",
    "Dorothy (Multilang)": "ThT5KcBeYPX3keUQqHPh",
    "Josh (Multilang)": "9F4C8ztpNUmXkdDDbz3J",
}

voice_label = st.selectbox("🧬 Pilih Voice Multibahasa", list(multilang_voices.keys()))
voice_id = multilang_voices[voice_label]

text = st.text_area("📜 Masukkan teks dalam bahasa apa pun yang didukung:", height=200)

if st.button("🔊 Konversi ke Suara"):
    if not api_key or not text.strip():
        st.error("Mohon isi API Key dan teks.")
    else:
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",  # ✅ Gunakan model multibahasa
            "voice_settings": {
                "stability": 0.6,
                "similarity_boost": 0.75
            }
        }

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        with st.spinner("🔄 Menghasilkan audio..."):
            response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            st.audio(response.content, format="audio/mp3")
            st.success("✅ Audio berhasil dibuat.")
        else:
            st.error(f"❌ Gagal: {response.status_code}\n{response.text}")
