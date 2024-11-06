<<<<<<< HEAD
<<<<<<< HEAD
=======
# import numpy as np
# import pandas as pd
# from sklearn.metrics.pairwise import cosine_similarity
# from embedding import embed_text
# from config import DATA_PATH

# # 유사도 기반 문제 찾기

# # 데이터 로드 및 임베딩 변환
# df = pd.read_csv(DATA_PATH)
# df['임베딩'] = df['임베딩'].apply(lambda x: np.fromstring(x.strip('[]'), sep=','))

# def find_similar_question(input_question, top_n=1):
#     input_embedding = embed_text(input_question)
#     similarities = cosine_similarity([input_embedding], np.stack(df['임베딩'].values))[0]
#     df['유사도'] = similarities
#     similar_questions = df.sort_values(by='유사도', ascending=False).head(top_n)
#     return similar_questions[['문제', '정답', '해설', '유사도']].iloc[0]


>>>>>>> aff5c57e11eff4b796a0c26cb34a755135eca838
=======
>>>>>>> d43ed311a022636ec41ad44fb510511dd2a9ffed
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from embedding import embed_text
<<<<<<< HEAD
from config import DATA_PATH

<<<<<<< HEAD
# 유사도 기반 문제 찾기

# 데이터 로드 및 임베딩 변환
=======
# 데이터 로드 및 유사도 기반 문제 추천 함수
>>>>>>> aff5c57e11eff4b796a0c26cb34a755135eca838
df = pd.read_csv(DATA_PATH)
df['임베딩'] = df['임베딩'].apply(lambda x: np.fromstring(x.strip('[]'), sep=','))

def find_similar_question(input_question, top_n=1):
    input_embedding = embed_text(input_question)
    similarities = cosine_similarity([input_embedding], np.stack(df['임베딩'].values))[0]
<<<<<<< HEAD
    df['유사도'] = similarities
    similar_questions = df.sort_values(by='유사도', ascending=False).head(top_n)
=======
    similar_questions = df.assign(유사도=similarities).nlargest(top_n, '유사도')
>>>>>>> aff5c57e11eff4b796a0c26cb34a755135eca838
    return similar_questions[['문제', '정답', '해설', '유사도']].iloc[0]
=======
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()
DATA_PATH = os.getenv("DATA_PATH")

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
>>>>>>> d43ed311a022636ec41ad44fb510511dd2a9ffed
