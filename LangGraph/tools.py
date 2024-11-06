from typing import TypedDict, Annotated, List, Union
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage
import operator

# GraphState - 각 노드가 수행한 작업들을 기억(상태 기록)하는 기능
class AgentState(TypedDict):
  input: str
  chat_history: list[BaseMessage] # 대화 내용 중 '이전 메시지' 목록
  agent_outcome: Union[AgentAction, AgentFinish, None] # 유효한 유형으로 `None`이 필요
  intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]


##   Custom Tools
from langchain.tools import BaseTool, StructuredTool, Tool, tool
import random

@tool("upper_case", return_direct=True)
def to_lower_case(input:str) -> str:
  """Returns the input as all upper case."""
  return input.upper() #.lower()

@tool("random_number", return_direct=True)
def random_number_maker(input:str) -> str:
    """Returns a random number between 0-100."""
    return random.randint(0, 100)

tools = [to_lower_case, random_number_maker]


from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain_openai.chat_models import ChatOpenAI

prompt = hub.pull("hwchase17/openai-functions-agent")

llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)