import streamlit as st
from dotenv import load_dotenv
from chains.langchain_my.constant import CHATBOT_MESSAGE, CHATBOT_ROLE
from chains.langchain_my.prompt import create_message
from chains.langchain_my.chain import create_chain_agent

# 로딩
load_dotenv()

def init_page_state():
    if "agent_chatbot" not in st.session_state:
        st.session_state.page2_initialized = True
        st.session_state.page2_messages = []

def app():
    st.title("Agent Chat Bot")
    init_page_state()

    for message in st.session_state.page2_messages:
        with st.chat_message(message[CHATBOT_MESSAGE.role.name]):
            st.markdown(message[CHATBOT_MESSAGE.content.name])

    prompt = st.chat_input("입력해주세요")
    if prompt:
        message = create_message(role=CHATBOT_ROLE.user, prompt=prompt)
        if message:
            with st.chat_message(CHATBOT_ROLE.user.name):
                st.write(prompt)
            
            st.session_state.page2_messages.append(
                create_message(role=CHATBOT_ROLE.user, prompt=prompt)
            )

            with st.chat_message(CHATBOT_ROLE.assistant.name):
                assistant_response = create_chain_agent(prompt, message_history=st.session_state.page2_messages)
                st.write(assistant_response)

                st.session_state.page2_messages.append(
                    create_message(role=CHATBOT_ROLE.assistant, prompt=assistant_response))

if __name__ == "__main__":
    app()