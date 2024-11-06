import streamlit as st
#from openai import OpenAI # API 통신용 모듈 
from langchain_openai import ChatOpenAI

from langchain.agents import create_openai_functions_agent
from langchain_community.cache import SQLiteCache
from langchain.globals import set_llm_cache
import time



from LangGraph.tools import llm, prompt, tools
from LangGraph.agent import agent_outcome
from LangGraph.graph import app
# @st.cache_data # 데이터를 caching 처리 
@st.cache_resource # 객체를 caching 처리 
def get_client():
    llm
    return llm

chat_prompt = prompt

def response_from_llm(prompt, message_history=[], model_id:str="gpt-4o-mini"):
    
    # chat_prompt

    
    # agent_runnable = create_openai_functions_agent(llm, tools, chat_prompt)

    # user_input = input("Enter your prompt: ")

    # inputs = {"input": user_input,
    #         "chat_history": [],
    #         "intermediate_steps":[]}
    
    # agent_outcome = agent_runnable.invoke(inputs)

    inputs = {"input": "give me a random number and then write in words and make it lower case.", "chat_history": []}

    for chunk in app.stream(inputs):
        yield print(list(chunk.values())[0])
        time.sleep(0.05)




## type 1
# inputs = {"input": "give me a random number and then write in words and make it lower case.", "chat_history": []}
# for s in app.stream(inputs):
#     print(list(s.values())[0])
#     print("-"*30)

