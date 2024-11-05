# import streamlit as st
# import time

# def display_typing_effect(text, delay=0.05):
#     # 빈 컨테이너 생성
#     output = st.empty()
#     typed_text = ""
#     for char in text:
#         typed_text += char
#         output.markdown(f"{typed_text}")  # 매 문자마다 컨테이너 업데이트
#         time.sleep(delay)


import streamlit as st
import time

def display_typing_effect(text, delay=0.05):
    output = st.empty()
    typed_text = ""
    for char in text:
        typed_text += char
        output.markdown(f"{typed_text}")
        time.sleep(delay)
