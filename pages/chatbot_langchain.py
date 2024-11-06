# app.py

import streamlit as st
from utils.rag_process import initialize_data, get_random_similar_question, answer_check_chain, extract_question

# 데이터 초기화
db = initialize_data()

st.title("운전면허 문제 챗봇")

# 세션 상태 초기화
if 'stage' not in st.session_state:
    st.session_state.stage = 'query'
if 'current_question' not in st.session_state:
    st.session_state.current_question = None

# 사용자 입력 처리
if st.session_state.stage == 'query':
    user_input = st.text_input("어떤 주제의 문제를 풀고 싶으신가요?")
    if user_input:
        similar_doc = get_random_similar_question(user_input, db)
        if similar_doc:
            question_data = extract_question(similar_doc)
            st.session_state.current_question = question_data
            st.session_state.stage = 'answer'
            st.rerun()
        else:
            st.write("해당 주제에 맞는 문제를 찾을 수 없습니다.")

elif st.session_state.stage == 'answer':
    # 문제 표시 부분 수정
    question_text = st.session_state.current_question['문제']
    question_parts = question_text.split('①')
    
    if len(question_parts) > 1:
        main_question = question_parts[0].strip()
        options = '①' + question_parts[1]
        
        # 보기를 줄바꿈으로 분리
        options = options.replace(' ①', '\n①')
        options = options.replace(' ②', '\n②')
        options = options.replace(' ③', '\n③')
        options = options.replace(' ④', '\n④')
        
        st.write(f"문제: {main_question}\n\n{options}")
    else:
        st.write(f"문제: {question_text}")

    user_answer = st.text_input("답변을 입력해주세요:")
    if user_answer:
        result = answer_check_chain(
            user_answer,
            st.session_state.current_question['문제'],
            st.session_state.current_question['정답'],
            st.session_state.current_question['해설']
        )
        st.write(result)
        if st.button("다른 문제 풀기"):
            st.session_state.stage = 'query'
            st.session_state.current_question = None
            st.rerun()