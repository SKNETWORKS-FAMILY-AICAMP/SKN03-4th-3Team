
import streamlit as st
from openai import OpenAI # API 통신용 모듈 
import time
#from lang_chain.chain import get_client



# @st.cache_data # 데이터를 caching 처리 
@st.cache_resource # 객체를 caching 처리 
########################################################## openai >>> rangchain 변형 (start)
def get_client():
    return OpenAI()
########################################################## openai >>> rangchain 변형 (end)
def response_from_llm(prompt,chain=None, message_history=[], model_id:str="gpt-4o-mini"):
    if len(message_history) == 0:
        # 최초 질문
        message_history.append(
            {
                "role": "assistant",
                "content": "You are a helpful assistant. You must answer in Korean.",
            }
        )

    # 사용자 질문 추가
    message_history.append(
        {
            "role": "user",
            "content": prompt,
        },
    )

    ############################################################################
    streaming = get_client(prompt).chat.completions.create(
        model=model_id,
        messages=message_history,
        stream=True
    )
    ############################################################################
    # streaming = get_client(prompt, message_history)
    # yield streaming
    return streaming.choices[0].message.content
    for chunk in streaming:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
            time.sleep(0.05)


