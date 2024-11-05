import openai

class AnswerCheckChain:
    def __init__(self, llm, recommend_chain):
        self.llm = llm
        self.recommend_chain = recommend_chain

    def __call__(self, user_answer):
        if user_answer.strip() == self.recommend_chain.current_answer.strip():
            return "정답입니다!"
        else:
            prompt = (
                f"사용자가 입력한 답이 틀렸습니다. 틀린 답: {user_answer}\n"
                f"문제: {self.recommend_chain.current_question}\n"
                f"정답: {self.recommend_chain.current_answer}\n"
                f"해설: {self.recommend_chain.current_explanation}\n\n"
                f"사용자의 틀린 답을 바탕으로 해설을 자세하게 설명해주세요."
            )

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant specialized in driving test questions."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['choices'][0]['message']['content']
