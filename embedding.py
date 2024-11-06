from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from config import MODEL_NAME

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
    return embeddings.squeeze().numpy()