import streamlit as st
import requests
import time

# =================== PAGE CONFIG ====================
st.set_page_config(page_title="🗣️ ElevenLabs TTS Multibahasa", layout="centered")

# =================== HEADER ====================
st.markdown("""
    <h1 style='text-align: center; color: #1f77b4;'>🎙️ ElevenLabs TTS Multibahasa</h1>
    <p style='text-align: center; font-size: 16px;'>Ketik teks dalam bahasa apa pun dan unduh hasil suaranya!</p>
""", unsafe_allow_html=True)

st.markdown("---")

# =================== API KEY ====================
api_key = st.secrets["api_key"] if "api_key" in st.secrets else ""

if not api_key:
    api_key = st.text_input("🔑 Masukkan API Key ElevenLabs kamu:", type="password")

st.markdown("---")

# =================== VOICE OPTIONS ====================
multilang_voices = {
    "🌍 Dandan (Multilang)": "9F4C8ztpNUmXkdDDbz3J",
    "🧑‍💼 Alex (Multilang)": "yl2ZDV1MzN4HbQJbMihG",
    "🎧 Nick (Multilang)": "WrPknjKhmIXkCONEtG3j",
}

voice_label = st.selectbox("🎤 Pilih Suara", list(multilang_voices.keys()))
voice_id = multilang_voices[voice_label]

# =================== TEXT INPUT ====================
text = st.text_area("📝 Masukkan Teks:", height=200, placeholder="Tulis teks dalam bahasa apa pun...")

st.markdown("---")

# =================== BUTTON & REQUEST ====================
if st.button("🚀 Konversi ke Suara", use_container_width=True):
    if not api_key or not text.strip():
        st.error("❗ Mohon isi API Key dan teks terlebih dahulu.")
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

        with st.spinner("🎛️ Sedang memproses audio..."):
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
            st.success("✅ Sukses! Audio berhasil dibuat.")
        else:
            st.error(f"❌ Gagal: {response.status_code}\n{response.text}")

st.markdown("---")
st.info("🔧 Tips: Kamu bisa mendapatkan Voice ID sendiri dari dashboard ElevenLabs dan minta saya tambahkan.")
