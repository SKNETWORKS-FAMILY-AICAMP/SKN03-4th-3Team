import os 
from dotenv import load_dotenv
load_dotenv()

import streamlit as st

st.set_page_config(page_title="유명인 소개 챗봇", page_icon="🤖")

st.title("유명인 소개 챗봇")

# 사이드바를 사용한 페이지 선택
page = st.sidebar.selectbox('페이지 선택', ['챗봇', 'agent'])

if page == '챗봇':
    from langchain_chatbot import chatbot
    chatbot()
elif page == 'agent':
    from pages.agent_chatbot import agent
    agent()

