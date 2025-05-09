import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv, set_key

ENV_PATH = ".env"
load_dotenv(ENV_PATH)

# =================== PAGE CONFIG ====================
st.set_page_config(page_title="ElevenLabs TTS Multilang", layout="centered")

st.title("🎙️ ElevenLabs Multilingual TTS")

# =================== API KEY ====================
api_key = os.getenv("ELEVEN_API_KEY", "")
input_api = st.text_input("🔑 API Key ElevenLabs:", value=api_key, type="password")

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("💾 Simpan"):
        set_key(ENV_PATH, "ELEVEN_API_KEY", input_api)
        st.success("API Key disimpan.")
with col2:
    if st.button("❌ Hapus"):
        set_key(ENV_PATH, "ELEVEN_API_KEY", "")
        st.warning("API Key dihapus.")

st.divider()

# =================== VOICE ID ====================
multilang_voices = {
    "🌍 Dandan (Multilang)": "9F4C8ztpNUmXkdDDbz3J",
    "🧑‍💼 Alex (Multilang)": "yl2ZDV1MzN4HbQJbMihG",
    "🎧 Nick (Multilang)": "WrPknjKhmIXkCONEtG3j",
    "🛠️ Gunakan Custom Voice ID": "custom"
}

voice_choice = st.selectbox("🎤 Pilih Suara:", list(multilang_voices.keys()))
voice_id = ""

if multilang_voices[voice_choice] == "custom":
    voice_id = st.text_input("🔧 Masukkan Custom Voice ID:")
else:
    voice_id = multilang_voices[voice_choice]

st.divider()

# =================== TEXT TO SPEECH ====================
text = st.text_area("📝 Teks (boleh multibahasa):", height=200)

if st.button("🚀 Konversi"):
    if not input_api.strip() or not voice_id.strip() or not text.strip():
        st.error("❗ Mohon isi semua field: API Key, Teks, dan Voice ID.")
    else:
        headers = {
            "xi-api-key": input_api.strip(),
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.6,
                "similarity_boost": 0.75
            }
        }
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        with st.spinner("🎧 Mengonversi..."):
            response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            audio_data = response.content
            filename = f"TTSBOIMKA_{int(time.time())}.mp3"
            st.audio(audio_data, format="audio/mp3")
            st.download_button(
                label="⬇️ Download MP3",
                data=audio_data,
                file_name=filename,
                mime="audio/mpeg"
            )
            st.success("✅ Audio berhasil dibuat.")
        else:
            st.error(f"❌ Error {response.status_code}: {response.text}")
