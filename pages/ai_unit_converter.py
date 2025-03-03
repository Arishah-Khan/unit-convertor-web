import streamlit as st
import os
import google.generativeai as genai
import speech_recognition as sr
import soundfile as sf
import tempfile
import threading
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("API Key not found! Please check your .env file.")
    st.stop()

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-pro")
except Exception as e:
    st.error(f"⚠️ API Configuration Error: {e}")
    st.stop()

st.set_page_config(page_title="AI-Powered Smart Unit Converter", page_icon="🎤", layout="centered")

if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

st.title("🎙️ AI-Powered Smart Unit Converter")
st.write("Convert units with AI-powered voice commands! 🎤")

# 🎤 Function to Recognize Speech from Uploaded Audio
def recognize_speech_from_file(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio."
        except sr.RequestError:
            return "API request error. Check internet."

# 🔊 Function to Convert Text to Speech & Play
def speak_text(text):
    try:
        tts = gTTS(text=text, lang="en")
        temp_audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        tts.save(temp_audio_path)

        # Play audio in Streamlit
        with open(temp_audio_path, "rb") as f:
            st.audio(f.read(), format="audio/mp3")

    except Exception as e:
        st.error(f"Voice Output Error: {e}")

st.sidebar.subheader("🔊 Voice Settings")
enable_voice = st.sidebar.checkbox("Enable Voice Output")

# 🎤 Audio File Upload Option
uploaded_audio = st.file_uploader("🎙️ Upload your voice command (WAV format)", type=["wav"])

# 🔢 Text Input Box
st.session_state["user_input"] = st.text_input("🔢 Enter conversion (e.g., '2 km to miles'):", value=st.session_state["user_input"])

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    convert_btn = st.button("🚀 Convert", use_container_width=True)
with col2:
    process_audio_btn = st.button("🎤 Process Audio", use_container_width=True)
with col3:
    clear_btn = st.button("🗑️ Clear", use_container_width=True)

# 🎤 Process Uploaded Audio
if process_audio_btn and uploaded_audio:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(uploaded_audio.read())
        temp_audio_path = temp_audio.name

    voice_text = recognize_speech_from_file(temp_audio_path)
    st.session_state["user_input"] = voice_text
    st.success(f"Recognized Speech: **{voice_text}**")
    st.rerun()

# 🚀 Convert Query
if convert_btn:
    if not st.session_state["user_input"]:
        st.warning("Please enter or upload a valid conversion query.")
    else:
        try:
            response = model.generate_content(
                f"Convert {st.session_state['user_input']} and give a short 2-line explanation."
            )
            result = response.text.strip() if response else "Conversion failed!"
            st.success(f" Result:\n{result}")

            if enable_voice:
                threading.Thread(target=speak_text, args=(result,), daemon=True).start()

        except Exception as e:
            st.error(f"Error: {e}")

# 🗑️ Clear Input
if clear_btn:
    st.session_state["user_input"] = ""
    st.rerun()
