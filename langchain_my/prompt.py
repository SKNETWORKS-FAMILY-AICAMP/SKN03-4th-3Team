
from common.constant import CHATBOT_MESSAGE, CHATBOT_ROLE

def create_message(role:CHATBOT_ROLE, prompt:str):
    return {
        CHATBOT_MESSAGE.role.name: role.name,
        CHATBOT_MESSAGE.content.name: prompt
    }

from langchain_core.prompts import ChatPromptTemplate

# def create_prompt():
#     # 프롬프트 생성
#     chat_prompt = ChatPromptTemplate.from_messages([
#         ("system", "이 시스템은 주식 쳇봇"),
#         ("user", "{user_input}"),
#     ])
#     return chat_prompt
def create_prompt():
    return ChatPromptTemplate.from_messages([
        (CHATBOT_ROLE.assistant.name, "이 시스템은 주식 쳇봇"),
        (CHATBOT_ROLE.user.name, "{user_input}"),
    ])


from langchain_core.prompts import PromptTemplate

from datetime import datetime
def get_today(a):
    # 오늘 날짜를 가져오기
    return datetime.today().strftime("%b-%d")


def create_prompt_lambda():
    # 프롬프트 템플릿 정의
    template = """{today} 가 생일인 유명인 {n} 명을 나열하세요.
    생년월일을 표기해 주세요.
    """
    
    # PromptTemplate 객체 생성 및 반환
    prompt = PromptTemplate.from_template(template)
    return prompt