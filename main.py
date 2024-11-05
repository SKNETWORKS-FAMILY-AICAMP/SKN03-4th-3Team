import streamlit as st

# 페이지 설정: 이 코드는 가장 먼저 위치해야 함
st.set_page_config(
    page_title="무면허라이더를 위한 챗봇",
    page_icon="🚦",  # 페이지 아이콘 설정
    layout="wide"    # 레이아웃 설정
)


# 사이드바에 제목 추가
st.sidebar.title("페이지 선택")

# 페이지 제목 설정
st.title("무면허라이더를 위한 챗봇")
st.write("여기에서 무면허 라이더를 위한 질문과 답변을 제공합니다.")

# 사용자 입력
user_input = st.text_input("질문을 입력하세요:", "")

# 기본 응답 생성
if user_input:
    # 간단한 조건문으로 응답 생성 (나중에 API 호출로 변경 가능)
    if "라이더" in user_input:
        response = "무면허 라이더에 대한 정보를 원하시면, 필요한 내용을 말씀해 주세요!"
    elif "안전" in user_input:
        response = "안전을 위해 헬멧을 꼭 착용하세요!"
    else:
        response = "죄송합니다, 이해하지 못했습니다. 다른 질문을 해 주세요."
    
    st.write("챗봇의 답변:", response)
