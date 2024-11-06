# import streamlit as st
# from pages import lambda_chatbot, parallel_chatbot, agent_chatbot

# # 세션 상태 초기화
# print(st.session_state)
# if "page" not in st.session_state:
#     st.session_state["page"] = "home"

# # 페이지에 따라 다른 파일의 app 함수 호출
# if st.session_state["page"] == "lambda_chatbot":
#     lambda_chatbot.app()
# elif st.session_state["page"] == "parallel_chatbot":
#     parallel_chatbot.app()
# elif st.session_state["page"] == "agent_chatbot":
#     agent_chatbot.app()

import streamlit as st
from pages import lambda_chatbot, parallel_chatbot, agent_chatbot, home, llm_chatbot


# 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state["page"] = "llm_chatbot"
print(st.session_state)
# 사이드바에 페이지 선택 옵션 추가
page = st.sidebar.selectbox(
    "페이지를 선택하세요", 
    ["llm_chatbot", "lambda_chatbot", "parallel_chatbot", "agent_chatbot"] # ,"home" ]
)
# 세션 상태 초기화 및 업데이트
if "page" not in st.session_state or st.session_state["page"] != page:
    st.session_state["page"] = page
    # 페이지 변경 시 즉시 리로드
    
    st.rerun()
    
# 페이지에 따라 다른 파일의 app 함수 호출
# if st.session_state["page"] == "home":
#     # 홈 페이지 내용
#     home.app()
    # 무난한 LLM 챗봇
# elif st.session_state["page"] == "llm_chatbot":
if st.session_state["page"] == "llm_chatbot":
    llm_chatbot.app()
elif st.session_state["page"] == "lambda_chatbot":
    lambda_chatbot.app()
elif st.session_state["page"] == "parallel_chatbot":
    parallel_chatbot.app()
elif st.session_state["page"] == "agent_chatbot":
    agent_chatbot.app()



# # 선택된 페이지로 상태 업데이트
# st.session_state["page"] = page