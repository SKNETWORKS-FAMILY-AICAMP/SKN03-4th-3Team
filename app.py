<<<<<<< HEAD
import openai
import streamlit as st
import time
=======
# import openai
# import streamlit as st
# import time
# from chains.recommend_chain import RecommendQuestionChain
# from chains.answer_check_chain import AnswerCheckChain
# from utils.find_similar_question import find_similar_question
# from utils.typing_effect import display_typing_effect

# # 체인 초기화
# recommend_chain = RecommendQuestionChain(find_similar_fn=find_similar_question)
# answer_check_chain = AnswerCheckChain(llm=openai.ChatCompletion, recommend_chain=recommend_chain)

# st.title("운전면허 필기 시험 챗봇")

# st.session_state["question"] = st.text_input("운전면허와 관련된 질문을 입력하세요:", key="question_input")

# if st.session_state["question"]:
#     st.session_state["recommended_question"] = recommend_chain(st.session_state["question"])


#     st.write("### 추천 문제:")
#     st.write(st.session_state["recommended_question"].replace("\n", "\n\n"))

#     user_answer = st.text_input("답을 입력하세요:", key="answer_input")

#     if user_answer:
#         st.session_state["answer_result"] = answer_check_chain(user_answer)
#         st.session_state["show_answer"] = True

# # 결과 출력
# if st.session_state["show_answer"]:
#     st.write("### 결과:")

#     # 타이핑 효과 적용
#     result_sentences = st.session_state["answer_result"].split(". ")
#     for sentence in result_sentences:
#         display_typing_effect(sentence + ".\n\n")


import openai
import streamlit as st
>>>>>>> aff5c57e11eff4b796a0c26cb34a755135eca838
from chains.recommend_chain import RecommendQuestionChain
from chains.answer_check_chain import AnswerCheckChain
from utils.find_similar_question import find_similar_question
from utils.typing_effect import display_typing_effect
<<<<<<< HEAD

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
=======
from utils.reset_state import reset_state
from utils.constant import CHATBOT_ROLE, CHATBOT_MESSAGE
from utils.prompt import create_message
import re

# 체인 초기화   
recommend_chain = RecommendQuestionChain(find_similar_fn=find_similar_question)
answer_check_chain = AnswerCheckChain(llm=openai.ChatCompletion, recommend_chain=recommend_chain)

# UI 설정
st.set_page_config(page_title="운전면허 필기 시험 챗봇", layout="centered")
st.title("🚗 운전면허 필기 시험 챗봇")

# 상태 초기화
reset_state()

# 대화 상태 저장
if "messages" not in st.session_state:
    st.session_state.messages = []
if "awaiting_answer" not in st.session_state:
    st.session_state.awaiting_answer = False

# 이전 대화 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message[CHATBOT_MESSAGE.role.name]):
        st.markdown(message[CHATBOT_MESSAGE.content.name])

# 입력창 (단일 입력창)
user_input = st.chat_input("질문을 입력하거나 답을 입력하세요")

# 사용자 입력 처리
if user_input:
    if not st.session_state.awaiting_answer:
        # 질문 입력 처리
        user_message = create_message(role=CHATBOT_ROLE.user, prompt=user_input)
        st.session_state.messages.append(user_message)

        # 화면에 사용자 질문 출력
        with st.chat_message(CHATBOT_ROLE.user.name):
            st.write(user_input)

        # 추천 문제 생성
        st.session_state["recommended_question"] = recommend_chain(user_input)
        assistant_message_content = st.session_state["recommended_question"]
        
        # 줄바꿈 처리된 추천 문제 생성
        assistant_message_content = re.sub(r'\n', '\n\n', st.session_state["recommended_question"])
        
        # 추천된 문제 정보를 상태에 저장
        st.session_state["current_question"] = recommend_chain.current_question
        st.session_state["current_answer"] = recommend_chain.current_answer
        st.session_state["current_explanation"] = recommend_chain.current_explanation

        # 추천 문제 메시지 추가 및 출력
        assistant_message = create_message(role=CHATBOT_ROLE.assistant, prompt=assistant_message_content)
        st.session_state.messages.append(assistant_message)

        with st.chat_message(CHATBOT_ROLE.assistant.name):
            st.markdown(assistant_message_content)

        # 답변 대기 상태로 전환
        st.session_state.awaiting_answer = True

    else:
        # 답변 입력 처리
        user_answer_message = create_message(role=CHATBOT_ROLE.user, prompt=user_input)
        st.session_state.messages.append(user_answer_message)

        # 화면에 사용자 답변 출력
        with st.chat_message(CHATBOT_ROLE.user.name):
            st.write(user_input)

        # 답변 검토 및 결과 생성
        answer_result = answer_check_chain(user_input)
        
        # 줄바꿈 처리된 결과 메시지 생성
        formatted_answer_result = "\n".join([sentence.strip() for sentence in answer_result.split(". ") if sentence])

        assistant_result_message = create_message(role=CHATBOT_ROLE.assistant, prompt=formatted_answer_result)
        st.session_state.messages.append(assistant_result_message)

        # 결과 메시지 화면 출력
        with st.chat_message(CHATBOT_ROLE.assistant.name):
            display_typing_effect(formatted_answer_result)

        # 상태 초기화하여 새로운 질문을 받을 수 있도록 함
        st.session_state.awaiting_answer = False
>>>>>>> aff5c57e11eff4b796a0c26cb34a755135eca838
