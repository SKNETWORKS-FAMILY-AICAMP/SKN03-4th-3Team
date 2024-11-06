from .tools import tools
from .agent import agent_outcome, agent_runnable

from langchain_core.agents import AgentFinish
from langgraph.prebuilt.tool_executor import ToolExecutor

# 도구들을 실행할 ToolExecutor 객체를 생성합니다.
tool_executor = ToolExecutor(tools)

output = tool_executor.invoke(agent_outcome)


def run_agent(data):
    agent_outcome = agent_runnable.invoke(data)
    return {"agent_outcome": agent_outcome}

def execute_tools(data):
    agent_action = data['agent_outcome']
    output = tool_executor.invoke(agent_action)
    return {"intermediate_steps": [(agent_action, str(output))]}

def should_continue(data):
    # AgentFinish는 사용자에게 다시 보낼 최종 메시지가 포함된 응답입니다.
    # 이 응답은 에이전트 실행을 종료하는데 사용되어야 합니다.
    if isinstance(data['agent_outcome'], AgentFinish):
        return "end"
    else:
        return "continue"