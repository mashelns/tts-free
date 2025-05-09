import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv

# Load API key dari .env
load_dotenv()

# =================== PAGE CONFIG ====================
st.set_page_config(page_title="🗣️ ElevenLabs Multilingual TTS", layout="centered")
st.markdown("""
    <h1 style='text-align: center; color: #1f77b4;'>🎙️ ElevenLabs TTS Multibahasa</h1>
    <p style='text-align: center; font-size: 16px;'>Masukkan teks dalam bahasa apa pun & hasilkan suara AI 🎧</p>
""", unsafe_allow_html=True)
st.markdown("---")

# =================== API KEY ====================
stored_api_key = os.getenv("ELEVEN_API_KEY")
api_key = stored_api_key if stored_api_key else ""

if stored_api_key:
    st.success("✅ API Key sudah disimpan.")
    if st.button("❌ Hapus API Key"):
        with open(".env", "w") as f:
            f.write("")
        st.warning("API Key berhasil dihapus. Silakan refresh.")
        st.stop()
else:
    api_key = st.text_input("🔑 Masukkan API Key ElevenLabs kamu:", type="password")
    if st.button("💾 Simpan API Key"):
        if api_key:
            with open(".env", "w") as f:
                f.write(f"ELEVEN_API_KEY={api_key}")
            st.success("API Key berhasil disimpan! Silakan refresh halaman.")
            st.stop()
        else:
            st.warning("API Key tidak boleh kosong.")

st.markdown("---")

# =================== VOICE OPTIONS ====================
st.subheader("🎤 Pilih Suara")

multilang_voices = {
    "🌍 Dandan (Multilang)": "9F4C8ztpNUmXkdDDbz3J",
    "🧑‍💼 Alex (Multilang)": "yl2ZDV1MzN4HbQJbMihG",
    "🎧 Nick (Multilang)": "WrPknjKhmIXkCONEtG3j",
    "➕ Masukkan Voice ID Sendiri": "custom"
}

voice_label = st.selectbox("Pilih voice:", list(multilang_voices.keys()))
voice_id = ""

if multilang_voices[voice_label] == "custom":
    custom_voice = st.text_input("🛠️ Masukkan Custom Voice ID:")
    voice_id = custom_voice.strip()
else:
    voice_id = multilang_voices[voice_label]

# =================== TEXT INPUT ====================
text = st.text_area("📝 Masukkan Teks:", height=200, placeholder="Tulis teks dalam bahasa apa pun...")

st.markdown("---")

# =================== BUTTON & REQUEST ====================
if st.button("🚀 Konversi ke Suara", use_container_width=True):
    if not api_key or not text.strip() or not voice_id:
        st.error("❗ Lengkapi API Key, teks, dan Voice ID.")
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

        with st.spinner("🎛️ Menghasilkan audio..."):
            response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            audio_data = response.content
            filename = f"TTSBOIMKA_{int(time.time())}.mp3"

            st.audio(audio_data, format="audio/mp3")
            st.download_button(
                label="⬇️ Download Hasil Suara (.mp3)",
                data=audio_data,
                file_name=filename,
                mime="audio/mpeg",
                use_container_width=True
            )
            st.success("✅ Audio berhasil dibuat!")
        else:
            st.error(f"❌ Gagal: {response.status_code}\n{response.text}")

st.markdown("---")
st.info("ℹ️ Tips: Kamu bisa ambil Voice ID dari dashboard ElevenLabs.")
