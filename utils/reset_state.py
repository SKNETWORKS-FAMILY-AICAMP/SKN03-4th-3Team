import streamlit as st

def reset_state():
    for key in ["question", "recommended_question", "answer_result", "show_answer"]:
        if key not in st.session_state:
            st.session_state[key] = "" if key != "show_answer" else False
