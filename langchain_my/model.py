
from langchain_openai import ChatOpenAI

def create_model(model_id="gpt-4o-mini"):
# 모델 생성
    chat = ChatOpenAI(
        model=model_id,
        # streaming=True,
    )
    return chat

