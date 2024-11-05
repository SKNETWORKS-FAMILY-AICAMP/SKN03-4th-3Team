import openai
import os

# 환경 변수 설정
openai.api_key = "OPENAIKEY"

# 모델 경로
MODEL_NAME = "intfloat/multilingual-e5-large"
DATA_PATH = "data/임베딩된_문제.csv"