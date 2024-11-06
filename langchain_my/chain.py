from langchain_my.prompt import create_prompt, create_message
from langchain_my.model import create_model
import streamlit as st
from common.constant import CHATBOT_ROLE
import time

# @st.cache_resource
# # 체인 생성 = 프롬프트 + 모델
# def create_chain(user_input:str):
#     chain = create_prompt() | create_model()

#     for answer in chain.stream({"user_input": user_input}):
#         if answer.content is not None:
#             yield answer.content
#             time.sleep(0.05)

############################################################################
# 추가 import 
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel
############################################################################

#########################################################################################################################################################
################################################## parallel 체인함수 생성
#########################################################################################################################################################
# 체인 생성 = 프롬프트 + 모델
@st.cache_resource # chain을 1개만 가질수 있도록 "캐싱"
def create_base_chain1():
    """기본 chain 객체를 생성하고 캐싱"""
    chain1 = (
        {"country": RunnablePassthrough()}
        | PromptTemplate.from_template("{country} 의 주가는?")
        | create_model()
    )

    return chain1

def create_base_chain2():

    chain2 = (
        {"country": RunnablePassthrough()}
        | PromptTemplate.from_template("{country} 의 회사 최근 이슈는?")
        | create_model()
    )
    return chain2
#######################################################
########### parallel chain ----- 체인 생성
def parallel_chain():
    chain1 = create_base_chain1()  # 캐시된 chain 사용
    chain2 = create_base_chain2()  # 캐시된 chain 사용
    combined_chain = RunnableParallel(stock =chain1, issue=chain2)
    return combined_chain
#######################################################

def create_chain_parallel(user_input: str, message_history:list=[]):
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
            "content": user_input,
        },
    )
    conversation_history = "\n".join([
        f"{msg['role']}: {msg['content']}" 
        for msg in message_history
    ])
    full_prompt = f"Previous conversation:\n{conversation_history}\n\nCurrent input: {user_input}"

    """캐시된 chain을 사용하여 응답 생성"""
    chain1 = create_base_chain1()  # 캐시된 chain 사용
    chain2 = create_base_chain2()  # 캐시된 chain 사용
    combined_chain = RunnableParallel(stock =chain1, issue=chain2)
    print("parallel작동")
    print(combined_chain)
    # for answer in combined_chain.stream({"country": user_input}):
    #     if "stock" in answer and answer["stock"].content is not None:
    #         yield answer["stock"].content
    #         # time.sleep(0.5)

    #     if "issue" in answer and answer["issue"].content is not None:
    #         yield answer["issue"].content
    #         # time.sleep(0.5)
    answer = combined_chain.invoke({"country": user_input})

    # 응답 형식 변환
    result = ""
    if "stock" in answer:
        result += answer["stock"].content + "\n\n"
    if "issue" in answer:
        result += answer["issue"].content
        
    # 올바른 메시지 형식으로 반환
    answer = {
        "role": "assistant",
        "content": result
    }
    print(f"answer: {answer}")
    print(f"answer['content']: {answer['content']}")
    return answer["content"]

# def get_client():
#     return create_model()

# def create_chain_llm(user_input: str, message_history:list=[]):
#     if len(message_history) == 0:
#         # 최초 질문
#         message_history.append(
#             {
#                 "role": "assistant",
#                 "content": "You are a helpful assistant. You must answer in Korean.",
#             }
#         )

#     # 사용자 질문 추가
#     message_history.append(
#         {
#             "role": "user",
#             "content": user_input,
#         },
#     )
#     conversation_history = "\n".join([
#         f"{msg['role']}: {msg['content']}" 
#         for msg in message_history
#     ])
#     full_prompt = f"Previous conversation:\n{conversation_history}\n\nCurrent input: {user_input}"
#     """캐시된 chain을 사용하여 응답 생성"""
#     chain = create_base_chain()  # 캐시된 chain 사용
#     print(message_history)
#     for answer in chain.stream({"user_input": user_input}):
#         if answer.content is not None:
#             yield answer.content
#             time.sleep(0.05)

# streaming = get_client(prompt).chat.completions.create(
#         model=model_id,
#         messages=message_history,
#         stream=True
#     )

# def create_chain(user_input: str, messages: list = []):
#     # 이전 대화 내용이 있다면 프롬프트에 포함
#     if messages:
#         conversation_history = "\n".join([
#             f"{msg['role']}: {msg['content']}" 
#             for msg in messages[:-1]  # 현재 user_input은 제외
#         ])
#         # 대화 히스토리를 포함한 프롬프트 생성
#         chain = create_prompt(f"Previous conversation:\n{conversation_history}\n\nCurrent input: {user_input}") | create_model()
#     else:
#         # 첫 대화인 경우
#         chain = create_prompt(user_input) | create_model()
    
#     answer = chain.invoke({"user_input": user_input})
#     return answer.content
#########################################################################################################################################################
################################################## lambda 체인함수 생성
#########################################################################################################################################################
from datetime import datetime
def get_today(a):
    # 오늘 날짜를 가져오기
    return datetime.today().strftime("%b-%d")

from langchain_core.output_parsers import StrOutputParser
from langchain_my.prompt import create_prompt_lambda
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_my.model import create_model

