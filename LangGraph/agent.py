from langchain.agents import create_openai_functions_agent
from .tools import prompt, llm
from .tools import tools

agent_runnable = create_openai_functions_agent(llm, tools, prompt)

inputs = {"input": "give me a random number and then write in words",
        "chat_history": [],
        "intermediate_steps":[]}
agent_outcome = agent_runnable.invoke(inputs)