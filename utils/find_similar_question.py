import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from embedding import embed_text
from config import DATA_PATH

# 유사도 기반 문제 찾기

# 데이터 로드 및 임베딩 변환
df = pd.read_csv(DATA_PATH)
df['임베딩'] = df['임베딩'].apply(lambda x: np.fromstring(x.strip('[]'), sep=','))

def find_similar_question(input_question, top_n=1):
    input_embedding = embed_text(input_question)
    similarities = cosine_similarity([input_embedding], np.stack(df['임베딩'].values))[0]
    df['유사도'] = similarities
    similar_questions = df.sort_values(by='유사도', ascending=False).head(top_n)
    return similar_questions[['문제', '정답', '해설', '유사도']].iloc[0]
