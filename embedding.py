from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
<<<<<<< HEAD
from config import MODEL_NAME

=======
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME")
>>>>>>> d43ed311a022636ec41ad44fb510511dd2a9ffed
# 텍스트 임베딩

# 모델 및 토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

def embed_text(text):
    if not isinstance(text, str):
        text = str(text)
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
<<<<<<< HEAD
    return embeddings.squeeze().numpy()
=======
    return embeddings.squeeze().numpy()
>>>>>>> d43ed311a022636ec41ad44fb510511dd2a9ffed
