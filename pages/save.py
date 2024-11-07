import streamlit as st

# 페이지 설정
st.set_page_config(page_title="메모장", layout="wide")
st.title("🚗 틀린 문제 저장 페이지")

# 이전 대화 기록을 세션 상태에서 가져오기
if "messages" in st.session_state and st.session_state.messages:
    saved_messages = st.session_state.messages
else:
    st.warning("저장된 대화 기록이 없습니다.")
    saved_messages = []

# 틀린 문제를 저장할 수 있는 리스트 초기화
if "incorrect_questions" not in st.session_state:
    st.session_state.incorrect_questions = []

# 대화 내용을 문제별로 표시
if saved_messages:
    st.subheader("💬 대화 내용")
    num_messages = len(saved_messages)
    message_pairs = []
    i = 0
    while i < num_messages:
        # 사용자 메시지 (질문)
        if saved_messages[i]['role'] == 'user':
            question = saved_messages[i]
            i += 1
            # AI 메시지 (답변)
            if i < num_messages and saved_messages[i]['role'] == 'assistant':
                answer = saved_messages[i]
                i += 1
            else:
                answer = None

            message_pairs.append((question, answer))
        else:
            i += 1
            continue

    for idx, (question, answer) in enumerate(message_pairs):
        # 문제 표시
        with st.expander(f"❓ 질문 {idx+1}: {question['content'][:30]}...", expanded=False):
            st.markdown(f"**사용자 질문:**")
            st.write(f"{question['content']}")
            if answer:
                st.markdown(f"**🤖 AI 답변:**")
                st.write(f"{answer['content']}")
            else:
                st.write("**AI 답변이 없습니다.**")
            
            # 버튼을 두 개의 열로 배치
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("💾 메모장에 저장", key=f"save_{idx}"):
                    # 이미 저장된 문제인지 확인
                    if {'question': question, 'answer': answer} not in st.session_state.incorrect_questions:
                        st.session_state.incorrect_questions.append({'question': question, 'answer': answer})
                        st.success("문제가 메모장에 저장되었습니다.")
                    else:
                        st.info("이 문제는 이미 메모장에 저장되어 있습니다.")
            with col2:
                pass  # 공간 확보를 위해 빈 열 사용
else:
    st.info("대화 내용이 없습니다.")

st.markdown("---")

# 틀린 문제 목록 표시
if st.session_state.incorrect_questions:
    st.subheader("📋 메모장")
    for idx, qa in enumerate(st.session_state.incorrect_questions, start=1):
        with st.expander(f"📝 문제 {idx}: {qa['question']['content'][:30]}...", expanded=False):
            st.markdown(f"**사용자 질문:**")
            st.write(f"{qa['question']['content']}")
            if qa['answer']:
                st.markdown(f"**🤖 AI 답변:**")
                st.write(f"{qa['answer']['content']}")
            else:
                st.write("**AI 답변이 없습니다.**")
            
            # 삭제 버튼을 우측에 배치
            col1, col2 = st.columns([5, 1])
            with col1:
                pass  # 공간 확보를 위해 빈 열 사용
            with col2:
                if st.button("🗑️ 삭제", key=f"delete_{idx}"):
                    st.session_state.incorrect_questions.pop(idx - 1)
                    st.success("문제가 메모장에서 삭제되었습니다.")
                    st.experimental_rerun()
else:
    st.info("아직 메모장에 저장된 문제가 없습니다.")


