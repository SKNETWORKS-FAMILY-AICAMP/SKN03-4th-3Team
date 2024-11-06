import streamlit as st
import time

<<<<<<< HEAD
def display_typing_effect(text, delay=0.05):
=======
def display_typing_effect(text, delay=0.03):
>>>>>>> d43ed311a022636ec41ad44fb510511dd2a9ffed
    output = st.empty()
    typed_text = ""
    for char in text:
        typed_text += char
        output.markdown(f"{typed_text}")
        time.sleep(delay)