def create_chain_lambda(user_input: int, message_history:list=[]):
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
            "content": user_input,
        },
    )
    # chain 을 생성합니다.
    chain = (
        {
            "today": RunnableLambda(get_today),
            "n": RunnablePassthrough()
        }
        | create_prompt_lambda()
        | create_model()
        | StrOutputParser()
    )
    print("lambda작동")
    for answer_lambda in chain.stream({"n": user_input}): # 어러움...왜 stream({"n": user_input}) 이 방법으로 작성하는 것인가
        if answer_lambda is not None:
            yield answer_lambda
            time.sleep(0.05)


def create_llm(user_input: int, message_history:list=[]):
    if user_input.isdigit():
        return create_chain_lambda(user_input, message_history)
    else:
        return create_chain_parallel(user_input, message_history)



#########################################################################################################################################################
################################################## llm 챗봇 체인함수 생성
#########################################################################################################################################################
@st.cache_resource # chain을 1개만 가질수 있도록 "캐싱"
def create_base_chain():
    """기본 chain 객체를 생성하고 캐싱"""
    return create_prompt() | create_model()

def create_chain_llm(prompt: str, message_history:list=[]):
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
    conversation_history = "\n".join([
        f"{msg['role']}: {msg['content']}" 
        for msg in message_history
    ])
    full_prompt = f"Previous conversation:\n{conversation_history}\n\nCurrent input: {prompt}"

    """캐시된 chain을 사용하여 응답 생성"""
    chain = create_base_chain()  # 캐시된 chain 사용
    print(message_history)
    for answer in chain.stream({"user_input": full_prompt}):
        if answer.content is not None:
            yield answer.content
            time.sleep(0.05)


#########################################################################################################################################################
################################################## agent 체인함수 생성
#########################################################################################################################################################
# from langchain_community.tools.tavily_search import TavilySearchResults
# def create_chain_agent(prompt: str, message_history:list=[]):
#     # 도구 생성
#     tool = TavilySearchResults(
#         max_results=6,
#         include_answer=True,
#         include_raw_content=True,
#         # include_images=True,
#         # search_depth="advanced", # or "basic"
#         include_domains=["wikipedia.org",  # 금융 정보
#                         ],
#         # exclude_domains = []
#     )   
#     # 도구 실행
#     answer = ""
#     results = tool.invoke({"query":f"{prompt} 에 대해서 알려줘"})
#     for result in results:
#         answer += result["content"]
#     print(f"result: {results}")
#     print(f"result[0]['content']: {results[0]['content']}")
#     return answer


# TavilySearchResults 클래스를 langchain_community.tools.tavily_search 모듈에서 가져옵니다.
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_openai_functions_agent
from dotenv import load_dotenv
from langchain.agents import AgentExecutor
from langchain import hub
from langchain.tools.render import render_text_description
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser

# TavilySearchResults 클래스의 인스턴스를 생성합니다
# k=5은 검색 결과를 5개까지 가져오겠다는 의미입니다
def create_chain_agent(user_input: str, message_history:list=[], model_id:str="gpt-4o-mini"):
    load_dotenv()
    tools = [
        TavilySearchResults(max_results=5,
                            include_domains=["https://www.koroad.or.kr/70th/main.do",
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do",
                                            
                                            # 서울
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=61&bcstIdx2=73",
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=61&bcstIdx2=74",
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=61&bcstIdx2=75",
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=61&bcstIdx2=76",

                                            # 부산
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=62&bcstIdx2=77",
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=62&bcstIdx2=78",
                                            
                                            # 대구
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=63&bcstIdx2=79",
                                            
                                            # 인천
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=64&bcstIdx2=80",
                                            
                                            # 경기
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=65&bcstIdx2=81",
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=65&bcstIdx2=82",
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=65&bcstIdx2=83",

                                            # 강원
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=66&bcstIdx2=84",
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=66&bcstIdx2=85",
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=66&bcstIdx2=86",
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=66&bcstIdx2=87",
                                        
                                            # 충청
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=67&bcstIdx2=88",
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=67&bcstIdx2=89",
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=67&bcstIdx2=90",
                                            
                                            # 대전
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=68&bcstIdx2=91",
                                            
                                            # 전라
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=69&bcstIdx2=92",
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=69&bcstIdx2=93",
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=69&bcstIdx2=94",

                                            # 경상
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=70&bcstIdx2=95",
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=70&bcstIdx2=96",
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=70&bcstIdx2=97",

                                            # 울산
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=71&bcstIdx2=98",

                                            # 제주
                                            "https://www.koroad.or.kr/main/content/view/MN05010523.do?bcstIdx1=72&bcstIdx2=99",
                                            ],
                            # include_patterns=[  # URL 패턴 추가
                            #                 "bcstIdx1=[0-9]+&bcstIdx2=[0-9]+",  # 모든 숫자 조합 허용
                            #                 ]
                            )
    ]
    prompt = hub.pull("hwchase17/react-chat")
    prompt = prompt.partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools])
    )
    memory = ConversationBufferMemory(memory_key="chat_history")

    llm = create_model()
    llm_with_stop = llm.bind(stop=["\nObservation"])
    
    agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_stop
    | ReActSingleInputOutputParser()
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
    )


    response = agent_executor.invoke({"input": f"{user_input}" })
    return response["output"]