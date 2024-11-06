##      Define the graph
from langgraph.graph import END, StateGraph
from .tools import AgentState
from .nodes import run_agent, execute_tools, should_continue



workflow = StateGraph(AgentState)
workflow.add_node("agent", run_agent)
workflow.add_node("action", execute_tools)
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END
    }
)
workflow.add_edge('action', 'agent')   # really this is the graph.
app = workflow.compile()    # to be like an app in here