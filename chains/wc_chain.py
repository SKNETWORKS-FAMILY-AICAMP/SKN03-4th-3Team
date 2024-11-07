from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from chains.CheckAnswer import CheckAnswer
from openai import OpenAI
import random
import re
from dotenv import load_dotenv
import os
from langchain.agents import AgentOutputParser
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.prompts import StringPromptTemplate, PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import AgentAction, AgentFinish
from typing import ClassVar
from typing import Union
from langchain_openai import ChatOpenAI
import streamlit as st

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
# OpenAI 클라이언트 대신 ChatOpenAI 모델 사용
chat_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

prompt = PromptTemplate(
    input_variables=["question"],
    template="질문: {question}\n답변:"
)

# LLMChain 생성
llm_chain = LLMChain(llm=chat_model, prompt=prompt)
def csv_load():
    loader = CSVLoader(file_path='/Users/gim-woncheol/Desktop/nolicense_rider/SKN03-4th-3Team/data/문제_정리.csv', encoding='utf-8-sig', source_column='문제')
    return loader.load()

def process_data(data):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    split_docs = text_splitter.split_documents(data)
    return split_docs

def create_vector_db(documents):
    return FAISS.from_documents(documents=documents, embedding=embeddings)

def get_random_similar_question(query, db, k=5):
    retriever = db.as_retriever(search_kwargs={"k": k})
    similar_docs = retriever.get_relevant_documents(query)
    if similar_docs:
        return random.choice(similar_docs)
    return None

db = None  # 전역 변수로 db 선언

# 초기화 함수
def initialize_data():
    global db
    data = csv_load()
    split_docs = process_data(data)
    db = create_vector_db(split_docs)
    return db


client = OpenAI()
answer_check_chain = CheckAnswer(client)

# 문제 추출 함수
def extract_question(doc):
    content = doc.page_content
    split_text = re.split(r"(문제:|정답:|해설:|사진:)", content)
    chunks = {}
    for i in range(1, len(split_text), 2):
        field = split_text[i].strip()
        content = split_text[i + 1].strip()
        chunks[field[:-1]] = content
    return chunks


def check_similarity(query, db):
    retriever = db.as_retriever(search_kwargs={"k": 1})
    similar_docs = retriever.get_relevant_documents(query)
    if similar_docs:
        return similar_docs[0].metadata.get('score', 0)
    return 0


def get_driving_question(query, db):
    doc = get_random_similar_question(query, db)
    if doc:
        question_data = extract_question(doc)
        return {
            "question": question_data.get('문제', ''),
            "answer": question_data.get('정답', ''),
            "explanation": question_data.get('해설', '')
        }
    return None

def chat_response(query):
    return f"운전면허 시험에 관한 질문을 해주세요. 예: '교통 신호에 대해 물어봐줘'"
    


class CustomPromptTemplate(StringPromptTemplate):
    template: ClassVar[str] = """당신은 운전면허 시험 문제를 제공하는 전문가입니다. 사용자의 질문에 따라 적절한 행동을 선택하세요.

{tools}

사용자 질문: {input}
{agent_scratchpad}

응답 형식:
1. 운전면허 관련 질문이거나 문제를 요청하는 경우:
   Action: 운전면허 문제 조회
   Action Input: <사용자 질문>

2. 일반적인 대화인 경우:
   Final Answer: <일반적인 응답>

행동:"""

    def format(self, **kwargs) -> str:
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\n관찰: {observation}\n"
        kwargs["agent_scratchpad"] = thoughts
        return self.template.format(**kwargs)

# 에이전트 도구 정의
tools = [
    Tool(
        name="운전면허 문제 조회",
        func=lambda x: get_driving_question(x, db),
        description="운전면허 시험 관련 질문을 찾고 문제를 반환합니다."
    ),
    Tool(
        name="답변 체크",
        func=lambda x: answer_check_chain(*x),
        description="사용자의 답변을 체크하고 피드백을 제공합니다."
    ),
    Tool(
        name="일반 대화",
        func=chat_response,
        description="운전면허와 관련 없는 질문에 대해 응답합니다."
    )
]

# 에이전트 출력 파서
class CustomOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # 운전면허 문제 파싱
        if "문제:" in llm_output:
            question = llm_output.split("문제:")[-1].split("답변을 입력해주세요.")[0].strip()
            return AgentFinish(
                return_values={"output": f"문제: {question}\n\n답변을 입력해주세요."},
                log=llm_output,
            )
        
        # 답변 체크 결과 파싱
        if "사용자가 선택한 답은" in llm_output:
            check_result = llm_output.strip()
            return AgentFinish(
                return_values={"output": check_result},
                log=llm_output,
            )
        
        action_match = re.search(r"Action\s*\d*\s*:(.*?)\n", llm_output, re.DOTALL)
        action_input_match = re.search(r"Action\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)", llm_output, re.DOTALL)
        
        if action_match and action_input_match:
            action = action_match.group(1).strip()
            action_input = action_input_match.group(1).strip(" ").strip('"')
            return AgentAction(tool=action, tool_input=action_input, log=llm_output)
        
        return AgentFinish(
            return_values={"output": llm_output.strip()},
            log=llm_output,
        )

# 에이전트 생성
def create_agent():
    prompt = CustomPromptTemplate(
        template=CustomPromptTemplate.template,
        tools=tools,
        input_variables=["input", "intermediate_steps"]
    )
    output_parser = CustomOutputParser()

    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=output_parser,
        stop=["\nObservation:"],
        allowed_tools=[tool.name for tool in tools],
        max_iterations=3,
        early_stopping_method="generate"
    )

    return AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

# 에이전트 실행
def run_agent(query):
    if "운전면허" in query and ("문제" in query or "시험" in query):
        question_data = get_driving_question(query, db)
        if question_data:
            st.session_state.current_question = question_data
            return f"문제: {question_data['question']}\n\n답변을 입력해주세요."
        else:
            return "죄송합니다. 관련된 문제를 찾을 수 없습니다."
    
    response = st.session_state.agent.run(query)
    if isinstance(response, dict) and 'question' in response:
        st.session_state.current_question = response
        return f"문제: {response['question']}\n\n답변을 입력해주세요."
    elif st.session_state.get('current_question'):
        result = answer_check_chain(query, 
                                    st.session_state.current_question['question'],
                                    st.session_state.current_question['answer'],
                                    st.session_state.current_question['explanation'])
        st.session_state.current_question = None
        return result
    else:
        return response

# 초기화
initialize_data()