import streamlit as st
from deep_translator import GoogleTranslator
import edge_tts
import asyncio
import io

# 1. Page Configuration
st.set_page_config(page_title="BhashaVriksh", layout="centered")

# 2. Custom CSS
st.markdown("""
    <style>
    .stApp { background-color: #AAFFC7; }
    .main-title {
        color: #215B63;
        font-family: 'Georgia', serif;
        font-weight: bold;
        text-align: center;
        font-size: 50px;
        margin-bottom: 0px;
    }
    .output-font {
        font-size: 28px !important;
        color: #1a3306 !important;
        font-weight: bold !important;
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #215B63;
        line-height: 1.6;
        max-width: 100%;
    }
    div.stButton > button:first-child {
        background-color: #215B63;
        color: white;
        border-radius: 20px;
        border: 2px solid #080616;
        font-weight: bold;
        height: 3em;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #3e662e;
        color: #fdf5e6;
    }
    .stTextArea textarea {
        background-color: #ffffff;
        border-radius: 10px;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown("<h1 class='main-title'>BhashaVriksh</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#215B63;'>भाषा से ज्ञान, ज्ञान से संस्कार</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. Language Map with Male Voices (Edge TTS)
indian_languages = {
    "Hindi": {"code": "hi", "voice": "hi-IN-MadhurNeural"},
    "English": {"code": "en", "voice": "en-IN-PrabhatNeural"},
    "Sanskrit": {"code": "sa", "voice": "hi-IN-MadhurNeural"}, # Using Hindi male for Sanskrit
    "Bengali": {"code": "bn", "voice": "bn-IN-BashkarNeural"},
    "Gujarati": {"code": "gu", "voice": "gu-IN-NiranjanNeural"},
    "Marathi": {"code": "mr", "voice": "mr-IN-ManoharNeural"},
    "Tamil": {"code": "ta", "voice": "ta-IN-ValluvarNeural"},
    "Telugu": {"code": "te", "voice": "te-IN-MohanNeural"}
}

# 5. Helper function for Audio
async def get_audio_payload(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

# 6. Layout
col1, col2 = st.columns(2)
with col1:
    st.markdown("### **Input**")
    source_text = st.text_area("", placeholder="Type here...", height=150, key="input")

with col2:
    st.markdown("### **Settings**")
    target_lang_name = st.selectbox("Choose Language", list(indian_languages.keys()))
    target_info = indian_languages[target_lang_name]
    st.write("") 
    translate_button = st.button("अनुवाद करें (Translate) →")

# 7. Logic
if translate_button:
    if not source_text.strip():
        st.warning("Please enter some text first!")
    else:
        with st.spinner('Translating & Generating Male Voice...'):
            try:
                # Translation
                translated = GoogleTranslator(source='auto', target=target_info["code"]).translate(source_text)
                final_output = translated.strip()
                
                st.markdown("---")
                st.write(f"**Translated Output ({target_lang_name}):**")
                
                # Big Font Output
                st.markdown(f'<div class="output-font">{final_output}</div>', unsafe_allow_html=True)
                
                # Male Audio Generation
                audio_bytes = asyncio.run(get_audio_payload(final_output, target_info["voice"]))
                st.audio(audio_bytes, format='audio/mp3')
                
            except Exception as e:
                st.error(f"Error: {e}")

# 8. Footer
st.markdown("---")
st.caption("By Achal Banabakode, Dhirubhai Ambani University (DAU)")
st.markdown("<center><p style='color:#215B63;'>🍃 Connecting the Roots of Indian Language to the Global Future🍃</p></center>", unsafe_allow_html=True)