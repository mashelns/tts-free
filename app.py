import streamlit as st
import requests

# ================================
# 🔐 Ambil API key dari secrets atau input user
# ================================
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["api_key"] if "api_key" in st.secrets else ""

st.title("🌍 ElevenLabs Multilingual TTS")

st.markdown("Ubah teks ke suara dengan ElevenLabs multibahasa.")

# API Key input (tersimpan)
st.session_state.api_key = st.text_input("🔑 API Key (tersimpan di sesi)", st.session_state.api_key, type="password")

# Multilingual voice options (official voices)
voices = {
    "Rachel (English/Spanish/French)": "21m00Tcm4TlvDq8ikWAM",
    "Antoni (EN/ES)": "ErXwobaYiN019PkySvjV",
    "Elli (EN/DE)": "MF3mGyEYCl7XYWbV9V6O",
    "Dorothy (Multilingual)": "ThT5KcBeYPX3keUQqHPh",
    "Josh (Multilingual)": "TxGEqnHWrfWFTfGW9XjX"
}

voice_name = st.selectbox("🧬 Pilih Voice Multibahasa", list(voices.keys()))
voice_id = voices[voice_name]

# Input teks
text = st.text_area("📜 Masukkan Teks", height=200, placeholder="Masukkan teks dalam bahasa apa pun yang didukung")

if st.button("🎤 Ubah ke Suara"):
    if not st.session_state.api_key or not text.strip():
        st.error("Harap isi API Key dan teks.")
    else:
        headers = {
            "xi-api-key": st.session_state.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "text": text,
            "voice_settings": {
                "stability": 0.6,
                "similarity_boost": 0.8
            }
        }

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        with st.spinner("Menghasilkan audio..."):
            response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            st.audio(response.content, format="audio/mp3")
            st.success("✅ Audio berhasil dibuat.")
        else:
            st.error(f"❌ Gagal: {response.status_code} - {response.text}")
