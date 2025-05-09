import streamlit as st
import requests
import time

st.set_page_config(page_title="ElevenLabs Multilingual TTS", layout="centered")
st.title("🗣️ ElevenLabs Multilingual TTS")
st.caption("Kalau yang mau custom voice ID, tinggal bilang 😄")

# Load API key
api_key = st.secrets["api_key"] if "api_key" in st.secrets else ""

# Fallback input
if not api_key:
    api_key = st.text_input("🔑 Masukkan API Key kamu", type="default")

# Multilingual voices
multilang_voices = {
    "Dandan (Multilang)": "9F4C8ztpNUmXkdDDbz3J",
    "Alex (Multilang)": "yl2ZDV1MzN4HbQJbMihG",
    "Nick (Multilang)": "WrPknjKhmIXkCONEtG3j",
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
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.6,
                "similarity_boost": 0.75
            }
        }

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        with st.spinner("🔄 Menghasilkan audio..."):
            response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            audio_data = response.content
            filename = f"TTSBOIMKA_{int(time.time())}.mp3"

            st.audio(audio_data, format="audio/mp3")
            st.download_button(
                label="⬇️ Download Audio",
                data=audio_data,
                file_name=filename,
                mime="audio/mpeg"
            )
            st.success("✅ Audio berhasil dibuat dan siap diunduh.")
        else:
            st.error(f"❌ Gagal: {response.status_code}\n{response.text}")
