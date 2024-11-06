import streamlit as st

# 페이지 설정
st.set_page_config(page_title="틀린 문제 저장", layout="centered")
st.title("🚗 틀린 문제 저장 페이지")

# 이전 대화 기록을 세션 상태에서 가져오기
if "messages" in st.session_state:
    saved_messages = st.session_state.messages
else:
    st.warning("저장된 대화 기록이 없습니다.")
    saved_messages = []

# 틀린 문제를 저장할 수 있는 리스트 초기화
if "incorrect_questions" not in st.session_state:
    st.session_state.incorrect_questions = []

# 이전 대화 내용 표시
for message in saved_messages:
    role = message.get("role")
    content = message.get("content")
    
    if role == "assistant":
        st.markdown(f"**AI:** {content}")
    elif role == "user":
        st.markdown(f"**사용자 질문/답변:** {content}")

# 틀린 문제 전체를 저장하는 버튼
if st.button("이 대화 내용을 틀린 문제로 통째로 저장"):
    # 저장 버튼을 누를 때, 전체 대화 내용을 틀린 문제로 저장
    st.session_state.incorrect_questions.append(saved_messages)
    st.success("대화 내용이 틀린 문제로 저장되었습니다.")

# 틀린 문제 목록 표시
if st.session_state.incorrect_questions:
    st.subheader("📋 틀린 문제 목록")
    for i, question_set in enumerate(st.session_state.incorrect_questions, start=1):
        st.markdown(f"### 문제 {i}")
        for question in question_set:
            role = question.get("role")
            content = question.get("content")
            
            if role == "assistant":
                st.markdown(f"**AI:** {content}")
            elif role == "user":
                st.markdown(f"**사용자 질문/답변:** {content}")
        
        st.markdown("---")  # 구분선을 추가하여 문제 구분
else:
    st.info("아직 틀린 문제가 저장되지 않았습니다.")

