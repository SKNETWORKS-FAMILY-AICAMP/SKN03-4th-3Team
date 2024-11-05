import openai
import streamlit as st
import time
from chains.recommend_chain import RecommendQuestionChain
from chains.answer_check_chain import AnswerCheckChain
from utils.find_similar_question import find_similar_question
from utils.typing_effect import display_typing_effect

# 체인 초기화
recommend_chain = RecommendQuestionChain(find_similar_fn=find_similar_question)
answer_check_chain = AnswerCheckChain(llm=openai.ChatCompletion, recommend_chain=recommend_chain)

st.title("운전면허 필기 시험 챗봇")

# 상태 초기화
if "question" not in st.session_state:
    st.session_state["question"] = ""
if "recommended_question" not in st.session_state:
    st.session_state["recommended_question"] = ""
if "answer_result" not in st.session_state:
    st.session_state["answer_result"] = ""
if "show_answer" not in st.session_state:
    st.session_state["show_answer"] = False


st.session_state["question"] = st.text_input("운전면허와 관련된 질문을 입력하세요:", key="question_input")

if st.session_state["question"]:
    st.session_state["recommended_question"] = recommend_chain(st.session_state["question"])


    st.write("### 추천 문제:")
    st.write(st.session_state["recommended_question"].replace("\n", "\n\n"))

    user_answer = st.text_input("답을 입력하세요:", key="answer_input")

    if user_answer:
        st.session_state["answer_result"] = answer_check_chain(user_answer)
        st.session_state["show_answer"] = True

# 결과 출력
if st.session_state["show_answer"]:
    st.write("### 결과:")

    # 타이핑 효과 적용
    result_sentences = st.session_state["answer_result"].split(". ")
    for sentence in result_sentences:
        display_typing_effect(sentence + ".\n\n")

    # 계속할지 묻는 버튼
    if st.button("계속하시겠습니까?"):
        # 상태 초기화
        st.session_state["question"] = ""
        st.session_state["recommended_question"] = ""
        st.session_state["answer_result"] = ""
        st.session_state["show_answer"] = False

# 종료 버튼
if st.button("종료"):
    st.write("종료합니다.")
