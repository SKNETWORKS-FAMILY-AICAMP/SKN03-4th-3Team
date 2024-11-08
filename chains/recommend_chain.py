from utils.find_similar_question import find_similar_question

class RecommendQuestionChain:
    def __init__(self, find_similar_fn):
        self.find_similar_fn = find_similar_fn
        self.current_question = None
        self.current_answer = None
        self.current_explanation = None

    def __call__(self, input_question):
        # find_similar_question 함수의 반환 값 확인
        response = self.find_similar_fn(input_question)
        self.current_question = response['문제']
        self.current_answer = response['정답']
        self.current_explanation = response['해설']
        # 추천 문제 반환
        return f"{self.current_question}" if self.current_question else "추천된 문제가 없습니다."