import streamlit as st
import time

def display_typing_effect(text, delay=0.05):
    output = st.empty()
    typed_text = ""
    for char in text:
        typed_text += char
        output.markdown(f"{typed_text}")
        time.sleep(delay)
