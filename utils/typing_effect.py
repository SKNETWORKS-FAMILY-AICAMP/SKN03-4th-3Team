<<<<<<< HEAD
=======
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


>>>>>>> aff5c57e11eff4b796a0c26cb34a755135eca838
import streamlit as st
import time

def display_typing_effect(text, delay=0.05):
<<<<<<< HEAD
    # 빈 컨테이너 생성
=======
>>>>>>> aff5c57e11eff4b796a0c26cb34a755135eca838
    output = st.empty()
    typed_text = ""
    for char in text:
        typed_text += char
<<<<<<< HEAD
        output.markdown(f"{typed_text}")  # 매 문자마다 컨테이너 업데이트
=======
        output.markdown(f"{typed_text}")
>>>>>>> aff5c57e11eff4b796a0c26cb34a755135eca838
        time.sleep(delay)
