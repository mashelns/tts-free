import streamlit as st
import requests

st.set_page_config(page_title="ElevenLabs TTS", layout="centered")
st.title("🗣️ ElevenLabs Text-to-Speech")

st.markdown("Masukkan API Key dan Voice ID dari akun ElevenLabs kamu.")

api_key = st.text_input("🔑 API Key", type="password")
voice_id = st.text_input("🧬 Voice ID")
text = st.text_area("📜 Masukkan Teks", height=200)

if st.button("🎤 Ubah ke Suara"):
    if not api_key or not voice_id or not text.strip():
        st.error("Harap lengkapi semua kolom.")
    else:
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "text": text,
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.75
            }
        }

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            st.audio(response.content, format="audio/mp3")
            st.success("✅ Sukses! Audio dihasilkan.")
        else:
            st.error(f"❌ Gagal: {response.status_code}\n{response.text}")
