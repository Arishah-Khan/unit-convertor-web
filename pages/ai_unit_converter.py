import streamlit as st
import os
import google.generativeai as genai
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

st.set_page_config(page_title="AI-Powered Smart Unit Converter", page_icon="🔢", layout="centered")

if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

st.title("🔢 AI-Powered Smart Unit Converter")
st.write("Convert units with AI-powered text input!")

st.session_state["user_input"] = st.text_input("Enter conversion (e.g., '2 km to miles'):", value=st.session_state["user_input"])

col1, col2 = st.columns([2, 1])
with col1:
    convert_btn = st.button("🚀 Convert", use_container_width=True)
with col2:
    clear_btn = st.button("🗑️ Clear", use_container_width=True)

if convert_btn:
    if not st.session_state["user_input"]:
        st.warning("Please enter a valid conversion query.")
    else:
        try:
            response = model.generate_content(
                f"Convert {st.session_state['user_input']} and give a short 2-line explanation."
            )
            result = response.text.strip() if response else "Conversion failed!"
            st.success(f"Result:\n{result}")
        except Exception as e:
            st.error(f"Error: {e}")

if clear_btn:
    st.session_state["user_input"] = ""
    st.rerun()
