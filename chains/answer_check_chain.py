import streamlit as st

class AnswerCheckChain:
    def __init__(self, llm, recommend_chain):
        self.llm = llm
        self.recommend_chain = recommend_chain

    def __call__(self, user_answer):
        # st.session_state에서 이전 추천된 값 불러오기
        current_question = st.session_state.get("current_question")
        current_answer = st.session_state.get("current_answer")
        current_explanation = st.session_state.get("current_explanation")

        # 값 확인
        # print("DEBUG: current_question =", current_question)
        # print("DEBUG: current_answer =", current_answer)
        # print("DEBUG: current_explanation =", current_explanation)
        # print("DEBUG: user_answer =", user_answer)

        # 정답 비교
        if current_answer and user_answer.strip() == current_answer.strip():
            return "정답입니다!"
        else:
            # current_answer가 None인 경우 기본 메시지 출력
            if not current_answer:
                return "추천된 정답이 없습니다. 다시 시도해 주세요."

            # prompt 내용 생성 및 출력
            prompt = (
                f"사용자가 입력한 답이 틀렸습니다. 틀린 답: {user_answer}\n"
                f"문제: {current_question}\n"
                f"정답: {current_answer}\n"
                f"해설: {current_explanation}\n\n"
                f"사용자의 틀린 답을 바탕으로 해설을 자세하게 설명해주세요."
            )
            # print("DEBUG: Prompt Content:\n", prompt)

            # LLM API 호출
            response = self.llm.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant specialized in driving test questions."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
            # return response['choices'][0]['message']['content']