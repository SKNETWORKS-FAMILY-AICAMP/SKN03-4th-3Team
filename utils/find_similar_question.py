import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from embedding import embed_text
from config import DATA_PATH

# 데이터 로드 및 유사도 기반 문제 추천 함수
df = pd.read_csv(DATA_PATH)
df['임베딩'] = df['임베딩'].apply(lambda x: np.fromstring(x.strip('[]'), sep=','))

def find_similar_question(input_question, top_n=5):
    input_embedding = embed_text(input_question)
    similarities = cosine_similarity([input_embedding], np.stack(df['임베딩'].values))[0]
    
    similar_questions = df.assign(유사도=similarities).nlargest(top_n, '유사도')
    selected_question = similar_questions.sample(n=1).iloc[0]
    return selected_question
    # return similar_questions[['문제', '정답', '해설', '유사도']].iloc[0]
