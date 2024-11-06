class AnswerCheckChain2:
    def __init__(self, client):
        self.client = client

    def __call__(self, user_answer, current_question, current_answer, current_explanation):
        if current_answer and user_answer.strip() == current_answer.strip():
            return "정답입니다!"
        else:
            if not current_answer:
                return "추천된 정답이 없습니다. 다시 시도해 주세요."

            prompt = (
                f"사용자가 입력한 답이 틀렸습니다. 틀린 답: {user_answer}\n"
                f"문제: {current_question}\n"
                f"정답: {current_answer}\n"
                f"해설: {current_explanation}\n\n"
                f"사용자의 틀린 답을 바탕으로 해설을 자세하게 설명해주세요."
            )

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant specialized in driving test questions."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content