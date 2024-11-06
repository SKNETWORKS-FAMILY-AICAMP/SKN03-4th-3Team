import streamlit as st
import os 
from dotenv import load_dotenv
# .env 파일에 등록된 변수(데이터)를 os 환경변수에 적용
load_dotenv()

from langchain_my.constant import CHATBOT_MESSAGE, CHATBOT_ROLE
from langchain_my.prompt import create_message
from langchain_my.chain import create_chain_agent
from langchain.memory import ConversationBufferMemory

def app():
    st.title("Agent Chat Bot")

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
            if "memory" not in st.session_state:
                st.session_state.memory = ConversationBufferMemory(memory_key="chat_history")
            # # 챗봇 답변 
            with st.chat_message(CHATBOT_ROLE.assistant.name):
                
                assistant_response = st.write(create_chain_agent(prompt, message_history = st.session_state.messages))
                print("작동하는건가?")
                st.markdown(assistant_response)
                memory = st.session_state.memory 
                # assistant_response = st.session_state.chain(prompt)
            # st.markdown(assistant_response)
            #     # assistant_response = response_from_llm(prompt)
            #     # st.markdown(assistant_response)
        #     assistant_response = st.write_stream(response_from_llm(prompt=prompt, message_history=st.session_state.messages))

                # 이력 추가 
                st.session_state.messages.append(
                    create_message(role=CHATBOT_ROLE.assistant, prompt=assistant_response))
