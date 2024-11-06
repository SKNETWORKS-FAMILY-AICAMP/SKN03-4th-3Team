import streamlit as st
#from openai import OpenAI # API 통신용 모듈 
from langchain_openai import ChatOpenAI

from langchain_community.cache import SQLiteCache
from langchain.globals import set_llm_cache
import time
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from datetime import datetime
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from dotenv import load_dotenv
 # .env 파일에 등록된 변수(데이터)를 os 환경변수에 적용
load_dotenv()


# @st.cache_data # 데이터를 caching 처리 
@st.cache_resource # 객체를 caching 처리 
def get_client():
    llm = ChatOpenAI(
    model="gpt-4o-mini"
)
    return llm

def get_today(*args, **kwargs):
    # 오늘 날짜를 가져오기
    return datetime.today().strftime("%b-%d")

def response_from_llm(prompt, message_history=[], model_id:str="gpt-4o-mini"):
    
    chat_prompt = PromptTemplate.from_template(
    "{today} 가 생일인 유명인 {n} 명을 나열하세요. 생년월일을 표기해 주세요."
)

    # 체인 생성 = 프롬프트 + 모델
    chain = (
    {"today": RunnableLambda(get_today), "n": RunnablePassthrough()}
    | chat_prompt
    | get_client()
    | StrOutputParser()
)

    set_llm_cache(SQLiteCache(database_path="my_llm_cache.db"))

    for chunk in chain.stream({"user_input": prompt}):
        yield chunk
        time.sleep(0.05)






