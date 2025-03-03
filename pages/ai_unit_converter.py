import streamlit as st
import os
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import pygame
import tempfile
import threading
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

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)  

        with st.status("🎤 Listening... Speak now!", expanded=True) as status:
            try:
                audio = recognizer.listen(source, timeout=15, phrase_time_limit=20)  
                
                status.update(label="🎙️ Processing... Please wait", state="running")  
                text = recognizer.recognize_google(audio)  
                
                status.update(label="Speech Recognized!", state="complete")
                return text
            
            except sr.UnknownValueError:
                status.update(label="Could not understand. Try again!", state="error")
                return None
            
            except sr.RequestError:
                status.update(label="API request error! Check internet.", state="error")
                return None

def speak_text(text):
    try:
        tts = gTTS(text=text, lang="en")
        temp_audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        tts.save(temp_audio_path)

        pygame.mixer.init()
        pygame.mixer.music.load(temp_audio_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            continue

    except Exception as e:
        st.error(f"Voice Output Error: {e}")


st.sidebar.subheader("🔊 Voice Settings")
enable_voice = st.sidebar.checkbox("Enable Voice Output")


st.session_state["user_input"] = st.text_input("🔢 Enter conversion (e.g., '2 km to miles'):", value=st.session_state["user_input"])

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    convert_btn = st.button("🚀 Convert", use_container_width=True)
with col2:
    voice_btn = st.button("🎤Voice Input", use_container_width=True)
with col3:
    clear_btn = st.button("🗑️ Clear", use_container_width=True)

if voice_btn:
    voice_text = recognize_speech()
    if voice_text:
        st.session_state["user_input"] = voice_text
        st.rerun()

if convert_btn:
    if not st.session_state["user_input"]:
        st.warning("Please enter or speak a valid conversion query.")
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

if clear_btn:
    st.session_state["user_input"] = "" 
    

    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
    
    st.rerun()
