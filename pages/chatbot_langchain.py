import streamlit as st
from dotenv import load_dotenv
from chains.langchain_my.constant import CHATBOT_MESSAGE, CHATBOT_ROLE
from chains.langchain_my.prompt import create_message
from chains.wc_chain import create_agent, run_agent, initialize_data

load_dotenv()




def app():
    st.title("운전면허 문제 챗봇")

    if "messages" not in st.session_state:
        st.session_state.messages = [] 
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "db" not in st.session_state:
        st.session_state.db = initialize_data()
    if "agent" not in st.session_state:
        st.session_state.agent = create_agent()

    for message in st.session_state.messages:
        with st.chat_message(message[CHATBOT_MESSAGE.role.name]):
            st.markdown(message[CHATBOT_MESSAGE.content.name])

    prompt = st.chat_input("입력해주세요")
    if prompt:
        message = create_message(role=CHATBOT_ROLE.user, prompt=prompt)
        if message:
            with st.chat_message(CHATBOT_ROLE.user.name):
                st.write(prompt)
            
            st.session_state.messages.append(message)

            with st.chat_message(CHATBOT_ROLE.assistant.name):
                assistant_response = run_agent(prompt)
                st.write(assistant_response)
                
                st.session_state.messages.append(
                    create_message(role=CHATBOT_ROLE.assistant, prompt=assistant_response))

app()