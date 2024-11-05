import os 
from dotenv import load_dotenv
# .env 파일에 등록된 변수(데이터)를 os 환경변수에 적용
load_dotenv()

from langchain_my.constant import CHATBOT_MESSAGE, CHATBOT_ROLE
from langchain_my.prompt import create_message

from langchain_my.chain import create_chain_lambda


# web ui/ux
import streamlit as st
# def app():
#     st.title("lambda 형 쳇봇")
#     # st.write("원하는 주식 회사 입력.")
#     # if st.button("parallel 형 쳇봇 페이지로 이동"):
#     #     st.session_state["page"] = "parallel_chatbot"
#     #     st.rerun()
#     # if st.button("agent 형 쳇봇 페이지로 이동"):
#     #     st.session_state["page"] = "agent_chatbot"
#     #     st.rerun()
#     # if st.button("홈으로 돌아가기"):
#     #     st.session_state["page"] = "home"
#     #     st.rerun()
def app():
    st.title("lambda 형 쳇봇")

    # 메세지를 저장 
    # messages = {"role":"", "content":""}
    #   role -> user(사용자) / assistant(AI)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 저장한 메세지를 화면에 표현 
    for message in st.session_state.messages:
        if message[CHATBOT_MESSAGE.role.name] in CHATBOT_ROLE.__members__:
            with st.chat_message(message[CHATBOT_MESSAGE.role.name]):
                st.markdown(message[CHATBOT_MESSAGE.content.name])


    # 사용자 입력
    prompt = st.chat_input("입력해주세요")
    # 사용자 입력이 있다면,
    if prompt:
        if not prompt.isdigit():
            with st.chat_message(CHATBOT_ROLE.user.name): # 사용자 입력 표현
                st.write(prompt)
            with st.chat_message(CHATBOT_ROLE.assistant.name): # 챗봇 답변 표현
                st.write("숫자만 다시입력해주세요")
        else:
            message = create_message(role=CHATBOT_ROLE.user, prompt=prompt)
            # # 전역 chain 초기화
            # if "chain" not in st.session_state:
            #     st.session_state.chain = create_chain(prompt) 
            # 입력값이 존재한다며, 
            if message:
                # 화면에 표현
                with st.chat_message(CHATBOT_ROLE.user.name):
                    st.write(prompt)
                
                # 이력 추가 
                # 내용  ::  message = {"role":"", "content":""}
                st.session_state.messages.append(message)

                # # 챗봇 답변 
                with st.chat_message(CHATBOT_ROLE.assistant.name):
                    assistant_response = st.write_stream(create_chain_lambda(prompt, message_history = st.session_state.messages))
                # st.markdown(assistant_response)
                #     # assistant_response = response_from_llm(prompt)
                #     # st.markdown(assistant_response)
            #     assistant_response = st.write_stream(response_from_llm(prompt=prompt, message_history=st.session_state.messages))

                    # 이력 추가 
                    st.session_state.messages.append(
                        create_message(role=CHATBOT_ROLE.assistant, prompt=assistant_response))